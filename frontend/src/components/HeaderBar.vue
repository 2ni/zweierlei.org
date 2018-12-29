<template>
  <div class="container">
    <div class="navbar-brand">
      <router-link class="navbar-item" :to="$localize('home')">zweierlei.org</router-link>


      <span class="navbar-burger burger" data-target="navbarMenu" @click="showNav = !showNav" :class="{ 'is-active': showNav }">
        <span></span>
        <span></span>
        <span></span>
      </span>
    </div>

    <div id="navbarMenu" class="navbar-menu" :class="{ 'is-active': showNav }">
      <div class="navbar-start">
        <router-link
          :key="navItem.name"
          v-for="navItem in navItems"
          class="navbar-item"
          v-bind:class="$route.name == navItem.name ? 'is-active' : ''"
          :to="$localize(navItem.path)">{{ navItem.name }}</router-link>
      </div>

      <div class="navbar-end">
        <div class="navbar-item">
          <span>{{ helloUser() }}</span><span v-if="user">&nbsp;|&nbsp;</span>
          <router-link :to="$localize('login?f='+$route.fullPath)">
            {{ isLoggedIn ? 'Logout' : 'Login'}}
          </router-link>
        </div>

        <div class="navbar-item has-dropdown is-hoverable">
          <a class="navbar-link">{{ $i18n.locale }}</a>
          <div class="navbar-dropdown">
            <a
               v-for="(v,lang) in this.$i18n.messages"
              class="navbar-item"
              v-if="lang != $i18n.locale"
              :href="$localize($route.fullPath.replace(/^\/[^\/]*/, ''), lang)"
              v-on:click="changeLang(lang, $event)">{{ lang }}</a>
          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script type="ts">
export default {
  methods: {
    changeLang(lang, event) {
      this.$i18n.locale = lang;
      const path = this.$route.fullPath.replace(/^\/[^\/]*\//, '');
      this.$router.push(this.$localize(path));
      if (event) {
        event.preventDefault();
      }
    },
    helloUser() {
      if (this.user) {
        return 'Hello ' + this.user.firstname;
      }
    },
  },
  data() {
    return {
      navItems: [],
      showNav: false,
      user: false,
    };
  },
  computed: {
    isLoggedIn() {
      this.user = JSON.parse(localStorage.getItem('user'));
      return this.$store.state.authentication.status === 'loggedIn';
    },
  },
  created() {
    this.$router.options.routes.forEach((elem) => {
      if (elem.children) {
        elem.children.forEach((child) => {
          if (child.meta && child.meta.showHeader) {
            this.navItems.push({path: child.path, name: child.name});
          }
        });
      }
    });
  },
};
</script>

<style scoped>
}
</style>
