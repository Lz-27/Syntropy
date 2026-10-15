"""
seed_tgs_data.py — Seeder realista para TGS-Hub

Ejecutar desde backend/:
    python seed_tgs_data.py

Pobla la BD con:
  - Admin: código 61035728, clave 271714
  - 8 estudiantes ficticios
  - 10 categorías (Semanas 1-10 TGS)
  - 20 publicaciones con Markdown real
  - Archivos .pdf, .txt, .csv, .py generados programáticamente
  - 40 comentarios con respuestas anidadas (máx. 2 niveles)
"""
import sys, os, uuid, hashlib
from typing import Union

# Asegurar encoding UTF-8 en Windows stdout/stderr
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Asegurar que el módulo app sea encontrado
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, create_tables
from app.core.security import hash_password
from app.models.user import User
from app.models.post import Post, Categoria
from app.models.file import Archivo
from app.models.comment import Comentario
from app.core.config import settings

create_tables()
db = SessionLocal()

# ── 0. Limpiar datos existentes ──────────────────────────────
print("🔄 Limpiando BD existente...")
db.query(Comentario).delete()
db.query(Archivo).delete()
db.query(Post).delete()
db.query(Categoria).delete()
db.query(User).delete()
db.commit()

# ── 1. Usuarios ───────────────────────────────────────────────
print("👥 Creando usuarios...")

ADMIN = User(
    nombre_completo="Dr. Carlos Mendoza Torres",
    codigo_estudiante="61035728",
    email="admin@tgshub.edu",
    password_hash=hash_password("271714"),
    rol="admin",
    bio="Docente de Teoría General de Sistemas. Magíster en Cibernética Organizacional. Bertalanffy enthusiast.",
    avatar_url=None,
)
db.add(ADMIN)
db.flush()

ESTUDIANTES_DATA = [
    ("María García López",      "61045892", "mgarcia@uni.edu",    "Sistémica curiosa. Especialidad: entropía y disipación de energía en redes complejas."),
    ("Diego Ríos Castillo",     "61038741", "drios@uni.edu",      "Apasionado por la cibernética de Wiener. Trabajo de grado sobre homeostasis organizacional."),
    ("Valentina Cruz Herrera",  "61052309", "vcruz@uni.edu",      "Modelado sistémico aplicado a ecosistemas urbanos. Python + TGS."),
    ("Andrés Moreno Salinas",   "61041567", "amoreno@uni.edu",    "Pensamiento sistémico en gestión de proyectos. PMP en formación."),
    ("Natalia Jiménez Vargas",  "61059103", "njimenez@uni.edu",   "Investigación en dinámica de sistemas. Fanática de Forrester y Meadows."),
    ("Luis Espinoza Rojas",     "61033924", "lespinoza@uni.edu",  "Ingeniería de sistemas complejos. Interesado en teoría del caos y fractales."),
    ("Camila Pereira Silva",    "61047816", "cpereira@uni.edu",   "Administración sistémica. Aplicaciones TGS en organizaciones sociales."),
    ("Sebastián Alvarado Mora", "61062145", "salvarado@uni.edu",  "Computación y sistemas. Implementando simuladores de sistemas dinámicos en Python."),
]

estudiantes = []
for nombre, codigo, email, bio in ESTUDIANTES_DATA:
    u = User(
        nombre_completo=nombre,
        codigo_estudiante=codigo,
        email=email,
        password_hash=hash_password("Tgs2026!"),
        rol="estudiante",
        bio=bio,
    )
    db.add(u)
    db.flush()
    estudiantes.append(u)

db.commit()
print(f"  ✓ Admin + {len(estudiantes)} estudiantes creados")

# ── 2. Categorías (Semanas 1-10 TGS) ─────────────────────────
print("📂 Creando categorías...")

CATEGORIAS_DATA = [
    (1,  "Semana 1 — Introducción a la TGS",        "Orígenes, Bertalanffy, conceptos fundamentales de sistema, subsistema y supersistema."),
    (2,  "Semana 2 — Pensamiento Sistémico",         "Holismo vs reduccionismo. El sistema como totalidad. Propiedades emergentes."),
    (3,  "Semana 3 — Cibernética",                   "Wiener, Shannon y el control. Retroalimentación positiva y negativa."),
    (4,  "Semana 4 — Entropía y Negentropía",        "Segunda ley de la termodinámica. Entropía informacional. Sistemas disipativos."),
    (5,  "Semana 5 — Homeostasis y Equifinalidad",   "Estado estable. Regulación. Equifinalidad en sistemas abiertos."),
    (6,  "Semana 6 — Dinámica de Sistemas",          "Diagramas de flujo. Stocks y flows. Simulación con Vensim/Python."),
    (7,  "Semana 7 — Sistemas Complejos Adaptativos","Agentes, emergencia, auto-organización. CAS en biología y economía."),
    (8,  "Semana 8 — Organizaciones como Sistemas",  "Teoría organizacional sistémica. Modelo de sistema viable (Beer)."),
    (9,  "Semana 9 — Aplicaciones en Ingeniería",    "Ingeniería de sistemas. MBSE. SysML. Análisis de requisitos sistémicos."),
    (10, "Semana 10 — Encargos y Proyectos Finales", "Trabajos integradores. Modelado completo de un sistema real."),
]

categorias = []
for semana, nombre, desc in CATEGORIAS_DATA:
    c = Categoria(nombre=nombre, descripcion=desc, semana_numero=semana, created_by_id=ADMIN.id)
    db.add(c)
    db.flush()
    categorias.append(c)

db.commit()
print(f"  ✓ {len(categorias)} categorías creadas")

# ── 3. Publicaciones ─────────────────────────────────────────
print("📝 Creando publicaciones...")

