import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'
import { useThemeStore } from './store/themeStore'

// Páginas (lazy en P12, por ahora directas para P1-P2)
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import PostDetail from './pages/PostDetail'
import NewPost from './pages/NewPost'
import FileExplorer from './pages/FileExplorer'
import Analytics from './pages/Analytics'
import Profile from './pages/Profile'

// Layout shell
import AppShell from './components/layout/AppShell'
import ProtectedRoute from './components/layout/ProtectedRoute'

function App() {
  const theme = useThemeStore((s) => s.theme)

  // Aplicar data-theme al montar
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  return (
    <BrowserRouter>
      <Routes>
        {/* Rutas públicas (sin shell) */}
        <Route path="/login"    element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Rutas protegidas (con AppShell) */}
        <Route element={<ProtectedRoute />}>
          <Route element={<AppShell />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard"    element={<Dashboard />} />
            <Route path="/posts/new"    element={<NewPost />} />
            <Route path="/posts/:id"    element={<PostDetail />} />
            <Route path="/files"        element={<FileExplorer />} />
            <Route path="/analytics"    element={<Analytics />} />
            <Route path="/profile"      element={<Profile />} />
            <Route path="/profile/:id"  element={<Profile />} />
          </Route>
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
