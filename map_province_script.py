# -*- coding: utf-8 -*-
"""
Created by Francesco Mattioli
Francesco@nientepanico.org
www.nientepanico.org
"""

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
    grezzi = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-20200318.csv", encoding = "ISO-8859-1")
    tutti = grezzi.iloc[-128:]
    indexNames = tutti[ tutti['lat'] == 0 ].index
    tutti.drop(indexNames , inplace=True)
    return tutti


#%%
raw = province_csv()
raw_and = andamento_json()

raw['text'] = raw['denominazione_provincia'] + '<br>Totale Casi ' + (raw['totale_casi']).astype(str)
limits = [(0,50),(50,100),(100,200),(200,300),(300,5000)]
colors = ["lightseagreen","royalblue", "#e377c2", "orange", "crimson"]
cities = []
scale = 2

#Load and read the geojson file for Italys regions. 
italy_url = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_provinces.geojson"
with urllib.request.urlopen(italy_url) as url:
        jdata = json.loads(url.read().decode())
              
pts = []#list of points defining boundaries of polygons
for  feature in jdata['features']:
    if feature['geometry']['type'] == 'Polygon':
        pts.extend(feature['geometry']['coordinates'][0])    
        pts.append([None, None])#mark the end of a polygon   
        
    elif feature['geometry']['type'] == 'MultiPolygon':
        for polyg in feature['geometry']['coordinates']:
            pts.extend(polyg[0])
            pts.append([None, None])#end of polygon
    elif feature['geometry']['type'] == 'LineString': 
        points.extend(feature['geometry']['coordinates'])
        points.append([None, None])
    else: pass           
    #else: raise ValueError("geometry type irrelevant for map")
x, y = zip(*pts)  

#%%

fig = make_subplots(rows=1, cols=2, 
                    vertical_spacing=0.019, 
                    specs=[[{"type": "scatter"},{"type": "scatter"}]], subplot_titles=("Unemployment rate"))






fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line_color='#999999', line_width=1.5, showlegend=False), row=1, col=1)

for i in range(len(limits)):
    lim = limits[i]
    df_sub = raw.loc[(raw["totale_casi"] >= lim[0]) & (raw["totale_casi"] <= lim[1])]
    fig.add_trace(go.Scatter(
        x = df_sub['long'],
        y = df_sub['lat'],
        text = df_sub['text'],
        mode='markers',
        marker = dict(size=df_sub['totale_casi']/scale,color = colors[i],sizemode = 'area'),
        name = '{0} - {1}'.format(lim[0],lim[1])), row=1, col=1)
    

fig.add_trace(go.Scatter(x=raw_and.data,y=raw_and.totale_casi,name="totale casi",line=dict(width=1.8)), row=1, col=2)

fig.update_layout(width=1800,  height=1000, autosize=True, showlegend = True, 
                  template = "plotly_white",
                  xaxis={"visible": False}, 
                  yaxis={"visible": False})

plot(fig, filename='map_province.html')