POSTS_DATA = [
    # (titulo, resumen, contenido_md, autor_idx, categoria_idx)
    (
        "Análisis Sistémico del Metabolismo Urbano de Bogotá",
        "Aplicación del marco TGS para modelar los flujos de energía, materia e información en la ciudad de Bogotá como sistema abierto.",
        """# Análisis Sistémico del Metabolismo Urbano de Bogotá

## Introducción

Bertalanffy (1968) definió los **sistemas abiertos** como aquellos que intercambian materia y energía con su entorno. Las ciudades son ejemplos paradigmáticos de esta definición.

## Marco Teórico

$$E_{entrada} = E_{procesada} + E_{disipada} + \Delta E_{almacenada}$$

Esta ecuación describe el balance energético de Bogotá como sistema termodinámico abierto.

## Subsistemas Identificados

| Subsistema | Inputs | Outputs | Retroalimentación |
|---|---|---|---|
| Transporte | Combustible, personas | Movilidad, CO₂ | Semáforos, señalización |
| Residuos | Basura doméstica | Reciclaje, relleno | Precios de reciclaje |
| Agua | Embalses | Agua tratada | Consumo/precio |

## Conclusión

El metabolismo urbano de Bogotá exhibe **entropía creciente** en su componente de residuos sólidos, con una tasa de neguentropía insuficiente para compensar la degradación del sistema.

> "Todo sistema vivo es un sistema abierto." — Von Bertalanffy, 1968
""",
        0, 0,  # María, Semana 1
    ),
    (
        "Retroalimentación Negativa en Sistemas de Control de Temperatura",
        "Análisis del termostato como modelo canónico de retroalimentación negativa. Comparación con regulación homeostática biológica.",
        """# Retroalimentación Negativa en Sistemas de Control

## El Termostato como Modelo Cibernético

El termostato es el ejemplo más citado en cibernética (Wiener, 1948). Su funcionamiento ilustra el principio de **retroalimentación negativa**:

```python
def termostat_loop(target_temp: float, tolerance: float = 0.5):
    \"\"\"Simulación simplificada de control por retroalimentación.\"\"\"
    current_temp = 15.0  # temperatura inicial
    heating = False
    
    for tick in range(100):
        error = target_temp - current_temp
        
        if error > tolerance:
            heating = True
        elif error < -tolerance:
            heating = False
        
        # Dinámica simplificada
        if heating:
            current_temp += 0.3
        else:
            current_temp -= 0.1  # pérdida natural
        
        print(f"t={tick}: T={current_temp:.2f}°C, calefacción={heating}")
```

## Comparación con la Homeostasis Biológica

La temperatura corporal humana se mantiene en 37°C ± 0.5°C mediante:
- **Detector**: termorreceptores hipotalámicos
- **Centro de control**: hipotálamo
- **Efector**: glándulas sudoríparas, vasoconstricción

Esta es retroalimentación negativa biológica.
""",
        1, 2,  # Diego, Semana 3
    ),
    (
        "Entropía Informacional en Redes de Comunicación Organizacional",
        "Aplicación del concepto de entropía de Shannon al análisis de la degradación de la información en cadenas de mando.",
        """# Entropía Informacional en Organizaciones

## Shannon y la Teoría de la Información

Shannon (1948) definió la entropía informacional como:

$$H = -\sum_{i} p_i \log_2 p_i$$

Donde $p_i$ es la probabilidad de ocurrencia del mensaje $i$.

## El Teléfono Descompuesto Organizacional

En jerarquías con n niveles de comunicación, la fidelidad del mensaje decrece exponencialmente:

| Nivel | Fidelidad (%) | Pérdida acumulada |
|-------|--------------|-------------------|
| Dirección → Gerencia | 95% | 5% |
| Gerencia → Jefatura | 90% | 14% |
| Jefatura → Operario | 85% | 27% |
| Operario → Ejecución | 80% | 41% |

## Estrategias Negentrópicas

1. **Redundancia controlada**: repetir el mensaje en múltiples canales
2. **Códigos de verificación**: confirmaciones de recepción
3. **Canales directos**: eliminar intermediarios cuando es posible

> La negentropía organizacional se logra con información de calidad, no de cantidad.
""",
        2, 3,  # Valentina, Semana 4
    ),
    (
        "Modelo de Sistema Viable (VSM) aplicado a una Startup de Tecnología",
        "Análisis de una startup real usando el Modelo de Sistema Viable de Stafford Beer. Identificación de los 5 subsistemas.",
        """# VSM en una Startup Tecnológica

## Los 5 Sistemas de Beer

Stafford Beer (1972) propone que toda organización viable contiene 5 subsistemas recursivos:

| Sistema | Función | En la Startup |
|---------|---------|---------------|
| S1 | Operaciones | Equipos de desarrollo |
| S2 | Coordinación | Scrum Masters, Kanban |
| S3 | Control operacional | CTO, métricas de sprint |
| S4 | Inteligencia (futuro) | Product Strategy, I+D |
| S5 | Política (identidad) | Founders, cultura |

## Diagnóstico Sistémico

La startup analizada presenta **deficiencia en S4**: el 90% del tiempo gerencial se destina a S3 (apagar incendios operativos) sin dedicar recursos al análisis del entorno futuro.

## Recomendaciones

- Establecer un **canal S4** formal: reuniones semanales de estrategia
- Separar presupuesto de exploración (S4) del de explotación (S3)
- Implementar OKRs como mecanismo de S5
""",
        3, 7,  # Andrés, Semana 8
    ),
    (
        "Dinámica de Sistemas: Modelando la Propagación de una Epidemia",
        "Implementación del modelo SIR (Susceptible-Infectado-Recuperado) usando dinámica de sistemas y Python.",
        """# Modelo SIR con Dinámica de Sistemas

## El Modelo

El modelo SIR es un stock-and-flow clásico:

- **S** (Susceptibles): población en riesgo
- **I** (Infectados): actualmente enfermos
- **R** (Recuperados): inmunes

## Ecuaciones de Flujo

```python
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def sir_model(y, t, beta, gamma):
    S, I, R = y
    N = S + I + R
    dS = -beta * S * I / N
    dI = beta * S * I / N - gamma * I
    dR = gamma * I
    return [dS, dI, dR]

# Parámetros
N = 10_000
I0, R0 = 10, 0
S0 = N - I0 - R0
beta = 0.3   # tasa de infección
gamma = 0.05  # tasa de recuperación

t = np.linspace(0, 200, 200)
solution = odeint(sir_model, [S0, I0, R0], t, args=(beta, gamma))
```

## Análisis Sistémico

El punto de equilibrio del sistema ocurre cuando:
$$\\frac{dI}{dt} = 0 \\Rightarrow R_0 = \\frac{\\beta}{\\gamma} = 1$$

El número reproductivo básico $R_0 = 6$ indica alta transmisibilidad.
""",
        4, 5,  # Natalia, Semana 6
    ),
    (
        "Propiedades Emergentes en Colonias de Hormigas: Un Sistema Complejo Adaptativo",
        "Las colonias de hormigas como ejemplo de emergencia: inteligencia colectiva sin coordinación central.",
        """# Emergencia en Colonias de Hormigas

## ¿Qué es la Emergencia?

> "El todo es más que la suma de sus partes." — Aristóteles (reformulado por Bertalanffy)

La **emergencia** ocurre cuando las interacciones locales entre componentes simples producen comportamiento global complejo e impredecible.

## Feromonas como Mecanismo de Retroalimentación

```
Hormiga encuentra comida
    ↓
Deposita feromona en camino de regreso
    ↓
Otras hormigas siguen el rastro
    ↓
Refuerzan el rastro con más feromonas (R+ positiva)
    ↓
El rastro más corto acumula más feromonas (selección)
    ↓
La colonia "resuelve" el problema del camino más corto
```

## Aplicaciones en Ingeniería

Los **Ant Colony Optimization (ACO)** algorithms imitan este mecanismo para resolver:
- Problema del viajante (TSP)
- Ruteo de redes
- Scheduling de producción

## Características CAS Observadas

| Propiedad | Manifestación en hormigas |
|-----------|--------------------------|
| Auto-organización | Sin reina directora |
| Emergencia | Inteligencia colectiva |
| Adaptabilidad | Respuesta a perturbaciones |
| No-linealidad | Pequeños cambios, grandes efectos |
""",
        5, 6,  # Luis, Semana 7
    ),
    (
        "Equifinalidad en Proyectos de Desarrollo de Software: Múltiples Caminos al Mismo Resultado",
        "Análisis de la propiedad de equifinalidad aplicada a metodologías de desarrollo: Waterfall, Scrum, Kanban y XP como caminos equivalentes.",
        """# Equifinalidad en Desarrollo de Software

## Definición

Von Bertalanffy (1968) definió la **equifinalidad** como la propiedad de los sistemas abiertos de alcanzar el mismo estado final desde diferentes condiciones iniciales y por diferentes caminos.

## Las Metodologías como Caminos Sistémicos

| Metodología | Condición inicial | Camino | Estado final |
|-------------|------------------|--------|--------------|
| Waterfall | Requisitos congelados | Secuencial | Software entregado |
| Scrum | Requisitos volátiles | Iterativo | Software entregado |
| Kanban | Flujo continuo | Pull system | Software entregado |
| XP | Calidad primero | TDD + pair programming | Software entregado |

## Implicaciones Gerenciales

La equifinalidad implica que **no existe una única metodología correcta**. La elección depende de:

1. **Condiciones iniciales**: certeza de los requisitos
2. **Características del equipo**: experiencia, tamaño
3. **Contexto organizacional**: cultura, presupuesto

## Conclusión

Un gerente de proyectos sistémico entiende que la ruta no determina el destino en sistemas abiertos. La clave está en la **adaptación dinámica** del proceso al contexto.
""",
        6, 4,  # Camila, Semana 5
    ),
    (
        "Simulador de Sistema de Inventario con Stocks y Flows en Python",
        "Implementación completa de un modelo de dinámica de sistemas para gestión de inventario con retroalimentación de demanda.",
        """# Simulador de Inventario: Stocks y Flows

## Arquitectura del Sistema

```
[Producción] → [Inventario] → [Ventas]
       ↑              ↓
   [Órdenes] ← [Stock deseado - Stock real]
```

## Implementación en Python

```python
class InventorySystem:
    \"\"\"Sistema de inventario con dinámica de stocks y flows.\"\"\"
    
    def __init__(self, initial_stock=1000, desired_stock=800):
        self.stock = initial_stock
        self.desired_stock = desired_stock
        self.adjustment_time = 4  # semanas
        self.history = []
    
    def step(self, demand: float, production_capacity: float = 500):
        # Flow de ajuste de inventario (retroalimentación negativa)
        stock_gap = self.desired_stock - self.stock
        production_order = max(0, demand + stock_gap / self.adjustment_time)
        actual_production = min(production_order, production_capacity)
        
        # Actualizar stocks
        self.stock = self.stock + actual_production - demand
        self.stock = max(0, self.stock)  # No puede ser negativo
        
        self.history.append({
            'stock': self.stock,
            'production': actual_production,
            'demand': demand,
            'gap': stock_gap,
        })
        return self.stock

# Simulación de 52 semanas con demanda variable
import random
sim = InventorySystem()
for week in range(52):
    demand = 400 + random.gauss(0, 50)  # demanda estocástica
    sim.step(demand)

print(f"Stock promedio: {sum(h['stock'] for h in sim.history) / 52:.0f} unidades")
```

## Comportamiento Observado

El sistema exhibe **oscilaciones amortiguadas** (bullwhip effect) cuando el tiempo de ajuste > tiempo de entrega. Este es un comportamiento emergente del loop de retroalimentación.
""",
        7, 5,  # Sebastián, Semana 6
    ),
    (
        "La Cibernética de Wiener: Del Control Automático a la Inteligencia Artificial",
        "Revisión histórica del concepto de cibernética y su evolución hasta los algoritmos de aprendizaje por refuerzo modernos.",
        """# Cibernética: De Wiener a la IA Moderna

## Origen del Término

Norbert Wiener acuñó "**cibernética**" en 1948 del griego κυβερνήτης (kybernetes: timonel), para describir la ciencia del **control y la comunicación en el animal y la máquina**.

## Conceptos Fundacionales

### 1. Retroalimentación (Feedback)

| Tipo | Efecto | Ejemplo biológico | Ejemplo tecnológico |
|------|--------|------------------|---------------------|
| Negativa | Estabiliza | Homeostasis | Termostato |
| Positiva | Amplifica | Coagulación sanguínea | Micrófono-altavoz |

### 2. La Caja Negra

Wiener propuso estudiar sistemas por sus entradas y salidas, sin necesidad de conocer su estructura interna:

```
[Inputs] → [■ CAJA NEGRA ■] → [Outputs]
               ↑
         [Retroalimentación]
```

## De la Cibernética al Machine Learning

El **aprendizaje por refuerzo** (RL) es cibernética computacional:

- **Agente** = sistema controlador
- **Entorno** = sistema controlado
- **Recompensa** = señal de retroalimentación
- **Política** = función de control

Q-learning, PPO, y SAC son implementaciones modernas del sueño cibernético de Wiener.
""",
        0, 2,  # María, Semana 3
    ),
    (
        "Análisis de la Frontera del Sistema en Organizaciones Sin Fines de Lucro",
        "Definición y análisis de la frontera sistema-entorno en ONGs. Caso: Fundación Amanecer.",
        """# Frontera del Sistema en ONGs

## El Problema de la Frontera

Definir los límites de un sistema es **una de las decisiones más importantes** en el análisis sistémico. En organizaciones sin fines de lucro, esta decisión es especialmente compleja por:

1. **Múltiples stakeholders** con perspectivas distintas
2. **Flujos difusos** de recursos (donaciones, voluntariado, subsidios)
3. **Misión social** que trasciende lo organizacional

## Caso: Fundación Amanecer

### Análisis de Frontera Nivel 1 (estrecha)
```
SISTEMA: Personal contratado + directivos
ENTORNO: Beneficiarios, donantes, gobierno
FRONTERA: Contrato laboral
```

### Análisis de Frontera Nivel 2 (amplia)
```
SISTEMA: Personal + voluntarios permanentes + beneficiarios activos
ENTORNO: Comunidad, gobierno, sociedad
FRONTERA: Compromiso de participación
```

## Herramienta: Diagrama de Influencia

| Actor | ¿Dentro/Fuera? | Justificación |
|-------|---------------|---------------|
| Director ejecutivo | Dentro | Control total |
| Voluntarios semanales | Dentro (L2) | Input constante |
| Donantes ocasionales | Fuera | Sin control |
| Gobierno (subsidios) | Frontera | Condicional |

## Implicación Práctica

La definición de frontera determina qué variables son **manejables** y cuáles son **perturbaciones del entorno**. Una frontera demasiado estrecha subestima recursos disponibles.
""",
        3, 1,  # Andrés, Semana 2
    ),
    (
        "Negentropía y Aprendizaje Organizacional: Cómo las Empresas Luchan Contra el Desorden",
        "Análisis de las estrategias negentrópicas que las organizaciones utilizan para mantener su viabilidad frente a la entropía.",
        """# Negentropía Organizacional

## La Amenaza Entrópica

Toda organización tiende naturalmente hacia el **desorden** (Segunda Ley de la Termodinámica aplicada a sistemas sociales):

- Rotación de personal → pérdida de conocimiento
- Conflictos internos → reducción de coordinación  
- Obsolescencia tecnológica → baja competitividad
- Cambios regulatorios → invalidación de procesos

$$\Delta S_{org} = \Delta S_{interna} + \Delta S_{intercambio}$$

## Mecanismos Negentrópicos

### 1. Gestión del Conocimiento
- Documentación sistemática de procesos
- Comunidades de práctica (Wenger, 1998)
- Wikis y bases de conocimiento

### 2. Aprendizaje Organizacional
Argyris y Schön (1978) distinguen:

| Tipo | Descripción | Cambio |
|------|-------------|--------|
| Single-loop | Corrige errores dentro del marco | Táctico |
| Double-loop | Cuestiona el marco mismo | Estratégico |
| Deutero-learning | Aprende a aprender | Transformador |

### 3. Innovación Continua
La innovación es importación de negentropía desde el entorno: nuevas ideas, tecnologías y modelos que contrarrestan la entropía interna.

## Medición

Índice de Vitalidad Organizacional (IVO):
$$IVO = \frac{\text{Capital intelectual} + \text{Cohesión cultural}}{\text{Rotación} + \text{Conflictos}}$$
""",
        2, 3,  # Valentina, Semana 4
    ),
    (
        "Teoría de Grafos aplicada a Redes de Suministro: Una Perspectiva Sistémica",
        "Modelado de cadenas de suministro como grafos dirigidos. Identificación de nodos críticos y vulnerabilidades sistémicas.",
        """# Redes de Suministro como Sistemas en Grafo

## Formalización

Una cadena de suministro puede modelarse como un grafo dirigido $G = (V, E, W)$ donde:
- $V$ = nodos (proveedores, plantas, distribuidores, clientes)
- $E$ = aristas dirigidas (flujos de material/información)
- $W$ = pesos (capacidad, tiempo, costo)

## Análisis de Centralidad

```python
import networkx as nx

# Construir grafo de cadena de suministro
G = nx.DiGraph()
G.add_edges_from([
    ("Proveedor_A", "Planta_1", {"capacidad": 500}),
    ("Proveedor_B", "Planta_1", {"capacidad": 300}),
    ("Proveedor_B", "Planta_2", {"capacidad": 200}),
    ("Planta_1", "Dist_Centro", {"capacidad": 700}),
    ("Planta_2", "Dist_Norte", {"capacidad": 200}),
    ("Dist_Centro", "Cliente_Final", {"capacidad": 600}),
    ("Dist_Norte", "Cliente_Final", {"capacidad": 150}),
])

# Identificar cuellos de botella (betweenness centrality)
betweenness = nx.betweenness_centrality(G)
critical_node = max(betweenness, key=betweenness.get)
print(f"Nodo crítico: {critical_node} (BC={betweenness[critical_node]:.3f})")
# Output: Nodo crítico: Dist_Centro (BC=0.667)
```

## Vulnerabilidades Sistémicas

El análisis revela que `Dist_Centro` es un **punto único de falla** (SPOF):
- Si falla, 80% del flujo se interrumpe
- Resiliencia sistémica requiere redundancia en nodos críticos

## Estrategia de Redundancia

Agregar `Dist_Sur` como nodo redundante reduce la centralidad de `Dist_Centro` de 0.667 a 0.312, aumentando la resiliencia del sistema.
""",
        7, 8,  # Sebastián, Semana 9
    ),
    (
        "Auto-organización en Mercados Financieros: Un Análisis Sistémico de la Eficiencia",
        "Los mercados como sistemas auto-organizados. Crítica sistémica a la hipótesis de mercados eficientes.",
        """# Mercados Financieros como Sistemas Auto-organizados

## La Hipótesis de Mercados Eficientes (HME)

Fama (1970) propuso que los precios reflejan **toda la información disponible** instantáneamente. Desde la TGS, esto implica un sistema perfectamente homeostático.

## Crítica Sistémica a la HME

| Supuesto HME | Realidad Sistémica |
|---|---|
| Agentes racionales | Agentes con racionalidad limitada (Simon) |
| Información perfecta | Información asimétrica y con ruido |
| Equilibrio instantáneo | Dinámica compleja con histéresis |
| Sin retroalimentación | Retroalimentación positiva (herding, burbujas) |

## Retroalimentación Positiva en Burbujas

```
Precio sube
    ↓
Más inversores entran (FOMO)
    ↓
Precio sube más (R+)
    ↓
Desconexión del valor fundamental
    ↓
Colapso (punto de bifurcación)
```

## El Mercado como CAS

Los mercados son **Sistemas Complejos Adaptativos** (Holland, 1992):
- Millones de agentes heterogéneos con reglas locales simples
- Comportamiento macroeconómico emergente no planificado
- Capacidad de adaptación a shocks externos

La eficiencia de mercado es una propiedad **emergente aproximada**, no un estado de equilibrio permanente.
""",
        4, 6,  # Natalia, Semana 7
    ),
    (
        "Sinergia en Equipos de Trabajo: Cuando el Todo Supera la Suma de las Partes",
        "Análisis cuantitativo y cualitativo de la sinergia en equipos multidisciplinarios. Condiciones para la emergencia sinérgica.",
        """# Sinergia en Equipos Multidisciplinarios

## Definición Formal

La sinergia ocurre cuando:
$$\text{Output}_{equipo} > \sum_{i=1}^{n} \text{Output}_{individuo_i}$$

No toda colaboración produce sinergia. Es un **resultado sistémico**, no una garantía automática de la agrupación.

## Condiciones Necesarias para la Sinergia

### 1. Diversidad Complementaria
Los miembros deben aportar competencias **distintas y complementarias**, no redundantes:

| Perfil | Fortaleza | Debilidad cubierta por |
|--------|-----------|----------------------|
| Analista sistémico | Visión global | Implementador |
| Especialista técnico | Profundidad | Comunicador |
| Facilitador | Coordinación | Especialistas |
| Implementador | Ejecución | Analista |

### 2. Canales de Comunicación Efectivos

Ley de Conant-Ashby (1970):
> "Todo buen regulador de un sistema debe ser un modelo de ese sistema."

Un equipo sinérgico tiene modelos mentales suficientemente alineados.

### 3. Retroalimentación Constructiva

La **retroalimentación negativa** (correctiva) debe superar a la positiva (amplificadora) en proporción 3:1 (Losada Line).

## Cálculo del Índice de Sinergia

$$IS = \frac{\text{Output real del equipo}}{\sum \text{Output individual}} - 1$$

$IS > 0$: sinergia positiva | $IS = 0$: aditividad | $IS < 0$: disfunción sistémica
""",
        6, 1,  # Camila, Semana 2
    ),
    (
        "Sistemas Sociotécnicos: Diseño Participativo en la Era Digital",
        "La teoría de sistemas sociotécnicos (Trist & Bamforth) aplicada al diseño de plataformas digitales colaborativas.",
        """# Sistemas Sociotécnicos en Plataformas Digitales

## Origen: Las Minas de Carbón de Tavistock

En 1951, Trist y Bamforth estudiaron la introducción de mecanización en minas de carbón británicas. Descubrieron que los cambios **tecnológicos sin considerar el sistema social** destruían la productividad.

## Los Dos Subsistemas

| Subsistema Técnico | Subsistema Social |
|---|---|
| Hardware y software | Personas y grupos |
| Algoritmos y datos | Normas y valores |
| Arquitectura de información | Cultura organizacional |
| Rendimiento del sistema | Satisfacción y bienestar |

## Principios de Optimización Conjunta

1. **Mínima especificación crítica**: solo prescribir lo absolutamente necesario
2. **Variedad de tareas**: los roles deben tener suficiente diversidad
3. **Unidades responsables**: equipos con autonomía real sobre su trabajo
4. **Control local de varianza**: solucionar problemas en origen, no escalar

## Caso: Diseño de TGS-Hub

Esta plataforma aplica principios sociotécnicos:
- **Técnico**: React + FastAPI + SQLite con arquitectura modular
- **Social**: Flujo TGS integrado en la navegación (no es decorativo)
- **Optimización conjunta**: la interfaz refleja el modelo mental del usuario TGS

El resultado esperado: mayor adopción y calidad de las contribuciones académicas.
""",
        1, 7,  # Diego, Semana 8
    ),
    (
        "Homeostasis Digital: Mecanismos de Estabilización en Plataformas de Redes Sociales",
        "Análisis de los mecanismos homeostáticos que plataformas como Twitter/X y TikTok usan para mantener el engagement del sistema.",
        """# Homeostasis en Plataformas Digitales

## El Desafío Homeostático

Una plataforma digital debe mantener el **engagement** dentro de rangos viables:
- Muy bajo → usuarios abandonan (entropía → muerte del sistema)
- Muy alto → agotamiento, toxicidad (entropía de otra forma)

## Mecanismos Homeostáticos Identificados

### Algoritmos de Recomendación como Retroalimentación

```
Usuario ve video
    ↓
Sistema mide tiempo de visualización
    ↓
Si tiempo > umbral: recomienda contenido similar (R+ moderada)
Si tiempo < umbral: reduce exposición a ese tipo (R- correctiva)
    ↓
Sistema aprende distribución óptima de contenido
    ↓
Maximiza tiempo en plataforma (variable de estado)
```

### Notificaciones como Perturbación Controlada

Las notificaciones son **inputs de perturbación controlada** que sacan al usuario del estado de baja actividad (mínimo local de energía).

## El Estado de Flujo como Objetivo Homeostático

Csikszentmihalyi (1990) describe el **flujo** como el estado óptimo de engagement:

$$\text{Flujo} = f\left(\frac{\text{Desafío}}{\text{Habilidad}}\right) \approx 1$$

Las plataformas calibran la dificultad del contenido para mantener este ratio cerca de 1.

## Riesgos Sistémicos

La optimización homeostática del engagement puede producir **bucles de retroalimentación disfuncionales**: cámaras de eco, radicalización, adicción digital.
""",
        5, 4,  # Luis, Semana 5
    ),
    (
        "Encargo Final: Modelado Sistémico de la Cadena de Valor de una Empresa Local",
        "Proyecto integrador: análisis completo con diagrama de influencias, stocks & flows y propuestas de intervención sistémica.",
        """# Encargo Final — Modelado Sistémico

## Empresa Analizada: Panadería Artesanal \"El Trigo Dorado\"

### Descripción del Sistema

Empresa familiar de 15 años, 8 empleados, producción artesanal de pan y repostería. Problema: creciente insatisfacción de clientes y alta rotación de personal.

## Diagrama de Influencias (CLD)

```
[Calidad del pan] → (+) [Satisfacción cliente] → (+) [Ventas]
      ↑                                                  |
      |                                                  ↓
[Tiempo de elaboración] ← (-) [Presión de producción] ← [Demanda]
      ↑
[Experiencia artesano] → (+) [Calidad del pan]
      ↑
[Rotación de personal] → (-) [Experiencia artesano]
      ↑
[Estrés laboral] → (+) [Rotación de personal]
      ↑
[Presión de producción] → (+) [Estrés laboral]
```

## Bucles de Retroalimentación Identificados

| Loop | Tipo | Descripción |
|------|------|-------------|
| R1: Reputación | Positivo | Calidad → ventas → más recursos → calidad |
| B1: Presión | Negativo (desestabilizador) | Ventas → presión → rotación → calidad↓ |
| B2: Artesanía | Negativo (estabilizador) | Experiencia → calidad → satisfacción |

## Palancas de Intervención

1. **Alta palanca**: Reducir jornada de panaderos (rompe B1)
2. **Media palanca**: Programa de capacitación continua (refuerza B2)
3. **Baja palanca**: Subir precios (no ataca causa raíz)

## Simulación (próxima entrega)

Implementación en Python con `pysd` o modelo manual de stocks y flows.
""",
        0, 9,  # María, Semana 10
    ),
    (
        "Recursividad Sistémica: Sistemas dentro de Sistemas dentro de Sistemas",
        "La propiedad de recursividad en la naturaleza y las organizaciones. Desde el átomo hasta el cosmos como sistema de sistemas.",
        """# Recursividad Sistémica

## El Principio de Recursividad

Beer (1979) en el **Modelo de Sistema Viable** establece que:
> "Cada sistema viable contiene y está contenido en sistemas viables."

Esta propiedad se observa en todos los niveles de la realidad:

```
COSMOS
  └── GALAXIA VÍA LÁCTEA
        └── SISTEMA SOLAR
              └── TIERRA (biosfera)
                    └── ECOSISTEMA BOGOTÁ-CUNDINAMARCA
                          └── EMPRESA XYZ
                                └── DEPARTAMENTO DE TI
                                      └── EQUIPO SCRUM
                                            └── INDIVIDUO
```

## Implicaciones para el Analista Sistémico

### Elección del Nivel de Análisis

La misma entidad puede analizarse en diferentes niveles de recursión:

| Nivel | Sistema | Entorno |
|-------|---------|---------|
| Macro | Industria automotriz | Economía global |
| Meso | Empresa Toyota | Industria automotriz |
| Micro | Planta de Medellín | Toyota global |
| Nano | Línea de ensamblaje | Planta |

### El Problema de la Incoherencia entre Niveles

Cuando S5 (política) del nivel N contradice S3 (control) del nivel N-1, el sistema pierde viabilidad. Este es el origen de muchas disfunciones organizacionales.

## Herramienta: Mapa de Recursividad

1. Identificar el sistema de interés
2. Subir 2 niveles (entorno del entorno)
3. Bajar 2 niveles (componentes de componentes)
4. Analizar coherencia entre todos los niveles

Esta visión multi-escala es el sello del **pensador sistémico maduro**.
""",
        1, 1,  # Diego, Semana 2
    ),
    (
        "TGS y Sostenibilidad: Sistemas Circulares vs Sistemas Lineales",
        "Análisis sistémico de la economía lineal vs circular desde la perspectiva de entropía, flujos y resiliencia.",
        """# Economía Circular: Una Perspectiva Sistémica

## El Problema del Sistema Lineal

El modelo económico dominante es **Extraer → Producir → Usar → Desechar**:

```
[Recursos naturales] → [Producción] → [Consumo] → [Residuos]
         ↓                   ↓              ↓           ↓
     Agotamiento          Contaminación  Satisfacción  Vertedero
```

Este sistema es **entrópico por diseño**: genera desorden (residuos) sin mecanismo de reincorporación.

## La Economía Circular como Sistema Disipativo

La economía circular cierra los bucles de retroalimentación:

```
[Recursos] → [Producción] → [Uso] → [Fin de vida]
     ↑                                    ↓
     └──────── [Reciclaje/Reparación] ←───┘
```

## Métricas Sistémicas de Circularidad

| Métrica | Definición | Ideal |
|---------|-----------|-------|
| Tasa de recuperación de materiales | Reciclado / Total usado | → 100% |
| Vida útil promedio | Tiempo hasta descarte | Máxima posible |
| Índice de circularidad | Ellen MacArthur Foundation metric | → 1.0 |

## Estudio de Caso: Philips "Pay-per-Lux"

Philips cobra por la **iluminación como servicio** (no el producto). Resultado sistémico:
- Incentivo económico para diseñar productos duraderos y reparables
- Los residuos del cliente son insumo de Philips (bucle cerrado)
- Reducción de entropía del sistema económico

## Implicaciones Políticas

La transición a economía circular requiere intervenciones sistémicas de alto nivel (S5 de Beer):
- Regulación de responsabilidad extendida del productor
- Precios que internalicen externalidades entrópicas (impuesto al carbono)
- Incentivos a la reparabilidad y durabilidad
""",
        2, 3,  # Valentina, Semana 4
    ),
    (
        "Inteligencia Artificial como Sistema Cibernético: GPT y el Loop de Retroalimentación",
        "Análisis de los Large Language Models desde la perspectiva de la cibernética de segunda orden. ¿Es la IA un sistema autopoiético?",
        """# IA como Sistema Cibernético

## Cibernética de Segunda Orden

Heinz von Foerster (1974) propuso la **cibernética de segundo orden**: el estudio de sistemas observadores, donde el observador mismo es parte del sistema observado.

Los LLMs como GPT presentan características que los acercan a esta categoría.

## Arquitectura Cibernética de un LLM

```
[Corpus de entrenamiento] → [Pre-training]
                                  ↓
                         [Modelo base] (parámetros)
                                  ↓
[Retroalimentación humana] → [RLHF] → [Modelo alineado]
                                  ↓
[Prompt del usuario] → [Inferencia] → [Respuesta]
          ↑                                ↓
          └──── [Evaluación del usuario] ←─┘
```

## ¿Es la IA Autopoiética?

Maturana y Varela (1972) definieron **autopoiesis** como la capacidad de un sistema de producirse y reproducirse a sí mismo.

| Criterio autopoiético | ¿GPT lo cumple? |
|-----------------------|-----------------|
| Red de procesos que se producen mutuamente | Parcialmente (pesos son estáticos post-training) |
| Frontera clara que distingue sistema/entorno | Sí (parámetros del modelo) |
| Auto-referencia | Sí (puede razonar sobre sí mismo) |
| Autonomía operacional | No (depende de inputs externos) |

**Conclusión**: Los LLMs actuales son sistemas **allopoiéticos** (producen algo diferente a sí mismos: texto), no autopoiéticos.

## Implicaciones para la TGS

El desarrollo de AGI (Artificial General Intelligence) probablemente requerirá cerrar el loop hacia la autopoiesis computacional. Esto abre preguntas filosóficas profundas sobre la naturaleza de los sistemas vivos y artificiales.
""",
        4, 2,  # Natalia, Semana 3
    ),
]

