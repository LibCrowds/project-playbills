<template>
  <libcrowds-viewer
    v-if="taskOpts.length"
    :taskOpts="taskOpts"
    @submit="handleResponse">
  </libcrowds-viewer>
</template>

<script>
import { api } from '../api'

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
      return api.get(`/project?short_name=${process.env.SHORT_NAME}`)
    },

    fetchNewTasks () {
      return api.get(`project/${this.project.id}/newtask?limit=100`)
    },

    handleResponse () {
      // TODO: refresh the page to fetch the next 100 tasks
      // TODO: handle response
    }
  },

  created () {
    this.fetchProject().then(r => {
      this.project = r.data[0]
      return this.fetchNewTasks()
    }).then(r => {
      this.tasks = r.data
    }).catch(error => {
      console.log(error)
    })
  }
}
</script>