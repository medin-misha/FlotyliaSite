import { defineStore } from 'pinia'

export const useStatesStore = defineStore('states', {
  state: () => ({
    state: 'table',
    states: {
      create: 'create',
      table: 'table',
      detail: 'detail',
    },
    instance_id: null,
  }),
  actions: {
    setCreateState() {
      this.state = this.states.create
    },
    setTableState() {
      this.state = this.states.table
    },
    setDetailState(id) {
      this.state = this.states.detail
      this.setInstanceId(id)
    },
    setInstanceId(id) {
      this.instance_id = id
    },
  },
})
