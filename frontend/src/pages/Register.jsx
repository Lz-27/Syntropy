import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../services/api'
import styles from './Login.module.css'

export default function Register() {
  const [form, setForm] = useState({
    nombre_completo: '', codigo_estudiante: '', email: '', password: '', confirm: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.password !== form.confirm) {
      setError('Las contraseñas no coinciden')
      return
    }
    setError(''); setLoading(true)
    try {
      await api.post('/auth/register', {
        nombre_completo: form.nombre_completo,
        codigo_estudiante: form.codigo_estudiante,
        email: form.email,
        password: form.password,
      })
      navigate('/login')
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al registrar')
    } finally {
      setLoading(false)
    }
  }

  const f = (key) => (e) => setForm((p) => ({ ...p, [key]: e.target.value }))

  return (
    <div className={styles.page}>
      <div className={styles.panel} aria-hidden="true">
        <div className={styles.panelContent}>
          <h1 className={styles.panelTitle}>TGS-Hub</h1>
          <p className={styles.panelSub}>Únete a la comunidad académica de Teoría General de Sistemas</p>
        </div>
      </div>
      <div className={styles.formSide}>
        <div className={styles.formCard}>
          <h2 className={styles.formTitle}>Crear cuenta</h2>
          <p className={styles.formSubtitle}>Ingresa tus datos institucionales</p>
          <form id="register-form" onSubmit={handleSubmit} className={styles.form} noValidate>
            {[
              { id: 'reg-name', label: 'Nombre completo', key: 'nombre_completo', type: 'text', placeholder: 'María García López' },
              { id: 'reg-code', label: 'Código de estudiante', key: 'codigo_estudiante', type: 'text', placeholder: '61035728' },
              { id: 'reg-email', label: 'Correo institucional', key: 'email', type: 'email', placeholder: 'usuario@uni.edu' },
              { id: 'reg-pass', label: 'Contraseña', key: 'password', type: 'password', placeholder: '••••••••' },
              { id: 'reg-confirm', label: 'Confirmar contraseña', key: 'confirm', type: 'password', placeholder: '••••••••' },
            ].map(({ id, label, key, type, placeholder }) => (
              <div key={id} className={styles.field}>
                <label htmlFor={id} className={styles.label}>{label}</label>
                <input id={id} type={type} className={styles.input} placeholder={placeholder}
                  value={form[key]} onChange={f(key)} required />
              </div>
            ))}
            {error && (
              <p className={styles.error} role="alert">
                <span className={styles.errorCode}>ERR</span>{error}
              </p>
            )}
            <button id="register-submit" type="submit" className={styles.submitBtn} disabled={loading}>
              {loading ? 'Registrando...' : 'Crear cuenta'}
            </button>
          </form>
          <p className={styles.registerLink}>
            ¿Ya tienes cuenta? <Link to="/login" className={styles.link}>Inicia sesión</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
