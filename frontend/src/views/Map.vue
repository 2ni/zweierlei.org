<template>
  <div class="view-map">
    <div class="container">
      <h3 class="title">Simple map</h3>
      <p class="subtitle">Center: {{ currentCenter.lat.toFixed(5) }}/{{ currentCenter.lng.toFixed(5) }}, Zoom: {{ currentZoom }} </p>
      <a class="button is-link is-medium" @click="showLongText">
        <template v-if="showParagraph">
          <span class="icon has-text-warning">
            <i class="fas fa-lg fa-toggle-on"></i>
          </span>
        </template>
        <template v-else>
          <span class="icon has-color-grey">
            <i class="fas fa-lg fa-toggle-off"></i>
          </span>
        </template>
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
      <l-marker v-for="marker in markers" :key="marker.key" :lat-lng="marker.pos">
        <l-popup>
          <div @click="popupClick">
            {{ marker.summary }}
            <p v-show="showParagraph">{{ marker.tooltip }}</p>
          </div>
        </l-popup>
      </l-marker>
    </l-map>
  </div>
</template>

<style>
.iconCurrentPos {
  text-align: center;
  line-height: 40px;
}
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
import { LMap, LTileLayer, LMarker, LDivIcon, LPopup } from 'vue2-leaflet';

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
      markers: [
        {key: 1, pos: {lat: 47.3769, lng: 8.5417}, summary: 'Zurich', tooltip: 'Best town in the world', icon: 'coffee'},
        {key: 2, pos: {lat: 47.36087, lng: 8.53320}, summary: 'Chateau Chalet', tooltip: 'Some decent castle there', icon: 'coffee'},
      ]
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.map = this.$refs.map.mapObject;
      navigator.geolocation.getCurrentPosition(this.moveToCurrentPosition);
    });
  },
  methods: {
    // https://stackoverflow.com/questions/49099987/use-marker-icon-with-only-awesome-fonts-no-surrounding-balloon
    moveToCurrentPosition(pos) {
      this.center = L.latLng(pos.coords.latitude, pos.coords.longitude);
      const marker = L.marker([pos.coords.latitude, pos.coords.longitude], {
        icon: L.divIcon({
          html: '<span class="has-text-link"><i class="fas fa-bullseye fa-lg"></i></span>',
          iconSize: [40, 40],
          className: 'iconCurrentPos',
        }),
      });
      const circle = L.circle([pos.coords.latitude, pos.coords.longitude], pos.coords.accuracy / 2, {
        weight: 3,
        color: 'blue',
        fillColor: '#cacaca',
        fillOpacity: 0.2,
      });
      this.map.addLayer(marker);
      this.map.addLayer(circle);
    },
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