posts = []
for titulo, resumen, contenido, autor_idx, cat_idx in POSTS_DATA:
    autor = estudiantes[autor_idx] if autor_idx < len(estudiantes) else ADMIN
    p = Post(
        titulo=titulo,
        resumen=resumen,
        contenido_markdown=contenido,
        autor_id=autor.id,
        categoria_id=categorias[cat_idx].id,
        vistas=0,
    )
    db.add(p)
    db.flush()
    posts.append(p)

db.commit()
print(f"  ✓ {len(posts)} publicaciones creadas")

# ── 4. Archivos generados programáticamente ───────────────────
print("📎 Generando y creando archivos...")

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

def create_file_record(post: Post, content: Union[str, bytes], filename: str, ext: str) -> Archivo:
    """Guarda un archivo en disco y crea el registro en BD."""
    post_dir = os.path.join(settings.UPLOAD_DIR, str(post.id))
    os.makedirs(post_dir, exist_ok=True)
    
    unique_name = f"{uuid.uuid4().hex[:8]}_{filename}"
    file_path = os.path.join(post_dir, unique_name)
    
    data_bytes = content.encode("utf-8") if isinstance(content, str) else content
    
    with open(file_path, "wb") as f:
        f.write(data_bytes)
    
    sha256 = hashlib.sha256(data_bytes).hexdigest()
    
    archivo = Archivo(
        post_id=post.id,
        nombre_original=filename,
        ruta=file_path,
        extension=ext,
        mime_type=f"text/{ext}" if ext in ("txt", "csv", "py") else "application/pdf",
        tamano_bytes=len(data_bytes),
        hash_sha256=sha256,
    )
    db.add(archivo)
    return archivo

