import { useState, useRef, useEffect } from 'react'
import { Sun, Moon, Globe, ChevronDown } from 'lucide-react'
import { useThemeStore } from '../../store/themeStore'
import styles from './ThemeSwitcher.module.css'

const THEMES = [
  {
    key: 'dark',
    label: 'Dark Matte',
    icon: Moon,
    swatch: '#161B22',
    accent: '#58A6FF',
  },
  {
    key: 'light',
    label: 'Academic Paper',
    icon: Sun,
    swatch: '#FFFFFF',
    accent: '#0969DA',
  },
  {
    key: 'navy',
    label: 'Cyber Navy',
    icon: Globe,
    swatch: '#0B1629',
    accent: '#38BDF8',
  },
]

export default function ThemeSwitcher() {
  const { theme, setTheme } = useThemeStore()
  const [open, setOpen] = useState(false)
  const ref = useRef(null)

  const current = THEMES.find((t) => t.key === theme) || THEMES[0]
  const Icon = current.icon

  // Cerrar al hacer click fuera
  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false)
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  return (
    <div className={styles.wrapper} ref={ref}>
      <button
        id="theme-switcher-btn"
        className={styles.trigger}
        onClick={() => setOpen((o) => !o)}
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-label={`Tema actual: ${current.label}. Cambiar tema`}
        title="Cambiar tema"
      >
        <Icon size={16} aria-hidden="true" />
        <ChevronDown size={12} className={open ? styles.chevronOpen : styles.chevron} aria-hidden="true" />
      </button>

      {open && (
        <ul
          className={styles.dropdown}
          role="listbox"
          aria-label="Seleccionar tema"
        >
          {THEMES.map(({ key, label, icon: TIcon, swatch, accent }) => (
            <li
              key={key}
              role="option"
              aria-selected={theme === key}
              className={[styles.option, theme === key ? styles.selected : ''].join(' ')}
              onClick={() => { setTheme(key); setOpen(false) }}
              onKeyDown={(e) => { if (e.key === 'Enter') { setTheme(key); setOpen(false) } }}
              tabIndex={0}
            >
              {/* Color swatch */}
              <span
                className={styles.swatch}
                style={{ background: swatch, boxShadow: `0 0 0 2px ${accent}` }}
                aria-hidden="true"
              />
              <TIcon size={14} aria-hidden="true" />
              <span className={styles.label}>{label}</span>
              {theme === key && <span className={styles.check}>✓</span>}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
