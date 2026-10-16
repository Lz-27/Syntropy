import { useState, useEffect } from 'react'
import {
  BarChart3,
  Layers,
  PieChart as PieIcon,
  Trophy,
  ArrowRight,
  RefreshCw,
  Loader2,
  FileText,
  MessageSquare,
  Paperclip,
  Activity
} from 'lucide-react'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts'
import { Avatar } from '../components/ui/Avatar'
import { Badge } from '../components/ui/Badge'
import api from '../services/api'
import styles from './Analytics.module.css'

// Paleta de colores para extensiones en el gráfico circular
const FILE_COLORS = ['#58A6FF', '#3FB950', '#D29922', '#A371F7', '#38BDF8', '#F78166', '#8B949E']

// Custom tooltip para el AreaChart
function CustomActivityTooltip({ active, payload, label }) {
  if (active && payload && payload.length) {
    return (
      <div className={styles.customTooltip}>
        <div className={styles.tooltipTitle}>{label}</div>
        <div className={styles.tooltipRow} style={{ color: '#58A6FF' }}>
          <span>● Publicaciones:</span>
          <strong>{payload[0]?.value || 0}</strong>
        </div>
        <div className={styles.tooltipRow} style={{ color: '#3FB950' }}>
          <span>● Retroalimentación:</span>
          <strong>{payload[1]?.value || 0}</strong>
        </div>
      </div>
    )
  }
  return null
}

