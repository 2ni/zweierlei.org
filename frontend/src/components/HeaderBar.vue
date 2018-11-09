<template>
  <div class="container">
    <div class="navbar-brand">
      <a class="navbar-item">zweierlei.org</a>
      <span class="navbar-burger burger" data-target="navbarMenu" @click="showNav = !showNav" :class="{ 'is-active': showNav }">
        <span></span>
        <span></span>
        <span></span>
      </span>
    </div>
    <div id="navbarMenu" class="navbar-menu" :class="{ 'is-active': showNav }">
      <div class="navbar-end">
        <router-link
          :key="navItem.name"
          v-for="navItem in navItems"
          class="navbar-item"
          v-bind:class="$route.name == navItem.name ? 'is-active' : ''"
          :to="'/' + $route.params.locale + '/' + navItem.path">
          {{ navItem.name }}
        </router-link>
        <ul class="navbar-item">
          <li v-for="(v,lang) in this.$i18n.messages">
            <a
              v-if="lang != $i18n.locale"
              :href="'/' + lang + $route.path.replace(/^\/[^\/]*/, '')"
              v-on:click="changeLang(lang, $event)">
              {{ lang }}
            </a>
            <span v-if="lang == $i18n.locale">{{ lang }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script type="ts">
export default {
  methods: {
    changeLang(lang, event) {
      this.$i18n.locale = lang;
      this.$router.push('/' + lang + '/' + this.$route.name);
      if (event) {
        event.preventDefault();
      }
    },
  },
  data() {
    return {
      navItems: [],
      showNav: false,
    };
  },
  created() {
    this.$router.options.routes.forEach((elem) => {
      if (elem.children) {
        elem.children.forEach((child) => {
          if (child.path !== '*') {
            this.navItems.push({path: child.path, name: child.name});
          }
        });
      }
    });
  },
};
</script>

<style>
nav li:after {
  content: '|';
}

nav li:last-child:after {
  content: '';
}
</style>
