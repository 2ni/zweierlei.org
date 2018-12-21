/*
 * help from
 * https://gist.github.com/FilipBartos/c2cc4df3dfda49f71360295e4101db2b
 * https://gist.github.com/mkjiau/650013a99c341c9f23ca00ccb213db1c
 * https://blog.sqreen.io/authentication-best-practices-vue/
 *
 */
import Vue from 'vue';
import axios from 'axios';
import router from './router';

const instance = axios.create({baseURL: process.env.VUE_APP_API_URL});

let isRefreshing = false
let subscribers = []

function onAccessTokenFetched(access_token) {
  subscribers = subscribers.filter(callback => callback(access_token))
}

function addSubscriber(callback) {
  subscribers.push(callback)
}

instance.interceptors.response.use((response) => {
  return response
}, (error) => {
  // console.log(error.response.status, error.response.data.msg);
  const { config, response: { status } } = error;
  const originalRequest = config;
  const userString = localStorage.getItem('user');
  const user = userString ? JSON.parse(userString) : null;

  if (status === 401) {
    if (!isRefreshing && !originalRequest.__retried) {
      originalRequest.__retried = true;
      isRefreshing = true
      const c = axios.create({baseURL: process.env.VUE_APP_API_URL, headers: {Authorization: 'Bearer ' + user.refresh_token}});
      c.post('refresh').then((r) => {
        // console.log('got new access_token'/*, r.data.access_token*/);
        user.access_token = r.data.access_token;
        localStorage.setItem('user', JSON.stringify(user));
        isRefreshing = false
        onAccessTokenFetched(r.data.access_token)
      })
      .catch((error) => {
        // refresh has expired -> redirect to login
        // console.log(error.response.status, error.response.data.msg);
        const { response: { status }, response: { data: { msg } } } = error;
        // console.log("refresh error", status, msg);
        if (status === 401) {
          localStorage.removeItem('user');
          // use route to load login form to not reload page completely
          // location.reload();
          let lang = window.location.pathname.replace(/^\/([^\/]*).*$/, '$1');
          router.push('/' + lang + '/login?f=' + window.location.pathname);
        }
      })
    }

    const retryOriginalRequest = new Promise((resolve) => {
      addSubscriber(access_token => {
        // originalRequest.headers.Authorization = 'Bearer ' + access_token
        resolve(instance(originalRequest))
      })
    })
    return retryOriginalRequest
  }
  return Promise.reject(error)
});


// always ensure that we take the newest access_token when using axios/$http
instance.interceptors.request.use((config) => {
  const userString = localStorage.getItem('user');
  const user = userString ? JSON.parse(userString) : null;
  if (user && user.access_token) {
    config.headers.Authorization = 'Bearer ' + user.access_token;
  }
  return config;
});

Vue.prototype.$http = instance;
