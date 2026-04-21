import api from './api'

function withTrailingSlash(url) {
  return url.endsWith('/') ? url : `${url}/`
}

const APIGetters = {
  getMeInfo: async () => api.get(`/admin/me`),
  getUniversal: async (url, page, limit, search, field) => {
    const params = {
      page,
      limit,
      ...(search != null && { search }),
      // ...(field != null && { field }),
    }
    return api.get(withTrailingSlash(url), { params }).then((response) => response)
  },
  getDetail: async (url, id) => api.get(`${url}/${id}`),
  getExport: async () => api.get(`/users/export`, { responseType: 'blob' }),
}

export default APIGetters
