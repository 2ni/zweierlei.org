import Vue from 'vue';
import VueI18n from 'vue-i18n';
import VeeValidate from 'vee-validate';
import L from 'leaflet';
import App from './App.vue';
import router from './router';
import store from './store';
import './registerServiceWorker';
import { http } from '@/services';
import './filters';
import { localize } from '@/mixins';
Vue.mixin(localize);

Vue.prototype.$http = http;

/*
import { fakeBackend } from './helpers';
fakeBackend();
*/

import { messages, defaultLocale } from './locales/lang.json';

import 'leaflet.icon.glyph';

// delete L.Icon.Default.prototype._getIconUrl; // needed to display default icon

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
  faEdit,
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
  faUpload,
  faCheck,
  faTimes,
  faEnvelope,
  faLock,
  faCamera,
} from '@fortawesome/free-solid-svg-icons';
library.add(
  faEdit,
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
  faUpload,
  faCheck,
  faTimes,
  faEnvelope,
  faLock,
  faCamera,
);
// import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
// Vue.component('font-awesome-icon', FontAwesomeIcon);
/* tslint:disable:no-var-requires */
const fontawesome = require('@fortawesome/vue-fontawesome');
Vue.component('font-awesome-icon', fontawesome.FontAwesomeIcon);

const locale = window.location.pathname.replace(/^\/([^\/]+).*/i, '$1');
Vue.use(VueI18n);
export const i18n = new VueI18n({
  locale: (locale.trim().length && locale !== '/') ? locale : defaultLocale,
  fallbackLocale: defaultLocale,
  messages,
});

router.beforeEach((to: any, from: any, next: any) => {
  i18n.locale = to.params.locale;

  if (to.meta.auth && store.state.authentication.status != 'loggedIn') {
    return next({
      path: '/' + to.params.locale + '/login',
      query: { f: to.path },
    });
  }

  next();
/*
  //next({path: '/'+from.params.locale+to.fullPath});
  next();
*/
});

Vue.use(VeeValidate);

import Default from './layouts/Default.vue';
import Empty from './layouts/Empty.vue';
import Full from './layouts/Full.vue';

Vue.component('default-layout', Default);
Vue.component('empty-layout', Empty);
Vue.component('full-layout', Full);

Vue.config.productionTip = false;

import { userService } from '@/services';

new Vue({
  router,
  i18n,
  store,
  render: (h) => h(App),
}).$mount('#app');
