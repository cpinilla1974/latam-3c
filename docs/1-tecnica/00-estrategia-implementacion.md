# Estrategia de Implementación - Calculadora País 4C

## ETAPAS DEL PROYECTO

### ETAPA 1: Operador Centralizado (305 HH / $25,010 USD)
**Duración**: 26 semanas (Oct 2025 - Mar 2026)
**Modelo operativo**: FICEM procesa todos los datos
**Usuarios**: 1 operador FICEM + empresas enviando archivos
**Tecnología**:
- App principal: Streamlit + Python + SQLite
- Stack: Pandas, SQLAlchemy, openpyxl
**Alcance**:
- Generador de templates Excel personalizados
- Upgrade de 2 calculadoras corporativas 3C con exportación automática
- Sistema de validación multinivel
- Motor de cálculos GCCA (A1-A3)
- Clasificación en bandas GCCA
- Base de datos de benchmarking anónimo
- Reportes individuales y dashboard consolidado
- 3 empresas piloto para validación

### ETAPA 2: Autoservicio Empresas (Futura)
**Modelo operativo**: Cada empresa gestiona sus datos
**Usuarios**: 50-100 empresas
**Tecnología**: React/Vue + FastAPI + PostgreSQL + Hosting cloud
**Alcance**:
- Portal por empresa con autenticación
- Formularios web dinámicos (eliminación de Excel)
- Dashboard interactivo en tiempo real
- API REST para integraciones
- Gestión multi-año
- Infraestructura de hosting escalable

## FASES DE ETAPA 1

### Fase 1: Excel, Validación e Integración Calculadoras (80 HH)
**Semanas 1-8 | Entrega: 26 Nov 2025**
- Generador dinámico de templates Excel
- Upgrade completo de 2 calculadoras corporativas 3C
- Módulo de exportación automática
- Validación con 3 empresas piloto
- Definiciones técnicas acordadas
- Formato Excel definitivo estandarizado

### Fase 2: Sistema Principal y Cálculos (125 HH)
**Semanas 9-15 | Entrega: 31 Ene 2026**
- Base de datos SQLite con modelos completos
- Motor de cálculos cemento (A1: Clinker, A2: Cemento)
- Motor de cálculos concreto (A3)
- Sistema de clasificación GCCA
- Interfaz web para operador FICEM
- Validación con datos reales de 5+ empresas

### Fase 3: Interfaz y Reportes (65 HH)
**Semanas 16-20 | Entrega: 25 Feb 2026**
- Dashboard principal con métricas clave
- Sistema de carga masiva de archivos Excel
- Reportes individuales por empresa
- Reportes comparativos simplificados
- Sistema de exportación de resultados

### Fase 4: Retroalimentación y Mejoras (25 HH)
**Semanas 21-26 | Entrega: 31 Mar 2026**
- Validación extendida con 3+ empresas
- Optimizaciones según feedback
- Documentación completa
- Transferencia de conocimiento

### Base de Datos de Benchmarking (35 HH - Continuo)
**Semanas 10-26 | Paralelo a Fases 2-4**
- Diseño e implementación de repositorio
- Sistema de agregación anónima por país/región
- Visualizaciones comparativas (curvas CO2 vs resistencia)
- Integración en reportes empresariales

## CRITERIO DE TRANSICIÓN
Pasar a Etapa 2 cuando:
- Proceso validado y estable en Etapa 1
- Propuesta técnico-económica detallada de Etapa 2
- Presupuesto aprobado para escalamiento