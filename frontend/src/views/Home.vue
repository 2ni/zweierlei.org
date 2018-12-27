<template>
  <div class="container">
    <div class="columns is-multiline">
      <div v-if="errored">
        <p>We could not retrieve the data at this moment.</p>
      </div>
      <div v-else-if="loading">
        Loading...
      </div>
      <div v-else class="column is-one-third" v-for="(story, i) in stories">

        <div class="card">
          <div class="card-image">
            <figure class="image is-4by3">
              <img :src="medias[i] ? medias[i] : 'https://bulma.io/images/placeholders/1280x960.png'" :title="story.title">
            </figure>
            <pre class="content is-small">{{ story }} {{ medias[i] }}</pre>
          </div>
          <div class="card-header">
            <p class="card-header-title has-background-dark has-text-white"><MapIcon :type="story.activity" />
              <router-link :to="'/'+$i18n.locale+'/edit/story/'+story.id">{{ story.title }}</router-link>
            </p>
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
  mounted() {
    (this as any).$http.get('stories')
      .then((responseStories) => {
        (this as any).stories = responseStories.data;
        for (let i = 0; i < (this as any).stories.length; i++) {
          (this as any).$http.get((this as any).stories[i].content_url)
            .then((responseContent) => {
              if (responseContent.data.medias[0]) {
                Vue.set((this as any).medias, i, responseContent.data.medias[0].url);
              }
            });
        }
      })
      .catch((error) => {
        (this as any).errored = true;
        console.log(error);
      })
      .finally(() => (this as any).loading = false);
  },
  data() {
    return {
      stories: null,
      medias: {},
      loading: true,
      errored: false,
    };
  },
};
</script>

<style scoped>
.card-header {
  position: absolute;
  top: 0;
  width: 100%;
  opacity: .8;
}
</style>
