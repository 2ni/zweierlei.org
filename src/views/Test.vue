<template>
<main id="main-test">
    <header>
      <div>
        <p>test</p>I have some height
      </div>
    </header>
    <div>
      <div class="content" @dragenter="emphasizeDropBox" @mouseout="deemphasizeDropBox">
        <p>I take up the remaining height</p>
        <div class="md-layout md-gutter">
          <!-- table example -->
          <div class="md-layout-item md-small-size-100">
            <md-card>
              <md-card-header>
                <div class="md-title">Friends</div>
                <div class="md-subhead">by ddm</div>
              </md-card-header>
              <md-card-content>
                <md-table>
                  <md-table-row>
                    <md-table-head>First name</md-table-head>
                    <md-table-head>Last name</md-table-head>
                    <md-table-head>Email</md-table-head>
                  </md-table-row>
                  <md-table-row v-for="contact in contacts" :key="contact.email">
                    <md-table-cell>{{contact.firstname}}</md-table-cell>
                    <md-table-cell>{{contact.lastname}}</md-table-cell>
                    <md-table-cell>{{contact.email}}</md-table-cell>
                  </md-table-row>
                </md-table>
              </md-card-content>
              <md-card-actions>
                <md-button v-on:click="fillTable" class="md-raised md-primary">Fill it up!</md-button>
                <md-button v-on:click="clearTable" class="md-raised md-primary">Clear data!</md-button>
              </md-card-actions>
            </md-card>
          </div>

          <!-- drag & drop file upload -->
          <div class="md-layout-item">
            <md-card>
              <md-card-header>
                <div class="md-title">File upload</div>
              </md-card-header>
              <md-card-content>
                <md-toolbar class="md-dense" v-show="isError">
                  <pre>Error! {{ this.error }}</pre>
                </md-toolbar>
                <form enctype='multipart/form-data' novalidate v-if='isInitial || isUploading || isSuccess'>
                  <div class='dropField' v-show="isDragging">
                    <p v-if='isInitial'>Drop Files anywhere</p>
                    <p v-if='isUploading'>Uploading {{ photoCount }} file(s)</p>
                    <input type="file" multiple name="photos" :disabled="isUploading" @change="processFile($event)" accept="image/*">
                  </div>
                  <md-field>
                    <label>Upload photos</label>
                    <md-file class="file-upload" @change='processFile($event)' name='photos' accept='image/*' :disabled='isUploading' multiple />
                  </md-field>
                </form>
              </md-card-content>
            </md-card>
            <div class="photos">
              <md-card style="z-index: 0" v-for='item in photos' :key="item.url">
                <md-card-media md-ratio='16:9'>
                  <img :src='item.url' :alt='item.originalName'>
                </md-card-media>
              </md-card>
            </div>
          </div>
        </div>
      </div>
    </div>
</main>
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
          .map(x => {
            data.append(event.target.name, event.target.files[x], event.target.files[x].name);
          });

      this.uploading(data);
      if (event) { return event.preventDefault(); }
    },
    uploading(data) {
      this.currentStatus = STATUS_UPLOADING;
      this.isDragging = false;

      upload(data).then(wait(1000)).then(x => {
        this.photos = this.photos.concat(x);
        this.currentStatus = STATUS_SUCCESS;
      })
      .catch(err => {
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

<style>
#main-test {
    height: 100%;
    width: 100%;
    margin: 0;
    display: table;
}

#main-test header {
    height: 0%;
    background-color: grey;
    display: table-row;
}

#main-test header div {
  display: table-cell;
  padding: 10px;
}

#main-test > div {
    background-color: pink;
    display: table-row;
}

#main-test .content {
  display: table-cell;
  padding: 10px;
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
  border: 10px solid black;
  opacity: 0;
}

.photos {
  z-index: 0;
}
</style>
