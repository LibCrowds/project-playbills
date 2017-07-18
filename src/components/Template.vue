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
      const generator = this.getGenerator(project)
      const opts = this.tasks.map(function (task) {
        let opts = task.info
        opts.generator = generator
      })
      console.log(opts)
      return opts
    }
  },

  methods: {
    getGenerator (project) {
      return {
        id: `${api.baseUrl}/project/${project.id}`,
        type: "Software",
        name: project.name,
        homepage: `${api.baseUrl}/project/${project.short_name}`
      }
    },

      https://playbills-backend.libcrowds.com/api/project/1
    },

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