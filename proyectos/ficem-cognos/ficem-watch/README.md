# FICEM Watch - Asistente Ejecutivo de Posicionamiento

## Objetivo

Herramienta de soporte para altos directivos de FICEM que proporciona en minutos:
- Respuestas **informadas y alineadas con la estrategia comunicacional** frente a noticias del día
- Historial de posicionamiento de FICEM sobre temas específicos
- Datos duros para responder interpelaciones
- Reportes ejecutivos que reflejan la voz institucional de FICEM

## Casos de Uso Día a Día

### 1. Respuesta Rápida a Noticias
**Pregunta**: "Salió una noticia sobre impuestos al carbono en Colombia, ¿qué debemos decir?"

| Capa | Aporte |
|------|--------|
| **Conocimiento** | Posición histórica de FICEM + contexto regional + datos relevantes |
| **Estrategia** | Formulación de respuesta con tono institucional + alineación con mensajes clave |

**Output**: Respuesta sugerida lista para usar, con citas verificables

### 2. Consulta de Historial
**Pregunta**: "¿Qué hemos dicho sobre factores clínker en los últimos 3 años?"

| Capa | Aporte |
|------|--------|
| **Conocimiento** | Línea de tiempo de posiciones + documentos clave + evolución |
| **Estrategia** | Identificación de cambios de postura + coherencia con lineamientos actuales |

**Output**: Resumen ejecutivo de evolución del discurso + alertas si hay inconsistencias

### 3. Datos Duros para Interpelaciones
**Pregunta**: "Gobierno pregunta cuántas empresas cumplen con X norma"

| Capa | Aporte |
|------|--------|
| **Conocimiento** | Estadísticas precisas + fuentes verificables + comparación regional |
| **Estrategia** | Contexto para presentar los datos (enfatizar logros, reconocer desafíos) |

**Output**: Datos con narrativa alineada a posicionamiento FICEM

### 4. Reporte Ejecutivo Urgente
**Pregunta**: "Necesito briefing completo sobre co-procesamiento para reunión en 1 hora"

| Capa | Aporte |
|------|--------|
| **Conocimiento** | Datos técnicos + posiciones históricas + referencias documentales |
| **Estrategia** | Estructura y tono según audiencia de la reunión (gobierno/industria/medios) |

**Output**: Reporte ejecutivo de 2 páginas con voz institucional FICEM + datos + referencias

### 5. Tema Sensible (Nuevo)
**Pregunta**: "¿Qué responder sobre el caso de contaminación en planta X?"

| Capa | Aporte |
|------|--------|
| **Conocimiento** | Información disponible sobre el caso + contexto |
| **Estrategia** | **ALERTA**: Tema sensible - requiere validación humana antes de responder |

**Output**: Borrador de respuesta + flag de revisión obligatoria + sugerencia de quién debe aprobar

## Inputs

### Para Capa 1 (Conocimiento)

**Documentos FICEM**:
- Redes Sociales
- 30 Reportes Sostenibilidad
- 41 Buenas Prácticas FICEM
- 5 Congresos FICEM
- ~100 Docs FICEM internos

**Organizaciones externas**: GCCA, FIP, IEA, CMBUREAU (14 institutos Canadá)

**Multilaterales**: BID, IFC, CAF, ONU Perú, Gobierno Peruano (CNCND, OICHA)

### Para Capa 2 (Estrategia)

**Lineamientos Comunicacionales FICEM** (documento a generar):
- Tono institucional
- Mensajes clave / pilares comunicacionales
- Adaptación por público objetivo
- Temas sensibles y protocolos de aprobación
- Ejemplos de referencia (qué imitar, qué evitar)

## Outputs

### Inmediatos (segundos)
- **Respuesta sugerida** alineada con estrategia comunicacional + citas verificables
- **Historial de posicionamiento** con análisis de coherencia
- **Datos duros** con narrativa contextualizada según lineamientos FICEM
- **Alertas** si el tema es sensible o requiere validación humana

### Ejecutivos (minutos)
- **Reporte completo** con voz institucional FICEM (2-3 páginas)
- **Referencias cruzadas** a documentos FICEM
- **Comparación** con posiciones de organizaciones internacionales
- **Adaptación por audiencia** según público objetivo indicado

## Interface

**Ultra-Simple** para directivos no técnicos:
- Chat conversacional (tipo ChatGPT)
- Búsqueda por voz opcional
- Exportación directa a PDF/Word
- Acceso móvil (responsive)

## Arquitectura de Dos Capas

### Capa 1: Conocimiento (Qué sabe FICEM)
- **RAG** (búsqueda semántica en historial FICEM)
- **Vector DB** (ChromaDB - memoria institucional)
- Los ~180 documentos, datos, posiciones históricas

### Capa 2: Estrategia Comunicacional (Cómo comunica FICEM)
El sistema NO solo busca información, sino que **filtra y formula respuestas** según:

- **Tono institucional**: Formal, técnico, propositivo (no reactivo/defensivo)
- **Mensajes clave**: Pilares comunicacionales que FICEM quiere reforzar
- **Públicos objetivo**: Adaptar mensaje según audiencia (gobierno, industria, medios, sociedad)
- **Temas sensibles**: Temas que requieren validación humana antes de responder
- **Posicionamiento diferencial**: Qué distingue a FICEM de otras voces del sector

