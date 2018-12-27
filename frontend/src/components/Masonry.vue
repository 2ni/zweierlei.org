<template>
  <div v-if="medias" class="tile is-ancestor">
    <div class="tile is-parent">
      <div class="tile is-child box has-background-grey-darker">
        <div class="masonry">
          <div class="masonryItem" v-for="media in medias">
            <figure class="image">
              <img :src="media.url">
            </figure>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class Masonry extends Vue {
  @Prop() private medias!: Array;
}
</script>

<style scoped>
.masonry {
  columns: 4;
  column-gap: 1em;
}

.masonryItem {
  background-color: black;
  display: inline-block;
  margin: 0 0 1em;
  width: 100%;
}
</style>
