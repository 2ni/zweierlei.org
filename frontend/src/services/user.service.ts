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
  logout,
  get,
  save,
};

// TODO use http for login instead of axios directly
function login(user: any) {
  return axios({url: 'login', baseURL: process.env.VUE_APP_API_URL, method: 'POST', data: user})
    .then((responseUser) => {
      if (responseUser.data.msg === 'ok') {
        localStorage.setItem('user', JSON.stringify(responseUser.data));
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
  // TODO call backend logout API
  localStorage.removeItem('user');
}

/*
 * Get user data from backend
 */
function get() {
  const p = new Promise((resolve, reject) => {
    http.get('users')
    .then((responseUser) => {
      resolve(responseUser);
    })
    .catch((errorUser) => {
      reject(errorUser);
    });
  });

    return p;
}

function save(data) {
  const p = new Promise((resolve, reject) => {
    http.post('users', data)
    .then((responseUser) => {
      // merge current data with new data (keeping tokens)
      const currentUser = JSON.parse(localStorage.getItem('user'));
      const newUser = { ...currentUser, ...responseUser.data };
      localStorage.setItem('user', JSON.stringify(newUser));
      resolve(responseUser);
    })
    .catch((errorUser) => {
      reject(errorUser);
    });
  });

    return p;
}