export default function Analytics() {
  const [data, setData] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  const fetchAnalytics = async () => {
    setIsLoading(true)
    try {
      const res = await api.get('/analytics')
      setData(res.data)
    } catch (err) {
      console.error('Error al cargar analíticas:', err)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchAnalytics()
  }, [])

  if (isLoading || !data) {
    return (
      <div className={styles.loadingState}>
        <Loader2 size={32} className="animate-spin" style={{ color: 'var(--signal)' }} />
        <span>Calculando métricas y sinergia del ecosistema TGS...</span>
      </div>
    )
  }

  const { activity_by_week = [], file_types = [], top_contributors = [], tgs_flow = {} } = data

  return (
    <div className={styles.container}>
      <header className={styles.pageHeader}>
        <div className={styles.sectionHeading}>
          <h1 className={styles.pageTitle}>
            <BarChart3 size={26} style={{ color: 'var(--signal)' }} />
            <span>Métricas Sistémicas y Analíticas</span>
          </h1>
          <button
            type="button"
            onClick={fetchAnalytics}
            className={styles.sectionTag}
            style={{ cursor: 'pointer', background: 'var(--surface-2)', border: '1px solid var(--boundary)', color: 'var(--muted)' }}
            title="Actualizar métricas"
          >
            <RefreshCw size={12} style={{ display: 'inline', marginRight: 4 }} />
            <span>Actualizar</span>
          </button>
        </div>
        <p className={styles.pageSubtitle}>
          // Monitoreo en tiempo real del flujo de entropía, sinergia académica y distribución de conocimiento
        </p>
      </header>

      {/* ── SECCIÓN 4: Diagrama de Flujo del Sistema TGS ───────────────── */}
      <section className={styles.flowSection} aria-label="Flujo del Sistema TGS">
        <div className={styles.sectionHeading}>
          <h2 className={styles.sectionTitle}>
            <Activity size={18} style={{ color: 'var(--signal)' }} />
            <span>Flujo Operacional del Sistema TGS</span>
          </h2>
          <span className={styles.sectionTag}>Modelo Sistémico Abierto</span>
        </div>

        <div className={styles.flowGrid}>
          {/* Nodo 1: Entradas */}
          <div className={`${styles.flowNode} ${styles.nodeAccentInput}`}>
            <div className={styles.nodeHeader}>
              <span className={styles.nodeLabel}>{tgs_flow.inputs?.label || 'Entradas (Inputs)'}</span>
              <Paperclip size={16} style={{ color: 'var(--signal)' }} />
            </div>
            <span className={styles.nodeSublabel}>{tgs_flow.inputs?.sublabel}</span>
            <div className={styles.nodeValue}>
              {tgs_flow.inputs?.value || 0}
              <span className={styles.nodeUnit}> {tgs_flow.inputs?.unit}</span>
            </div>
          </div>

          {/* Nodo 2: Procesamiento */}
          <div className={`${styles.flowNode} ${styles.nodeAccentProcess}`}>
            <div className={styles.nodeHeader}>
              <span className={styles.nodeLabel}>{tgs_flow.processes?.label || 'Procesamiento'}</span>
              <FileText size={16} style={{ color: '#a371f7' }} />
            </div>
            <span className={styles.nodeSublabel}>{tgs_flow.processes?.sublabel}</span>
            <div className={styles.nodeValue}>
              {tgs_flow.processes?.value || 0}
              <span className={styles.nodeUnit}> {tgs_flow.processes?.unit}</span>
            </div>
          </div>

          {/* Nodo 3: Salidas */}
          <div className={`${styles.flowNode} ${styles.nodeAccentOutput}`}>
            <div className={styles.nodeHeader}>
              <span className={styles.nodeLabel}>{tgs_flow.outputs?.label || 'Salidas (Outputs)'}</span>
              <ArrowRight size={16} style={{ color: 'var(--pulse)' }} />
            </div>
            <span className={styles.nodeSublabel}>{tgs_flow.outputs?.sublabel}</span>
            <div className={styles.nodeValue}>
              {tgs_flow.outputs?.value || 0}
              <span className={styles.nodeUnit}> {tgs_flow.outputs?.unit}</span>
            </div>
          </div>

          {/* Nodo 4: Retroalimentación */}
          <div className={`${styles.flowNode} ${styles.nodeAccentFeedback}`}>
            <div className={styles.nodeHeader}>
              <span className={styles.nodeLabel}>{tgs_flow.feedback?.label || 'Retroalimentación'}</span>
              <MessageSquare size={16} style={{ color: 'var(--amber)' }} />
            </div>
            <span className={styles.nodeSublabel}>{tgs_flow.feedback?.sublabel}</span>
            <div className={styles.nodeValue}>
              {tgs_flow.feedback?.value || 0}
              <span className={styles.nodeUnit}> {tgs_flow.feedback?.unit}</span>
            </div>
          </div>
        </div>
      </section>

      {/* ── SECCIÓN 1 & 2: Gráficos de Actividad y Tipos de Archivo ─────── */}
      <div className={styles.chartsGrid}>
        {/* Gráfico 1: Actividad por Semana */}
        <div className={styles.chartCard}>
          <div className={styles.sectionHeading}>
            <h2 className={styles.sectionTitle}>
              <Layers size={18} style={{ color: 'var(--signal)' }} />
              <span>Actividad y Producción por Semana Académica</span>
            </h2>
            <div style={{ display: 'flex', gap: 12, fontFamily: 'var(--font-mono)', fontSize: '11px' }}>
              <span style={{ color: '#58A6FF' }}>■ Posts</span>
              <span style={{ color: '#3FB950' }}>■ Comentarios</span>
            </div>
          </div>

          <div className={styles.chartContainer}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={activity_by_week} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorPosts" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#58A6FF" stopOpacity={0.35} />
                    <stop offset="95%" stopColor="#58A6FF" stopOpacity={0.0} />
                  </linearGradient>
                  <linearGradient id="colorComms" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3FB950" stopOpacity={0.35} />
                    <stop offset="95%" stopColor="#3FB950" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <XAxis
                  dataKey="semana"
                  stroke="var(--muted)"
                  fontSize={11}
                  tickLine={false}
                  axisLine={{ stroke: 'var(--boundary)' }}
                />
                <YAxis
                  stroke="var(--muted)"
                  fontSize={11}
                  tickLine={false}
                  axisLine={{ stroke: 'var(--boundary)' }}
                />
                <Tooltip content={<CustomActivityTooltip />} />
                <Area
                  type="monotone"
                  dataKey="posts"
                  stroke="#58A6FF"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorPosts)"
                />
                <Area
                  type="monotone"
                  dataKey="comentarios"
                  stroke="#3FB950"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorComms)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Gráfico 2: Distribución de tipos de archivo */}
        <div className={styles.chartCard}>
          <div className={styles.sectionHeading}>
            <h2 className={styles.sectionTitle}>
              <PieIcon size={18} style={{ color: '#A371F7' }} />
              <span>Tipos de Archivo</span>
            </h2>
          </div>

          <div className={styles.chartContainer} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <ResponsiveContainer width="100%" height={180}>
              <PieChart>
                <Pie
                  data={file_types}
                  cx="50%"
                  cy="50%"
                  innerRadius={45}
                  outerRadius={75}
                  paddingAngle={4}
                  dataKey="count"
                >
                  {file_types.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={FILE_COLORS[index % FILE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(value, name, item) => [`${value} archivos`, item.payload.name]}
                  contentStyle={{
                    backgroundColor: 'var(--surface-2)',
                    borderColor: 'var(--boundary)',
                    borderRadius: '4px',
                    fontFamily: 'var(--font-mono)',
                    fontSize: '12px',
                    color: 'var(--prose)',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>

            {/* Leyenda en JetBrains Mono */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, justifyContent: 'center', marginTop: 8 }}>
              {file_types.map((ft, idx) => (
                <div key={ft.extension} style={{ display: 'flex', alignItems: 'center', gap: 4, fontFamily: 'var(--font-mono)', fontSize: '11px', color: 'var(--muted)' }}>
                  <span style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: FILE_COLORS[idx % FILE_COLORS.length] }} />
                  <span>{ft.name}: {ft.count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* ── SECCIÓN 3: Top Contribuidores (Ranking de Sinergia) ─────────── */}
      <section className={styles.rankingSection} aria-label="Ranking de Sinergia Académica">
        <div className={styles.sectionHeading}>
          <h2 className={styles.sectionTitle}>
            <Trophy size={18} style={{ color: '#ffd700' }} />
            <span>Ranking de Sinergia Académica (Top Contribuidores)</span>
          </h2>
          <span className={styles.sectionTag}>Puntaje = Posts(10) + Archivos(5) + Feedback(3) + Reacciones(2)</span>
        </div>

        <table className={styles.rankingTable}>
          <thead>
            <tr>
              <th style={{ width: 50, textAlign: 'center' }}>#</th>
              <th>Estudiante / Investigador</th>
              <th>Código</th>
              <th>Publicaciones</th>
              <th>Feedback</th>
              <th>Evidencias</th>
              <th>Reacciones</th>
              <th style={{ textAlign: 'right' }}>Puntaje Total</th>
            </tr>
          </thead>
          <tbody>
            {top_contributors.map((user, idx) => {
              const rankClass =
                idx === 0
                  ? styles.rankFirst
                  : idx === 1
                  ? styles.rankSecond
                  : idx === 2
                  ? styles.rankThird
                  : styles.rankDefault

              return (
                <tr key={user.id}>
                  <td style={{ textAlign: 'center' }}>
                    <span className={`${styles.rankBadge} ${rankClass}`}>
                      {idx + 1}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                      <Avatar name={user.nombre_completo} src={user.avatar_url} size="sm" />
                      <div>
                        <strong style={{ display: 'block', color: 'var(--prose)' }}>
                          {user.nombre_completo}
                        </strong>
                        {user.rol === 'admin' && (
                          <Badge variant="signal" style={{ fontSize: '10px', padding: '1px 4px' }}>
                            Docente
                          </Badge>
                        )}
                      </div>
                    </div>
                  </td>
                  <td style={{ fontFamily: 'var(--font-mono)' }}>
                    [{user.codigo_estudiante || 'N/A'}]
                  </td>
                  <td style={{ fontFamily: 'var(--font-mono)' }}>{user.posts_count}</td>
                  <td style={{ fontFamily: 'var(--font-mono)' }}>{user.comments_count}</td>
                  <td style={{ fontFamily: 'var(--font-mono)' }}>{user.files_count}</td>
                  <td style={{ fontFamily: 'var(--font-mono)' }}>{user.reactions_count}</td>
                  <td style={{ textAlign: 'right' }}>
                    <span className={styles.scorePill}>{user.score} pts</span>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </section>
    </div>
  )
}
