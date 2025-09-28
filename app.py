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
st.subheader("Data viewer")

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

    # Histograma simple
    fig = px.histogram(
        df_plot,
        x="price",
        nbins=bins,
        title=None,
    )
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))

    st.plotly_chart(fig, use_container_width=True)