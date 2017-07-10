import Vue from 'vue'
import VueCustomElement from 'vue-custom-element'
import LibCrowdsViewer from 'libcrowds-viewer'
import Template from '@/components/Template'

Vue.config.ignoredElements = [
  'project-iiif-mark-template',
  'project-iiif-mark-tutorial',
  'project-iiif-mark-results'
]

Vue.use(VueCustomElement)
Vue.customElement('project-iiif-mark-template', Template)
