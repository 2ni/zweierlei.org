<template>
  <div class="container" @dragenter="emphasizeDropBox" @mouseout="deemphasizeDropBox">

    <NotFound v-if="idNotFound" />

    <template v-else>

      <div class="tile is-ancestor">

        <!-- drag & drop file upload -->
        <div class="tile is-parent">
          <div class="tile is-8 is-child notification is-warning is-paddingless card">
            <header class="card-header">
              <p v-if="isNewStory" class="card-header-title">Create a story</p>
              <p v-else class="card-header-title">Update the story</p>
            </header>
            <div class="card-content">
              <form enctype="multipart/form-data" novalidate @submit.prevent="processSubmit">
                <div class="field">
                  <p class="control has-icons-left has-icons-right">
                    <input
                      v-validate="'required|max:100'"
                      name="title"
                      class="input"
                      v-bind:class="{ 'is-danger': errors.has('title') }"
                      type="text"
                      placeholder="Give some meaningful title"
                      v-model="story.title"
                    >
                    <span class="icon is-small is-left">
                      <i class="fas fa-coffee"></i>
                    </span>
                    <span v-show="errors.has('title')" class="icon is-small is-right">
                      <i class="fas fa-times has-text-danger"></i>
                    </span>
                  </p>
                  <p v-show="errors.has('title')" class="help is-danger">{{ errors.first('title') }}</p>
                </div>
                <div class="field">
                  <p class="control has-icons-right">
                  <textarea
                    v-validate="'required'"
                    name="description"
                    class="textarea"
                    v-bind:class="{ 'is-danger': errors.has('description') }"
                    placeholder="Meaningful description"
                    v-model="story.description"
                  ></textarea>
                    <span v-show="errors.has('description')" class="icon is-small is-right">
                      <i class="fas fa-times has-text-danger"></i>
                    </span>
                  </p>
                  <p v-show="errors.has('description')" class="help is-danger">{{ errors.first('description') }}</p>
                </div>
                <div class="field">
                  <div class="control has-icons-left">
                    <div class="select" v-bind:class="{ 'is-danger': errors.has('activity') }">
                      <select v-validate="{ is_not: 'undefined' }" name="activity" v-model="story.activity">
                        <option disabled value="undefined">Activity</option>
                        <option v-for="activity in activities" :value="activity">{{ $t('activity.'+activity) }}</option>
                      </select>
                    </div>
                    <div v-for="activity in activities" v-show="story.activity == activity" class="icon is-small is-left"><i class="fas" :class="['fa-'+activity]"></i></div>
                  </div>
                  <p v-show="errors.has('activity')" class="help is-danger">{{ errors.first('activity') }}</p>
                </div>
                <div class="dropField" v-show="isDragging || isUploading">
                  <p v-if="isInitial">Drop Files anywhere</p>
                  <p v-if="isUploading">Uploading {{ photosToUpload.length }} file(s)</p>
                  <input type="file" multiple name="photos" :disabled="isUploading" @change="processFile($event)" accept="image/*">
                </div>
                <div class="field">
                  <div class="label">
                    <label class="file-label">
                    <input type="file" class="file-input" @change="processFile($event)" name="photos" accept="image/*" :disabled="isUploading" multiple />
                    <span class="file-cta">
                      <span class="file-icon">
                        <i class="fas fa-upload"></i>
                      </span>
                      <span class="file-label">
                        <template v-if="isUploading">Uploading...</template>
                        <template v-else>Choose some files...</template>
                      </span>
                    </span>
                    </label>
                  </div>
                </div>
                <div class="field">
                  <div class="control">
                    <button class="button is-link" :disabled="isSaving">
                      <span v-if="isUploading || isSaving" class="icon is-small"><i class="fas fa-sync-alt fa-spin"></i></span>
                      <span>{{ $t('save') }}</span>
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>

          <div class="tile is-child">
            <header class="card-header">
              <p class="card-header-title">Meta information</p>
            </header>
            <div class="card-content">
              <table class="table">
                <tbody>
                  <tr v-for="(value, key) in storyExposed" :key="key">
                    <td>{{ key }}</td><td>{{ value }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>

      <Masonry :medias="photos" />

    </template>

  </div>
</template>

<script type="ts">
import NotFound from '@/components/NotFound.vue';
import MapIcon from '@/components/MapIcon.vue';
import Masonry from '@/components/Masonry.vue';

import { storyService } from '@/services';
import { filterObject } from '@/helpers';

// with thanks to https://github.com/chybie/file-upload-vue
// import { upload } from '@/services/file-upload.service';

const STATUS_INITIAL = 0;
const STATUS_UPLOADING = 1;
const STATUS_SAVING = 2;

export default {
  components: {
    NotFound,
    MapIcon,
    Masonry,
  },
  mounted() {
    if (!this.isNewStory) {
      storyService.get(this.$route.params.id)
        .then((responseGet) => {
          this.story = responseGet.data;
          this.photos = responseGet.data.medias;
        })
        .catch((errorGet) => {
          const { response: { status }, response: { data: { msg } } } = errorGet;
          if (status === 404) {
            this.idNotFound = true;
          } else {
            console.log(status, msg);
          }
        });
    }
  },
  data() {
    return {
      activities: ['utensils', 'camera', 'running'],
      story: {},
      photos: [],
      photosToUpload: [],
      currentStatus: STATUS_INITIAL,
      isDragging: null,
      idNotFound: false,
    };
  },
  methods: {
    processSubmit(e) {
      this.currentStatus = STATUS_SAVING;
      this.$http.post('stories' + (this.isNewStory ? '' : '/' + this.$route.params.id), this.story)
      .then((response) => {
        const { data } = response;
        if (this.isNewStory) {
          // upload attached medias after saving new story
          if (this.photosToUpload.length) {
            const medias = this.createFormData(this.photosToUpload);
            this.uploading(data.content_url, medias, true);
          } else {
            this.currentStatus = STATUS_INITIAL;
          }

          // new entry -> redirect to detail page
          this.$router.push({name: 'EditStory', params: {id: data.id}});
        } else {
          this.$store.dispatch('alert/success', $t('data.saved'));
          this.currentStatus = STATUS_INITIAL;
        }

        // just set data from what we got
        this.story = data;
      })
      .catch((error) => {
        const { response: { status }, response: { data: { msg } } } = error;
        if (status === 422) {
          // set errors returned from backend
          // https://github.com/baianat/vee-validate/issues/1153
          for (const element in msg) {
            if (msg.hasOwnProperty(element)) {
              const field = this.$validator.fields.find({name: element});
              field.setFlags({invalid: true});
              this.errors.add({
                field: field.name,
                msg: msg[element],
                id: field.id,
                scope: field.scope,
              });
            }
          }
        }
      });
    },
    emphasizeDropBox() {
      this.isDragging = true;
    },
    deemphasizeDropBox(event) {
      this.isDragging = false;
    },
    processFile(event) {
      const num = event.target.files.length;
      // this.photosToUpload.push.apply(this.photosToUpload, event.target.files);
      Array.prototype.push.apply(this.photosToUpload, event.target.files);

      // preview medias and ignore invalid ones
      for (let i = 0; i < num; i++) {
        const mime = event.target.files[i].type;
        // TODO better check for images https://stackoverflow.com/a/42983450/59391
        if (!mime.startsWith('image/')) {
          this.photosToUpload.splice(i, 1);
          continue;
        }

        const reader = new FileReader();
        reader.addEventListener('load', function(e) {
          // ensure reactivity
          this.photos.push({url: e.target.result});
          // var args = [this.photos.length, 0].concat({url: e.target.result});
          // this.photos.splice.apply(this.photos, args);
        }.bind(this), false);
        reader.readAsDataURL(event.target.files[i]);
      }

      if (!this.photosToUpload.length) {
        this.currentStatus = STATUS_INITIAL;
        this.deemphasizeDropBox();
        this.$store.dispatch('alert/error', 'No file was uploaded');
      } else {
        if (this.isNewStory) {
          // upload files after saving data
          this.deemphasizeDropBox();
        } else {
          // upload files instantly
          const medias = this.createFormData(this.photosToUpload);
          this.uploading(this.story.content_url, medias);
          event.target.value = null; // needed to be able to upload same media multiple times
        }
      }
      if (event) { return event.preventDefault(); }
    },
    createFormData(files) {
      const medias = new FormData();
      Array
          .from(Array(files.length).keys())
          .map((x) => {
            medias.append('medias', files[x]);
          });
      return medias;
    },
    uploading(contentUrl, medias, newStory = false) {
      if (!newStory) {
        this.currentStatus = STATUS_UPLOADING;
      }

      this.$http.put(contentUrl, medias)
        .then((response) => {
          this.currentStatus = STATUS_INITIAL;
          this.deemphasizeDropBox();
          if (newStory) {
            this.$store.dispatch('alert/success', 'Data successfully saved');
          }
          this.photosToUpload = [];
          this.story = response.data.story;
        })
        .catch((error) => {
          this.currentStatus = STATUS_INITIAL;
          const { response: { status }, response: { data: { msg } } } = error;
          this.$store.dispatch('alert/error', status + ': ' + msg);
          this.photosToUpload = [];
        });
    },
  },
  computed: {
    storyExposed() {
      return filterObject(this.story, ['created_human', 'lat', 'lon']);
    },
    isNewStory() {
      return this.$route.params.id === undefined;
    },
    isInitial() {
      return this.currentStatus === STATUS_INITIAL;
    },
    isUploading() {
      return this.currentStatus === STATUS_UPLOADING;
    },
    isSaving() {
      return this.currentStatus === STATUS_SAVING;
    },
  },
};
</script>

<style scoped>
.tile.is-child {
  margin: 0 .5em;
}

.dropField {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  border: 5px dotted yellow;
  align: center;
  z-index: 1;
}

.dropField p {
  position: absolute;
  left: 50%;
  top: 50%;
  font-size: 50px;
  color: yellow;
  transform: translate(-50%,-50%);
  -ms-transform: translate(-50%,-50%);
}

.dropField input {
  width: 100%;
  height: 100%;
  position: absolute;
  cursor: pointer;
  opacity: 0;
}

.photos {
  z-index: 0;
}
</style>
