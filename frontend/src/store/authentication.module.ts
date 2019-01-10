import { userService } from '@/services';
import router from '@/router';
import store from '@/store';
import { filterObject } from '@/helpers';

let initialState = { status: null, user: null };

export const authentication = {
  namespaced: true,
  state: initialState,
  actions: {
    login({ dispatch, commit }, user) {
      commit('loginRequest', user);

      return userService.login(user)
      .then(
        (currentuser) => {
          commit('loginSuccess', currentuser);
        },
        (error) => {
          commit('loginFailure', error);
          return Promise.reject(error);
        },
      );
    },
    refresh(context) {
      return userService.refresh(context.state.user)
      .then(
        (tokens) => {
          context.commit('refreshSuccess', tokens);
        },
        (error) => {
          context.commit('loginFailure', error);
          return Promise.reject(error);
        },
      );
    },
    logout({ commit }) {
      userService.logout();
      commit('logout');
    },
    save({ commit }, data) {
      return userService.save(data.entrypoint, data.user)
      .then(
        (currentuser) => {
          commit('loginSuccess', currentuser);
      });

    },
    set({ commit }, currentuser) {
      commit('loginSuccess', currentuser);
    },
  },
  mutations: {
    loginRequest(state, currentuser) {
      state.status = 'loggingIn';
      state.user = currentuser;
    },
    loginSuccess(state, currentuser) {
      state.status = 'loggedIn';
      state.user = filterObject(currentuser, ['uid', 'firstname', 'access_token', 'refresh_token']);
    },
    refreshSuccess(state, tokens) {
      state.user.access_token = tokens.access_token;
    },
    loginFailure(state) {
      state.status = 'loginFailed';
      state.user = null;
    },
    logout(state) {
      state.status = null;
      state.user = null;
    },
  },
};
