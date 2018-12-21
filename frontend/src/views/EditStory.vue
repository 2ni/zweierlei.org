<template>
  <div class="container" @dragenter="emphasizeDropBox" @mouseout="deemphasizeDropBox">

      <div class="tile is-ancestor">

        <!-- drag & drop file upload -->
        <div class="tile is-parent">
          <div class="tile is-child notification is-warning is-paddingless card">
            <header class="card-header">
              <p class="card-header-title">Create a story</p>
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
                        <option v-for="activity in activities" :value="activity">{{ $t('activity_'+activity) }}</option>
                      </select>
                    </div>
                    <div v-for="activity in activities" v-show="story.activity == activity" class="icon is-small is-left"><i class="fas" :class="['fa-'+activity]"></i></div>
                  </div>
                  <p v-show="errors.has('activity')" class="help is-danger">{{ errors.first('activity') }}</p>
                </div>
                <div class="dropField" v-show="isDragging || isUploading">
                  <p v-if="isInitial">Drop Files anywhere</p>
                  <p v-if="isUploading">Uploading {{ photoCount }} file(s)</p>
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
                      <span>{{ saveText }}</span>
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>

      <div class="tile is-ancestor">
        <div class="tile is-parent">
          <div class="columns is-multiline">
            <div class="column is-one-quarter" v-for="photo in photos">
              <div class="card" style="z-index: 0;">
                <div class="card-image">
                  <figure class="image">
                    <img :src="photo.url" />
                  </figure>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
</div>
</template>

<script type="ts">
import MapIcon from '@/components/MapIcon.vue';

// with thanks to https://github.com/chybie/file-upload-vue
// import { upload } from '@/services/file-upload.service';

const STATUS_INITIAL = 0;
const STATUS_UPLOADING = 1;
const STATUS_SAVING = 2;
const STATUS_ERROR = 3;

export default {
  components: {
    MapIcon,
  },
  mounted() {
    if (!this.isNewStory) {
      this.$http.get('stories/' + this.$route.params.id)
      .then((responseStories) => {
        this.story = responseStories.data;
        this.$http.get(this.story.content_url)
          .then((responseContent) => {
            this.photos = responseContent.data.medias;
          });
      })
      .catch((error) => {
        console.log(error.response.status, error.response.data.msg);
      });
    }
  },
  data() {
    return {
      activities: ['utensils', 'camera', 'running'],
      story: {},
      photos: [],
      photosToUpload: [],
      photoCount: null,
      currentStatus: STATUS_INITIAL,
      isDragging: null,
      saveText: 'Save',
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
          const medias = this.createFormData(this.photosToUpload);
          this.uploading(data.content_url, medias, true);

          // new entry -> redirect to detail page
          this.$router.push({name: 'EditStory', params: {id: data.id}});
        } else {
          this.$store.state.alert = { message: 'Data successfully saved.', type: 'success' };
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
          console.log(status, msg);
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
      this.photoCount = event.target.files.length;
      if (!this.photoCount) { return; }

      // preview medias
      for (let i = 0; i < this.photoCount; i++) {
        const reader = new FileReader();
        reader.addEventListener('load', function(e) {
          // ensure reactivity
          this.photos.push({url: e.target.result});
          // var args = [this.photos.length, 0].concat({url: e.target.result});
          // this.photos.splice.apply(this.photos, args);
        }.bind(this), false);
        reader.readAsDataURL(event.target.files[i]);
      }

      this.photosToUpload.push.apply(this.photosToUpload, event.target.files);

      if (this.isNewStory) {
        // upload files when saving
        this.deemphasizeDropBox();
      } else {
        // upload files instantly
        const medias = this.createFormData(this.photosToUpload);
        this.uploading(this.story.content_url, medias);
        event.target.value = null; // needed to be able to upload same media multiple times
      }
      if (event) { return event.preventDefault(); }
    },
    createFormData(files) {
      const medias = new FormData();
      Array
          .from(Array(this.photoCount).keys())
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
            this.$store.state.alert = { message: 'Data successfully saved.', type: 'success' };
          }

          // const { data: { responseMedias } } = response;
          // var args = [this.photos.length, 0].concat(responseMedias);
          // Array.prototype.splice.apply(this.photos, args);
          // console.log("photos processed", this.photos);
          // this.photos = this.photos.concat(responseMedias);
        })
        .catch((error) => {
          const { response: { status }, response: { data: { msg } } } = error;
          console.log('upload error', status, msg);
          this.currentStatus = STATUS_ERROR;
        });
    },
  },
  computed: {
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
    isError() {
      return this.currentStatus === STATUS_ERROR;
    },
  },
};
</script>

<style scoped>
.container {
  padding: 1em 0;
}

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