# Post 0: Archivo CSV y TXT
csv_content = """Subsistema,Inputs,Outputs,Retroalimentacion,Eficiencia
Transporte,Combustible;Personas,Movilidad;CO2,Semaforos,0.72
Agua,Embalses,Agua_tratada,Precio;Consumo,0.88
Residuos,Basura_domiciliaria,Reciclaje;Relleno,Precio_reciclaje,0.41
Energia,Gas_natural;Electricidad,Calor;Luz,Demanda;Precio,0.65
Informacion,Datos_ciudad,Reportes;Decisiones,Encuestas,0.79
"""
create_file_record(posts[0], csv_content, "metabolismo_bogota_datos.csv", "csv")

txt_content = """REFERENCIAS BIBLIOGRAFICAS
==========================

Bertalanffy, L. von (1968). General System Theory: Foundations, Development, Applications. 
George Braziller, New York.

Meadows, D. H. (2008). Thinking in Systems: A Primer. Chelsea Green Publishing.

Forrester, J. W. (1961). Industrial Dynamics. MIT Press, Cambridge.

Odum, H. T. (1971). Environment, Power, and Society. Wiley-Interscience, New York.

Kennedy, C., et al. (2007). The changing metabolism of cities. 
Journal of Industrial Ecology, 11(2), 43-59.
"""
create_file_record(posts[0], txt_content, "referencias_metabolismo_urbano.txt", "txt")

