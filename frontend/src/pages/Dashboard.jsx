/**
 * Dashboard — Vista central de TGS-Hub
 * P7: KPIs del ecosistema + Feed de publicaciones con filtros
 */
import { useEffect, useState, useCallback } from 'react'
import { Link } from 'react-router-dom'
import {
  FileText, Paperclip, MessageSquare, Users,
  LayoutGrid, List, AlertTriangle, FilePlus, RefreshCw,
} from 'lucide-react'
import api from '../services/api'
import { usePosts } from '../hooks/usePosts'
import { PostCard, PostCardSkeleton } from '../components/posts/PostCard'
import styles from './Dashboard.module.css'

// ── KPI config ─────────────────────────────────────────────────
const KPI_CONFIG = [
  { key: 'total_posts',      label: 'Publicaciones', Icon: FileText,       color: 'var(--signal)' },
  { key: 'total_archivos',   label: 'Archivos',      Icon: Paperclip,      color: 'var(--pulse)' },
  { key: 'total_comentarios',label: 'Feedback',      Icon: MessageSquare,  color: 'var(--amber)' },
  { key: 'usuarios_activos', label: 'Sinergia',      Icon: Users,          color: 'var(--text-muted)' },
]

function formatKPI(n) {
  if (n === undefined || n === null) return '—'
  if (n >= 1000) return `${(n / 1000).toFixed(1)}k`
  return String(n)
}

// ── Componente KPI Card ─────────────────────────────────────────
function KPICard({ Icon, label, value, color, loading }) {
  return (
    <div className={styles.kpiCard} style={{ '--kpi-color': color }}>
      <Icon size={22} className={styles.kpiIcon} aria-hidden="true" />
      <div className={styles.kpiBody}>
        {loading ? (
          <div style={{
            width: 60, height: 28, borderRadius: 4,
            background: 'var(--surface-2)',
            animation: 'pulse 1.4s infinite',
          }} />
        ) : (
          <div className={styles.kpiValue}>{formatKPI(value)}</div>
        )}
        <div className={styles.kpiLabel}>{label}</div>
      </div>
    </div>
  )
}

// ── Filtros de orden ────────────────────────────────────────────
const ORDER_OPTIONS = [
  { value: 'recent',  label: 'Más reciente' },
  { value: 'views',   label: 'Más vistas' },
  { value: 'oldest',  label: 'Más antiguo' },
]

