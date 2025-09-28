# Importar las librerías necesarias
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Config ---
st.set_page_config(page_title="Vehicles Dashboard", layout="centered")

# --- Título ---
st.header("Anuncios de vehículos – Panel interactivo")

# --- Datos ---
car_data = pd.read_csv("vehicles_us.csv")

# =====================
# Panel: Data viewer
# =====================
st.subheader("🔎 Data viewer")

# Lugar donde mostraremos el botón arriba del panel
dl_placeholder = st.container()

with st.expander("🔎 Data Viewer", expanded=True):
    # Controles de vista
    columnas = st.multiselect(
        "Columnas a mostrar",
        options=list(car_data.columns),
        default=list(car_data.columns),
    )
    filas = st.slider("Filas a mostrar", min_value=5, max_value=200, value=25, step=5)
    ocultar_nulos = st.checkbox("Ocultar filas con valores nulos", value=False)

    # Construcción de la vista
    vista = car_data[columnas] if columnas else car_data.copy()
    if ocultar_nulos:
        vista = vista.dropna()

    # Tabla
    st.dataframe(vista.head(filas), use_container_width=True)

# Botón de descarga (arriba del panel)
with dl_placeholder:
    sp1, sp2 = st.columns([6, 2])  # empuja el botón hacia la derecha
    with sp2:
        csv_bytes = vista.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Descargar CSV (vista)",
            data=csv_bytes,
            file_name="vehicles_us_view.csv",
            mime="text/csv",
            use_container_width=True,
        )

# Panel 2: Histograma de precios 
# ================================
st.subheader("📊 Distribución de precios")

df_price = car_data.dropna(subset=["price"]).copy()
if df_price.empty:
    st.warning("No hay datos de precio disponibles.")
else:
    p_min, p_max = int(df_price["price"].min()), int(df_price["price"].max())
    rango = st.slider(
        "Rango de precio",
        min_value=p_min,
        max_value=p_max,
        value=(p_min, p_max),
        step=max(1, (p_max - p_min) // 100),
        help="Filtra los autos por precio para el histograma",
    )
    bins = st.slider("Número de bins", min_value=10, max_value=120, value=40, step=5)

    # Filtrar por rango
    mask = (df_price["price"] >= rango[0]) & (df_price["price"] <= rango[1])
    df_plot = df_price.loc[mask]

    # Botón para construir el histograma
    if st.button("Construir histograma"):
        st.write("Histograma de precios")
        fig = px.histogram(
            df_plot,
            x="price",
            nbins=bins,
            title=None,
        )
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Ajusta los filtros y pulsa **Construir histograma** para ver el gráfico.")


# Panel 3: Dispersión (price vs odometer)
# ================================
st.subheader("📈 Dispersión: precio vs odómetro")

# Datos válidos para el scatter
df_scatter = car_data.dropna(subset=["price", "odometer"]).copy()
if df_scatter.empty:
    st.warning("No hay filas con 'price' y 'odometer' para graficar.")
else:
    # Rangos para filtrar
    odo_min, odo_max = int(df_scatter["odometer"].min()), int(df_scatter["odometer"].max())
    prc_min, prc_max = int(df_scatter["price"].min()), int(df_scatter["price"].max())

    st.caption("Filtra el rango antes de graficar (útil para quitar outliers extremos).")
    c1, c2 = st.columns(2)
    with c1:
        rango_odo = st.slider(
            "Rango de odómetro (km)",
            min_value=odo_min, max_value=odo_max,
            value=(odo_min, odo_max),
            step=max(1, (odo_max - odo_min) // 100)
        )
    with c2:
        rango_price = st.slider(
            "Rango de precio",
            min_value=prc_min, max_value=prc_max,
            value=(prc_min, prc_max),
            step=max(1, (prc_max - prc_min) // 100)
        )

    # Filtro por rangos
    mask = (
        (df_scatter["odometer"].between(rango_odo[0], rango_odo[1])) &
        (df_scatter["price"].between(rango_price[0], rango_price[1]))
    )
    df_plot = df_scatter.loc[mask]

    # Color opcional para facilitar lectura
    color_by = st.selectbox(
        "Color por (opcional)",
        options=["(ninguno)", "condition", "type", "fuel", "transmission"],
        index=0
    )
    color_kw = {} if color_by == "(ninguno)" else {"color": color_by}

    # Botón para construir la dispersión
    if st.button("Construir dispersión"):
        st.write("Dispersión: odómetro vs precio")
        fig = px.scatter(
            df_plot,
            x="odometer", y="price",
            hover_data=["model", "model_year", "condition", "type"],
            opacity=0.6,
            height=520,
            **color_kw
        )
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
        fig.update_xaxes(title="Odómetro (km)")
        fig.update_yaxes(title="Precio")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Ajusta los filtros y pulsa **Construir dispersión** para ver el gráfico.")
