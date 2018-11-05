<template>
    <component :is="layout">
      <router-view />
    </component>
</template>

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

<style>
html, body {
  height: 100%;
}
</style>
