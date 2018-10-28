<template>
    <component :is="layout">
      <router-view />
    </component>
</template>

<style>
@import "https://fonts.googleapis.com/css?family=Roboto:400,500,700,400italic|Material+Icons";
html, body {
  margin: 0;
  padding: 0;
}
</style>

<script lang="ts">
const defaultLayout = 'default';

export default {
  computed: {
    layout(): string {
      return (this.$route.meta.layout || defaultLayout) + '-layout';
    },
  },
};

</script>
