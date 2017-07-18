<template>
  <libcrowds-viewer
    v-if="taskOpts"
    :taskOpts="taskOpts"
    @submit="handleResponse">
  </libcrowds-viewer>
</template>

<script>
import axios from 'axios'

export default {
  data: function () {
    return {
      project: {},
      tasks: []
    }
  },

  computed: {
    taskOpts: function () {
      return this.tasks.map(function (task) {
        return task.info
      })
    }
  },

  methods: {
    fetchProject () {
      const shortname = `${process.env.SHORT_NAME}`
      const api = `${process.env.API_URL}`
      const url = `${api}/project?short_name=${shortname}`
      axios.get(url, {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json'
        },
        data: {}
      }).then(r => {
        this.project = r.data
      }).catch(error => {
        console.log(error)
      })
    },

    fetchNewTasks () {
      const api = `${process.env.API_URL}`
      const url = `${api}/project/${this.project.id}/newtask?limit=100`
      axios.get(url, {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json'
        },
        data: {}
      }).then(r => {
        this.tasks = r.data
      }).catch(error => {
        console.log(error)
      })
    },

    handleResponse () {
      // TODO: refresh the page to fetch the next 100 tasks
      // TODO: handle response
    }
  },

  watch: {
    project: function () {
      this.fetchNewTasks()
    }
  },

  created () {
    this.fetchProject()
  }
}
</script>