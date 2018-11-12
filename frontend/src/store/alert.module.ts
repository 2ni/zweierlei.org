export const alert = {
    namespaced: true,
    state: {
        message: null,
        type: null,
    },
    actions: {
        success({ commit }, message: any) {
            commit('success', message);
        },
        error({ commit }, message: any) {
            commit('error', message);
        },
        clear({ commit }, message: any) {
            commit('success', message);
        },
    },
    mutations: {
        success(state: any, message: any) {
            state.type = 'success';
            state.message = message;
        },
        error(state: any, message: any) {
            state.type = 'danger';
            state.message = message;
        },
        clear(state: any) {
            state.type = null;
            state.message = null;
        },
    },
};
