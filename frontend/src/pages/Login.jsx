import { useState, useEffect } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import styles from './Login.module.css'

export default function Login() {
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login, isAuthenticated } = useAuthStore()
  const navigate = useNavigate()
  const location = useLocation()

  // Evitar bucle si from apunta a /login o no está definido
  const rawFrom = location.state?.from?.pathname
  const from = rawFrom && rawFrom !== '/login' ? rawFrom : '/dashboard'

  // Si ya está autenticado, redirigir automáticamente
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard', { replace: true })
    }
  }, [isAuthenticated, navigate])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login({ username: form.email.trim(), password: form.password })
      navigate(from, { replace: true })
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        (err.code === 'ERR_NETWORK' || !err.response
          ? 'No se pudo conectar con el servidor backend (puerto 8000).'
          : 'Credenciales inválidas')
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.page}>
      {/* Panel izquierdo — diagrama TGS */}
      <div className={styles.panel} aria-hidden="true">
        <div className={styles.panelContent}>
          <div className={styles.diagram}>
            <div className={styles.node} data-type="input">
              <span className={styles.nodeLabel}>Inputs</span>
              <span className={styles.nodeDesc}>Conocimiento que entra</span>
            </div>
            <div className={styles.arrow} aria-hidden="true" />
            <div className={styles.node} data-type="process">
              <span className={styles.nodeLabel}>Procesos</span>
              <span className={styles.nodeDesc}>Análisis sistémico</span>
            </div>
            <div className={styles.arrow} aria-hidden="true" />
            <div className={styles.node} data-type="output">
              <span className={styles.nodeLabel}>Outputs</span>
              <span className={styles.nodeDesc}>Publicaciones y archivos</span>
            </div>
            <div className={styles.feedbackLine} aria-hidden="true">
              <span className={styles.feedbackLabel}>Feedback</span>
            </div>
          </div>
          <h1 className={styles.panelTitle}>TGS-Hub</h1>
          <p className={styles.panelSub}>Plataforma académica para la Teoría General de Sistemas</p>
        </div>
      </div>

      {/* Panel derecho — formulario */}
      <div className={styles.formSide}>
        <div className={styles.formCard}>
          <h2 className={styles.formTitle}>Iniciar Sesión</h2>
          <p className={styles.formSubtitle}>Accede con tu código o correo institucional</p>

          <form id="login-form" onSubmit={handleSubmit} className={styles.form} noValidate>
            <div className={styles.field}>
              <label htmlFor="login-email" className={styles.label}>Correo o código de estudiante</label>
              <input
                id="login-email"
                type="text"
                className={styles.input}
                placeholder="usuario@uni.edu / 61035728"
                value={form.email}
                onChange={(e) => setForm((f) => ({ ...f, email: e.target.value }))}
                required
                autoComplete="username"
              />
            </div>

            <div className={styles.field}>
              <label htmlFor="login-password" className={styles.label}>Contraseña</label>
              <input
                id="login-password"
                type="password"
                className={styles.input}
                placeholder="••••••••"
                value={form.password}
                onChange={(e) => setForm((f) => ({ ...f, password: e.target.value }))}
                required
                autoComplete="current-password"
              />
            </div>

            {error && (
              <p className={styles.error} role="alert">
                <span className={styles.errorCode}>ERR</span>
                {error}
              </p>
            )}

            <button
              id="login-submit"
              type="submit"
              className={styles.submitBtn}
              disabled={loading}
            >
              {loading ? 'Verificando...' : 'Iniciar Sesión'}
            </button>
          </form>

          <p className={styles.registerLink}>
            ¿No tienes cuenta?{' '}
            <Link to="/register" className={styles.link}>Regístrate</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
