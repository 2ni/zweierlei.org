<template>
  <div class="view-map">
    <div class="container">
      <div class="block content is-large">
        <MapIcon type="running" />
        <span class="title">Simple Map</span>
      </div>
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
        <l-marker v-for="marker in markers" :key="marker.key" :lat-lng="marker.pos" :icon="icons[marker.icon]">
        <l-popup>
          <div @click="popupClick">
            {{ marker.summary }}
            <p v-show="showParagraph">{{ marker.tooltip }}</p>
          </div>
        </l-popup>
      </l-marker>
      <div v-if='isMapLoading' class="is-overlay is-size-2 has-text-weight-bold">
        <p>Detecting your position...</p>
      </div>
    </l-map>
  </div>
</template>

<style>
.is-overlay {
  opacity: 0.8;
}
.is-overlay p {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%,-50%);
  -ms-transform: translate(-50%,-50%);
}
.mapIcons {
  text-align: center;
  line-height: 40px;
}
.mapLabels {
  font-size: 18px;
  top: -20px;
}
.mapLabels .fa-coffee, .fa-running {
  top: -7px;
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
import MapIcon from '@/components/MapIcon.vue';

export default {
  name: 'Example',
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LDivIcon,
    LPopup,
    MapIcon,
  },
  data() {
    return {
      zoom: 13,
      center: L.latLng(47.3769, 8.5417),
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      currentZoom: 13,
      currentCenter: L.latLng(47.3769, 8.5417),
      showParagraph: false,
      positionFound: false,
      map: null,

      icons: {
        coffee: L.divIcon({
          html: '\
<span class="is-large">\
  <span class="fa-stack">\
    <i class="fa-stack-2x fas fa-map-marker has-text-warning"></i>\
    <i class="fa-stack-1x fas fa-coffee"></i>\
  </span>\
</span>',
          iconSize: [40, 40],
          className: 'mapIcons mapLabels',
        }),
        running: L.divIcon({
          html: '\
<span class="is-large">\
  <span class="fa-stack">\
    <i class="fa-stack-2x fas fa-map-marker has-text-warning"></i>\
    <i class="fa-stack-1x fas fa-running"></i>\
  </span>\
</span>',
          iconSize: [40, 40],
          className: 'mapIcons mapLabels',
        }),
        utensils: L.divIcon({
          html: '\
<span class="is-large">\
  <span class="fa-stack">\
    <i class="fa-stack-2x fas fa-map-marker has-text-warning"></i>\
    <i class="fa-stack-1x fas fa-utensils"></i>\
  </span>\
</span>',
          iconSize: [40, 40],
          className: 'mapIcons mapLabels',
        }),

      },
      markers: [],
      /*
      markers: [
        {
          key: 1,
          pos: { lat: 47.3769, lng: 8.5417 },
          summary: 'Zurich',
          tooltip: 'Best town in the world',
          icon: 'coffee'
        },
        {
          key: 2,
          pos: {lat: 47.36095, lng: 8.53328},
          summary: 'Chateau Chalet',
          tooltip: 'Some decent castle there',
          icon: 'running'
        },
        {
          key: 3,
          pos: {lat: 47.38, lng: 8.55},
          summary: 'Läckerli',
          tooltip: 'This speciality is special',
          icon: 'utensils'
        },
      ],
      */
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.map = this.$refs.map.mapObject;
      navigator.geolocation.getCurrentPosition(this.moveToCurrentPosition);
    });
  },
  computed: {
    isMapLoading() {
      return !this.positionFound;
    },
  },
  methods: {
    // https://stackoverflow.com/questions/49099987/use-marker-icon-with-only-awesome-fonts-no-surrounding-balloon
    moveToCurrentPosition(pos) {
      this.positionFound = true;
      this.center = L.latLng(pos.coords.latitude, pos.coords.longitude);
      const marker = L.marker([pos.coords.latitude, pos.coords.longitude], {
        icon: L.divIcon({
          html: '<span class="has-text-link"><i class="fas fa-crosshairs fa-lg"></i></span>',
          iconSize: [40, 40],
          className: 'mapIcons',
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

      const icons = ['coffee', 'running', 'utensils'];
      for (let i = 0; i < 100; i++) {
        this.markers.push({
          key: i,
          pos: {
            lat: Math.random() * .1 + this.center.lat - .05,
            lng: Math.random() * .1 + this.center.lng - .05},
          summary: 'Foo',
          tooltip: 'Description',
          icon: icons[Math.round(Math.random() * 2)],
        });
      }

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
