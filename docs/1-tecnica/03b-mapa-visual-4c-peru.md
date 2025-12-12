# Mapa Visual - 4C Perú

**Versión**: 1.0
**Fecha**: 2025-12-07
**Propósito**: Referencia rápida de estructura, rutas y componentes

---

## MAPA DE SITIO

```
                             4C PERÚ
                                │
                     ┌──────────┴──────────┐
                     │                     │
                   Login              Públicas
                  (/)                  Info, etc.
                     │
         ┌───────────┼───────────┐
         │                       │
      EMPRESA              COORDINADOR
    /empresa/            /coordinador/
         │                       │
    ┌────┴─────────────┬─────┐   ├─ Dashboard
    │                  │     │   ├─ Ciclo Actual
    │                  │     │   │  ├─ Pendientes
    │                  │     │   │  ├─ Por Validar
 Ciclo             Resultados  │   │  └─ Validados
Actual            & Reportes   │   │
  │                  │         │   ├─ Hoja de Ruta
  ├─ Descargar    ├─ Actual    │   │  ├─ Dashboard
  ├─ Mi Envío     ├─ Histórico│   │  └─ Comparativa 2030
  └─ Comentarios  └─ Benchmark│   │
                                │   ├─ Análisis
                                │   │  ├─ Benchmarking
                                │   │  └─ Tendencias
                                │   │
                                │   └─ Reportes
                                │      ├─ Ciclo Anual
                                │      ├─ Ministerio
                                │      └─ Exportar FICEM
```

---

## VISTA EMPRESA (Flujo Anual)

```
INICIO DE AÑO / CICLO ABIERTO
          │
          ▼
    [Dashboard Empresa]
    Estado: BORRADOR
          │
          ├─────────────────────┐
          │                     │
          ▼                     ▼
    [Descargar              [Mi Envío]
     Plantilla]           Estado actual
          │                     │
          ▼                     │
    Excel local             ┌───┴─────────────┬─────┐
   Completa datos        BORRADOR          ENVIADO │
          │                  │                     │
          └──────────────┐   │            ┌────────┤
                         │   │            │        │
                         ▼   ▼            ▼        ▼
                    [Cargar Excel]   Esperar    [Comentarios]
                         │           Revisión   ← VALIDANDO
                         │              │           │
                         ▼              │        ┌──┴──────┐
                    ENVIADO             │        │         │
                         │              │    Aprobado  Rechazado
                         │              │        │         │
                         └──────────────┘        │         │
                                │               │     Corregir &
                                ▼               │      Reenviar
                         [Ver Comentarios]  ┌───┴─┐
                                │           │     │
                                └───────────┘     │
                                      │           │
                                      └───────────┘
                                            │
                                            ▼
                                    [Resultado Final]
                            FICEM publica banda GCCA
                                            │
                                    ┌───────┴───────┐
                                    │               │
                            Ver Huella      Ver Benchmark
                         & Banda GCCA       (anónimo)
                                    │
                                    ▼
                              [Reportes]
                           Descargar PDF/Excel
```

---

## VISTA COORDINADOR (Flujo de Validación)

```
CICLO ABIERTO
      │
      ▼
[Dashboard]
Métricas rápidas + Hoja de Ruta
      │
      ├──────────────────────────┬───────────────────┐
      │                          │                   │
      ▼                          ▼                   ▼
[Ciclo Actual]        [Hoja de Ruta 2050]    [Análisis]
Revisar Envíos        Dashboard Progreso      Benchmarking
      │               Comparativa 2030        Tendencias
      │               Proyección 2050              │
      │                          │                │
      ├─ Pendientes              │         Consultas
      ├─ Por Validar             │         & Gráficos
      └─ Validados               │
           │                     │
           ▼                     ▼
    ┌──────────────┐      [Alertas & Análisis]
    │ Revisar Envío│      - Gap 2030
    │ - Validar    │      - Empresas rezagadas
    │ - Comentar   │      - Recomendaciones
    └──────────────┘
           │
      ┌────┴────┐
      │         │
   Aprobar   Rechazar
      │         │
      ▼         ▼
   APROBADO  RECHAZADO
      │         │
      │     [Empresa recibe
      │      feedback, corrige
      │      y reenvía]
      │         │
      └────┬────┘
           │
      ┌────┴──────┐
      │            │
    Envío a    Espera
  FICEM Core  siguiente
      │       ciclo
      ▼
FICEM calcula
central &
publica
      │
      ▼
Ver resultado en
[Validados]
```

---

## ESTRUCTURA DE URLS

### EMPRESA

