import { defineStore } from 'pinia'
import { userSchema, userCreateSchema } from '../forms/userFrom.js'

export const usePageStore = defineStore('page', {
  state: () => ({
    pageData: {
      adres: '/users',
      name: 'Users',
      createSchema: userCreateSchema,
      schema: userSchema,
      view: 'crud',
    },
    paginationData: {
      page: 1,
      limit: 50,
      search: '',
      filter: '',
    },
  }),
  actions: {
    // pageStore.setPage(menu[index].url, menu[index].name, menu[index].createSchema, menu[index].schema)
    setPage(adres, name, createSchema, schema, view = 'crud') {
      this.pageData.adres = adres
      this.pageData.name = name
      this.pageData.schema = schema
      this.pageData.createSchema = createSchema
      this.pageData.view = view
      console.log(this.pageData)
    },
    setSearchParams(search) {
      this.paginationData.search = search
    },
    setPaginationParams(page, limit) {
      this.paginationData.page = page
      this.paginationData.limit = limit
    },
    nextPage() {
      this.paginationData.page += 1
    },
    prevPage() {
      this.paginationData.page -= 1
    },
    resetSearchParams() {
      this.paginationData.search = ''
      this.paginationData.filter = ''
    },
  },
})
