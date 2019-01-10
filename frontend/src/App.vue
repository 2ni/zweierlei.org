<template>
    <component :is="layout">
      <transition v-on:enter="alertOpen" v-on:leave-to="alertClosed" name="alert">
        <div v-if="alert.message" :class="`box notification is-${alert.type}`">{{ alert.message }}</div>
      </transition>
      <router-view />
    </component>
</template>

<script lang="ts">
const defaultLayout = 'default';
import { delay } from '@/helpers';

export default {
  computed: {
    layout(): string {
      return (this.$route.meta.layout || defaultLayout) + '-layout';
    },
    alert() {
      return this.$store.state.alert;
    },
  },
  methods: {
    alertClosed(el, done) {
      this.$store.dispatch('alert/clear');
    },
    alertOpen(el, done) {
      delay(2000)
        .then(() => {
          this.$store.dispatch('alert/clear');
        });
    },
  },
  /*
  watch: {
    $route(to: any, from: any) {
      // clear alert on location change
      this.$store.dispatch('alert/clear');
    },
  },
  mounted() {
    // this.$store.dispatch('alert/error', 'Foo');
  },
  */
};

</script>

<style>
html, body {
  height: 100%;
}
.alert-leave-active {
  transition: opacity .5s;
}
.alert-leave-to {
  opacity: 0;
}
</style>
