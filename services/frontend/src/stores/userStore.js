import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.user,
    stateUser: (state) => state.user,
  },

  actions: {
    async register(form) {
      try {
        await axios.post('register', form)

        const userForm = new FormData()
        userForm.append('username', form.username)
        userForm.append('password', form.password)

        await this.logIn(userForm)
      } catch (error) {
        console.error('Registration failed:', error)
      }
    },

    async logIn(user) {
      try {
        const response = await axios.post('login', user)
        if (response.status === 200) {
          await this.viewMe()
          return true
        } else {
          console.error('Login failed:', response.data)
          return false
        }
      } catch (error) {
        console.error('Login error:', error)
        return false
      }
    },

    async viewMe() {
      try {
        const { data } = await axios.get('users/whoami', { withCredentials: true })
        this.user = data
      } catch (error) {
        console.error('Error fetching user info:', error)
      }
    },

    async deleteUser(id) {
      try {
        await axios.delete(`user/${id}`)
      } catch (error) {
        console.error('Failed to delete user:', error)
      }
    },

    async logOut() {
      try {
        await axios.post('/logout') // deletes the auth cookie
      } catch (err) {
        console.error('Logout request failed:', err)
      }
      this.$reset()           // reset store state to default (Pinia method)
      localStorage.removeItem('user')  // clear persisted user data
      delete axios.defaults.headers.common['Authorization']
    },
    
    async fetchCurrentUser() {
      try {
        const baseUrl = process.env.VUE_APP_API_BASE_URL;
        const response = await axios.get(`${baseUrl}/users/whoami`, { withCredentials: true })
        this.user = response.data
        return true
      } catch (error) {
        this.user = null
        return false
      }
    }
    
  },

  persist: {
    key: 'user',
    storage: localStorage, // or sessionStorage
  },
})
