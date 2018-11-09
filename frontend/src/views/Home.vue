<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-one-third" v-for="story in stories">

        <div class="card">
          <div class="card-image">
            <figure class="image is-4by3">
              <img :src="story.img ? story.img + '?' + Math.random() : 'https://bulma.io/images/placeholders/1280x960.png'" alt="foo">
            </figure>
          </div>
          <div class="card-header">
            <p class="card-header-title has-background-dark has-text-white"><MapIcon :type="story.activity" />{{ story.title }}</p>
          </div>
          <div class="card-content">
            <p class="content is-small">{{ story.description }}</p>
          </div>
        </div>

      </div>
    </div>

    <!--
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/>
    -->
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import MapIcon from '@/components/MapIcon.vue';
// import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src

export default {
  name: 'Home',
  components: {
    MapIcon,
    // HelloWorld,
  },
  data() {
    return {
      stories: require('@/views/stories.json'),
    };
  },
};
</script>

<style scoped>
.container {
  padding: 1em 0;
}
.card-header {
  position: absolute;
  top: 0;
  width: 100%;
  opacity: .8;
}
</style>
