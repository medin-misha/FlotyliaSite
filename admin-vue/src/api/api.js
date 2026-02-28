import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

api.interceptors.request.use(
  (config) => {
    const token = useAuthStore().getToken
    config.headers.Authorization = `Bearer ${token}`
    return config
  },
  (error) => {
    console.log(error)
    return Promise.reject(error)
  },
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.log(error.response)
    if (error.response.status === 401) {
      const store = useAuthStore()
      store.logout()
    } else if (error.response.status === 400) {
      console.log(error.response)
    } else {
      alert('Ошибка, скорее всего вы чёто не правильно заполнили')
      console.log(error.response)
    }
    return Promise.reject(error)
  },
)

export default api