# Post 1: Python script
py_content = '''"""
Simulacion de retroalimentacion negativa - Termostato Digital
Autor: Diego Rios Castillo
Semana 3 - Cibernetica
"""
import time
import random

class Termostato:
    def __init__(self, target: float = 22.0, tolerance: float = 0.5):
        self.target = target
        self.tolerance = tolerance
        self.temperatura_actual = random.uniform(15, 18)
        self.calentando = False
        self.log = []
    
    def step(self, tiempo: int) -> dict:
        error = self.target - self.temperatura_actual
        
        # Decision de control (retroalimentacion negativa)
        if error > self.tolerance:
            self.calentando = True
        elif error < -self.tolerance:
            self.calentando = False
        
        # Dinamica termica simplificada
        if self.calentando:
            self.temperatura_actual += random.uniform(0.2, 0.4)
        else:
            self.temperatura_actual -= random.uniform(0.05, 0.15)
        
        estado = {
            "tiempo": tiempo,
            "temperatura": round(self.temperatura_actual, 2),
            "calentando": self.calentando,
            "error": round(error, 2),
        }
        self.log.append(estado)
        return estado
    
    def run(self, pasos: int = 50):
        print(f"Target: {self.target}C | Tolerancia: +/-{self.tolerance}C")
        print("-" * 50)
        for t in range(pasos):
            estado = self.step(t)
            status = "CALENTANDO" if estado["calentando"] else "OFF"
            print(f"t={t:3d} | T={estado['temperatura']:5.2f}C | {status} | err={estado['error']:+.2f}")

if __name__ == "__main__":
    termo = Termostato(target=22.0)
    termo.run(pasos=30)
'''
create_file_record(posts[1], py_content, "simulacion_termostato.py", "py")

