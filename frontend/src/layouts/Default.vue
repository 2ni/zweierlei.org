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
    <slot />
    <footer class="has-background-warning">
      <footer-bar />
    </footer>
  </section>
</template>
