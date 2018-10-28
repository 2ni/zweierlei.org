<template>
  <main id="main-map">
    <div>
      <div class="container">
        <div>
          <header>
            <h3>Simple map</h3>
            <p>Marker is placed at {{ marker.lat }}, {{ marker.lng }}</p>
            <p> Center is at {{ currentCenter }} and the zoom is: {{ currentZoom }} </p>
            <button @click="showLongText">Toggle Long popup</button>
          </header>
        </div>
        <div>
          <l-map
            class="map"
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
      </div>
    </div>
  </main>
</template>

<style>
#main-map {
  height: 100%;
  display:table-row;
  width: 100%;
  background: pink;
}

#main-map > div {
  display: table-cell;
}

#main-map .container {
  display: table;
  width: 100%;
  height: 100%;
}

#main-map .container > div {
  display: table-row;
}

#main-map .container header {
  display: table-cell;
  height: 1%;
}

#main-map .container .map {
  background: lightgreen;
  height: 100%;
  border: 1px solid green;
}

.leaflet-tile-pane {
  -webkit-filter: grayscale(90%);
  filter: grayscale(90%);
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
