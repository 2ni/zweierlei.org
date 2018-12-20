/*
 * http://jasonwatmore.com/post/2018/07/06/vue-vuex-jwt-authentication-tutorial-example#loginpage-vue
 * might be easier: https://scotch.io/tutorials/handling-authentication-in-vue-using-vuex
 *
 * handles all api calls concerning authentication of the user
 */
// import { authHeader } from '@/helpers';
import axios from 'axios';

export const userService = {
  login,
  logout,
};

function login(user: any) {
  return axios({url: 'login', baseURL: process.env.VUE_APP_API_URL, method: 'POST', data: user})
    .then((user) => {
      if (user.data.msg == 'ok') {
        localStorage.setItem('user', JSON.stringify(user.data));
      }
    })
    .catch((error) => {
      if (error.response.status === 401) {
        logout();
        return Promise.reject(error.response.data.msg);
      }
    });
}

function logout() {
  localStorage.removeItem('user');
}
