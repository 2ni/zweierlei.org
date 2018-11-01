import Vue from 'vue';
import VueI18n from 'vue-i18n';
import L from 'leaflet';
import App from './App.vue';
import router from './router';
import store from './store';
import './registerServiceWorker';

import 'leaflet.icon.glyph';

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

import VueMaterial from 'vue-material';
import 'vue-material/dist/vue-material.min.css';
import 'vue-material/dist/theme/default.css';
Vue.use(VueMaterial);
// import VueMaterial from 'vue-material';
// Vue.use(VueMaterial);

import 'vue-material/dist/vue-material.min.css';
import { MdButton, MdLayout, MdCard, MdTable, MdField, MdDialog, MdToolbar } from 'vue-material/dist/components';
Vue.use(MdLayout);
Vue.use(MdButton);
Vue.use(MdCard);
Vue.use(MdTable);
Vue.use(MdField);
Vue.use(MdDialog);
Vue.use(MdToolbar);

Vue.use(VueI18n);
export const i18n = new VueI18n({
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en: {
      hello: 'Hello',
    },
    de: {
      hello: 'Hallo',
    },
  },
});

import Default from './layouts/Default.vue';
import Empty from './layouts/Empty.vue';
import Full from './layouts/Full.vue';

Vue.component('default-layout', Default);
Vue.component('empty-layout', Empty);
Vue.component('full-layout', Full);

Vue.config.productionTip = false;

new Vue({
  router,
  i18n,
  store,
  render: (h) => h(App),
}).$mount('#app');
