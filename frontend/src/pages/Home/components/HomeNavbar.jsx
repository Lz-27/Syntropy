import { Link } from 'react-router-dom'
import { LogIn, UserCheck, LogOut, ArrowRight } from 'lucide-react'
import { useAuthStore } from '../../../store/authStore'
import ThemeSwitcher from '../../../components/layout/ThemeSwitcher'
import styles from '../Home.module.css'

export function HomeNavbar() {
  const { user, isAuthenticated, logout } = useAuthStore()

  return (
    <nav className={styles.navbar} role="navigation" aria-label="Navegación principal">
      <Link to="/" className={styles.navBrand}>
        <div className={styles.brandLogo}>∑</div>
        <span className={styles.brandText}>TGS-Hub</span>
        <span className={styles.brandTag}>v1.0</span>
      </Link>

      <div className={styles.navRight}>
        <ThemeSwitcher />

        {isAuthenticated && user ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <div className={styles.userBadgeStatus}>
              <span className={styles.userActiveDot} />
              <span>{user.nombre_completo?.split(' ')[0]} ({user.rol})</span>
            </div>
            <Link to="/dashboard" className={styles.btnPrimary}>
              <span>Ir al Dashboard</span>
              <ArrowRight size={15} />
            </Link>
            <button
              onClick={logout}
              className={styles.btnSecondary}
              style={{ padding: '8px 12px' }}
              title="Cerrar sesión para cambiar de usuario"
            >
              <LogOut size={15} />
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <Link to="/login" className={styles.btnPrimary}>
              <LogIn size={15} />
              <span>Iniciar Sesión</span>
            </Link>
            <Link to="/register" className={styles.btnSecondary}>
              <UserCheck size={15} />
              <span>Registrarse</span>
            </Link>
          </div>
        )}
      </div>
    </nav>
  )
}
