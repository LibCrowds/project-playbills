<template>
  <div id="project">
    <libcrowds-viewer
      confirm-before-unload
      show-note
      :scheme="scheme"
      :server="server"
      :image-api-prefix="imageApiPrefix"
      :presentation-api-prefix="presentationApiPrefix"
      :image-id="imageId"
      @submit="handleResponse">
    </libcrowds-viewer>
  </div>
</template>

<script>
import context from 
import LibCrowdsViewer from 'libcrowds-viewer'

console.log('module loaded')

export default {
  data: function () {
    return {
      scheme: "https",
      server: "api.bl.uk",
      imageApiPrefix: "image/iiif",
      presentationApiPrefix: "metadata/iiif"
    }
  },

  components: {
    LibCrowdsViewer
  },

  methods: {
    fetchNewTask () {
      // TODO: fetch a new task for the user
    },
    handleResponse () {
      // TODO: handle response
      this.fetchNewTask()
    }
  },

  mounted () {
    console.log('mounted')
    this.fetchNewTask()
  }
}
</script>