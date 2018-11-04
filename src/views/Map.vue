<template>
  <div class="view-map">
    <div class="container">
      <h3 class="title">Simple map</h3>
      <p>Center is at {{ currentCenter }} and the zoom is: {{ currentZoom }} </p>
      <a class="button is-link is-medium" @click="showLongText">
        <span class="icon has-text-warning">
          <i class="fas fa-lg fa-toggle-on"></i>
        </span>
        <span>Long popup</span>
      </a>
    </div>
    <l-map
      class="container-map"
      ref="map"
      :zoom="zoom"
      :center="center"
      @move="centerUpdate"
      @update:zoom="zoomUpdate">
      <l-tile-layer
        :url="url"
        :attribution="attribution"/>
      <l-marker :lat-lng="marker">
        <l-popup>
          <div @click="popupClick">
            I am a tooltip
            <p v-show="showParagraph">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque sed pretium nisl, ut sagittis sapien. Sed vel sollicitudin nisi. Donec finibus semper metus id malesuada.
            </p>
          </div>
        </l-popup>
      </l-marker>
    </l-map>
  </div>
</template>

<style>
.leaflet-tile-pane {
  -webkit-filter: grayscale(90%);
  filter: grayscale(90%);
}
.view-map {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.view-map .container {
  padding: 1em 0;
}
.container-map {
  flex: 1;
}
</style>

<script>
import 'leaflet/dist/leaflet.css';
import { LMap, LTileLayer, LMarker, LPopup } from 'vue2-leaflet';

export default {
  name: 'Example',
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
  },
  data() {
    return {
      zoom: 13,
      center: L.latLng(47.3769, 8.5417),
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      marker: L.latLng(47.3769, 8.5417),
      currentZoom: 13,
      currentCenter: L.latLng(47.3769, 8.5417),
      showParagraph: false,
      map: null,
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.map = this.$refs.map.mapObject;
    });
  },
  methods: {
    zoomUpdate(zoom) {
      this.currentZoom = zoom;
    },
    centerUpdate(e) {
      this.currentCenter = this.map.getCenter();
    },
    showLongText() {
      this.showParagraph = !this.showParagraph;
    },
    popupClick() {
      alert('Popup Click!');
    },
  },
};
</script>
