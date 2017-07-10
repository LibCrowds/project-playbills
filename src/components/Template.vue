<template>
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
</template>

<script>
import LibCrowdsViewer from 'libcrowds-viewer'

console.log(LibCrowdsViewer)

export default {
  data: function () {
    return {
      scheme: "https",
      server: "api.bl.uk",
      imageApiPrefix: "image/iiif",
      presentationApiPrefix: "metadata/iiif",
      imageId: null
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

  created () {
    console.log('created')
  },

  mounted () {
    console.log('mounted')
    this.fetchNewTask()
  }
}
</script>