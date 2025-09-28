# vehicles_app
Proyecto de construcción de una app web

🚗 Vehicles Dashboard

Esta aplicación web interactiva, construida con Streamlit, permite explorar y analizar un dataset de anuncios de venta de automóviles en EE.UU. El objetivo es brindar a los administradores de anuncios y analistas de mercado una herramienta sencilla para visualizar, filtrar y detectar patrones clave en los datos de vehículos.

✨ Funcionalidades principales

1. 📋 Data Viewer
- Muestra los datos del dataset (vehicles_us.csv) en una tabla interactiva.
- Permite seleccionar las columnas visibles y el número de filas a mostrar.
- Incluye un checkbox para ocultar filas con valores nulos.
- Ofrece un botón para descargar en CSV la vista filtrada actual.

2. 📊 Distribución de precios
- Genera un histograma de precios de los vehículos.
- Controles para ajustar:
    - Rango de precios (mínimo y máximo).
    - Número de bins (intervalos).
- Botón "Construir histograma" que genera el gráfico dinámicamente.

3. 📈 Dispersión precio vs odómetro
- Construye un gráfico de dispersión para analizar la relación entre:
    - price (precio) y odometer (kilometraje).
- Filtros interactivos para limitar rangos de kilometraje y precio.
- Opción de colorear los puntos por variables adicionales (condition, type, fuel, transmission).
- Botón "Construir dispersión" que genera el gráfico tras configurar los filtros.

🎯 Objetivo

El dashboard permite:
- Detectar outliers o anomalías (autos con alto kilometraje y precios desproporcionados).
- Identificar oportunidades (vehículos casi nuevos con precios bajos).
- Explorar la distribución de precios para análisis de mercado.
- Exportar subconjuntos de datos filtrados de manera sencilla.

🛠️ Tecnologías utilizadas

- Python 3.x
- Streamlit para la construcción del dashboard.
- Pandas para la manipulación de datos.
- Plotly Express para la creación de visualizaciones interactivas.