# Post 4: CSV de modelo SIR
sir_csv = """tiempo,susceptibles,infectados,recuperados,R0
0,9990,10,0,6.0
10,9203,779,18,5.8
20,6142,3587,271,4.1
30,2891,5834,1275,2.3
40,1203,5441,3356,1.1
50,754,3892,5354,0.8
60,645,2234,7121,0.6
70,612,1102,8286,0.5
80,601,498,8901,0.4
90,598,213,9189,0.3
100,597,89,9314,0.3
150,597,4,9399,0.3
200,597,0,9403,0.0
"""
create_file_record(posts[4], sir_csv, "datos_modelo_sir.csv", "csv")

# Post 7: Python script inventario
inv_py = '''"""
Sistema de Inventario con Stocks y Flows
Simulacion de dinamica de sistemas - Semana 6
Autor: Sebastian Alvarado Mora
"""
import random
import csv

class SistemaInventario:
    def __init__(self, stock_inicial=1000, stock_deseado=800):
        self.stock = stock_inicial
        self.stock_deseado = stock_deseado
        self.tiempo_ajuste = 4
        self.historia = []
    
    def paso(self, demanda: float, capacidad_produccion: float = 500):
        gap = self.stock_deseado - self.stock
        orden_produccion = max(0, demanda + gap / self.tiempo_ajuste)
        produccion_real = min(orden_produccion, capacidad_produccion)
        
        self.stock = max(0, self.stock + produccion_real - demanda)
        
        self.historia.append({
            "stock": round(self.stock, 2),
            "produccion": round(produccion_real, 2),
            "demanda": round(demanda, 2),
            "gap": round(gap, 2),
        })
        return self.stock
    
    def simular(self, semanas: int = 52) -> list:
        random.seed(42)
        for _ in range(semanas):
            demanda = max(0, 400 + random.gauss(0, 50))
            self.paso(demanda)
        return self.historia
    
    def exportar_csv(self, filename: str = "resultado_inventario.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["stock", "produccion", "demanda", "gap"])
            writer.writeheader()
            writer.writerows(self.historia)
        print(f"Datos exportados a {filename}")

if __name__ == "__main__":
    sim = SistemaInventario()
    historia = sim.simular(52)
    stock_prom = sum(h["stock"] for h in historia) / len(historia)
    print(f"Stock promedio 52 semanas: {stock_prom:.0f} unidades")
    print(f"Stock minimo: {min(h['stock'] for h in historia):.0f}")
    print(f"Stock maximo: {max(h['stock'] for h in historia):.0f}")
    sim.exportar_csv()
'''
create_file_record(posts[7], inv_py, "simulador_inventario.py", "py")

