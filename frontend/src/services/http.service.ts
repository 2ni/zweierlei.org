/*
 * help from
 * https://gist.github.com/FilipBartos/c2cc4df3dfda49f71360295e4101db2b
 * https://gist.github.com/mkjiau/650013a99c341c9f23ca00ccb213db1c
 * https://blog.sqreen.io/authentication-best-practices-vue/
 *
 */
import Vue from 'vue';
import axios from 'axios';
import router from '@/router';
import store from '@/store';

const http = axios.create({ baseURL: process.env.VUE_APP_API_URL });

let workingOnRefresh = false;
let subscribers = [];

// directly redir to login page on certain conditions
const redirMsgs = [
  'fresh token required',
  'missing authorization header',
];

function onAccessTokenFetched(withoutToken) {
  subscribers = (subscribers as any).filter((callback) => callback(withoutToken));
}

function addSubscriber(callback) {
  workingOnRefresh = false;
  (subscribers as any).push(callback);
}

function redirToLogin() {
  subscribers = [];

  const lang = window.location.pathname.replace(/^\/([^\/]*).*$/, '$1');
  router.push('/' + lang + '/login?f=' + window.location.pathname);
}

http.interceptors.response.use((response) => {
  return response;
}, (error) => {
  const { config, response: { status }, response: { data: { msg } } } = error;
  let origConfig = config;

  console.log('error', status, msg);
  /*
  if (origConfig.__retried) {
    console.log('retried error');
    return Promise.reject('retried error');
  }
  */

  // access token expired
  if (status === 401) {

    for (var i = 0; i < redirMsgs.length; i++) {
      if (msg.toLowerCase().indexOf(redirMsgs[i]) != -1) {
        redirToLogin();
        return Promise.reject(error);
      }
    }

    console.log('workingOnRefresh', workingOnRefresh);
    console.log('retried', origConfig.__retried);

    if (!workingOnRefresh && !origConfig.__retried) {
      console.log('refreshing token');
      workingOnRefresh = true;
      origConfig.__retried = true;

      store.dispatch('authentication/refresh')
      .then(() => {
        console.log('access token refreshed');
        onAccessTokenFetched();
      })
      // refresh token expired
      // retry calls w/o token
      .catch(() => {
        console.log('refresh token expired');
        store.dispatch('authentication/logout')
        .then(() => {
          console.log('logged out');
          // remove token and __retried
          onAccessTokenFetched(true);
        });
      });
    }

    // in case refresh token is expired token will be removed in interceptors.request
    const retryOriginalRequest = new Promise((resolve) => {
      console.log('added subscriber', origConfig.url);
      addSubscriber((withoutToken = false) => {
        if (withoutToken) {
          console.log('trying w/o token');
          delete origConfig.__retried;
          delete config.headers.Authorization;
        }
        console.log('consuming subscriber', origConfig.url, origConfig);
        resolve(http(origConfig));
      });
    });
    return retryOriginalRequest;

  }

  return Promise.reject(error);
});

http.interceptors.request.use((config) => {
  console.log('******** http with access_token', config.method.toUpperCase(), config.baseURL+'/'+config.url);
  console.log('subscribers', subscribers.length);
  console.log('__retried', config.__retried);
  if (store.state.authentication.user) {
    console.log('call with token: ...', store.state.authentication.user.access_token.substr(-5));
    config.headers.Authorization = 'Bearer ' + store.state.authentication.user.access_token;
  }
  console.log('********');

  return config;
});

export { http };
