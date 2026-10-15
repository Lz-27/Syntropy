# TGS-Hub (Syntropy)

> **Plataforma Académica Colaborativa y Sistema de Gestión del Conocimiento para Teoría General de Sistemas (TGS)**  
> Construida bajo el paradigma sistémico: **Entradas → Procesamiento → Salidas → Retroalimentación (Feedback)**.

[![React](https://img.shields.io/badge/React-19.2-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-8.3-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)

---

## 📌 Tabla de Contenidos
1. [Visión y Principios del Proyecto](#-visión-y-principios-del-proyecto)
2. [Stack Tecnológico](#-stack-tecnológico)
3. [Arquitectura del Sistema](#-arquitectura-del-sistema)
4. [Estructura del Proyecto](#-estructura-del-proyecto)
5. [Guía de Inicio Rápido (Quickstart)](#-guía-de-inicio-rápido-quickstart)
6. [Credenciales por Defecto (Seeder)](#-credenciales-por-defecto-seeder)
7. [Variables de Entorno](#-variables-de-entorno)
8. [Sistema de Diseño y Temas](#-sistema-de-diseño-y-temas)
9. [Seguridad y Gestión de Archivos](#-seguridad-y-gestión-de-archivos)
10. [Plan de Ejecución y Estado del Roadmap](#-plan-de-ejecución-y-estado-del-roadmap)

---

## 🔬 Visión y Principios del Proyecto

**TGS-Hub (Syntropy)** es una plataforma académica creada para estudiantes de Ingeniería y Administración. Modela la interacción y el debate académico a través de los principios fundamentales de la Teoría General de Sistemas:

* **Entradas (Inputs):** Exploración y recepción de publicaciones, lecturas académicas y datasets.
* **Procesamiento:** Análisis, síntesis y contextualización de conceptos sistémicos mediante editor Markdown enriquecido.
* **Salidas (Outputs):** Publicación de artículos, trabajos de investigación y repositorios de archivos adjuntos (.pdf, .py, .docx, .csv, etc.).
* **Retroalimentación (Feedback):** Hilos de comentarios anidados, auditoría de interacciones y reacciones académicas tipadas (`aporte_valioso`, `duda`, `excelente_analisis`).

---

## 🛠️ Stack Tecnológico

### Frontend
* **Core:** [React 19](https://react.dev/) + [Vite](https://vitejs.dev/)
* **Enrutamiento:** [React Router v7](https://reactrouter.com/)
* **Gestión de Estado:** [Zustand](https://zustand-demo.pmnd.rs/)
* **Cliente HTTP:** [Axios](https://axios-http.com/) con interceptores JWT automáticos
* **Edición y Contenido:** `@uiw/react-md-editor`, `react-syntax-highlighter`
* **Archivos y Visualización:** `react-dropzone`, `react-pdf`
* **Métricas y Visualización:** `recharts`, `lucide-react`
* **Estilizado:** CSS nativo con variables tokens (`tokens.css`, `typography.css`)

### Backend
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+)
* **Servidor ASGI:** [Uvicorn](https://www.uvicorn.org/)
* **ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
* **Base de Datos:** SQLite (configurable a PostgreSQL mediante `DATABASE_URL`)
* **Validación de Datos:** [Pydantic v2](https://docs.pydantic.dev/) + `pydantic-settings`
* **Seguridad:** Autenticación JWT (`python-jose`), hashing de contraseñas con `passlib[bcrypt]` (factor de costo 12)
* **Gestión Multimedia & Archivos:** `aiofiles`, `Pillow` (generación de miniaturas), validación de hash SHA-256

---

## 🏛️ Architecture / Arquitectura

El proyecto sigue una arquitectura desacoplada cliente-servidor orientada a servicios y flujo sistémico (**Entrada ➔ Procesamiento ➔ Salida ➔ Feedback**), conectada mediante una API REST protegida por tokens Bearer JWT:

```mermaid
flowchart LR
    %% Clases y Estilos
    classDef userNode fill:#1f2937,stroke:#3b82f6,stroke-width:2px,color:#f3f4f6;
    classDef clientNode fill:#111827,stroke:#38bdf8,stroke-width:1px,color:#e5e7eb;
    classDef serverNode fill:#0f172a,stroke:#10b981,stroke-width:1px,color:#e5e7eb;
    classDef dataNode fill:#18181b,stroke:#f59e0b,stroke-width:1px,color:#e5e7eb;

    User(["👤 Usuario / Estudiante"]):::userNode

    subgraph FE ["Capas de Presentación (Frontend — React 19 + Vite)"]
        UI["AppShell & Vistas<br/>(Dashboard, Editor, Feed)"]:::clientNode
        State["Estado & Store<br/>(Zustand authStore)"]:::clientNode
        Themes["Tokens de Diseño<br/>(tokens.css / 3 Temas)"]:::clientNode
        ClientHTTP["Cliente Axios<br/>(JWT Interceptor)"]:::clientNode

        Themes -.-> UI
        UI <--> State
        State --> ClientHTTP
    end

    subgraph BE ["Servicios y Lógica de Negocio (Backend — FastAPI)"]
        Gatekeeper["Seguridad & Auth<br/>(OAuth2 / JWT / Bcrypt)"]:::serverNode
        
        subgraph Routers ["Routers & Endpoints"]
            R_Auth["/auth"]:::serverNode
            R_Posts["/posts"]:::serverNode
            R_Files["/files"]:::serverNode
            R_Comm["/comments"]:::serverNode
        end

        subgraph Services ["Servicios Core"]
            S_Post["PostService"]:::serverNode
            S_File["FileService<br/>(SHA-256 / Chunks)"]:::serverNode
            S_Audit["Auditoría & Logs"]:::serverNode
        end

        Gatekeeper --> Routers
        R_Posts --> S_Post
        R_Files --> S_File
        R_Comm --> S_Audit
    end

    subgraph Storage ["Almacenamiento y Persistencia"]
        FileSystem[("Sistema de Archivos<br/>/uploads")]:::dataNode
        DB[("Base de Datos Relacional<br/>SQLite / PostgreSQL")]:::dataNode
    end

    %% Conexiones principales
    User -->|"Interacciones UI / Events"| UI
    ClientHTTP -->|"HTTP REST / JSON & Multipart"| Gatekeeper
    S_File -->|"Stream I/O & Thumbnails"| FileSystem
    S_Post & S_File & S_Audit -->|"SQLAlchemy ORM"| DB
```

### 🗄️ Modelo Relacional del Ecosistema

```mermaid
erDiagram
    USUARIO ||--o{ POST : "publica"
    USUARIO ||--o{ COMENTARIO : "escribe"
    USUARIO ||--o{ AUDITORIA_LOG : "genera"
    CATEGORIA ||--o{ POST : "clasifica"
    POST ||--o{ ARCHIVO : "adjunta"
    POST ||--o{ COMENTARIO : "recibe"
    COMENTARIO ||--o{ COMENTARIO : "responde a (padre_id)"

    USUARIO {
        int id PK
        string codigo_estudiante UK
        string nombre_completo
        string email UK
        string password_hash
        string rol "admin | estudiante"
        datetime created_at
    }

    CATEGORIA {
        int id PK
        string nombre
        int semana_numero
        string descripcion
    }

    POST {
        int id PK
        string titulo
        text resumen
        text contenido_markdown
        int autor_id FK
        int categoria_id FK
        int vistas
        datetime created_at
    }

    ARCHIVO {
        int id PK
        int post_id FK
        string nombre_original
        string ruta
        string hash_sha256
        int tamano_bytes
        string mime_type
        int descargas
    }

    COMENTARIO {
        int id PK
        int post_id FK
        int usuario_id FK
        int padre_id FK "self-reference"
        text contenido
        boolean is_deleted
        datetime created_at
    }

    AUDITORIA_LOG {
        int id PK
        int usuario_id FK
        string accion
        string entidad
        int entidad_id
        string ip
        datetime timestamp
    }
```

---

## 📂 Estructura del Proyecto

```text
Syntropy/
├── backend/
│   ├── app/
│   │   ├── core/               # Configuración, DB engine y utilidades de seguridad JWT
│   │   ├── models/             # Modelos ORM (User, Post, Categoria, Archivo, Comentario, Audit)
│   │   ├── schemas/            # Esquemas Pydantic para validación y serialización
│   │   ├── repositories/       # Abstracciones de acceso a datos
│   │   ├── services/           # Lógica de negocio (FileService con SHA-256, PostService)
│   │   ├── routers/            # Controladores de rutas (auth, posts, files, comments)
│   │   └── main.py             # Inicialización de FastAPI, CORS y montaje estático
│   ├── uploads/                # Directorio de almacenamiento físico de archivos
│   ├── seed_tgs_data.py        # Poblador de datos realistas para el entorno académico
│   ├── requirements.txt        # Dependencias Python
│   └── .env.example            # Plantilla de variables de entorno del backend
├── frontend/
│   ├── src/
│   │   ├── components/         # Componentes modulares (layout, ui, posts, files, comments)
│   │   ├── design/             # Tokens CSS multi-tema y escalas tipográficas
│   │   ├── hooks/              # Custom hooks (useAuth, useTheme, usePosts, useFiles)
│   │   ├── pages/              # Vistas principales (Dashboard, Login, Register, Profile, etc.)
│   │   ├── services/           # Cliente Axios con inyección de Bearer Token
│   │   ├── store/              # Estado global con Zustand (authStore)
│   │   ├── App.jsx             # Enrutador principal y Guards de autenticación
│   │   └── main.jsx            # Punto de entrada de la aplicación
│   └── package.json            # Scripts y dependencias del frontend
├── tgs_hub_execution_plan.md   # Especificación arquitectónica y plan maestro de 12 fases
└── README.md                   # Documentación técnica general
```

---

## 🚀 Guía de Inicio Rápido (Quickstart)

### Prerrequisitos
* **Python**: 3.11 o superior
* **Node.js**: 20 o superior
* **Gestor de paquetes Node**: `pnpm` o `npm`

---

### 1. Configuración del Backend

1. Entra al directorio del backend y crea un entorno virtual:
   ```bash
   cd backend
   python -m venv .venv
   ```

2. Activa el entorno virtual:
   * **Windows (PowerShell):**
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   * **Linux / macOS:**
     ```bash
     source .venv/bin/activate
     ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura el archivo de variables de entorno:
   ```bash
   cp .env.example .env
   ```

5. Ejecuta el seeder para inicializar la base de datos con categorías de semanas TGS, usuarios de prueba y posts académicos:
   ```bash
   python seed_tgs_data.py
   ```

6. Inicia el servidor de desarrollo:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   * *Documentación interactiva Swagger:* [http://localhost:8000/docs](http://localhost:8000/docs)
   * *Healthcheck:* [http://localhost:8000/health](http://localhost:8000/health)

---

### 2. Configuración del Frontend

1. Abre una nueva terminal, dirígete a la carpeta `frontend` e instala dependencias:
   ```bash
   cd frontend
   pnpm install
   # o bien: npm install
   ```

2. Inicia el servidor de desarrollo con Vite:
   ```bash
   pnpm dev
   # o bien: npm run dev
   ```

3. Abre tu navegador en [http://localhost:5173](http://localhost:5173).

---

## 🔑 Credenciales por Defecto (Seeder)

El script `seed_tgs_data.py` genera cuentas de prueba preconfiguradas:

| Rol | Código / Usuario | Contraseña | Nombre |
|---|---|---|---|
| **Administrador** | `61035728` | `271714` | Docente Administrador TGS |
| **Estudiante** | `20241001` | `password123` | Carlos Mendoza |
| **Estudiante** | `20241002` | `password123` | Valeria Quispe |

> Se crean además 10 categorías académicas (correspondientes a las Semanas 1 a 10 de la asignatura: Bertalanffy, Cibernética, Entropía, Homeostasis, etc.), 20 publicaciones con Markdown enriquecido y archivos adjuntos de prueba.

---

## ⚙️ Variables de Entorno

### Backend (`backend/.env`)

| Variable | Tipo | Descripción | Valor por Defecto |
|---|---|---|---|
| `SECRET_KEY` | `str` | Clave secreta para firmar tokens JWT (se recomienda generar con openssl) | *Clave temporal de desarrollo* |
| `DATABASE_URL` | `str` | Cadena de conexión SQLAlchemy (SQLite o PostgreSQL) | `sqlite:///./tgs_hub.db` |
| `UPLOAD_DIR` | `str` | Directorio local de destino para archivos subidos | `uploads` |
| `MAX_FILE_MB` | `int` | Tamaño máximo permitido por archivo (MB) | `100` |
| `ALLOWED_EXTENSIONS`| `str` | Lista separada por comas de formatos autorizados | `pdf,docx,pptx,xlsx,txt,csv,png,jpg,py,zip...` |
| `CORS_ORIGINS` | `str` | Orígenes web permitidos para peticiones cruzadas | `http://localhost:5173,http://localhost:3000` |
| `ACCESS_TOKEN_EXPIRE_DAYS` | `int` | Vigencia de la sesión en días | `7` |

---

## 🎨 Sistema de Diseño y Temas

La interfaz se concibió bajo las pautas de **`frontend-design`** e **`impeccable`**, priorizando un estilo *Academic Tech / Cyber-Systemic* que descarta los clichés de SaaS genéricos.

### Modos Soportados
1. **Dark Matte (Predeterminado):** Fondo carbón profundo (`#0D1117`), superficies `#161B22` y bordes sutiles `#21262D`.
2. **Academic Paper (Claro):** Fondo `#FAFBFC`, superficies blancas puras y contrastes tipográficos para lectura prolongada.
3. **Deep Cyber Navy:** Paleta azul marino nocturna (`#060D1F` / `#0B1629`) con acentos cian y esmeralda.

### Tipografías
* **UI y Lectura General:** *Plus Jakarta Sans* (pesos 300, 400, 500, 600)
* **Datos Técnicos, Hashes y Código:** *JetBrains Mono* (pesos 400, 500)

---

## 🔒 Seguridad y Gestión de Archivos

* **Hashing Criptográfico:** Cada archivo cargado se procesa en bloques de 8 KB generando su huella **SHA-256** para certificar integridad y detectar duplicados.
* **Control de Formatos:** Doble validación (extensión autorizada y verificación de tipos MIME).
* **Control de Acceso Basado en Roles (RBAC):** Dependencias FastAPI para aislar permisos entre estudiantes y docentes administradores (`require_role("admin")`).
* **Visualización sin descarga forzosa:** Endpoints dedicados para streaming inline (`Content-Disposition: inline`) para el previsualizador universal.

---

## 🗺️ Plan de Ejecución y Estado del Roadmap

El proyecto sigue el plan estructurado en 12 fases detallado en [tgs_hub_execution_plan.md](file:///c:/PROYECTOS/FULL%20STACK/Syntropy/tgs_hub_execution_plan.md):

* [x] **P1 — Fundación del Sistema:** Tokens de diseño, fuentes y estructura de directorios.
* [x] **P2 — Backend Core:** Modelos ORM, esquemas Pydantic, Auth JWT y Seeder TGS.
* [x] **P3 — Backend API (Posts y Archivos):** Endpoints REST para publicaciones y gestión de archivos.
* [ ] **P4 — Backend API (Comentarios y Auditoría):** Hilos recursivos, reacciones académicas y logs de auditoría.
* [x] **P5 — Frontend Shell:** AppShell, glassmorphism Header, Sidebar con flujo TGS y ThemeSwitcher.
* [x] **P6 — Frontend Auth:** Páginas de Login, Registro y guardias de ruta (`ProtectedRoute`). *(Perfil en desarrollo)*.
* [ ] **P7 — Frontend Dashboard y Feed:** KPIs sistémicos y feed con filtrado por semanas TGS.
* [ ] **P8 — Frontend Editor y Gestor de Archivos:** Editor Markdown en vivo y Dropzone con drag & drop.
* [ ] **P9 — Frontend Debate y Comentarios:** Hilos interactivos de discusión y reacciones académicas.
* [ ] **P10 — Analíticas y Explorador:** Gráficos con Recharts, diagrama interactivo de flujo y navegador de archivos.
* [ ] **P11 — Previsualizador Universal:** Modal de lectura para PDF, código fuente, imágenes y hash SHA-256.
* [ ] **P12 — QA, Accesibilidad y Cierre:** Auditoría de contraste, soporte móvil responsivo total y optimización.

---

## 📄 Licencia

Este proyecto se distribuye para fines académicos e investigativos en el marco del estudio de la **Teoría General de Sistemas**.
