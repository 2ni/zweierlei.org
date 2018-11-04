<template>
  <div class="container">
    <div class="navbar-brand">
      <a class="navbar-item">zweierlei.org</a>
      <span class="navbar-burger burger" data-target="navbarMenu">
        <span></span>
        <span></span>
        <span></span>
      </span>
    </div>
    <div id="navbarMenu" class="navbar-menu">
      <div class="navbar-end">
        <router-link class="navbar-item is-active" to="/">Home</router-link>
        <router-link class="navbar-item" to="/about">About</router-link>
        <router-link class="navbar-item" to="/map">Map</router-link>
        <router-link class="navbar-item" to="/test">Test</router-link>
        <router-link class="navbar-item" to="/bulma">Bulma</router-link>
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
