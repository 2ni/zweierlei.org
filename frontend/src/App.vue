<template>
    <component :is="layout">
      <div v-if="alert.message" :class="`box notification is-${alert.type}`">{{ alert.message }}</div>
      <router-view />
    </component>
</template>

<script lang="ts">
const defaultLayout = 'default';

export default {
  computed: {
    layout(): string {
      return ((this as any).$route.meta.layout || defaultLayout) + '-layout';
    },
    alert() {
      return (this as any).$store.state.alert;
    },
  },
  watch: {
    $route(to: any, from: any) {
      // clear alert on location change
      (this as any).$store.dispatch('alert/clear');
    },
  },
  mounted() {
    // (this as any).$store.state.alert = { message: 'Foo', type: 'danger' };
  },
};

</script>

<style>
html, body {
  height: 100%;
}
</style>
