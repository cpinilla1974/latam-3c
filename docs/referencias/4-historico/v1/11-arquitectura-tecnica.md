# Arquitectura Técnica - LATAM-3C

## ETAPA 1

### Base de Datos
- SQLite para ambas aplicaciones

### Aplicaciones

**App Formularios**
- Streamlit con links únicos
- SQLite para tokens temporales

**App Principal FICEM (v1/)**
- Streamlit para operador único
- SQLite para datos empresas
- Core de lógica separado de UI

## ETAPA 2

### Base de Datos
- PostgreSQL

### Aplicaciones

**Backend API**
- FastAPI
- Autenticación por empresa

**Frontend Portal**
- React o Vue