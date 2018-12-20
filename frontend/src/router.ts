import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';
import Login from './views/Login.vue';
import Map from './views/Map.vue';
import Test from './views/Test.vue';
import Form from './views/Form.vue';
import Bulma from './views/Bulma.vue';
import Base from './views/Base.vue';
import EditStory from './views/EditStory.vue';
import PageNotFound from './views/PageNotFound.vue';

import { defaultLocale } from './locales/lang.json';

Vue.use(Router);

// https://stackoverflow.com/questions/51065687/vue-i18n-adding-locale-to-the-url-using-routerview
export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      redirect: '/' + defaultLocale, // `/${defaultLocale}`
    },
    {
      // path: `/(de|en)`,
      // path: '/:locale([a-z]{2})',
      path: '/:locale(en|de)',
      component: Base,
      children: [
        {
          path: 'edit',
          component: Base,
          children: [
            {
              path: 'story/:id?',
              name: 'EditStory',
              component: EditStory,
              meta: { auth: true },
            },
          ],
        },
        {
          path: 'login',
          name: 'Login',
          component: Login,
        },
        {
          path: '',
          redirect: { name: 'Home' },
        },
        {
          path: 'home',
          name: 'Home',
          component: Home,
        },

        {
          path: 'about',
          name: 'About',
          // route level code-splitting
          // this generates a separate chunk (about.[hash].js) for this route
          // which is lazy-loaded when the route is visited.
          component: () => import(/* webpackChunkName: "about" */ './views/About.vue'),
          meta: { auth: true },
        },
        {
          path: 'map',
          name: 'Map',
          component: Map,
          meta: { layout: 'full' },
        },
        {
          path: 'form',
          name: 'Form',
          component: Form,
        },
        {
          path: 'test',
          name: 'Full page',
          component: Test,
          meta: { layout: 'empty' },
        },
        {
          path: 'bulma',
          name: 'Bulma',
          component: Bulma,
          meta: { layout: 'empty' },
        },
        {
          path: '*',
          name: 'Notfound',
          component: PageNotFound,
        },
      ],
    },
    {
      path: '/([a-z]{2}/.*)',
      redirect: (to: any) => {
        return '/' + defaultLocale + to.path.replace(/^\/[^\/]+/, '');
      },
    },
    {
      path: '/*',
      redirect: (to: any) => {
      return '/' + defaultLocale + to.path;
      },
    },
  ],
});