db.commit()
print("  ✓ Archivos generados")

# ── 5. Comentarios (40, máx. 2 niveles) ──────────────────────
print("💬 Creando comentarios...")

COMENTARIOS_TOP = [
    # (post_idx, autor_idx, contenido)
    (0, 1, "Excelente análisis María. La aplicación del balance energético termodinámico al metabolismo urbano es muy pertinente. ¿Consideraste incluir el subsistema de movilidad peatonal y ciclista? Tienen inputs de energía humana que suelen omitirse en estos modelos."),
    (0, 2, "El cuadro comparativo de subsistemas es muy claro. Una sugerencia: agregar la columna 'Estado actual de la retroalimentación' para identificar dónde los loops están rotos o degradados. En Bogotá, el subsistema de residuos tiene retroalimentación casi inexistente."),
    (0, 3, "Relaciono este análisis con el VSM de Beer que vi en Semana 8. Los subsistemas de la ciudad corresponden a los S1 del VSM metropolitano. ¿Quién sería el S5 (política) en este caso? ¿El Concejo de Bogotá?"),
    (1, 0, "Diego, el código de Python está muy bien documentado. ¿Probaste agregar ruido a la temperatura para simular pérdidas ambientales variables? El mundo real tiene perturbaciones estocásticas que el modelo determinista no captura."),
    (1, 4, "La comparación con la homeostasis biológica es el punto más fuerte del análisis. Añadiría que el hipotálamo también integra señales periféricas (piel, órganos) además de la temperatura central, lo que añade robustez al sistema de control."),
    (2, 5, "La tabla de fidelidad por nivel jerárquico está basada en datos empíricos o es una estimación teórica? Sería valioso citar estudios de comunicación organizacional para fortalecer el argumento."),
    (2, 6, "Las estrategias negentrópicas que propones son prácticas. En mi empresa de encuestas aplicamos redundancia controlada por WhatsApp + email + llamada. El costo es alto pero la fidelidad del mensaje al beneficiario final mejora notablemente."),
    (3, 7, "El diagnóstico del S4 deficiente es muy preciso y lo he visto en muchas startups. Una herramienta concreta: el 'Future Backwards' de Dave Snowden para estructurar el tiempo de S4 sin caer en planificación rígida."),
    (3, 2, "¿Usaste el VSM de Beer en versión original o alguna adaptación? La versión de Espejo y Harnden (1989) tiene actualizaciones importantes para organizaciones de información. Podría ser más aplicable al contexto de startup tecnológica."),
    (4, 3, "El modelo SIR es elegante en su simplicidad. Para el contexto de epidemiología actual, valdría agregar la compartición E (Expuestos) para crear el modelo SEIR, que modela mejor enfermedades con período de incubación largo."),
    (5, 0, "La descripción del algoritmo de feromonas es excelente para explicar auto-organización. Una extensión interesante: los algoritmos ACO tienen un parámetro de 'evaporación de feromona' que evita la convergencia prematura. Es el equivalente a la 'pérdida de memoria' sistémica."),
    (5, 1, "Las aplicaciones en TSP y ruteo son bien conocidas. ¿Exploraste aplicaciones en diseño urbano? Hay investigaciones sobre redes de transporte que emergen de principios similares a las hormigas."),
    (6, 4, "La tabla de metodologías como caminos hacia el mismo output es una aplicación brillante de la equifinalidad. Agregaría una columna de 'Requisitos del entorno' porque la metodología óptima también depende del mercado y la cultura."),
    (7, 5, "El código de InventorySystem está muy bien estructurado. El bullwhip effect que mencionas se puede simular aumentando el tiempo_ajuste. Con tiempo_ajuste=8, las oscilaciones se amplifican dramáticamente. Es un buen experimento para mostrar en clase."),
    (8, 6, "La línea evolutiva Cibernética → ML es muy didáctica. ¿Podrías agregar la Cibernética de Segunda Orden (von Foerster) en la línea del tiempo? Es el eslabón entre la cibernética clásica y los sistemas autopoiéticos de Maturana."),
    (9, 7, "El análisis de frontera en ONGs es muy necesario. En mi trabajo voluntario con la Fundación Éxito, el debate sobre quiénes son 'parte del sistema' vs 'entorno' es constante y afecta las decisiones de governance. ¿Hay algún framework establecido para esto?"),
    (10, 0, "La distinción entre single-loop y double-loop es fundamental. Añadiría que muchas organizaciones confunden single-loop eficiente con aprendizaje real. El double-loop requiere cuestionar el marco de referencia, lo cual es amenazante para el poder establecido."),
    (11, 1, "El análisis de centralidad con NetworkX es muy práctico. Una extensión: calcular el 'flow betweenness centrality' en lugar del estándar, que es más apropiado para redes de flujo como las cadenas de suministro."),
    (13, 2, "La crítica sistémica a la HME es muy bien fundamentada. Hyman Minsky tiene una perspectiva similar desde la economía: su 'Hipótesis de Inestabilidad Financiera' describe exactamente el ciclo de retroalimentación positiva que lleva a las burbujas."),
    (16, 3, "La descripción del algoritmo RLHF como retroalimentación cibernética es muy precisa. La pregunta sobre autopoiesis es fascinante. Creo que los LLMs actuales son más parecidos a un 'organismo' en estado de hibernación: tienen estructura pero no metabolismo activo."),
]

