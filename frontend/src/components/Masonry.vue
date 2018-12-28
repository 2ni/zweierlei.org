<template>
  <div{{ width }}</div>
  <div v-if="medias.length" class="tile is-ancestor">
    <div class="tile is-parent">
      <div class="tile is-child box has-background-grey-darker">
        <div class="masonry" ref="masonry">
          <div class="masonryItem" v-for="media in medias">
            <figure class="image">
              <img :src="media.url | imageSize('360')">
            </figure>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">

export default {
  props: [ 'medias' ],
  mounted() {
    this.$nextTick(() => {
      window.addEventListener('resize', this.resized);
    });
  },
  methods: {
    resized(event) {
      const el = this.$refs.masonry.querySelector('img');
      const newWidth = el.clientWidth;
      if (this.width !== newWidth) {
        console.log('resized', this.$refs.masonry.clientWidth, el.clientWidth);
        this.width = el.clientWidth;
      }
    },
    calculateWidth() {
      this.width = this.$refs.masonry[0].querySelector('img').clientWidth;
    },
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resized);
  },
  data() {
    return {
      width: 0,
    };
  },
};
</script>

<style scoped>
.masonry {
  columns: 4;
  column-gap: 1em;
}

@media (max-width: 768px) {
  .masonry {
    columns: 1;
    columng-gap: 1em;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .masonry {
    columns: 2;
    columng-gap: 1em;
  }
}

.masonryItem {
  background-color: black;
  display: inline-block;
  margin: 0 0 1em;
  width: 100%;
}
</style>
