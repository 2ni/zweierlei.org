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
                <form enctype='multipart/form-data' novalidate v-if='isInitial || isUploading'>
                  <div class='dropBox' v-bind:class="{ dropBoxHighlight: isDragging }">
                    <input type="file" multiple name="files" :disabled="isUploading" @change="processFile($event)" accept="image/*">
                    <!--
                    <md-field>
                      <label>Upload files</label>
                      <md-file class="file-upload" @change='processFile($event)' name='files' accept='image/*' :disabled='isUploading' multiple />
                    </md-field>
                    -->
                    <p v-if='isInitial'>Drop files here</p>
                    <p v-if='isUploading'>Uploading {{ fileCount }} file(s)</p>
                  </div>
                </form>
              </md-card-content>
            </md-card>
            <md-card v-for='item in files' :key="item.url">
              <md-card-media md-ratio='16:9'>
                <img src='item.url' alt='item.originalName'>
              </md-card-media>
            </md-card>
          </div>
        </div>
      </div>
    </div>
</main>
</template>

<script type="ts">
const STATUS_INITIAL = 0;
const STATUS_UPLOADING = 1;
const STATUS_SUCCESS = 2;
const STATUS_FAILED = 3;

export default {
  data() {
    return {
      contacts: [{firstname: 'John', lastname: 'Doe', email: 'john.doe@gmail.com'}],
      files: null,
      fileCount: null,
      currentStatus: STATUS_INITIAL,
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
    uploading(data) {
      this.currentStatus = STATUS_UPLOADING;
    },
    emphasizeDropBox() {
      this.isDragging = true;
    },
    deemphasizeDropBox(event) {
      this.isDragging = false;
    },
    processFile(event) {
      this.fileCount = event.target.files.length;
      const data = new FormData();

      if (!this.fileCount) { return; }

      Array
          .from(Array(event.target.files.length).keys())
          .map(x => {
            data.append(event.target.name, event.target.files[x], event.target.files[x].name);
          });

      this.uploading(data);

      console.log(event.target.name);
      console.log(event.target.files[0].name);
      console.log(event.target.files.length);

      if (event) { return event.preventDefault(); }
    },
  },
  computed: {
    isInitial() {
      return this.currentStatus === STATUS_INITIAL;
    },
    isUploading() {
      return this.currentStatus === STATUS_UPLOADING;
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

.dropBox {
  background: lightgrey;
  border: 2px solid lightgrey;
  position: relative;
  cursor: pointer;
  overflow: hidden;
  padding: 0;
}

.dropBox input {
  width: 100%;
  height: 200px;
  position: absolute;
  cursor: pointer;
  border: 1px solid black;
  opacity: 0;
}

/*
.dropBox .file-upload .md-input {
  width: 100%;
  height: 200px;
  position: absolute;
  cursor: pointer;
  border: 1px solid black;
}
*/

.dropBoxHighlight {
  border: 2px dotted black;
}

.dropBox p {
  text-align: center;
}

</style>
