import pandas as pd
import plotly.graph_objects as go
import numpy as np


def ploteo_data(data,graph_container):

    # Convertir los datos a un DataFrame
    # df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count','banda_central','banda_superior','banda_inferior'])
    df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close','banda_central','banda_superior','banda_inferior', 'signal'])

    # Convertir el tiempo (Unix timestamp) a formato de fecha legible
    df['time'] = pd.to_datetime(df['time'], unit='s')

    # Convertir los strings de 'open', 'high', 'low', 'close' a floats
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)

    # Crear el gráfico OHLC con Plotly
    fig = go.Figure(data=[go.Candlestick(x=df['time'],
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['close'],
                                         name='OHLC')])

    # Añadir las bandas de Bollinger al gráfico
    fig.add_trace(go.Scatter(x=df['time'], y=df['banda_central'],
                             line=dict(color='blue', width=1),
                             name='Banda Central'))
    fig.add_trace(go.Scatter(x=df['time'], y=df['banda_superior'],
                             line=dict(color='red', width=1),
                             name='Banda Superior'))
    fig.add_trace(go.Scatter(x=df['time'], y=df['banda_inferior'],
                             line=dict(color='green', width=1),
                             name='Banda Inferior'))

    df['compra'] = np.where(df['signal'] == 1, 1, 0)
    df['venta'] = np.where(df['signal'] == -1, 1, 0)

    # Señales de Compra
    fig.add_trace(go.Scatter(x=df.loc[df['compra'] == 1, 'time'],
                             y=df.loc[df['compra'] == 1, 'close'],
                             mode='markers',
                             name='Señal de Compra',
                             marker=dict(symbol='arrow-up', color='green', size=10)))

    # Señales de Venta
    fig.add_trace(go.Scatter(x=df.loc[df['venta'] == 1, 'time'],
                             y=df.loc[df['venta'] == 1, 'close'],
                             mode='markers',
                             name='Señal de Venta',
                             marker=dict(symbol='arrow-up', color='red', size=10)))

    # Configurar el gráfico
    fig.update_layout(title='Gráfico OHLC (actualizado cada minuto)',
                      xaxis_title='Fecha',
                      yaxis_title='Precio',
                      xaxis_rangeslider_visible=False)

    # Mostrar el gráfico en el contenedor de Streamlit
    graph_container.plotly_chart(fig)
