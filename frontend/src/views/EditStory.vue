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
              <p class="notification is-danger" v-show="isError">
                <pre>Error! {{ this.error }}</pre>
              </p>
              <form enctype="multipart/form-data" novalidate v-if="isInitial || isUploading || isSuccess" @submit.prevent="processForm">
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
                        <option v-for="activity in activities" :value="activity">{{activity}}</option>
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
                    <button class="button is-link">Save</button>
                  </div>
                </div>
              </form>
            </div>

            <div class="photos">
              <div class="card" style="z-index: 0;" v-for="photo in photos" :key="photo.url">
                <div class="card-image">
                  <figure class="image is-16by9">
                    <img :src="photo.url" :alt="photo.originalName" />
                  </figure>
                </div>
                <div class="card-content">
                  <p class="content is-small">{{ photo.originalName }}</p>
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
import { upload } from '@/services/file-upload.service';
// import { wait } from '@/helpers';

const STATUS_INITIAL = 0;
const STATUS_UPLOADING = 1;
const STATUS_SUCCESS = 2;
const STATUS_ERROR = 3;

export default {
  components: {
    MapIcon,
  },
  mounted() {
    if (this.$route.params.id) {
      this.$http.get('stories/' + this.$route.params.id)
      .then(response => {
        this.story = response.data;
      })
      .catch(error => {
      })
    }
  },
  data() {
    return {
      activities: ['utensils', 'coffee', 'running'],
      story: {},
      photos: [],
      photoCount: null,
      currentStatus: STATUS_INITIAL,
      error: null,
      isDragging: null,
      showDropBox: true,
    };
  },
  methods: {
    processForm(e) {
      this.$http.post('stories' + (this.$route.params.id ? '/'+this.$route.params.id : ''), this.story)
      .then(response => {
        const { data } = response;
        this.$store.state.alert = { message: 'Data successfully saved.', type: 'success' };
        if (!this.$route.params.id) {
          // new entry -> redirect to detail page
          this.$router.push({name: 'EditStory', params: {'id': data.id}});
        }

        // just set data from what we got
        this.story = data;
      })
      .catch(error => {
        const { response: { status }, response: { data: { msg } } } = error;
        if (status === 422) {
          // set errors returned from backend
          // https://github.com/baianat/vee-validate/issues/1153
          console.log(status, msg);
          for (var element in msg) {
            let field = this.$validator.fields.find({name: element});
            field.setFlags({invalid: true});
            this.errors.add({
              field: field.name,
              msg: msg[element],
              id: field.id,
              scope: field.scope,
            });
          }
        }
      })
    },
    emphasizeDropBox() {
      this.isDragging = true;
    },
    deemphasizeDropBox(event) {
      this.isDragging = false;
    },
    processFile(event) {
      this.photoCount = event.target.files.length;
      const data = new FormData();

      if (!this.photoCount) { return; }

      Array
          .from(Array(this.photoCount).keys())
          .map((x) => {
            data.append(event.target.name, event.target.files[x], event.target.files[x].name);
          });

      this.uploading(data);
      if (event) { return event.preventDefault(); }
    },
    uploading(data) {
      this.currentStatus = STATUS_UPLOADING;
      this.isDragging = false;

      // upload(data).then(wait(1000)).then((x) => {
      upload(data).then((x) => {
        this.photos = this.photos.concat(x);
        this.currentStatus = STATUS_SUCCESS;
      })
      .catch((err) => {
        this.error = err. response;
        this.currentStatus = STATUS_ERROR;
      });
    },
  },
  computed: {
    isInitial() {
      return this.currentStatus === STATUS_INITIAL;
    },
    isUploading() {
      return this.currentStatus === STATUS_UPLOADING;
    },
    isError() {
      return this.currentStatus === STATUS_ERROR;
    },
    isSuccess() {
      return this.currentStatus === STATUS_SUCCESS;
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