// ── Dashboard ───────────────────────────────────────────────────
export default function Dashboard() {
  const [stats, setStats]       = useState(null)
  const [statsLoading, setStatsLoading] = useState(true)
  const [categories, setCategories]     = useState([])
  const [viewMode, setViewMode] = useState('grid') // 'grid' | 'list'
  const [firstBatch, setFirstBatch]     = useState(false)

  const {
    posts, total, isLoading, hasMore, filters, error,
    setFilter, fetchPosts, fetchNextPage,
  } = usePosts()

  // ── Carga inicial ─────────────────────────────────────────────
  useEffect(() => {
    // Stats del ecosistema — endpoint global
    api.get('/stats')
      .then((res) => {
        setStats(res.data)
        setStatsLoading(false)
      })
      .catch(() => {
        // Fallback: extraer total de posts del endpoint de listado
        api.get('/posts')
          .then((r) => setStats({ total_posts: r.data.total }))
          .catch(() => {})
          .finally(() => setStatsLoading(false))
      })

    // Categorías para el filtro
    api.get('/posts/categories').then((res) => {
      setCategories(res.data || [])
    }).catch(() => {})

    // Primer fetch del feed
    setFirstBatch(true)
    fetchPosts(1).finally(() => setFirstBatch(false))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])



  // Refresh manual
  const handleRefresh = useCallback(() => {
    setFirstBatch(true)
    fetchPosts(1).finally(() => setFirstBatch(false))
  }, [fetchPosts])

  const skeletonCount = 6

  return (
    <div className={styles.page}>
      {/* ── KPIs ──────────────────────────────────────────────── */}
      <div className={styles.kpiGrid}>
        {KPI_CONFIG.map(({ key, label, Icon, color }) => (
          <KPICard
            key={key}
            Icon={Icon}
            label={label}
            value={stats?.[key]}
            color={color}
            loading={statsLoading}
          />
        ))}
      </div>

      {/* ── Filtros ────────────────────────────────────────────── */}
      <div className={styles.filterBar} role="toolbar" aria-label="Filtros del feed">
        <span className={styles.filterLabel}>Filtrar:</span>

        {/* Categoría */}
        <div className={styles.filterGroup}>
          <select
            id="filter-categoria"
            className={styles.filterSelect}
            value={filters.categoria_id ?? ''}
            onChange={(e) => setFilter('categoria_id', e.target.value ? Number(e.target.value) : null)}
            aria-label="Filtrar por categoría"
          >
            <option value="">Todas las semanas</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>{cat.nombre}</option>
            ))}
          </select>
        </div>

        <div className={styles.filterDivider} />

        {/* Ordenamiento */}
        <div className={styles.filterGroup}>
          {ORDER_OPTIONS.map(({ value, label }) => (
            <button
              key={value}
              id={`filter-order-${value}`}
              className={`${styles.filterPill} ${filters.order_by === value ? styles.active : ''}`}
              onClick={() => setFilter('order_by', value)}
              aria-pressed={filters.order_by === value}
            >
              {label}
            </button>
          ))}
        </div>

        <div className={styles.filterSpacer} />

        {/* Toggle de vista */}
        <div className={styles.viewToggle} role="group" aria-label="Modo de vista">
          <button
            id="view-grid"
            className={`${styles.viewBtn} ${viewMode === 'grid' ? styles.active : ''}`}
            onClick={() => setViewMode('grid')}
            aria-label="Vista en grilla"
            aria-pressed={viewMode === 'grid'}
          >
            <LayoutGrid size={15} />
          </button>
          <button
            id="view-list"
            className={`${styles.viewBtn} ${viewMode === 'list' ? styles.active : ''}`}
            onClick={() => setViewMode('list')}
            aria-label="Vista en lista"
            aria-pressed={viewMode === 'list'}
          >
            <List size={15} />
          </button>
        </div>
      </div>

      {/* ── Feed ──────────────────────────────────────────────── */}
      <div>
        {/* Header del feed */}
        <div className={styles.feedHeader}>
          <h2 className={styles.feedTitle}>
            Publicaciones
            {total > 0 && (
              <span className={styles.feedCount}> · {total} en total</span>
            )}
          </h2>
          <div style={{ display: 'flex', gap: 8 }}>
            <Link
              id="new-post-btn"
              to="/posts/new"
              style={{
                display: 'inline-flex', alignItems: 'center', gap: 6,
                padding: '6px 14px',
                background: 'var(--signal)',
                color: '#000',
                border: 'none',
                borderRadius: 'var(--radius-sm)',
                fontSize: 'var(--text-sm)',
                fontWeight: 'var(--weight-medium)',
                cursor: 'pointer',
                textDecoration: 'none',
              }}
            >
              <FilePlus size={15} aria-hidden="true" />
              Nueva publicación
            </Link>
            <button
              id="refresh-feed"
              onClick={handleRefresh}
              aria-label="Actualizar feed"
              style={{
                display: 'flex', alignItems: 'center',
                padding: '6px 10px',
                background: 'transparent',
                color: 'var(--text-muted)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-sm)',
                cursor: 'pointer',
                transition: 'var(--t-fast)',
              }}
            >
              <RefreshCw size={15} style={isLoading ? { animation: 'spin 1s linear infinite' } : {}} />
            </button>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className={styles.errorBanner} role="alert">
            <AlertTriangle size={16} aria-hidden="true" />
            {error}
          </div>
        )}

        {/* Grid/Lista */}
        <div
          className={viewMode === 'grid' ? styles.feedGrid : styles.feedList}
          style={{ marginTop: 16 }}
        >
          {/* Skeletons mientras carga */}
          {isLoading && posts.length === 0 &&
            Array.from({ length: skeletonCount }).map((_, i) => (
              <PostCardSkeleton key={`sk-${i}`} />
            ))
          }

          {/* Posts */}
          {posts.map((post, idx) => (
            <PostCard
              key={post.id}
              post={post}
              isFirstBatch={firstBatch && idx < 6}
            />
          ))}

          {/* Estado vacío */}
          {!isLoading && posts.length === 0 && !error && (
            <div className={styles.empty}>
              <FileText size={40} className={styles.emptyIcon} aria-hidden="true" />
              <p className={styles.emptyTitle}>Sin publicaciones aún</p>
              <p className={styles.emptyText}>
                Sé el primero en compartir un análisis sistémico con la comunidad.
              </p>
              <Link
                to="/posts/new"
                style={{
                  marginTop: 8,
                  padding: '8px 20px',
                  background: 'var(--signal-10)',
                  border: '1px solid var(--signal)',
                  borderRadius: 'var(--radius-sm)',
                  color: 'var(--signal)',
                  textDecoration: 'none',
                  fontSize: 'var(--text-sm)',
                  fontWeight: 'var(--weight-medium)',
                }}
              >
                Crear primera publicación
              </Link>
            </div>
          )}
        </div>

        {/* Load more */}
        {hasMore && (
          <div className={styles.loadMore}>
            <button
              id="load-more-btn"
              className={styles.loadMoreBtn}
              onClick={fetchNextPage}
              disabled={isLoading}
            >
              {isLoading ? 'Cargando...' : 'Cargar más publicaciones'}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
