import api from './api'

const APIGetters = {
  getMeInfo: async () => api.get(`/admin/me`),
  getUniversal: async (url, page, limit, search, field) => {
    const params = {
      page,
      limit,
      ...(search != null && { search }),
      // ...(field != null && { field }),
    }
    // try {
    return api.get(`${url}`, { params }).then((response) => response)
    // } catch(error) {return error}
  },
  getDetail: async (url, id) => api.get(`${url}/${id}`),
  getExport: async () => api.get(`users/export`, { responseType: 'blob' }),
}

export default APIGetters
