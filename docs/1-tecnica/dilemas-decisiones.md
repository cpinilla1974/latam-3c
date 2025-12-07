# Dilemas y Decisiones - LATAM-3C

## Propósito
Documentar decisiones de diseño que podrían cambiar según evolucione el proyecto. Las decisiones iniciales permiten construir el prototipo, pero no son definitivas.

## DILEMAS ACTIVOS

### 1. Nivel de Agregación de Datos
**Pregunta**: ¿Los datos serán agregados solo a nivel de compañía o también a nivel de planta?

**Opciones**:
- A) Solo compañía (más simple, menos detalle)
- B) Compañía y planta (más complejo, más trazabilidad)
- C) Híbrido: algunos datos por planta, otros por compañía

**Decisión inicial para prototipo**: **Opción A - Solo compañía**
- Simplifica el modelo
- Reduce complejidad de carga
- Suficiente para consolidación regional

**Revisitar cuando**: 
- Empresas requieran comparar entre sus plantas
- Se necesite vincular con datos GCCA por planta

---

### 2. Pseudonimización de Datos
**Pregunta**: ¿Los datos de las compañías se guardarán pseudonimizados?

**Opciones**:
- A) Totalmente pseudonimizados (sin mapeo reversible)
- B) Pseudonimizados con mapeo reversible (tabla separada con acceso restringido)
- C) Nominados pero con estricto control de acceso

**Decisión inicial para prototipo**: **Opción A - Totalmente pseudonimizados**
- Máxima privacidad
- Evita conflictos de confidencialidad
- Simplifica aspectos legales

**Revisitar cuando**:
- Se requiera auditoría nominada
- Empresas soliciten benchmarking directo
- Reguladores requieran identificación

---

### 3. Gestión de Usuarios
**Pregunta**: ¿Cómo manejar autenticación y autorización?

**Opciones**:
- A) Sistema simple con códigos de acceso
- B) Integración con Django auth
- C) SSO empresarial (OAuth, SAML)

**Decisión inicial para prototipo**: **Opción A - Códigos de acceso**

**Revisitar cuando**: Se defina el stack definitivo

---

### 4. Almacenamiento de Históricos
**Pregunta**: ¿Qué pasa con datos anteriores cuando se re-carga?

**Opciones**:
- A) Sobrescribir (solo último válido)
- B) Versionado completo (todo se guarda)
- C) Snapshot anual (una versión final por año)

**Decisión inicial para prototipo**: **Opción B - Versionado**

**Revisitar cuando**: Volumen de datos sea problema

---

### 5. Cálculos CO2
**Pregunta**: ¿Los cálculos se ejecutan on-demand o batch?

**Opciones**:
- A) On-demand al cargar
- B) Batch nocturno
- C) Trigger manual

**Decisión inicial para prototipo**: **Opción A - On-demand**

**Revisitar cuando**: Tiempo de cálculo sea excesivo

---

### 6. Factores de Emisión
**Pregunta**: ¿Factores globales o personalizados por empresa?

**Opciones**:
- A) Globales por país
- B) Personalizables por empresa
- C) Mixto con valores por defecto

**Decisión inicial para prototipo**: **Opción A - Globales por país**

**Revisitar cuando**: Empresas tengan factores certificados propios

---

### 7. Fuente de Datos de Combustibles para Clinker
**Pregunta**: ¿De dónde tomar los datos de consumo de combustibles para clinker?

**Opciones**:
- A) De archivos GCCA por planta (datos operativos detallados)
- B) Solicitar en Excel por cada tipo de clinker (más granular por producto)
- C) Ambos, con validación cruzada

**Decisión inicial para prototipo**: **Opción A - De archivos GCCA**
- Simplifica el Excel de entrada
- Evita duplicación de datos
- GCCA ya tiene estos datos validados

**Revisitar cuando**:
- Empresas produzcan múltiples tipos de clinker con consumos muy diferentes
- Se requiera trazabilidad específica por tipo de clinker
- No todas las empresas tengan archivos GCCA completos

**Implicaciones**:
- Los datasets de clinker tomarán combustibles del dataset GCCA de su planta
- El Excel solo pedirá producción y materias primas por clinker
- Necesitamos lógica para distribuir combustibles entre tipos de clinker

---

## DECISIONES TOMADAS

### Motor de Base de Datos
**Decisión**: SQLite para prototipo, PostgreSQL para producción
**Razón**: Simplicidad inicial, escalabilidad futura
**Estado**: CONFIRMADO

### Frecuencia de Reporte
**Decisión**: Anual
**Razón**: Requerimiento establecido
**Estado**: CONFIRMADO

### Formato de Entrada
**Decisión**: Excel con estructura definida
**Razón**: Familiaridad de usuarios
**Estado**: CONFIRMADO

---

## PROCESO DE REVISIÓN

Las decisiones se revisarán:
1. Al finalizar el prototipo
2. Después de pruebas con usuarios
3. Antes de pasar a producción

Cada cambio debe documentarse con:
- Fecha
- Razón del cambio
- Impacto en el sistema
- Migración requerida