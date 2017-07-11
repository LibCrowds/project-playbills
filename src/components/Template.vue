<template>
  <libcrowds-viewer
    confirm-before-unload
    show-note
    :scheme="scheme"
    :server="server"
    :image-api-prefix="imageApiPrefix"
    :presentation-api-prefix="presentationApiPrefix"
    :image-id="imageId"
    :manifest-id="manifestId"
    @submit="handleResponse">
  </libcrowds-viewer>
</template>

<script>
export default {
  data: function () {
    return {
      scheme: "https",
      server: "api.bl.uk",
      imageApiPrefix: "image/iiif",
      presentationApiPrefix: "metadata/iiif",
      imageId: '',
      manifestId: ''
    }
  },

  methods: {
    fetchProject () {
      const shortname = `${process.env.SHORT_NAME}`
      console.log(shortname)
      const url = `/project/${shortname}/`
      pybossaApi.get(url).then(r => {
        console.log(r)
      }).catch(error => {
        console.log(error)
      })
    },
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
    this.fetchProject()
  }
}
</script>