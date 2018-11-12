/*
 * http://jasonwatmore.com/post/2018/07/06/vue-vuex-jwt-authentication-tutorial-example#loginpage-vue
 *
 * handles all api calls concerning authentication of the user
 */
import { authHeader } from '@/helpers';

export const userService = {
  login,
  logout,
};

const API_URL = 'http://localhost:8080';

function login(username: any, password: any) {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  };

  return fetch(`${API_URL}/users/authenticate`, requestOptions)
    .then(handleResponse)
    .then(
      (user) => {
        if (user.token) {
          localStorage.setItem('user', JSON.stringify(user));
        }
        return user;
      },
      /*
      (error) => {
        console.log(error);
        dispatch('alert/error', { error }, { root: true });
      },
      */
    );
}

function logout() {
  localStorage.removeItem('user');
}

function handleResponse(response: any) {
  return response.text().then((text: any) => {
    const data = text && JSON.parse(text);
    if (!response.ok) {
      if (response.status === 401) {
        // auto logout if 401 from api
        logout();
        location.reload(true);
      }

      const error = (data && data.message) || response.statusText;
      return Promise.reject(error);
    }

    return data;
  });
}
