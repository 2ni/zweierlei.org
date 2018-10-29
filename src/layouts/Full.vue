<script>
import HeaderBar from '@/components/HeaderBar';
import FooterBar from '@/components/FooterBar';

export default {
  components: {
    HeaderBar,
    FooterBar,
  },
};
</script>

<template>
  <section class="layout-base layout-full">
    <header-bar />
    <slot />
    <footer-bar />
  </section>
</template>

<style>
  section.layout-full {
    height: 100%;
    border: 3px solid red;
  }
</style>
