import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Bell, LogOut, Menu } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import ThemeSwitcher from './ThemeSwitcher'
import styles from './Header.module.css'

export default function Header({ onToggleSidebar }) {
  const [search, setSearch] = useState('')
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className={styles.header} role="banner">
      {/* Left: Menu toggle + Brand */}
      <div className={styles.left}>
        <button
          className={styles.menuBtn}
          onClick={onToggleSidebar}
          aria-label="Toggle sidebar"
        >
          <Menu size={18} />
        </button>
        <span className={styles.brand}>TGS-Hub</span>
      </div>

      {/* Center: Search */}
      <div className={styles.center}>
        <div className={styles.searchWrapper} role="search">
          <Search size={14} className={styles.searchIcon} aria-hidden="true" />
          <input
            id="global-search"
            type="search"
            placeholder="Buscar publicaciones, archivos, autores..."
            className={styles.searchInput}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            aria-label="Búsqueda global"
          />
        </div>
      </div>

      {/* Right: Actions */}
      <div className={styles.right}>
        <ThemeSwitcher />

        <button
          className={styles.iconBtn}
          aria-label="Notificaciones"
          title="Notificaciones"
        >
          <Bell size={18} />
        </button>

        {user && (
          <div className={styles.userMenu}>
            <div className={styles.avatarSmall} aria-hidden="true">
              {user.avatar_url
                ? <img src={user.avatar_url} alt={user.nombre_completo} />
                : <span>{user.nombre_completo?.charAt(0).toUpperCase()}</span>
              }
            </div>
            <button
              className={styles.iconBtn}
              onClick={handleLogout}
              aria-label="Cerrar sesión"
              title="Cerrar sesión"
            >
              <LogOut size={16} />
            </button>
          </div>
        )}
      </div>
    </header>
  )
}
