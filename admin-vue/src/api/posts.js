import api from './api'

function withTrailingSlash(url) {
  return url.endsWith('/') ? url : `${url}/`
}

const APIPosts = {
  createFile: async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return await api.post(withTrailingSlash('/files'), formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
  createPost: async (URL, body) => {
    return await api.post(withTrailingSlash(URL), body)
  },
  updatePost: async (URL, id, body) => {
    return await api.patch(`${URL}/${id}`, body)
  },
  deletePost: async (URL, id) => {
    return await api.delete(`${URL}/${id}`)
  },
  bulkUpdateStatus: async (url, ids, newStatus) => {
    return await api.patch(`${url}/bulk-status`, { ids, status: newStatus })
  },
  bulkDelete: async (url, ids) => {
    return await api.delete(`${url}/bulk`, { data: { ids } })
  },
}

export default APIPosts
