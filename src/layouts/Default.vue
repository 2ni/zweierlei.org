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
  <section class="layout-base layout-default">
    <header-bar />
    <slot />
    <footer-bar />
  </section>
</template>
