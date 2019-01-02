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

const http = axios.create({ baseURL: process.env.VUE_APP_API_URL });

let isRefreshing = false;
let subscribers = [];

function onAccessTokenFetched(accessToken) {
  subscribers = (subscribers as any).filter((callback) => callback(accessToken));
}

function addSubscriber(callback) {
  (subscribers as any).push(callback);
}

function redirToLogin() {
  localStorage.removeItem('user');
  // use route to load login form to not reload page completely
  // location.reload();
  const lang = window.location.pathname.replace(/^\/([^\/]*).*$/, '$1');
  router.push('/' + lang + '/login?f=' + window.location.pathname);
}

http.interceptors.response.use((response) => {
  return response;
}, (error) => {
  // console.log(error.response.status, error.response.data.msg);
  const { config, response: { status } } = error;
  const originalRequest = config;
  const userString = localStorage.getItem('user');
  const user = userString ? JSON.parse(userString) : [];

  if (status === 401) {
    if (!isRefreshing && !originalRequest.__retried) {
      originalRequest.__retried = true;
      isRefreshing = true;
      console.log('refreshing token', user);
      if (!user.refresh_token) {
        redirToLogin();
      }

      const c = axios.create({
        baseURL: process.env.VUE_APP_API_URL,
        headers: { Authorization: 'Bearer ' + user.refresh_token },
      });
      c.post('refresh').then((r) => {
        // console.log('got new access_token'/*, r.data.access_token*/);
        user.access_token = r.data.access_token;
        localStorage.setItem('user', JSON.stringify(user));
        isRefreshing = false;
        onAccessTokenFetched(r.data.access_token);
      })
      .catch((responseErrorRefresh) => {
        // refresh has expired -> redirect to login
        // console.log(responseErrorRefresh.response.status, responseErrorRefresh.response.data.msg);
        const { response: { status: errorRefresh }, response: { data: { msg } } } = responseErrorRefresh;
        // console.log("refresh error", errorRefresh, msg);
        if (errorRefresh === 401) {
          redirToLogin();
        }
      });
    } else {
      // if retry failed -> redir to login page too (eg fresh token required)
      redirToLogin();
    }

    const retryOriginalRequest = new Promise((resolve) => {
      addSubscriber((accessToken) => {
        // originalRequest.headers.Authorization = 'Bearer ' + accessToken
        resolve(http(originalRequest));
      });
    });
    return retryOriginalRequest;
  }
  return Promise.reject(error);
});


// always ensure that we take the newest access_token when using axios/$http
http.interceptors.request.use((config) => {
  const userString = localStorage.getItem('user');
  const user = userString ? JSON.parse(userString) : null;
  if (user && user.access_token) {
    config.headers.Authorization = 'Bearer ' + user.access_token;
  }
  return config;
});

export { http };
