# Sistema de Captura de Datos - LATAM-3C

## REQUERIMIENTO: Formularios Dinámicos

### Problema identificado
Los formularios Excel actuales contienen muchos campos irrelevantes según el tipo de planta:
- Plantas integradas vs molienda necesitan campos diferentes
- Autogeneración eléctrica activa/desactiva secciones
- Concreto con/sin canteras propias cambia estructura

### Requerimiento
Sistema de cuestionario inicial que genere Excel personalizado con solo los campos relevantes para cada empresa según su configuración específica.

### Flujo básico propuesto
1. Cuestionario inicial determina tipo de operación
2. Genera Excel con solo hojas y campos aplicables
3. Excel se completa offline y circula internamente
4. Excel final se reporta a FICEM

## PROPUESTAS DE IMPLEMENTACIÓN

### V1: Link único + Streamlit
- Email con link único (token temporal)
- Formulario simple Streamlit sin autenticación
- Genera y descarga Excel personalizado
- Datos guardados temporalmente para sesión

### V2: Portal empresarial
- Frontend React/Vue + Backend FastAPI
- Autenticación por empresa
- Portal completo con dashboard
- Flujo digital completo sin Excel