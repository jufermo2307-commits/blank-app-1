import streamlit as st

# --------------------------
# CONFIGURACIÓN
# --------------------------
st.set_page_config(page_title="Mecánica de Suelos", layout="centered")

st.markdown("""
<style>
h1, h2, h3 {color: #1f4e79;}
.stButton>button {
    background-color: #1f4e79;
    color: white;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

st.title("Aplicación de Mecánica de Suelos")

# --------------------------
# MENÚ
# --------------------------
menu = st.sidebar.selectbox(
    "Módulos",
    ["Inicio", "Gravimetría", "Volumetría", "Atterberg", "Resolución de problemas complejos"]
)

# --------------------------
# INICIO
# --------------------------
if menu == "Inicio":

    st.title("Calculadora de Suelos")

    st.info("""
Esta es una aplicación de calculadora en formato beta, desarrollada por los estudiantes de Ingeniería Civil de la Universidad Pontificia Bolivariana:

- Juan Fernando Monterrosa  
- Jannier David Navarro Martínez
""")

    st.success("""
En el menú ubicado a la izquierda encontrarás los diferentes modos para usar la calculadora.
""")

    st.markdown("---")

    st.header("Descripción")
    st.write("""
Esta aplicación permite realizar cálculos geotécnicos fundamentales como:

- Contenido de humedad  
- Densidades del suelo  
- Relaciones de fase  
- Límites de Atterberg  

Además, incluye un módulo avanzado para resolver automáticamente problemas complejos de mecánica de suelos a partir de diferentes combinaciones de datos.
""")
# --------------------------
# GRAVIMETRÍA
# --------------------------
elif menu == "Gravimetría":

    w_humedo = st.number_input("Peso húmedo (g)", min_value=0.0)
    w_seco = st.number_input("Peso seco (g)", min_value=0.0)

    if st.button("Calcular humedad"):
        if w_seco == 0:
            st.error("El peso seco no puede ser cero.")
        else:
            humedad = ((w_humedo - w_seco) / w_seco) * 100
            st.success(f"Humedad = {humedad:.2f} %")

# --------------------------
# VOLUMETRÍA
# --------------------------
elif menu == "Volumetría":

    peso = st.number_input("Peso (g)", min_value=0.0)
    volumen = st.number_input("Volumen (cm³)", min_value=0.0)
    humedad = st.number_input("Humedad (%)", min_value=0.0)

    if st.button("Calcular densidades"):
        if volumen == 0:
            st.error("Volumen no puede ser cero")
        else:
            gamma = peso / volumen
            gamma_d = gamma / (1 + humedad/100)

            st.success(f"γ húmeda = {gamma:.3f}")
            st.success(f"γ seca = {gamma_d:.3f}")

# --------------------------
# ATTERBERG
# --------------------------
elif menu == "Atterberg":

    LL = st.number_input("Límite líquido", min_value=0.0)
    LP = st.number_input("Límite plástico", min_value=0.0)

    if st.button("Calcular"):
        if LP > LL:
            st.error("LP no puede ser mayor que LL")
        else:
            IP = LL - LP
            st.success(f"Índice de plasticidad = {IP:.2f}")

# --------------------------
# MÓDULO AVANZADO
# --------------------------
elif menu == "Resolución de problemas complejos":

    st.header("Relaciones de Fase - Modo Laboratorio")

    st.info("Puedes ingresar datos de laboratorio o teóricos. El sistema resolverá automáticamente.")

    # --------------------------
    # PESOS
    # --------------------------
    Ws = st.number_input("Ws - Peso seco / sólidos (g)", 0.0)
    Ww = st.number_input("Ww - Peso agua (g)", 0.0)
    W = st.number_input("W - Peso total (g)", 0.0)

    W_h = st.number_input("Peso muestra húmeda (g)", 0.0)
    W_s = st.number_input("Peso muestra seca (g)", 0.0)

    # --------------------------
    # VOLÚMENES
    # --------------------------
    Vs = st.number_input("Vs - Volumen sólidos (cm³)", 0.0)
    Vw = st.number_input("Vw - Volumen agua (cm³)", 0.0)
    Vv = st.number_input("Vv - Volumen vacíos (cm³)", 0.0)
    V = st.number_input("V - Volumen total (cm³)", 0.0)

    V_h = st.number_input("Volumen muestra húmeda (cm³)", 0.0)
    V_s = st.number_input("Volumen muestra seca (cm³)", 0.0)

    # --------------------------
    # PROPIEDADES
    # --------------------------
    Gs = st.number_input("Gs - Gravedad específica", 0.0)
    w = st.number_input("w - Humedad (%)", 0.0)
    S_input = st.number_input("S - Grado de saturación (%)", 0.0)

    if st.button("Resolver sistema"):

        # Conversión
        w = w/100 if w != 0 else None
        S_input = S_input/100 if S_input != 0 else None

        # NORMALIZACIÓN
        data = {
            "Ws": Ws if Ws != 0 else (W_s if W_s != 0 else None),
            "Ww": Ww if Ww != 0 else None,
            "W": W if W != 0 else (W_h if W_h != 0 else None),
            "Vs": Vs if Vs != 0 else None,
            "Vw": Vw if Vw != 0 else None,
            "Vv": Vv if Vv != 0 else None,
            "V": V if V != 0 else (V_h if V_h != 0 else None),
            "Gs": Gs if Gs != 0 else None,
            "w": w,
            "S": S_input
        }

        # --------------------------
        # MOTOR ITERATIVO
        # --------------------------
        for _ in range(15):

            # PESOS
            if data["W"] is None and data["Ws"] and data["Ww"]:
                data["W"] = data["Ws"] + data["Ww"]

            if data["Ww"] is None and data["W"] and data["Ws"]:
                data["Ww"] = data["W"] - data["Ws"]

            if data["Ws"] is None and data["W"] and data["Ww"]:
                data["Ws"] = data["W"] - data["Ww"]

            # HUMEDAD
            if data["w"] is None and data["Ww"] and data["Ws"]:
                data["w"] = data["Ww"] / data["Ws"]

            if data["Ww"] is None and data["w"] and data["Ws"]:
                data["Ww"] = data["w"] * data["Ws"]

            # VOLÚMENES
            if data["V"] is None and data["Vs"] and data["Vv"]:
                data["V"] = data["Vs"] + data["Vv"]

            if data["Vv"] is None and data["V"] and data["Vs"]:
                data["Vv"] = data["V"] - data["Vs"]

            if data["Vs"] is None and data["V"] and data["Vv"]:
                data["Vs"] = data["V"] - data["Vv"]

            # RELACIÓN CON Gs
            if data["Vs"] is None and data["Ws"] and data["Gs"]:
                data["Vs"] = data["Ws"] / data["Gs"]

            if data["Gs"] is None and data["Ws"] and data["Vs"]:
                data["Gs"] = data["Ws"] / data["Vs"]

            # SATURACIÓN POR VOLUMEN
            if data["S"] is None and data["Vw"] and data["Vv"]:
                data["S"] = data["Vw"] / data["Vv"]

            # VOLUMEN DE AGUA DESDE S
            if data["Vw"] is None and data["S"] and data["Vv"]:
                data["Vw"] = data["S"] * data["Vv"]

        # --------------------------
        # RESULTADOS
        # --------------------------
        st.subheader("Resultados")

        # Densidades
        if data["W"] and data["V"]:
            st.success(f"γ húmeda = {data['W']/data['V']:.4f}")
        else:
            st.warning("Falta W o V")

        if data["Ws"] and data["V"]:
            st.success(f"γ seca = {data['Ws']/data['V']:.4f}")
        else:
            st.warning("Falta Ws o V")

        # e
        if data["Vv"] and data["Vs"]:
            e = data["Vv"]/data["Vs"]
            st.success(f"e = {e:.4f}")
        else:
            e = None
            st.warning("No se pudo calcular e")

        # n
        if data["Vv"] and data["V"]:
            st.success(f"n = {data['Vv']/data['V']:.4f}")
        else:
            st.warning("No se pudo calcular n")

        # humedad
        if data["w"]:
            st.success(f"w = {data['w']*100:.2f}%")

        # SATURACIÓN
        if data["S"]:
            st.success(f"S = {data['S']*100:.2f}%")
        elif data["w"] and data["Gs"] and e:
            S = (data["w"] * data["Gs"]) / e
            st.success(f"S (calculado) = {S*100:.2f}%")
        else:
            st.warning("No se pudo calcular S")

        # VALIDACIÓN
        st.subheader("Chequeo físico")

        if data["Vw"] and data["Vv"] and data["Vw"] > data["Vv"]:
            st.error("Vw > Vv → imposible físicamente")

        if data["S"] and data["S"] > 1:
            st.error("S > 100% → imposible")

        if e and e < 0:
            st.error("e negativo no es válido")

        st.subheader("Variables calculadas")
        st.write(data)