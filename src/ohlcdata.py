import krakenex
import funciones
import streamlit as st
k = krakenex.API()

# class     --> datos OHLC
# object    --> datos OHLC con 2 atributos: tiempo y par moneda

class OhlcData:

    def __init__(self, pair, since):
        self.pair = pair
        self.since = since
        # self.ohlc_data = []
        # self.k = krakenex.API()

    def data_download(self):

        params = {'pair' : self.pair, 'since' : self.since}

        try:
            ret = k.query_public('OHLC', params)
            bars = ret['result'][self.pair]

            # actualizamos 'since'
            self.since = ret['result']['last']
            params['since'] = self.since
            return bars

        except KeyError as e:
            st.error(f"Error al obtener los datos de kraken.API: {e}")
            print(e)
        except Exception as e:
            st.error(f"Ha ocurrido un error: {e}")
            print(e)

    def data_update(self):

        params = {'pair': self.pair, 'since': self.since}

        ret = k.query_public('OHLC', params)
        bars = ret['result'][self.pair]

        # funciones.lineprint(funciones.now())
        # print(len(bars))
        # for b in bars:
        #     print(b)

        return bars