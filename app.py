import streamlit as st
import pandas as pd

# Supongamos que tienes un DataFrame llamado 'data'
data = pd.read_csv('archivo_consolidado.csv')

data['Fecha Nacimiento'] = pd.to_datetime(
    data['Fecha Nacimiento'], 
    dayfirst=True,      # Interpretar las fechas en formato DD-MM-YYYY
    errors='coerce'     # Convierte valores inválidos en NaT
)

# Calcular la edad solo para fechas válidas
data['Edad'] = data['Fecha Nacimiento'].apply(
    lambda x: pd.Timestamp.today().year - x.year - 
    ((pd.Timestamp.today().month, pd.Timestamp.today().day) < (x.month, x.day)) if pd.notna(x) else None
)

# Configura la página para usar el modo ancho
st.set_page_config(layout="wide")

columna1,columna2,columna3, = st.columns([1,3,1])
with columna1:
    # Muestra el logo usando el nuevo parámetro
    st.image("logo.png", width=120)

with columna2:
    # Título de la aplicacións
    st.title('Club Deportivo Concón National')
    # Subtítulo
    st.subheader('Plataforma Área de Scouting')
    st.write("")  # Primer salto de línea
    st.write("")  # Segundo salto de línea


# Filtros interactivos
# Crear columnas para los filtros
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Filtrar por Equipo
    equipo = st.multiselect('Selecciona el Equipo', options=data['Equipo'].unique())


with col2:
    # Filtrar por Nacionalidad
    nacionalidad = st.multiselect('Selecciona la Nacionalidad', options=data['Nacionalidad'].unique())

with col3:
    # Filtrar por Posición
    posicion = st.multiselect('Selecciona la Posición', options=data['Posicion'].unique())

with col4:

     # Filtrar por Edad
    edad_min = int(data['Edad'].min())
    edad_max = int(data['Edad'].max())

    edad_filtro = st.slider(
        'Selecciona el rango de Edad',
        min_value=edad_min,
        max_value=edad_max,
        value=(edad_min, edad_max),
        step=1
    )

fil1, fil2, fil3, fil4 = st.columns(4)

with fil1:
    division = st.multiselect('Selecciona la División', options=data['Division'].unique())


# Aplicar filtros
filtered_data = data.copy()

# Filtrar los datos


if equipo:
    filtered_data = filtered_data[filtered_data['Equipo'].isin(equipo)]

if nacionalidad:
    filtered_data = filtered_data[filtered_data['Nacionalidad'].isin(nacionalidad)]

if posicion:
    filtered_data = filtered_data[filtered_data['Posicion'].isin(posicion)]

if division:
    filtered_data = filtered_data[filtered_data['Division'].isin(division)]

# Filtrar por Edad, incluyendo los valores None
filtered_data = filtered_data[
    (pd.isna(filtered_data['Edad'])) | 
    ((filtered_data['Edad'] >= edad_filtro[0]) & (filtered_data['Edad'] <= edad_filtro[1]))
]


st.write("")  # Primer salto de línea
st.write("")  # Segundo salto de línea

columna1,columna2,columna3, = st.columns([1,3,1])

with columna1:
    st.metric(label="Cantidad total de jugadores", value=len(filtered_data))

with columna2:
# Mostrar datos filtrados
    columnas_seleccionadas = ["Nombre Jugador","Posicion","Posicion Secundaria","Edad","Nacionalidad","Equipo","Division","Valor de Mercado","Link Jugador"]
    st.subheader("Tabla con vista detallada")
    # Eliminar la hora, manteniendo solo la fecha
    filtered_data['Fecha Nacimiento'] = filtered_data['Fecha Nacimiento'].dt.date
st.dataframe(filtered_data)