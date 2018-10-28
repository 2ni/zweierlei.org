<template>
  <nav>
    <div>
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> |
      <router-link to="/map">Map</router-link> |
      <router-link to="/test">Test</router-link>
      <ul>
        <li v-for="(v,lang) in this.$i18n.messages">
          <a v-if="lang != currentLocale" :href="lang" v-on:click="changeLang(lang, $event)">{{lang}}</a>
          <span v-if="lang == currentLocale">{{lang}}</span>
        </li>
      </ul>
    </div>
  </nav>
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
nav {
  width: 100%;
  background: lightgrey;
  display: table-row;
}
nav > div {
  border: 1px solid grey;
  display: table-cell;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

nav ul {
  list-style-type: none;
  text-align: center;
  padding: 0;
  position: absolute;
  top: 0;
  right: 10px;
  margin: 5px 0;
}

nav li {
  display: inline;
}

nav li:after {
  content: ' | ';
}

nav li:last-child:after {
  content: '';
}
</style>
