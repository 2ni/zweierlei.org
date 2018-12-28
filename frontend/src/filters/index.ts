import Vue from 'vue';

// filter to get imageSize, eg <url> | imageSize('360')
Vue.filter('imageSize', (value, size) => value.replace(/orig/g, size));
