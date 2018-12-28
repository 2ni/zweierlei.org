<template>
  <div class="container">

    <NotFound v-if="idNotFound"/>

    <template v-if="story">
      <div v-if="story" class="tile is-ancestor">
        <div class="tile is-parent">
          <div class="tile is-child box">
            <router-link v-if="story.edit_url" :to="'/'+$i18n.locale+story.edit_url">
              <span class="icon">
                <i class="fa fa-edit"></i>
              </span>
            </router-link>
            <p class="title"><MapIcon :type="story.activity"/>{{ story.title}}</p>
            <p>{{ story.description }}</p>
          </div>
        </div>
      </div>

      <Masonry :medias="story.medias" />

    </template>

  </div>
</template>

<script type="ts">
import { storyService } from '@/services';
import NotFound from '@/components/NotFound.vue';
import MapIcon from '@/components/MapIcon.vue';
import Masonry from '@/components/Masonry.vue';

export default {
  mounted() {
    storyService.get(this.$route.params.id)
      .then((responseGet) => {
        this.story = responseGet.data;

        // https://hackernoon.com/masonry-layout-technique-react-demo-of-100-css-control-of-the-view-e4190fa4296
        /*
        console.log('medias', this.story.medias);
        const cols = 4;
        const out = [];
        let col = 0;
        while(col < cols) {
          console.log('col', col);
            for(let i = 0; i < this.story.medias.length; i += cols) {
                console.log('i+col', i + col);
                let _val = this.story.medias[i + col];
                if (_val !== undefined)
                    out.push(_val);
            }
            col++;
        }

        console.log('reorderedMedias', out);
        this.story.medias = out;
        */
      })
      .catch((errorGet) => {
        const { response: { status }, response: { data: { msg } } } = errorGet;
        if (status === 404) {
          this.idNotFound = true;
        } else {
          console.log(status, msg);
        }
      });
  },
  data() {
    return {
      idNotFound: false,
      story: null,
    };
  },
  methods: {
  },
  components: {
    NotFound,
    MapIcon,
    Masonry,
  },
};
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

.box .icon {
  position: absolute;
  top: 20px;
  right: 0;
}
</style>
