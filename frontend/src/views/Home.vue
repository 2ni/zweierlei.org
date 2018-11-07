<template>
  <div class="container">
    <div class="columns is-multiline">
      <div class="column is-one-third" v-for="story in stories">

        <div class="card">
          <div class="card-image">
            <figure class="image is-4by3">
              <img :src="story.img ? story.img : 'https://bulma.io/images/placeholders/1280x960.png'" alt="foo">
            </figure>
          </div>
          <div class="card-header">
            <p class="card-header-title has-background-dark has-text-white">{{ story.title }}</p>
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
import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src

export default {
  name: 'Home',
  components: {
    HelloWorld,
  },
  data() {
    return {
      stories: [
        {id: 1, title: 'Some Title', description: 'Some text', img: 'https://picsum.photos/1280x960/?'+Math.random()},
        {id: 2, title: 'Beeing a philosoph', description: '... is like a flower in the prairie, a vessel in the wind, an elefant in the shower. Almost like stars in the sky.', img:'https://picsum.photos/1280x960/?'+Math.random()},
        {id: 3, title: 'Do some peace', description: 'And have a break.', img: 'https://picsum.photos/1280x960/?'+Math.random()},
        {id: 4, title: 'Newbie', description: 'Ich hab das noch nie gemacht, also bin ich wahrscheinlich gut darin - Anne Kjaer Riechert', img: 'https://picsum.photos/1280x960/?'+Math.random()},
        {id: 5, title: 'Come get some', description: 'DukeNukem'},
      ],
    };
  },
}
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
