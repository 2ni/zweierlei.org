<template>
  <div class="container">
    <div class="columns is-multiline">
      <div v-if="errored">
        <p>We could not retrieve the data at this moment.</p>
      </div>
      <div v-else-if="loading">
        Loading...
      </div>
      <div v-else class="column is-half" v-for="(story, i) in stories">

        <div class="card">
          <router-link :to="'/'+$i18n.locale+story.detail_url">
            <div class="card-image">
              <figure class="image">
                <img v-if="medias[i]" :src="medias[i] | imageSize('360')" :title="story.title">
                <img v-else src="https://bulma.io/images/placeholders/1280x960.png" :title="story.title">
              </figure>
              <!-- <pre class="content is-small">{{ story }} {{ medias[i] }}</pre> -->
            </div>
          </router-link>
          <div class="card-header">
            <p class="card-header-title has-background-dark has-text-white"><MapIcon :type="story.activity" />
              {{ story.title }}
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
        console.log('responseStories', responseStories);
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
        console.log('errorHome', error);
        (this as any).errored = true;
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

.card-content .content {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
   -webkit-box-orient: vertical;
   -webkit-line-clamp: 3; /* number of lines to show */
   line-height: 18px;        /* fallback */
   max-height: 54px;
}

.card {
  height: 420px;
  overflow: hidden;
}

.card-image {
  height: 320px;
  overflow: hidden;
}
</style>
