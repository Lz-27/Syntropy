import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const THEME_KEY = 'tgs-hub-theme'

const getInitialTheme = () => {
  return 'dark'
}

export const useThemeStore = create(
  persist(
    (set) => ({
      theme: getInitialTheme(),
      setTheme: (theme) => {
        document.documentElement.setAttribute('data-theme', theme)
        set({ theme })
      },
    }),
    {
      name: THEME_KEY,
      onRehydrateStorage: () => (state) => {
        if (state?.theme) {
          document.documentElement.setAttribute('data-theme', state.theme)
        }
      },
    }
  )
)