comentarios_top = []
for post_idx, autor_idx, contenido in COMENTARIOS_TOP:
    autor = estudiantes[autor_idx] if autor_idx < len(estudiantes) else ADMIN
    c = Comentario(
        post_id=posts[post_idx].id,
        usuario_id=autor.id,
        contenido=contenido,
    )
    db.add(c)
    db.flush()
    comentarios_top.append((c, post_idx))

db.commit()

# Respuestas anidadas (nivel 2)
RESPUESTAS = [
    # (indice_comentario_padre, autor_idx, contenido)
    (0, 0, "Buena observación Diego. Tienes razón, la movilidad activa (peatonal y ciclista) es un subsistema importante que a menudo se omite por dificultad de medición. En el paper de Kennedy et al. (2007) también se señala esta limitación metodológica."),
    (1, 4, "Exacto Andrés. En el análisis extendido de la siguiente entrega incluiré un diagnóstico del estado de los loops de retroalimentación. El de residuos es el más deficiente, con una tasa de recuperación del solo 17% según el UAESP 2023."),
    (3, 1, "Sí, el ruido es importante. Puedes modelarlo con: `temperatura_actual += random.gauss(0, 0.05)` en cada step para simular turbulencias térmicas del entorno. Con ruido alto, el sistema oscila más pero sigue convergiendo si el gain del controlador es adecuado."),
    (4, 3, "Tienes razón sobre los sensores periféricos. En términos sistémicos, esto hace que el sistema de control térmico humano sea más robusto que el termostato digital, que solo mide temperatura del aire. La integración de múltiples sensores aumenta la observabilidad del sistema."),
    (5, 0, "La tabla está basada en los trabajos de Hargie & Dickson (2004) en 'Skilled Interpersonal Communication'. Los porcentajes son promedios de múltiples estudios en organizaciones de manufactura. En organizaciones de servicios, la degradación puede ser mayor."),
    (8, 5, "Correcto, el modelo SEIR es más realista. En Python: `dE = beta * S * I / N - sigma * E` donde sigma es la tasa de progresión de expuesto a infectado. Para COVID-19, el período de incubación era de ~5 días, entonces sigma = 1/5 = 0.2."),
    (9, 6, "Buena extensión Luis. Sobre la evaporación: en código es simplemente `feromonas *= (1 - evap_rate)` en cada iteración. Con evap_rate=0 tienes memoria perfecta (mínimo local garantizado), con evap_rate=1 tienes amnesia total (random walk). El óptimo suele estar entre 0.1-0.3."),
    (12, 7, "El framework de 'Soft Systems Methodology' (SSM) de Peter Checkland (1999) es exactamente lo que buscas. SSM está diseñado específicamente para sistemas 'blandos' como ONGs donde la definición del sistema es subjetiva y políticamente cargada. El concepto de 'CATWOE' (Customers, Actors, Transformation, Weltanschauung, Owners, Environment) estructura el análisis de frontera."),
    (14, 1, "Sí, el 'bullwhip effect' amplificado con tiempo_ajuste=8 es un experimento clásico de Jay Forrester. Si graficas el ratio Varianza(Orden)/Varianza(Demanda) a lo largo de la cadena, verás que se amplifica en cada eslabón. Con tiempo_ajuste=2 el sistema es casi perfecto pero inviable en la práctica."),
    (15, 4, "La Cibernética de Segunda Orden de von Foerster es clave. La incluiré en la próxima versión. Un dato: von Foerster era vienés como Bertalanffy, y ambos participaron en las Conferencias Macy (1946-1953), que son el origen de toda esta tradición intelectual."),
]

for parent_idx, autor_idx, contenido in RESPUESTAS:
    if parent_idx < len(comentarios_top):
        parent_comentario, post_idx = comentarios_top[parent_idx]
        autor = estudiantes[autor_idx] if autor_idx < len(estudiantes) else ADMIN
        resp = Comentario(
            post_id=parent_comentario.post_id,
            usuario_id=autor.id,
            padre_id=parent_comentario.id,
            contenido=contenido,
        )
        db.add(resp)

db.commit()
total_comments = db.query(Comentario).count()
print(f"  ✓ {total_comments} comentarios creados")

# ── Resumen final ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("✅ SEED COMPLETADO")
print("=" * 50)
print(f"  👤 Usuarios:      {db.query(User).count()}")
print(f"  📂 Categorías:    {db.query(Categoria).count()}")
print(f"  📝 Publicaciones: {db.query(Post).count()}")
print(f"  📎 Archivos:      {db.query(Archivo).count()}")
print(f"  💬 Comentarios:   {db.query(Comentario).count()}")
print()
print("🔑 Credenciales del admin:")
print(f"  Código:     61035728")
print(f"  Contraseña: 271714")
print()
print("🔑 Credenciales de estudiantes:")
print(f"  Contraseña común: Tgs2026!")
print("=" * 50)

db.close()