```
/empresa/dashboard
  └─ Inicio, estado ciclo, acciones rápidas

/empresa/ciclo-actual/descargar
  └─ Seleccionar tipo de producto + descargar Excel

/empresa/ciclo-actual/mi-envio
  └─ Gestionar envío (borrador → enviado → validación)

/empresa/ciclo-actual/comentarios
  └─ Ver feedback del coordinador

/empresa/resultados/actual
  └─ Huella final + banda GCCA (si publicado)

/empresa/resultados/historico
  └─ Evolución anual de huellas

/empresa/resultados/benchmarking
  └─ Comparación anónima vs industria Perú

/empresa/reportes/individual
  └─ Generar reporte PDF/Excel
```

### COORDINADOR

```
/coordinador/dashboard
  └─ KPIs del ciclo + indicadores Hoja de Ruta

/coordinador/ciclo-actual/pendientes
  └─ Tabla de envíos (ENVIADO, VALIDANDO, RECHAZADO)

/coordinador/ciclo-actual/por-validar
  └─ Filtro rápido (ENVIADO + RECHAZADO)

/coordinador/ciclo-actual/validados
  └─ Historial de aprobados + estado en FICEM

/coordinador/hoja-ruta/dashboard
  └─ Speedometer 2025 vs 2030, gráficos, bandas GCCA

/coordinador/hoja-ruta/comparativa-2030
  └─ Análisis gap, velocidad de reducción requerida

/coordinador/analisis/benchmarking
  └─ Ranking de empresas Perú (anónimo)

/coordinador/analisis/tendencias
  └─ Evolución 2021-2025, percentiles

/coordinador/reportes/ciclo-anual
  └─ Reporte oficial ciclo 2025 (PDF/Excel)

/coordinador/reportes/ministerio
  └─ Reporte formal para PRODUCE

/coordinador/reportes/exportar-ficem
  └─ Exportar datos consolidados (CSV/JSON/Excel)
```

---

## COMPONENTES REUTILIZABLES

```
components/
│
├── auth/
│   ├─ LoginForm
│   │   └─ Email + password, envía a /api/auth/login
│   │
│   └─ ProtectedRoute
│       └─ Verifica JWT, redirige a login si no existe
│
├── layouts/
│   ├─ NavbarEmpresa
│   │   └─ Logo, menu empresa, tema, logout
│   │
│   ├─ NavbarCoordinador
│   │   └─ Logo, menu coordinador, tema, logout
│   │
│   ├─ Footer
│   │   └─ Links legales, versión
│   │
│   └─ Sidebar (futuro)
│       └─ Menú lateral colapsible
│
├── shared/
│   ├─ ThemeToggle
│   │   └─ Light/Dark theme switcher
│   │
│   ├─ LoadingSpinner
│   │   └─ Spinner animado
│   │
│   ├─ ErrorAlert
│   │   └─ Alert con icono de error
│   │
│   ├─ SuccessAlert
│   │   └─ Alert con icono de success
│   │
│   └─ StatusBadge
│       └─ Badge para estados (ENVIADO, APROBADO, etc.)
│
├── charts/ (usando Plotly o Chart.js)
│   ├─ HuellaChart
│   │   └─ Línea temporal de huella
│   │
│   ├─ BandaGccaChart
│   │   └─ Distribución de bandas GCCA
│   │
│   ├─ BenchmarkingChart
│   │   └─ Box plot o histograma + tu posición
│   │
│   └─ ProgresoHojadeRutaChart
│       └─ Speedometer 2025 vs 2030 vs 2050
│
└── forms/
    ├─ UploadExcelForm
    │   └─ Input file, validación local
    │
    ├─ ValidacionLocalForm
    │   └─ Mostrar errores/advertencias
    │
    └─ ComentariosForm
        └─ Textarea para coordinador + botones Aprobar/Rechazar
```

---

## FLUJO DE DATOS (DATOS)

