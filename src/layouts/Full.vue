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
  <section class="view-full">
    <nav class="navbar has-background-warning">
      <header-bar />
    </nav>
    <main>
      <slot />
    </main>
    <footer class="has-background-warning">
      <footer-bar />
    </footer>
  </section>
</template>

<style>
.view-full {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.view-full main {
  flex: 1;
}
</style>
