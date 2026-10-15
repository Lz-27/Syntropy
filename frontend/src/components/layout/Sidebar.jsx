import { NavLink } from 'react-router-dom'
import {
  Inbox, Cpu, BarChart3, MessageSquare,
  FolderOpen, Tag, User, ChevronLeft, ChevronRight
} from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import styles from './Sidebar.module.css'

const NAV_SECTIONS = [
  {
    label: 'FLUJO DEL SISTEMA',
    items: [
      { icon: Inbox,          label: 'Entradas',  to: '/dashboard',   title: 'Feed de publicaciones' },
      { icon: Cpu,            label: 'Procesos',  to: '/posts/new',   title: 'Nueva publicación' },
      { icon: BarChart3,      label: 'Salidas',   to: '/analytics',   title: 'Analíticas' },
      { icon: MessageSquare,  label: 'Feedback',  to: '/files',       title: 'Archivos compartidos' },
    ],
  },
  {
    label: 'RECURSOS',
    items: [
      { icon: FolderOpen,  label: 'Archivos',    to: '/files',    title: 'Explorador de archivos' },
      { icon: Tag,         label: 'Categorías',  to: '/dashboard', title: 'Categorías TGS' },
      { icon: User,        label: 'Perfil',      to: '/profile',  title: 'Mi perfil' },
    ],
  },
]

const ROL_LABELS = {
  admin:      'Administrador',
  estudiante: 'Estudiante',
}

export default function Sidebar({ collapsed, onToggle }) {
  const user = useAuthStore((s) => s.user)

  return (
    <aside
      className={styles.sidebar}
      data-collapsed={collapsed}
      aria-label="Navegación principal"
    >
      {/* Toggle button */}
      <button
        className={styles.toggle}
        onClick={onToggle}
        aria-label={collapsed ? 'Expandir sidebar' : 'Colapsar sidebar'}
        title={collapsed ? 'Expandir sidebar' : 'Colapsar sidebar'}
      >
        {collapsed ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
      </button>

      {/* User info */}
      {user && (
        <div className={styles.userSection}>
          <div className={styles.avatar} aria-hidden="true">
            {user.avatar_url ? (
              <img src={user.avatar_url} alt={user.nombre_completo} />
            ) : (
              <span>{user.nombre_completo?.charAt(0).toUpperCase()}</span>
            )}
          </div>
          {!collapsed && (
            <div className={styles.userInfo}>
              <p className={styles.userName}>{user.nombre_completo}</p>
              <span className={styles.userBadge}>{ROL_LABELS[user.rol] || user.rol}</span>
            </div>
          )}
        </div>
      )}

      {/* Navigation */}
      <nav className={styles.nav}>
        {NAV_SECTIONS.map((section) => (
          <div key={section.label} className={styles.section}>
            {!collapsed && (
              <p className={styles.sectionLabel}>{section.label}</p>
            )}
            <ul className={styles.navList} role="list">
              {section.items.map(({ icon: Icon, label, to, title }) => (
                <li key={to + label}>
                  <NavLink
                    to={to}
                    className={({ isActive }) =>
                      [styles.navItem, isActive ? styles.active : ''].join(' ')
                    }
                    title={collapsed ? title : undefined}
                  >
                    <Icon size={18} strokeWidth={1.75} aria-hidden="true" />
                    {!collapsed && <span className={styles.navLabel}>{label}</span>}
                  </NavLink>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </nav>
    </aside>
  )
}
