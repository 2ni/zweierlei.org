<template>
  <div class="container">
    <div class="columns">
      <div class="column">
        <div class="card">
          <div class="card-header">
            <p class="card-header-title has-background-dark has-text-white">Some Title</p>
          </div>
          <div class="card-content">
            <p class="content is-small">Some text</p>
          </div>
        </div>
      </div>
      <div class="column">
        <div class="box">
          <p>Some more text</p>
        </div>
      </div>
      <div class="column">
        <div class="box">
          <p>Enough is enough</p>
        </div>
      </div>
    </div>

    <div class="columns">
      <div class="column">
        <div class="box has-background-info">
          <p>What do you want</p>
        </div>
      </div>
      <div class="column">
        <div class="box">
          <p>Some cookies.</p>
        </div>
      </div>
      <div class="column">
        <div class="box">
          <p>And some love.</p>
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

@Component({
  components: {
    HelloWorld,
  },
})
export default class Home extends Vue {}
</script>

<style scoped>
.container {
  padding: 1em 0;
}
</style>
