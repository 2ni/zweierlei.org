import Vue from 'vue';
import Vuex from 'vuex';

import { alert } from '@/store/alert.module';
import { authentication } from '@/store/authentication.module';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    alert,
    authentication,
  },
  state: {

  },
  mutations: {

  },
  actions: {

  },
});
