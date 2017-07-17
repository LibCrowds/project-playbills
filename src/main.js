import Vue from 'vue'
import VueCustomElement from 'vue-custom-element'
import LibCrowdsViewer from 'libcrowds-viewer'
import Template from '@/components/Template'

Vue.config.ignoredElements = [
  'project-iiif-annotate-template',
  'project-iiif-annotate-tutorial',
  'project-iiif-annotate-results'
]

Vue.use(VueCustomElement)
Vue.use(LibCrowdsViewer)
Vue.customElement('project-iiif-annotate-template', Template)
