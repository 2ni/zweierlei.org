<template>
    <span :title="(type ? type : 'coffee')" class="mapIconStack fa-stack">
      <i class="fa-stack-2x fas fa-map-marker has-text-warning"></i>
      <i class="mapIcon has-text-dark fa-stack-1x fas" :class="'fa-' + (type ? type : 'coffee')"></i>
    </span>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class MapIcon extends Vue {
  @Prop() private type!: string;
}
</script>

<style>
.mapIconStack {
  vertical-align: bottom;
  margin-right: 2px;
}
.mapIconStack .mapIcon {
  top: -8px;
}
</style>
