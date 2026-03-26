import streamlit as st

# --------------------------
# CONFIGURACIÓN
# --------------------------
st.set_page_config(page_title="Mecánica de Suelos", layout="centered")

# ESTILO PERSONALIZADO
st.markdown("""
<style>
h1, h2, h3 {
    color: #1f4e79;
}
.stButton>button {
    background-color: #1f4e79;
    color: white;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# LOGO
st.image("logo_upb.png", width=180)

# MENSAJE INICIAL
st.warning("Esta es una aplicación BETA en fase de prueba, desarrollada por los estudiantes Juan Fernando Monterrosa y Jannier Navarro de Ingeniería Civil de la Universidad Pontificia Bolivariana.")

st.title("Aplicación de Mecánica de Suelos")

st.info('"El suelo es el material más importante en cualquier obra de ingeniería." - Karl Terzaghi')

st.success("Puede navegar entre los diferentes módulos utilizando el menú ubicado en la parte izquierda.")

# --------------------------
# MENÚ (Se agregó "Diagrama de Fases")
# --------------------------
menu = st.sidebar.selectbox(
    "Módulos",
    ["Inicio", "Gravimetría", "Volumetría", "Diagrama de Fases", "Atterberg", "Normatividad"]
)

# --------------------------
# INICIO
# --------------------------
if menu == "Inicio":
    st.header("Descripción")
    st.write("""
Esta aplicación permite calcular propiedades básicas de suelos utilizadas en ingeniería civil, tales como contenido de humedad, densidad y límites de Atterberg, además de realizar una clasificación del suelo y evaluar su aptitud para construcción.
""")

# --------------------------
# GRAVIMETRÍA
# --------------------------
elif menu == "Gravimetría":
    st.header("Contenido de Humedad")

    w_humedo = st.number_input("Peso húmedo (g)", min_value=0.0)
    w_seco = st.number_input("Peso seco (g)", min_value=0.0)

    if st.button("Calcular"):
        if w_seco == 0:
            st.error("El peso seco debe ser mayor que cero.")
        elif w_humedo < w_seco:
            st.error("El peso húmedo no puede ser menor que el peso seco.")
        else:
            humedad = ((w_humedo - w_seco) / w_seco) * 100

            st.subheader("Resultados")
            st.table({
                "Parámetro": ["Peso húmedo", "Peso seco", "Humedad"],
                "Valor": [w_humedo, w_seco, f"{humedad:.2f} %"]
            })

            st.subheader("Interpretación")
            st.write("""
El contenido de humedad representa la cantidad de agua presente en el suelo respecto a su peso seco. Valores elevados pueden indicar suelos blandos o saturados, mientras que valores bajos corresponden a materiales más estables.
""")

# --------------------------
# VOLUMETRÍA
# --------------------------
elif menu == "Volumetría":
    st.header("Densidad del Suelo")

    peso = st.number_input("Peso (g)", min_value=0.0)
    volumen = st.number_input("Volumen (cm³)", min_value=0.0)
    humedad = st.number_input("Humedad (%)", min_value=0.0)

    if st.button("Calcular"):
        if volumen == 0:
            st.error("El volumen debe ser mayor que cero.")
        else:
            gamma = peso / volumen
            gamma_d = gamma / (1 + humedad/100)

            st.subheader("Resultados")
            st.table({
                "Parámetro": ["Densidad húmeda", "Densidad seca"],
                "Valor": [f"{gamma:.2f}", f"{gamma_d:.2f}"]
            })

            st.subheader("Interpretación")
            st.write("""
La densidad húmeda incluye el contenido de agua del suelo, mientras que la densidad seca permite evaluar su grado de compactación. Valores altos de densidad seca indican mejores condiciones estructurales.
""")

# --------------------------
# NUEVO MÓDULO: DIAGRAMA DE FASES
# --------------------------
elif menu == "Diagrama de Fases":
    st.header("Relaciones Gravimétricas y Volumétricas")
    st.write("Ingrese los datos obtenidos en laboratorio para determinar las proporciones de aire, agua y sólidos.")

    col1, col2 = st.columns(2)
    with col1:
        Gs = st.number_input("Gravedad específica de sólidos (Gs)", min_value=0.1, value=2.65)
        V_total = st.number_input("Volumen Total (Vt) [cm³]", min_value=0.01)
    with col2:
        W_total = st.number_input("Peso Total (Wt) [g]", min_value=0.01)
        W_seco = st.number_input("Peso Seco (Ws) [g]", min_value=0.01)

    if st.button("Calcular Diagrama"):
        if W_seco > W_total:
            st.error("El peso seco no puede ser mayor al peso total.")
        else:
            # Cálculos de Masas y Volúmenes
            Ww = W_total - W_seco  # Peso del agua
            Vw = Ww / 1.0          # Volumen del agua (asumiendo dens. agua = 1g/cm3)
            Vs = W_seco / (Gs * 1.0) # Volumen de sólidos
            Vv = V_total - Vs      # Volumen de vacíos
            
            # Resultados Principales
            e = Vv / Vs            # Relación de vacíos
            n = (Vv / V_total) * 100 # Porosidad
            S = (Vw / Vv) * 100    # Grado de saturación
            
            st.subheader("Resultados del Diagrama")
            st.table({
                "Propiedad": ["Índice de Poros (e)", "Porosidad (n)", "Grado de Saturación (S)"],
                "Valor": [f"{e:.3f}", f"{n:.2f} %", f"{min(S, 100.0):.2f} %"]
            })
            
            st.info(f"**Nota:** El volumen de sólidos calculado es de {Vs:.2f} cm³ y el volumen de vacíos es de {Vv:.2f} cm³.")

# --------------------------
# ATTERBERG
# --------------------------
elif menu == "Atterberg":
    # ... (Tu código original de Atterberg se mantiene igual)
    st.header("Límites de Atterberg")

    LL = st.number_input("Límite Líquido", min_value=0.0)
    LP = st.number_input("Límite Plástico", min_value=0.0)

    if st.button("Calcular"):
        if LP > LL:
            st.error("El límite plástico no puede ser mayor que el límite líquido.")
        else:
            IP = LL - LP
            A_line = 0.73 * (LL - 20)

            # Clasificación
            if LL < 50:
                if IP >= A_line:
                    clasificacion = "CL (Arcilla de baja plasticidad)"
                else:
                    clasificacion = "ML (Limo)"
            else:
                if IP >= A_line:
                    clasificacion = "CH (Arcilla de alta plasticidad)"
                else:
                    clasificacion = "MH (Limo de alta plasticidad)"

            # Aptitud
            if "CL" in clasificacion:
                apto = "Moderadamente apto"
                mensaje = "Puede presentar cambios volumétricos."
                solucion = "Control de humedad y compactación adecuada."

            elif "CH" in clasificacion:
                apto = "No apto"
                mensaje = "Alta compresibilidad y expansividad."
                solucion = "Estabilización con cal o reemplazo del suelo."

            elif "ML" in clasificacion:
                apto = "Poco apto"
                mensaje = "Baja cohesión y sensibilidad al agua."
                solucion = "Mejorar drenaje y compactación."

            else:
                apto = "No apto"
                mensaje = "Baja resistencia estructural."
                solucion = "Estabilización o sustitución del suelo."

            # RESULTADOS
            st.subheader("Resultados")
            st.table({
                "Parámetro": ["LL", "LP", "IP", "Clasificación"],
                "Valor": [LL, LP, f"{IP:.2f}", clasificacion]
            })

            # EVALUACIÓN
            st.subheader("Evaluación para construcción")
            st.write(f"Aptitud: {apto}")
            st.write(f"Motivo: {mensaje}")
            st.write(f"Recomendación: {solucion}")

# --------------------------
# NORMATIVIDAD
# --------------------------
elif menu == "Normatividad":
    st.header("Normatividad Colombiana e Internacional en Mecánica de Suelos")

    st.write("""
La caracterización de suelos en Colombia se rige principalmente por las especificaciones del Instituto Nacional de Vías (INVIAS) y las Normas Técnicas Colombianas (NTC), complementadas con estándares internacionales como ASTM y AASHTO. Estas normas establecen procedimientos estandarizados para la ejecución de ensayos de laboratorio y campo, garantizando la confiabilidad de los resultados en estudios geotécnicos.

------------------------------
 CONTENIDO DE HUMEDAD
------------------------------
* INV E-122: Determinación del contenido de agua (humedad) mediante secado en horno.  
* ASTM D2216: Standard Test Methods for Laboratory Determination of Water Content of Soil and Rock.

Este ensayo permite conocer la cantidad de agua presente en el suelo, parámetro fundamental para evaluar su comportamiento mecánico.

------------------------------
 LÍMITES DE ATTERBERG
------------------------------
* INV E-125: Determinación del límite líquido.  
* INV E-126: Determinación del límite plástico.  
* ASTM D4318: Standard Test Methods for Liquid Limit, Plastic Limit, and Plasticity Index of Soils.

Estos ensayos permiten determinar el comportamiento plástico del suelo y son esenciales para su clasificación mediante el sistema SUCS.

------------------------------
 ANÁLISIS GRANULOMÉTRICO
------------------------------
* INV E-123: Análisis granulométrico por tamizado.  
* INV E-124: Análisis granulométrico por hidrómetro.  
* ASTM D6913: Particle Size Distribution (Sieve Analysis).  
* ASTM D7928: Particle Size Distribution (Hydrometer Analysis).

Permiten conocer la distribución de tamaños de partículas del suelo, lo cual es clave para su clasificación y comportamiento hidráulico.

------------------------------
 PESO ESPECÍFICO Y DENSIDAD
------------------------------
* INV E-128: Determinación del peso específico de los sólidos.  
* ASTM D854: Specific Gravity of Soil Solids.  

* INV E-142: Determinación de la densidad en laboratorio.  
* ASTM D7263: Laboratory Determination of Density.

Estos ensayos permiten evaluar la relación entre masa y volumen del suelo, fundamental en estudios de compactación y resistencia.

------------------------------
 ENSAYOS DE COMPACTACIÓN
------------------------------
* INV E-141: Ensayo Proctor estándar.  
* INV E-142: Ensayo Proctor modificado.  
* ASTM D698: Standard Proctor Test.  
* ASTM D1557: Modified Proctor Test.

Permiten determinar la relación óptima entre humedad y densidad para lograr una adecuada compactación del suelo.

------------------------------
 RESISTENCIA DEL SUELO
------------------------------
* INV E-152: Ensayo de corte directo.  
* ASTM D3080: Direct Shear Test.  

* INV E-153: Ensayo de compresión inconfinada.  
* ASTM D2166: Unconfined Compressive Strength.

Estos ensayos permiten determinar la resistencia al corte y la capacidad del suelo para soportar cargas.

------------------------------
 CONSOLIDACIÓN
------------------------------
* INV E-154: Ensayo de consolidación unidimensional.  
* ASTM D2435: One-Dimensional Consolidation Test.

Permite evaluar asentamientos del suelo bajo cargas a lo largo del tiempo.

------------------------------
 PERMEABILIDAD
------------------------------
* INV E-130: Ensayo de permeabilidad en laboratorio.  
* ASTM D2434: Permeability Test.

Determina la capacidad del suelo para permitir el paso del agua, fundamental en drenajes y estabilidad.

------------------------------
 CLASIFICACIÓN DE SUELOS
------------------------------
* Sistema SUCS (Unified Soil Classification System).  
* AASHTO M145: Clasificación de suelos para carreteras.

Estos sistemas permiten categorizar los suelos según sus propiedades físicas y mecánicas.

------------------------------
 IMPORTANCIA EN INGENIERÍA
------------------------------
El cumplimiento de estas normas garantiza resultados confiables en estudios geotécnicos, permitiendo diseñar cimentaciones, estructuras y obras civiles seguras. Además, aseguran la estandarización de procedimientos y la comparabilidad de resultados a nivel nacional e internacional.

El uso adecuado de estas normativas permite prevenir fallas estructurales, optimizar diseños y garantizar la estabilidad de las obras en función de las condiciones del suelo.
""")