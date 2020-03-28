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
raw_reg = datiregioni_csv("03","27")

raw_reg.sort_values('totale_casi', axis=0, inplace=True, ascending=False)

#%%
#Plotto
fig = make_subplots(rows=2, cols=1, 
                    vertical_spacing=0.15,
                    specs=[[{"type": "bar"}],
                           [{"type": "scatter"}]],
                    subplot_titles=("Casi Attivi", "Andamenti"))

fig.add_trace(go.Bar(name='Deceduti', x=raw_reg["denominazione_regione"], y=raw_reg["deceduti"]), row=1, col=1)
fig.add_trace(go.Bar(name='Casi attivi', x=raw_reg["denominazione_regione"],
                     y=(raw_reg["totale_casi"]-raw_reg["deceduti"])-raw_reg["dimessi_guariti"],
                     text = (raw_reg["totale_casi"]-raw_reg["deceduti"])-raw_reg["dimessi_guariti"]), row=1, col=1)

fig.update_traces(textposition='outside')

fig.add_trace(go.Scatter(
                x=raw_anda.data,
                y=raw_anda['totale_ospedalizzati'],
                name="Ospedalizzati",
                line=dict(color='#ABD71F', width=4),
                opacity=0.8), row=2, col=1)

fig.add_trace(go.Scatter(
                x=raw_anda.data,
                y=raw_anda['terapia_intensiva'],
                name="Ricoverati in terapia intensiva",
                line=dict(color='#1FD7A7', width=4),
                opacity=0.8), row=2, col=1)

fig.add_trace(go.Scatter(
                x=raw_anda.data,
                y=raw_anda['isolamento_domiciliare'],
                name="Isolamento domiciliare",
                line=dict(color='#4B1FD7', width=4),
                opacity=0.8), row=2, col=1)

fig.add_trace(go.Scatter(
                x=raw_anda.data,
                y=raw_anda['dimessi_guariti'],
                name="Dimessi guariti",
                line=dict(color='#D71F4F', width=4),
                opacity=0.8), row=2, col=1)

# Use date string to set xaxis range
fig.update_layout(xaxis_range=[raw_anda.data.iloc[0],raw_anda.data.iloc[-1]])



fig.update_layout(barmode='stack')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', showlegend=False)
plot(fig, filename="reg_bar")

