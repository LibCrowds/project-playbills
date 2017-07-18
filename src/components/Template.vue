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
      tasks: [],
      user: null
    }
  },

  computed: {
    taskOpts: function () {
      const generator = this.getGenerator(this.project)
      const creator = this.user ? this.getCreator(this.user) : null
      const opts = this.tasks.map(function (task) {
        let opts = task.info
        opts.generator = generator
        if (creator) {
          opts.creator = creator
        }
        return opts
      })
      console.log(opts)
      return opts
    }
  },

  methods: {
    getGenerator (project) {
      return {
        id: `${process.env.PYBOSSA_URL}/api/project/${project.id}`,
        type: 'Software',
        name: project.name,
        homepage: `${process.env.PYBOSSA_URL}/project/${project.short_name}`
      }
    },

    getCreator (user) {
      return {
        id: `${process.env.PYBOSSA_URL}/api/user/${user.id}`,
        type: 'Person',
        name: user.fullname,
        nickname: user.name
      }
    },

    fetchCurrentUser () {
      return api.get(`/account/profile`)
    },

    fetchProject () {
      return api.get(`/api/project?short_name=${process.env.SHORT_NAME}`)
    },

    fetchNewTasks () {
      return api.get(`/api/project/${this.project.id}/newtask?limit=100`)
    },

    handleResponse () {
      // TODO: refresh the page to fetch the next 100 tasks
      // TODO: handle response
    }
  },

  created () {
    this.fetchCurrentUser().then(r => {
      this.user = 'user' in r.data ? r.data.user : null
      return this.fetchProject()
    }).then(r => {
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