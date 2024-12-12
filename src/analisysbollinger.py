import numpy as np
import funciones
import pandas as pd

# class     --> datos Bandas de Bollinger
# object    --> datos OHLC con datos para análisis de Bollinger con 1 atributo: los periodos utilizados para el cálculo

class AnalisysBollinger:
    def __init__(self,ohlc_data,periodos, multiplicador):
        self.ohlc_data = ohlc_data
        self.periodos = periodos
        self.multiplicador = multiplicador

    def add_bollinger(self):
        if len(self.ohlc_data) < self.periodos:
            raise ValueError(f"Se requieren al menos {self.periodos} períodos para calcular las bandas.")

        # creamos una lista con los valores necesarios para calcular la banda en cada período
        bollinger_data = []
        for i in range(self.periodos,len(self.ohlc_data)):
            
            # list_close_value --> lista con los valores de cierre para calcular bandas
            list_close_value = []
            for d in self.ohlc_data[i-self.periodos:i]:
                list_close_value.append(float(d[4]))
            banda_central = (np.mean(list_close_value))
            banda_superior = banda_central + self.multiplicador * np.std(list_close_value)
            banda_inferior = banda_central - self.multiplicador * np.std(list_close_value)

            # calculamos señales de compra
            close_value = float(self.ohlc_data[i][4]) # para mejor entendimiento
            if close_value < banda_inferior:
                signal = 1
            elif close_value > banda_superior:
                signal = -1
            else:
                signal = 0

            # Rescribimos los valores de Bollinger en modo string
            banda_central_f = f"{banda_central:.1f}"
            banda_superior_f = f"{banda_superior:.1f}"
            banda_inferior_f = f"{banda_inferior:.1f}"

            bollinger_data.append([
                self.ohlc_data[i][0],
                self.ohlc_data[i][1],
                self.ohlc_data[i][2],
                self.ohlc_data[i][3],
                self.ohlc_data[i][4],
                banda_central_f,
                banda_superior_f,
                banda_inferior_f,
                signal
            ])

        now = funciones.now()
        now_f = now.strftime('%Y-%m-%d %H:%M:%S')
        funciones.lineprint(now_f)

        # Introducimos un error para verificar que la dimensión de la lista es la que corresponde
        correct_size = 720-self.periodos
        if len(bollinger_data) != correct_size:
            raise ValueError (f"Error: La longitud de la lista debe ser {correct_size}, pero es {len(bollinger_data)}.")

        # Convertir a DataFrame de pandas
        df = pd.DataFrame(bollinger_data,
                          columns=["Unix_Date", "Open", "High", "Low", "Close", "central_band", "upper_band",
                                   "lower_band", "Signal"])
        # Convertir la columna "Fecha Unix" de Unix a formato UTC
        df['Fecha'] = pd.to_datetime(df['Unix_Date'], unit='s', utc=True).dt.strftime('%Y-%m-%d %H:%M:%S')
        # Eliminar la columna original "Fecha Unix" que no es necesaria ahora
        df = df.drop(columns=["Unix_Date"])
        # Reorganizar las columnas para que "Fecha" sea la primera columna
        df = df[["Fecha", "Open", "High", "Low", "Close", "central_band", "upper_band", "lower_band", "Signal"]]

        # Imprimir los primeros 5 registros con los encabezados
        print(df.head())
        print("\n---------")
        # Imprimir los últimos 5 registros con los encabezados
        print(df.tail())

        return bollinger_data