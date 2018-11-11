<template>
  <div class="container" @dragenter="emphasizeDropBox" @mouseout="deemphasizeDropBox">

      <div class="tile is-ancestor">
        <div class="tile is-4 is-parent">
          <div class="tile is-child box notification is-info">
            <p class="title">One</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin ornare magna eros, eu pellentesque tortor vestibulum ut. Maecenas non massa sem. Etiam finibus odio quis feugiat facilisis.</p>
          </div>
        </div>
        <div class="tile is-parent">
          <div class="tile is-child box">
            <p class="title">Three</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam semper diam at erat pulvinar, at pulvinar felis blandit. Vestibulum volutpat tellus diam, consequat gravida libero rhoncus ut. Morbi maximus, leo sit amet vehicula eleifend, nunc dui porta orci, quis semper odio felis ut quam.</p>
            <p>Integer sollicitudin, tortor a mattis commodo, velit urna rhoncus erat, vitae congue lectus dolor consequat libero. Donec leo ligula, maximus et pellentesque sed, gravida a metus. Cras ullamcorper a nunc ac porta. Aliquam ut aliquet lacus, quis faucibus libero. Quisque non semper leo.</p>
          </div>
        </div>
      </div>

      <div class="tile is-ancestor">

        <!-- table example -->
        <div class="tile is-parent">
          <div class="tile is-child notification is-paddingless is-warning card">
	    <div class="card-content">
	      <p class="title">Friends</p>
	      <p class="subtitle">by ddm</p>
	      <table class="table">
		<thead>
		  <tr>
		    <th>First name</th>
		    <th>Last name</th>
		    <th>Email</th>
		  </tr>
		</thead>
		<tbody>
		  <tr v-for="contact in contacts" :key="contact.email">
		    <td>{{contact.firstname}}</td>
		    <td>{{contact.lastname}}</td>
		    <td>{{contact.email}}</td>
		  </tr>
		</tbody>
	      </table>
	    </div>
	    <footer class="card-footer">
	      <a href="#" class="card-footer-item" v-on:click="fillTable">Fill it up!</a>
	      <a href="#" class="card-footer-item" v-on:click="clearTable">Clear data!</a>
	    </footer>
          </div>
        </div>

        <!-- drag & drop file upload -->
        <div class="tile is-parent">
          <div class="tile is-child notification is-warning is-paddingless card">
            <header class="card-header">
              <p class="card-header-title">File upload</p>
            </header>
            <div class="card-content">
              <p class="notification is-danger" v-show="isError">
                <pre>Error! {{ this.error }}</pre>
              </p>
              <form enctype="multipart/form-data" novalidate v-if="isInitial || isUploading || isSuccess">
                <div class="field">
                  <p class="control has-icons-left has-icons-right">
                    <input class="input" type="text" placeholder="Give some meaningful title">
                    <span class="icon is-small is-left">
                      <i class="fas fa-coffee"></i>
                    </span>
                    <span class="icon is-small is-right">
                      <i class="fas fa-check has-text-success"></i>
                    </span>
                  </p>
                  <p class="help is-success">Title</p>
                </div>
                <div class="field">
                  <p class="control has-icons-right">
                    <textarea class="textarea is-danger" placeholder="Meaningful description"></textarea>
                    <span class="icon is-small is-right">
                      <i class="fas fa-times has-text-danger"></i>
                    </span>
                  </p>
                  <p class="help is-danger">Mandatory field!</p>
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
// with thanks to https://github.com/chybie/file-upload-vue
import { upload } from './file-upload.fake.service';
import { wait } from './utils';

const STATUS_INITIAL = 0;
const STATUS_UPLOADING = 1;
const STATUS_SUCCESS = 2;
const STATUS_ERROR = 3;

export default {
  data() {
    return {
      contacts: [{firstname: 'John', lastname: 'Doe', email: 'john.doe@gmail.com'}],
      photos: [],
      photoCount: null,
      currentStatus: STATUS_INITIAL,
      error: null,
      isDragging: null,
      showDropBox: true,
    };
  },
  methods: {
    fillTable() {
      this.contacts.push({firstname: 'Foo', lastname: 'Bar', email: 'foobar@mail.com'});
    },
    clearTable() {
      this.contacts.splice(0, this.contacts.length);
    },
    dragDropAvailable() {
      // https://serversideup.net/drag-and-drop-file-uploads-with-vuejs-and-axios/
      const div = document.createElement('div');
      return ( ( 'draggable' in div )
          || ( 'ondragstart' in div && 'ondrop' in div ) )
          && 'FormData' in window
          && 'FileReader' in window;
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

      upload(data).then(wait(1000)).then((x) => {
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
