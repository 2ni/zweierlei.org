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
  <section class="layout-default">
    <nav class="navbar has-background-warning">
      <header-bar />
    </nav>
    <div class="main"><slot /></div>
    <footer class="has-background-warning">
      <footer-bar />
    </footer>
  </section>
</template>

<style scoped>
.navbar {
  position: fixed;
  width: 100%;
}
.main {
  padding-top: 90px;
}
</style>
