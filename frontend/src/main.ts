import Vue from 'vue';
import VueI18n from 'vue-i18n';
import L from 'leaflet';
import App from './App.vue';
import router from './router';
import store from './store';
import './registerServiceWorker';

import {messages, defaultLocale } from './locales/lang.json';

import 'leaflet.icon.glyph';

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

import 'bulma/css/bulma.css';

// see https://fontawesome.com/icons?d=gallery&m=free
// https://github.com/FortAwesome/vue-fontawesome#get-started
import { library, dom } from '@fortawesome/fontawesome-svg-core';
dom.watch(); // be able to use <i class="fas fa-coffee"></i>
import {
  faCoffee,
  faSyncAlt,
  faToggleOn,
  faToggleOff,
  faLocationArrow,
  faBullseye,
  faMapMarker,
  faRunning,
  faUtensils,
  faCrosshairs,
} from '@fortawesome/free-solid-svg-icons';
library.add(
  faCoffee,
  faSyncAlt,
  faToggleOn,
  faToggleOff,
  faLocationArrow,
  faBullseye,
  faMapMarker,
  faRunning,
  faUtensils,
  faCrosshairs,
);
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
Vue.component('font-awesome-icon', FontAwesomeIcon);

let locale = window.location.pathname.replace(/^\/([^\/]+).*/i,'$1');
console.log(locale);
Vue.use(VueI18n);
export const i18n = new VueI18n({
  locale: (locale.trim().length && locale != "/") ? locale : defaultLocale,
  fallbackLocale: defaultLocale,
  messages,
});

router.beforeEach((to, from, next) => {
  console.log(to.params);
  i18n.locale = to.params.locale;
  next();
/*
  let locale = to.params.locale;
  if (!locale) {
    console.log(locale, to.path);
    //router.go(i18n.fallbackLocale + to.path);
    locale = i18n.fallbackLocale;
  }
  i18n.locale = locale;

  //next({path: '/'+from.params.locale+to.fullPath});
  next();
*/
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