```
EMPRESA CARGA DATOS
         │
         ▼
   POST /api/envios
   (con FormData del Excel)
         │
         ▼
FICEM-CORE parsea
   │ Validación estructura
   │ Almacena archivo binario
   │ Crea registro de envío
   │
   └─ Retorna { envio_id, estado: "BORRADOR" }
         │
         ▼
EMPRESA VE DATOS (preview)
   GET /api/envios/{id}
         │
         ▼
EMPRESA ENVÍA
   POST /api/envios/{id}/enviar
   └─ Estado → ENVIADO
   └─ Notificación a coordinadores
         │
         ▼
COORDINADOR REVISA
   GET /api/envios?estado=ENVIADO
   POST /api/envios/{id}/comentarios
         │
      ┌──┴──┐
      │     │
   APRUEBA  RECHAZA
      │        │
      ▼        │
   POST /api/  │
   envios/{id}/│
   aprobar    │
      │        │
      ▼        ▼
   APROBADO  RECHAZADO
      │        └─ Vuelve a BORRADOR
      │
      ▼
FICEM-CORE CALCULA
   Ejecuta motor A1-A3
   Asigna banda GCCA
   Calcula benchmarking
         │
         ▼
FICEM-CORE PUBLICA
   Estado → PUBLICADO
         │
         ▼
EMPRESA / COORDINADOR VEN
   GET /api/resultados/{id}
   └─ Huella + banda + comparativas
```

---

## MATRIZ DE PERMISOS

```
                     Empresa    Empresa    Empresa      Coordinador   Oficial
                     Editor     Supervisor Observador   (ASOCEM)      Gobierno
                     ─────────  ────────── ──────────   ────────────  ─────────
Ver Dashboard         ✅         ✅         ✅            ✅            ✅
Descargar Plantilla   ✅         ✅         ─             ─             ─
Cargar Excel          ✅         ─          ─             ─             ─
Validar Local         ✅         ─          ─             ─             ─
Enviar                ✅         ✅         ─             ─             ─
Ver Comentarios       ✅         ✅         ✅            ✅            ✅
Ver Resultado         ✅         ✅         ✅            ✅            ✅
Ver Benchmark         ✅         ✅         ✅            ✅            ✅
Descargar Reporte     ✅         ✅         ✅            ✅            ✅

Revisar Envíos        ─          ─          ─             ✅            ✅
Comentar Envío        ─          ─          ─             ✅            ✅
Aprobar Envío         ─          ─          ─             ✅            ✅
Rechazar Envío        ─          ─          ─             ✅            ✅
Ver Hoja de Ruta      ─          ─          ─             ✅            ✅
Ver Análisis          ─          ─          ─             ✅            ✅
Generar Reportes      ─          ─          ─             ✅            ✅
Exportar a FICEM      ─          ─          ─             ─             ✅
```

---

## ESTADOS Y TRANSICIONES

```
EMPRESA SUBMISSION STATES:

                    CREAR ENVÍO
                         │
                         ▼
                    ┌─────────┐
                    │ BORRADOR │  ◄─── Empresa puede modificar
                    └────┬────┘
                         │
                 POST /envios/{id}/enviar
                         │
                         ▼
                    ┌─────────┐
                    │ ENVIADO  │  ◄─── En cola para coordinador
                    └────┬────┘
                         │
                 GET /envios/{id}/comentarios (polling)
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
    ┌──────────┐                    ┌──────────┐
    │VALIDANDO │◄──────────────────►│RECHAZADO │
    │(revisión)│  POST .../rechazar │(solicita │
    └────┬─────┘                    │corrección)
         │                           └──────┬──┘
         │                                  │
         │ POST .../aprobar          Empresa reenvía
         │                                  │
         ▼                                  │
    ┌──────────┐                           │
    │APROBADO  │◄──────────────────────────┘
    │(enviado  │
    │a FICEM)  │
    └────┬─────┘
         │
    FICEM executa
    cálculos centrales
         │
         ▼
    ┌──────────┐
    │CALCULANDO│
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │PUBLICADO │  ◄─── Resultados finales disponibles
    └──────────┘

LEYENDA: ◄─── Permite volver atrás en ciertos casos
```

---

## TIMELINE DEL AÑO

```
ENERO 2025                CICLO ABIERTO
    │
    ├─ Coordinador publica plazo: 31 de marzo
    │
    ├─ Empresas descargan plantilla
    │
    ├─ FEBRERO-MARZO
    │  └─ Empresas cargan datos (local calculation)
    │
    └─ 31 de MARZO: DEADLINE ENVÍO
        │
        ├─ ABRIL
        │  └─ Coordinador revisa + comenta
        │     Empresas corrigen si es necesario
        │
        └─ 30 de ABRIL: DEADLINE APROBACIÓN
            │
            ├─ MAYO
            │  └─ FICEM ejecuta cálculos centrales
            │
            └─ 31 de MAYO: PUBLICACIÓN
                │
                ├─ JUNIO
                │  └─ Empresas y coordinadores ven resultados
                │
                └─ Fin de ciclo 2025
```

---

**Última actualización**: 2025-12-07
**Próximo paso**: Implementar páginas comenzando con Login y Dashboard Empresa