**Fuente**: Lineamientos de comunicación FICEM (ver sección "Levantamiento de Estrategia Comunicacional")

### Flujo de Generación de Respuesta

```
Pregunta del usuario
        ↓
[Capa 1: Conocimiento]
   Busca información relevante en base de datos
        ↓
[Capa 2: Estrategia]
   Filtra y formula según lineamientos comunicacionales
        ↓
Respuesta alineada con estrategia FICEM + citas verificables
```

## Levantamiento de Estrategia Comunicacional

**Prerequisito crítico**: Antes de desarrollar el sistema, se debe sistematizar la estrategia comunicacional de FICEM en un documento estructurado que alimente la Capa 2.

### Metodología de Levantamiento

#### Paso 1: Identificación de Fuentes
Ubicar dónde está la estrategia comunicacional actualmente (dispersa o parcial):
- Documentos de planificación estratégica FICEM
- Manuales de marca/identidad
- Lineamientos internos de vocería
- Comunicados oficiales anteriores (para inferir patrones)
- Entrevistas con directivos clave

#### Paso 2: Entrevistas Estructuradas
Sesiones con responsables de comunicación FICEM para extraer:

| Elemento | Preguntas Guía |
|----------|----------------|
| **Tono institucional** | ¿Cómo debe sonar FICEM? ¿Qué adjetivos lo describen? ¿Qué evitar? |
| **Mensajes clave** | ¿Cuáles son los 3-5 pilares que FICEM siempre quiere reforzar? |
| **Públicos objetivo** | ¿Quiénes son las audiencias principales? ¿Cómo varía el mensaje para cada una? |
| **Temas sensibles** | ¿Qué temas requieren aprobación antes de responder? ¿Hay líneas rojas? |
| **Posicionamiento** | ¿Qué distingue la voz de FICEM de otras organizaciones del sector? |
| **Ejemplos** | ¿Comunicados que representan bien el estilo FICEM? ¿Ejemplos de lo que NO hacer? |

#### Paso 3: Documento de Lineamientos
Consolidar en documento estructurado con formato específico para alimentar el System Prompt:

```
LINEAMIENTOS COMUNICACIONALES FICEM
===================================

1. TONO INSTITUCIONAL
   - Características: [lista]
   - Evitar: [lista]

2. MENSAJES CLAVE
   - Pilar 1: [descripción]
   - Pilar 2: [descripción]
   ...

3. PÚBLICOS Y ADAPTACIÓN
   - Gobierno: [cómo adaptar]
   - Industria: [cómo adaptar]
   - Medios: [cómo adaptar]
   - Sociedad civil: [cómo adaptar]

4. TEMAS SENSIBLES (requieren validación humana)
   - [tema 1]: por qué es sensible
   - [tema 2]: por qué es sensible

5. EJEMPLOS DE REFERENCIA
   - Buen ejemplo: [link/cita]
   - Contraejemplo: [qué evitar]
```

#### Paso 4: Validación
- Revisión del documento por directivos FICEM
- Aprobación formal antes de implementar en el sistema

### Responsable
Este levantamiento debe ser realizado por FICEM (área de comunicaciones) con apoyo metodológico del equipo de desarrollo.

### Entregable
Documento `lineamientos-comunicacionales-ficem.md` que se incorpora al System Prompt del LLM.

---

## Tecnología

- **RAG** (búsqueda semántica en historial FICEM)
- **Vector DB** (ChromaDB - memoria institucional)
- **LLM** (Claude/GPT - generación de respuestas)
- **Framework** (LangChain - orquestación)
- **System Prompt Estratégico** (lineamientos comunicacionales como instrucciones base del LLM)

## Riesgos Identificados

### Alto Impacto
1. **Alucinaciones del LLM**: Respuesta incorrecta en tema crítico
   - Mitigación: Validación humana antes de uso público + citas verificables

2. **Datos desactualizados**: Posición obsoleta frente a cambio reciente
   - Mitigación: Timestamp visible + alerta de antigüedad de fuente

3. **Acceso no autorizado**: Información sensible FICEM expuesta
   - Mitigación: Autenticación robusta + logs de auditoría

4. **Desalineación con estrategia comunicacional**: Respuesta correcta en contenido pero con tono/enfoque incorrecto
   - Mitigación: Lineamientos comunicacionales formalizados + revisión periódica del System Prompt + feedback loop con usuarios

5. **Lineamientos desactualizados**: Estrategia comunicacional cambió pero el sistema no se actualizó
   - Mitigación: Proceso de actualización definido + responsable asignado + versionamiento de lineamientos

### Medio Impacto
4. **Dependencia de LLM externo**: Caída de servicio Claude/OpenAI
   - Mitigación: Fallback a modelo local (menor calidad pero disponible)

5. **Costo operativo**: Consultas frecuentes pueden ser costosas
   - Mitigación: Cache de respuestas similares + tier gratuito limitado

### Bajo Impacto
6. **Curva de aprendizaje**: Directivos no adoptan la herramienta
   - Mitigación: Interface ultra-simple + capacitación breve

## Estado

Fase: **Conceptualización**
Usuarios objetivo: **Directivos FICEM** (5-10 usuarios iniciales)

## Documentación Adicional

- [Análisis de Mercado y Buenas Prácticas](analisis-mercado-buenas-practicas.md) - Benchmarking con sistemas similares, riesgos identificados