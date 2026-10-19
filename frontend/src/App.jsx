import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect, lazy, Suspense } from 'react'
import { Loader2 } from 'lucide-react'
import { useThemeStore } from './store/themeStore'

// Layout shell
import AppShell from './components/layout/AppShell'
import ProtectedRoute from './components/layout/ProtectedRoute'

// Páginas con Code Splitting / Lazy Loading (P12)
const Login = lazy(() => import('./pages/Login'))
const Register = lazy(() => import('./pages/Register'))
const Dashboard = lazy(() => import('./pages/Dashboard'))
const PostDetail = lazy(() => import('./pages/PostDetail'))
const NewPost = lazy(() => import('./pages/NewPost'))
const FileExplorer = lazy(() => import('./pages/FileExplorer'))
const Analytics = lazy(() => import('./pages/Analytics'))
const Profile = lazy(() => import('./pages/Profile'))

function PageFallback() {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '60vh',
        gap: '12px',
        color: 'var(--muted)',
        fontFamily: 'var(--font-mono)',
        fontSize: 'var(--text-xs)',
      }}
    >
      <Loader2 size={24} className="animate-spin" style={{ color: 'var(--signal)' }} />
      <span>// Sincronizando subsistema...</span>
    </div>
  )
}

function App() {
  const theme = useThemeStore((s) => s.theme)

  // Aplicar data-theme al montar
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  return (
    <BrowserRouter>
      <Suspense fallback={<PageFallback />}>
        <Routes>
          {/* Rutas públicas (sin shell) */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Rutas protegidas (con AppShell) */}
          <Route element={<ProtectedRoute />}>
            <Route element={<AppShell />}>
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/posts/new" element={<NewPost />} />
              <Route path="/posts/:id" element={<PostDetail />} />
              <Route path="/posts/:id/edit" element={<NewPost />} />
              <Route path="/files" element={<FileExplorer />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/profile/:id" element={<Profile />} />
            </Route>
          </Route>

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}

export default App
