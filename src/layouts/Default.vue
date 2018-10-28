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
  <section>
    <header-bar />
    <slot />
    <footer-bar />
  </section>
</template>

<style>
  section {
    height: 100%;
  }
</style>
