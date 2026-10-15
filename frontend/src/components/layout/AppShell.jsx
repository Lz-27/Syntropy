import { useState, useEffect } from 'react'
import { Outlet } from 'react-router-dom'
import Header from './Header'
import Sidebar from './Sidebar'
import styles from './AppShell.module.css'

const SIDEBAR_KEY = 'tgs-hub-sidebar'

export default function AppShell() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(() => {
    return localStorage.getItem(SIDEBAR_KEY) === 'collapsed'
  })

  const toggleSidebar = () => {
    setSidebarCollapsed((prev) => {
      const next = !prev
      localStorage.setItem(SIDEBAR_KEY, next ? 'collapsed' : 'expanded')
      return next
    })
  }

  return (
    <div
      className={styles.shell}
      style={{
        '--current-sidebar': sidebarCollapsed
          ? 'var(--sidebar-collapsed)'
          : 'var(--sidebar-width)',
      }}
    >
      <Sidebar collapsed={sidebarCollapsed} onToggle={toggleSidebar} />
      <div className={styles.main}>
        <Header onToggleSidebar={toggleSidebar} />
        <main className={styles.content}>
          <Outlet />
        </main>
      </div>
    </div>
  )
}
