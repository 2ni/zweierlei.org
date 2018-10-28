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
  html, body {
    height: 100%;
  }

  section {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    border: 3px solid red;
    height: 100%;
    display: table;
    width: 100%;
  }
</style>
