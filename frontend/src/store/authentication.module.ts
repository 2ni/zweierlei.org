import { userService } from '@/services';
import router from '@/router';

const user = JSON.parse((localStorage as any).getItem('user'));
const initialState = user ? { status: 'loggedIn', user } : { status: null, user: null };

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
                        dispatch('alert/error', error, { root: true });
                        return new Promise((resolve, reject) => reject(error));
                    },
                );
        },
        logout({ commit }) {
            userService.logout();
            commit('logout');
        },
    },
    mutations: {
        loginRequest(state, currentuser) {
            state.status = 'loggingIn';
            state.user = currentuser;
        },
        loginSuccess(state, currentuser) {
            state.status = 'loggedIn';
            state.user = currentuser;
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
