# Diagrama de Flujo - Calculadora 3C País

## Proceso Completo: Recopilación y Análisis de Datos

```mermaid
graph TD
    %% Actores principales
    A[🏭 Empresas Cementeras<br/>y Concreteras] 
    B[🏛️ FICEM<br/>Federación]
    C[📊 Sistema 3C País<br/>Calculadora]
    D[🌎 Países LATAM<br/>Indicadores Nacionales]

    %% Proceso de ingreso de datos
    A --> E[📝 Acceso a Formularios<br/>Ingreso de Datos]
    E --> F{Tipo de Planta}
    
    F -->|Cemento| G[🏭 Formulario Cemento<br/>• Datos empresa<br/>• Datos planta<br/>• Producción clínker<br/>• Composición cemento<br/>• Emisiones proceso]
    F -->|Concreto| H[🚛 Formulario Concreto<br/>• Datos empresa<br/>• Datos planta<br/>• Dosificaciones<br/>• Resistencias<br/>• Transporte]

    %% Generación de archivos
    G --> I[📊 Generación Excel<br/>Plantilla validable]
    H --> I

    %% Validación y carga
    I --> J[✅ Validación Externa<br/>Revisión técnica]
    J --> K[🔄 Carga al Sistema<br/>Base de datos]

    %% Procesamiento y cálculos
    L --> M[⚙️ Motor de Cálculos]
    M --> N[🧮 Cálculo Huellas CO2<br/>• Cemento: Factor emisión<br/>• Concreto: Huella total]
    N --> O[📈 Clasificación GCCA<br/>• Bandas cemento (A-G)<br/>• Bandas concreto (AA-F)]

    %% Agregación por país
    O --> P[🌐 Agregación Nacional<br/>Consolidación datos]
    P --> Q[📊 Indicadores País<br/>• CO2/Clínker<br/>• CO2/Cemento<br/>• CO2/Concreto<br/>• CO2/Resistencia]

    %% Outputs finales
    Q --> R[🎯 Dashboard Nacional<br/>Visualizaciones]
    Q --> S[📋 Reportes FICEM<br/>Comparativos regionales]
    Q --> T[🌍 Benchmarking<br/>Internacional]

    %% Feedback loop
    S --> B
    B --> U[📢 Políticas y<br/>Mejores Prácticas]
    U --> A

    %% Estilos
    classDef empresa fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef sistema fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef proceso fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef output fill:#fff3e0,stroke:#f57c00,stroke-width:2px

    class A,E,F,G,H empresa
    class C,I,J,L,M,N,O,P sistema
    class K,U proceso
    class Q,R,S,T,D output
```

## Flujo de Datos Detallado

```mermaid
sequenceDiagram
    participant E as 🏭 Empresa
    participant S as 📊 Sistema 3C
    participant V as ✅ Validador
    participant F as 🏛️ FICEM
    participant P as 🌎 País

    Note over E,P: Fase 1: Ingreso de Datos
    E->>S: Accede a formularios
    S->>E: Presenta formulario específico
    E->>S: Completa datos operacionales
    S->>E: Genera JSON + Excel
    
    Note over E,P: Fase 2: Validación
    E->>V: Envía archivo Excel
    V->>V: Revisa consistencia datos
    V->>E: Retroalimenta correcciones
    E->>S: Carga archivo validado

    Note over E,P: Fase 3: Procesamiento
    S->>S: Calcula huellas CO2
    S->>S: Aplica clasificación GCCA
    S->>S: Agrega datos por país
    
    Note over E,P: Fase 4: Resultados
    S->>F: Genera indicadores regionales
    S->>P: Publica dashboard nacional
    F->>E: Comparte benchmarks
    E->>S: Mejora datos siguiente ciclo
```

## Arquitectura de Datos

```mermaid
erDiagram
    EMPRESA ||--o{ PLANTA-CEMENTO : opera
    EMPRESA ||--o{ PLANTA-CONCRETO : opera
    
    EMPRESA {
        string nombre
        string pais
        string responsable
        string contacto
    }
    
    PLANTA-CEMENTO {
        string id_planta
        float capacidad_clinker
        float produccion_anual
        float factor_co2
        string tipo_cemento
    }
    
    PLANTA-CONCRETO {
        string id_planta
        float capacidad_m3
        float resistencia_promedio
        float contenido_cemento
        float huella_co2
    }
    
    PLANTA-CEMENTO ||--o{ CALCULO-CEMENTO : genera
    PLANTA-CONCRETO ||--o{ CALCULO-CONCRETO : genera
    
    CALCULO-CEMENTO {
        float emisiones_proceso
        float emisiones_energia
        string banda_gcca
        date fecha_calculo
    }
    
    CALCULO-CONCRETO {
        float huella_materiales
        float huella_transporte
        string banda_gcca
        date fecha_calculo
    }
    
    CALCULO-CEMENTO ||--o{ INDICADOR-PAIS : agrega
    CALCULO-CONCRETO ||--o{ INDICADOR-PAIS : agrega
    
    INDICADOR-PAIS {
        string pais
        float co2_clinker_promedio
        float co2_cemento_promedio
        float co2_concreto_promedio
        float indice_eficiencia
        date periodo
    }
```

## Casos de Uso Principales

```mermaid
graph LR
    %% Actores
    EM[🏭 Empresa]
    FI[🏛️ FICEM]
    GOB[🏛️ Gobierno]
    
    %% Sistema
    SYS[📊 Sistema 3C País]
    
    %% Casos de uso empresas
    EM --> UC1[Registrar datos<br/>operacionales]
    EM --> UC2[Generar reporte<br/>huella carbono]
    EM --> UC3[Comparar con<br/>benchmarks]
    
    %% Casos de uso FICEM
    FI --> UC4[Consolidar datos<br/>regionales]
    FI --> UC5[Generar indicadores<br/>comparativos]
    FI --> UC6[Identificar mejores<br/>prácticas]
    
    %% Casos de uso gobierno
    GOB --> UC7[Consultar indicadores<br/>nacionales]
    GOB --> UC8[Definir políticas<br/>ambientales]
    
    %% Conexiones al sistema
    UC1 --> SYS
    UC2 --> SYS
    UC3 --> SYS
    UC4 --> SYS
    UC5 --> SYS
    UC6 --> SYS
    UC7 --> SYS
    UC8 --> SYS
```
