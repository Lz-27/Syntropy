import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import api from '../services/api'

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (credentials) => {
        const res = await api.post('/auth/login', credentials)
        const { access_token, user } = res.data
        api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        set({ user, token: access_token, isAuthenticated: true })
        return user
      },

      logout: () => {
        delete api.defaults.headers.common['Authorization']
        set({ user: null, token: null, isAuthenticated: false })
      },

      refreshUser: async () => {
        try {
          const res = await api.get('/auth/me')
          set({ user: res.data })
        } catch {
          get().logout()
        }
      },

      setToken: (token) => {
        if (token) {
          api.defaults.headers.common['Authorization'] = `Bearer ${token}`
        }
        set({ token })
      },
    }),
    {
      name: 'tgs-hub-auth',
      onRehydrateStorage: () => (state) => {
        if (state?.token) {
          api.defaults.headers.common['Authorization'] = `Bearer ${state.token}`
        }
      },
    }
  )
)
