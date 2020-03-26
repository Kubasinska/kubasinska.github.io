import pandas as pd
import numpy as np
from plotly.offline import plot
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import json
import urllib.request
import plotly.io as pio


#%%
def datiregioni_csv(mm,gg):
    grezzi = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-2020" + mm + gg + ".csv")
    return grezzi


def andamento_json():
    grezzi = pd.read_json("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json")
    return grezzi

def province_json():
    grezzi = pd.read_json("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json")
    tutti = grezzi.iloc[-128:]
    indexNames = tutti[ tutti['lat'] == 0 ].index
    tutti.drop(indexNames , inplace=True)
    return tutti

def province_csv():
    grezzi = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-20200325.csv", encoding = "ISO-8859-1")
    tutti = grezzi.iloc[-128:]
    indexNames = tutti[ tutti['lat'] == 0 ].index
    tutti.drop(indexNames , inplace=True)
    return tutti


#%%
raw_prov = province_csv()
raw_anda = andamento_json()
raw_reg = datiregioni_csv("03","25")

#%%
#Plotto

import plotly.graph_objects as go
import numpy as np

fig = go.Figure(go.Histogram(x=raw_reg["denominazione_regione"], y=raw_reg["totale_casi"]))

fig.add_trace(go.Histogram(x=raw_reg["denominazione_regione"], y=raw_reg["deceduti"]))

fig.update_layout(barmode="overlay",bargap=0.1)

plot(fig)