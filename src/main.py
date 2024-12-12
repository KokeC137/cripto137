import time
import streamlit as st

from ohlcdata import OhlcData
from analisysbollinger import AnalisysBollinger
from ploteo_data import ploteo_data

# Crear una bandera de control en session_state
if 'running' not in st.session_state:
    st.session_state.running = True  # la aplicación se inicia automáticamente

# Mostrar los parámetros en Streamlit
pair = st.selectbox("Elige un par de moneda:", ["BTC/USD", "ETH/USD", "LTC/EUR", "XRP/EUR"])
period = st.selectbox("Elige el período de análisis para las bandas de Bollinger", ["20", "10", "50", "200"])
multiplicador = st.selectbox("Elige el multiplicador de análisis para las bandas de Bollinger", ["2", "1", "2.5", "3"])
size = st.selectbox("Elige el tamaño de la muestra a graficar", ["500", "100", "300", "700"])

if period == "200" and size == "100":
    st.error(f"Por la estructuración del código, no es posible graficar con un periodo de {period} y una muestra de {size} elementos. Prueba con el resto.")

# Crear un contenedor para el gráfico
graph_container = st.empty()

# Botón para iniciar el bucle
if st.button("Iniciar"):
    st.session_state.running = True  # Marcar que el bucle debe ejecutarse

# Botón para detener el bucle
if st.button("Detener"):
    st.session_state.running = False  # Detener el bucle

# Función principal
def run_bucle():
    data = OhlcData(pair, "1499000000")  # UTC 2017-07-02 12:53:20
    first_time = True
    iforshow = 700 - int(size) + 1

    ohlc_data = []
    while st.session_state.running:  # Solo corre si running es True
        if first_time:
            download = data.data_download()
            ohlc_data.extend(download)
            first_time = False
        else:
            update = data.data_update()
            ohlc_data.pop(0)
            ohlc_data[-1] = update[0]
            ohlc_data.append(update[1])

        analisys_bollinger = AnalisysBollinger(ohlc_data, int(period), float(multiplicador))
        bollinger_data = analisys_bollinger.add_bollinger()
        ploteo_data(bollinger_data[iforshow:], graph_container)
        time.sleep(60)

# Verificar si se debe ejecutar el bucle
if st.session_state.running:
    run_bucle()
