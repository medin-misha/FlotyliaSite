import { defineStore } from 'pinia'
import Cookies from 'js-cookie'

const isHttpsOnly =
  import.meta.env.VITE_HTTPS_ONLY === 'true' ||
  (typeof window !== 'undefined' && window.location.protocol === 'https:')

const cookieOptions = {
  secure: isHttpsOnly,
  sameSite: 'strict',
  expires: 7,
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: Cookies.get('user'),
    token: Cookies.get('token'),
  }),
  actions: {
    logout() {
      this.user = Cookies.remove('user')
      this.token = Cookies.remove('token')
      window.location.reload()
    },
    login(username, token) {
      this.token = token
      this.user = username
      Cookies.set('user', username, cookieOptions)
      Cookies.set('token', token, cookieOptions)
      window.location.reload()
    },
    isLogin() {
      return this.user && this.token
    },
  },
  getters: {
    getToken() {
      return this.token
    },
    getUser() {
      return this.user
    },
  },
})
