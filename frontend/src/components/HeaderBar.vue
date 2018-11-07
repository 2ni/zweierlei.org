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
          v-for="(navItem,index) in navItems"
          class="navbar-item"
          v-bind:class="currentRoute == navItem.toLowerCase() ? 'is-active':''"
          :to="'/'+(index==0 ? '' : navItem.toLowerCase())">
          {{ navItem }}
        </router-link>
        <ul class="navbar-item">
          <li v-for="(v,lang) in this.$i18n.messages">
            <a v-if="lang != currentLocale" :href="lang" v-on:click="changeLang(lang, $event)">{{lang}}</a>
            <span v-if="lang == currentLocale">{{lang}}</span>
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
      if (event) {
        event.preventDefault();
      }
    },
  },
  computed: {
    currentLocale() {
      return this.$i18n.locale;
    },
    currentRoute() {
      return this.$route.name;
    },
  },
  data() {
    return {
      navItems: ['Home', 'About', 'Map', 'Test', 'Bulma'],
      showNav: false,
    };
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
