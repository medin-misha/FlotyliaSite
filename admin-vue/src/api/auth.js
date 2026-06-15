import api from './api.js'
import { useAuthStore } from '../stores/auth.js'

function withTrailingSlash(url) {
  return url.endsWith('/') ? url : `${url}/`
}

// Универсальная функция для запроса
const request = async (method, url, data = null, params = null) => {
  try {
    const response = await api.request({
      method: method,
      url: url,
      data: data,
      params: params,
    })
    return response.data
  } catch (error) {
    return { error: error }
  }
}

const getJWT = async (name, password) => {
  return await request('post', '/admin/login', { username: name, password: password })
}
const login = async (name, password) => {
  const jwtResponse = await getJWT(name, password)
  if (jwtResponse) {
    const store = useAuthStore()
    store.login(name, jwtResponse.access_token)
  }
}

const APIAuth = {
  createAdmin: async (name, password) =>
    request('post', withTrailingSlash('/admin'), { username: name, password: password }),
  login,
  getAdmins: async (page, limit) =>
    request('get', withTrailingSlash('/admin'), null, { page: page, limit: limit }),
  getMeInfo: async () => request('get', '/admin/me'),
  deleteAdmin: async (id) => request('delete', `/admin/${id}`),
  getAdminById: async (id) => request('get', `/admin/${id}`),
}

export default APIAuth
