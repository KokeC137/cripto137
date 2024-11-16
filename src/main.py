import time
import streamlit as st

from ohlcdata import OhlcData
from analisysbollinger import AnalisysBollinger
from ploteo_data import ploteo_data

import os
import subprocess

# Título para la app
st.title("Selecciona un par de moneda")

# Lista de opciones para el desplegable (puedes poner los pares de moneda que necesites)
available_pairs = ["BTC/USD", "ETH/USD", "LTC/EUR", "XRP/EUR"]
available_periods = ["20","10","50","200"]
available_multipliers = ["2","1","2.5","3"]
available_size = ["500","100","300","700"]

# Desplegable de par monedas
pair = st.selectbox("Elige un par de moneda:", available_pairs)
st.write(f"Has seleccionado: {pair}")

# Desplegable para el periodo de análisis Bollinger
period = st.selectbox("Elige el período de análisis para las bandas de Bollynger", available_periods)
st.write(f"Has seleccionado: {period}")

# Desplegable para el multiplicador de análisis Bollinger
multiplicador = st.selectbox("Elige el período de análisis para las bandas de Bollynger", available_multipliers)
st.write(f"Has seleccionado: {multiplicador}")

# Desplegable para el tamaño de la muestra ploteada
size = st.selectbox("Elige el tamaño de la muestra a graficar", available_size)
st.write(f"Has seleccionado: {size}")

if size == 700:
    size = 699

# Index for plot
iforshow = 700 - int(size)

# Crear un contenedor en Streamlit para el gráfico
graph_container = st.empty()

since = str(1499000000) # UTC 2017-07-02 12:53:20

data = OhlcData(pair,since)

first_time = True
ohlc_data = []

while True:

    if first_time:
        download = data.data_download()
        ohlc_data.extend(download)
        first_time = False
    else:
        update = data.data_update()
        ohlc_data.pop(0)
        ohlc_data[-1] = update[0]
        ohlc_data.append(update[1])

    analisys_bollinger = AnalisysBollinger(ohlc_data,int(period),int(multiplicador))
    bollinger_data = analisys_bollinger.add_bollinger()
    ploteo_data(bollinger_data[iforshow:], graph_container)
    time.sleep(60)