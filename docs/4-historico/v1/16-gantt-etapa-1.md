# Diagrama Gantt - ETAPA 1 LATAM-3C

## Timeline: Octubre 2024 - Marzo 2025

```mermaid
gantt
    title Plan ETAPA 1 - LATAM-3C
    dateFormat YYYY-MM-DD
    axisFormat %b

    section FASE 1 Formularios
    App formularios básica          :f1, 2024-10-01, 1w
    Generador Excel                 :f2, after f1, 2w
    Prueba 3 empresas              :f3, after f2, 2w
    Ajustes según feedback         :f4, after f3, 2w
    Recopilar datos reales         :f5, after f4, 1w
    Sistema carga básico           :f6, after f5, 2w

    section FASE 2 Sistema
    Base datos y modelos           :s1, 2024-12-01, 2w
    Cálculos cemento/clinker       :s2, after s1, 2w
    Cálculos concreto             :s3, after s2, 2w
    Clasificación GCCA            :s4, after s3, 2w
    Interfaz operador FICEM       :s5, after s4, 2w
    Testing datos reales          :s6, after s5, 2w

    section FASE 3 Reportes
    Generación reportes           :r1, 2025-02-01, 2w
    Dashboard indicadores         :r2, after r1, 2w
    Pruebas empresas finales      :r3, after r2, 2w
    Ajustes finales              :r4, after r3, 2w
    Deploy y capacitación        :r5, after r4, 1w

    section Hitos
    Empresas comprometidas        :milestone, 2024-10-07, 0d
    Formato validado             :milestone, 2024-11-15, 0d
    Datos reales obtenidos       :milestone, 2024-11-30, 0d
    Cálculos funcionando         :milestone, 2025-01-31, 0d
    Sistema completo             :milestone, 2025-03-15, 0d
    Entrega final               :milestone, 2025-03-31, 0d
```

## Versión ASCII (alternativa)

```
ACTIVIDAD                       OCT    NOV    DIC    ENE    FEB    MAR
                              |------|------|------|------|------|------|
                              S1 S2 S3 S4|S1 S2 S3 S4|S1 S2 S3 S4|S1 S2 S3 S4|S1 S2 S3 S4|S1 S2 S3 S4

FASE 1: FORMULARIOS (160 HH)
App formularios básica         ██
Generador Excel                   ████
Prueba 3 empresas                     ████
Ajustes según feedback                    ████
Recopilar datos reales                        ██
Sistema carga básico                          ████

FASE 2: SISTEMA PRINCIPAL (200 HH)
Base datos y modelos                                ████
Cálculos cemento/clinker                               ████
Cálculos concreto                                          ████
Clasificación GCCA                                             ████
Interfaz operador FICEM                                            ████
Testing datos reales                                                  ██

FASE 3: REPORTES (180 HH)
Generación reportes                                                        ████
Dashboard indicadores                                                          ████
Pruebas empresas finales                                                          ████
Ajustes finales                                                                      ████
Deploy y capacitación                                                                    ██

HITOS CRÍTICOS
✓ Empresas comprometidas       ▲
✓ Formato validado                    ▲
✓ Datos reales obtenidos                     ▲
✓ Cálculos funcionando                                    ▲
✓ Sistema completo                                                           ▲
✓ Entrega final                                                                       ▲

DISPONIBILIDAD EMPRESAS
Alta                           ████████████████
Baja (vacaciones)                              ████████████████
Media                                                          ████████████████████████

```

## Leyenda
- ██ = Trabajo activo
- ▲ = Hito/Milestone
- Semanas (S1-S4) por mes

## Carga de trabajo
- **Oct-Nov**: 160 HH (80 HH/mes = 20h/semana)
- **Dic-Ene**: 200 HH (100 HH/mes = 25h/semana)
- **Feb-Mar**: 180 HH (90 HH/mes = 22.5h/semana)
- **Promedio**: 22.5 horas/semana

## Dependencias críticas
1. Formularios → Validación empresas → Datos reales
2. Datos reales → Desarrollo sistema → Testing
3. Sistema completo → Pruebas finales → Entrega