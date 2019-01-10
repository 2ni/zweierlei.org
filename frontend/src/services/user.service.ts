/*
 * http://jasonwatmore.com/post/2018/07/06/vue-vuex-jwt-authentication-tutorial-example#loginpage-vue
 * might be easier: https://scotch.io/tutorials/handling-authentication-in-vue-using-vuex
 *
 * handles all api calls concerning authentication of the user
 */
// import { authHeader } from '@/helpers';
import axios from 'axios';
import { http } from '@/services';

export const userService = {
  login,
  refresh,
  logout,
  get,
  save,
};

function login(user: any) {
  return axios({url: 'login', baseURL: process.env.VUE_APP_API_URL, method: 'POST', data: user})
    .then((responseUser) => {
      if (responseUser.data.msg === 'ok') {
        return Promise.resolve(responseUser.data);
      }
    })
    .catch((error) => {
      if (error.response.status === 401) {
        logout();
        return Promise.reject(error.response.data.msg);
      }
    });
}

function refresh(user: any) {
  return axios({
      url: 'refresh',
      baseURL: process.env.VUE_APP_API_URL,
      method: 'POST',
      headers: { Authorization: 'Bearer ' + user.refresh_token },
      })
    .then((responseUser) => {
      if (responseUser.data.msg === 'ok') {
        return Promise.resolve(responseUser.data);
      }
    })
    .catch((error) => {
      logout();
      return Promise.reject(error.response.data.msg);
    });
}

function logout() {
  // TODO call backend logout API
}

/*
 * Get user data from backend
 * noLogin in config does not redirect to login page
 */
function get() {
  const p = new Promise((resolve, reject) => {
    http.get('users')
    .then((responseUser) => {
      resolve(responseUser.data);
    })
    .catch((errorUser) => {
      reject(errorUser);
    });
  });

    return p;
}

/*
 * Save data from an existing user
 * entrypoint = 'users|register'
 */
function save(entrypoint, data) {
  const p = new Promise((resolve, reject) => {
    http.post(entrypoint, data)
    .then((responseUser) => {
      resolve(responseUser.data);
    })
    .catch((errorUser) => {
      reject(errorUser);
    });
  });

    return p;
}
