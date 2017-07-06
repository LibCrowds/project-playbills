import Vue from 'vue'
/* eslint-enable */
import App from './App.vue';

Vue.component('libcrowds-viewer', LibcrowdsViewer)

/* eslint-disable no-new */
new Vue({
  el: '#project-playbills-mark',
  render: h => h(App)
})