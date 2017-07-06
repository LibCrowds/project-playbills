<template>
  <div id="project-content">
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
import LibCrowdsViewer from 'libcrowds-viewer'

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
      
    },
    handleResponse () {
      // TODO: handle response
    }
  }
}
</script>