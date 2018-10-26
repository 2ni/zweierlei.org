<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> |
      <router-link to="/map">Map</router-link>
    </div>
    <ul id="lang">
      <li v-for="(v,lang) in this.$i18n.messages">
        <a v-if="lang != currentLocale" :href="lang" v-on:click="changeLang(lang, $event)">{{lang}}</a>
        <span v-if="lang == currentLocale">{{lang}}</span>
      </li>
    </ul>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

#lang {
  list-style-type: none;
  text-align: center;
}

#lang li {
  display: inline;
}

#lang li:after {
  content: ' | ';
}

#lang li:last-child:after {
  content: '';
}
</style>

<script lang="ts">
export default {
  methods: {
    changeLang(lang: any, event: any) {
      (this as any).$i18n.locale = lang;
      if (event) {
        event.preventDefault();
      }
    },
  },
  computed: {
    currentLocale(): string {
      return (this as any).$i18n.locale;
    },
  },
};

</script>
