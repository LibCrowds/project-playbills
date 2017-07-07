import Vue from 'vue'
/* eslint-enable */
import LibcrowdsViewer from 'libcrowds-viewer'
import App from '@/Template'

Vue.component('libcrowds-viewer', LibcrowdsViewer)

/* eslint-disable no-new */
new Vue({
  el: '#project-iiif-mark-template',
  // render: h => h(App)
})
