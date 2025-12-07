# CAMBIO DE ARQUITECTURA - 2025-12-06

## Resumen Ejecutivo

**Decisión**: Pasar de arquitectura monolítica (v1) a arquitectura de dos aplicaciones separadas

**Aplicaciones**:
1. **FICEM CORE**: Backend centralizado con motor de cálculos, validaciones y BD
2. **4C PERÚ**: Frontend específico para Perú con dashboards y reportes

**Beneficio principal**: Reutilización de lógica para múltiples países (Colombia, Ecuador, etc.)

---

## Documentación Relacionada

### Para entender la decisión:
- 📌 `docs/3-sesiones/sesion_2025-12-06.md` - Registro de decisiones y cambios

### Para implementar:
- 📋 `docs/1-tecnica/00-plan-etapa-1-dos-apps.md` - Plan de implementación actual
- 🔧 `docs/1-tecnica/01-arquitectura-ficem-4c.md` - Especificación técnica detallada

### Para ver cómo era antes:
- 📚 `docs/4-historico/v1/13-plan-etapa-1-HASTA_2025-12-06.md` - Plan anterior (monolito)

---

## Cambios Inmediatos

✅ Limpieza de páginas dummy (11 archivos eliminados, 4 duplicados removidos)
✅ Menú organizado en 8 secciones con 27 páginas funcionales
✅ Título "4C Perú" visible en sidebar de toda la aplicación

---

## Próximos Pasos

1. Separar código v1 en carpetas `ficem-core/` y `4c-peru/`
2. Implementar motor de cálculos A1-A3 en FICEM Core
3. Crear APIs REST para comunicación
4. Integrar 4C Perú como consumidor de APIs

---

**Sesión**: 2025-12-06
**Documentado por**: Claude Code
**Fecha de implementación**: Por definir
