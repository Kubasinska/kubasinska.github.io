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
#Uploading Data
#Source --> https://github.com/pcm-dpc/COVID-19

def andamento_nazionale():
    raw = pd.read_json("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json")
    return raw

def province():
    raw_prov = pd.read_json("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json")
    all_prov = raw_prov.iloc[-128:]
    indexNames = all_prov[ all_prov['lat'] == 0 ].index
    all_prov.drop(indexNames , inplace=True)
    return all_prov

def regioni():
    raw_regioni = pd.read_json("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json")
    all_regioni = raw_regioni.iloc[-21:]
    return all_regioni

#%%

df_regioni = regioni()
df_province = province()
df_andamento = andamento_nazionale()

#%%

df_province['text'] = df_province['denominazione_provincia'] + '<br>Totale Casi ' + (df_province['totale_casi']).astype(str)
df_regioni['text'] = df_regioni['denominazione_regione'] + '<br>Totale Casi ' + (df_regioni['totale_casi']).astype(str)
limits_prov = [(0, 50), (50, 100), (100, 200), (200, 300), (300, 5000)]
limits_regioni = [(0, 50), (50, 100), (100, 200), (200, 300), (300, 5000)]
colors = ["lightseagreen", "royalblue", "#e377c2", "orange", "crimson"]
cities = []
scale_factor = 2

#%%

# Load and read the geojson file for Italy's provinces.
italy_prov_url = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_provinces.geojson"
with urllib.request.urlopen(italy_prov_url) as url_prov:
    jdata_prov = json.loads(url_prov.read().decode())

pts_prov = []  # list of points defining boundaries of polygons
for feature_prov in jdata_prov['features']:
    if feature_prov['geometry']['type'] == 'Polygon':
        pts_prov.extend(feature_prov['geometry']['coordinates'][0])
        pts_prov.append([None, None])  # mark the end of a polygon

    elif feature_prov['geometry']['type'] == 'MultiPolygon':
        for polyg_prov in feature_prov['geometry']['coordinates']:
            pts_prov.extend(polyg_prov[0])
            pts_prov.append([None, None])  # end of polygon
    elif feature_prov['geometry']['type'] == 'LineString':
        points_prov.extend(feature_prov['geometry']['coordinates'])
        points_prov.append([None, None])
    else:
        pass

x_prov, y_prov = zip(*pts_prov)

# Load and read the geojson file for Italy's regions.
italy_region_url = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"
with urllib.request.urlopen(italy_region_url) as url_region:
    jdata_region = json.loads(url_region.read().decode())

pts_region = []  # list of points defining boundaries of polygons
for feature_region in jdata_region['features']:
    if feature_region['geometry']['type'] == 'Polygon':
        pts_region.extend(feature_region['geometry']['coordinates'][0])
        pts_region.append([None, None])  # mark the end of a polygon

    elif feature_region['geometry']['type'] == 'MultiPolygon':
        for polyg_region in feature_region['geometry']['coordinates']:
            pts_region.extend(polyg_region[0])
            pts_region.append([None, None])  # end of polygon
    elif feature_region['geometry']['type'] == 'LineString':
        points_region.extend(feature_region['geometry']['coordinates'])
        points_region.append([None, None])
    else:
        pass

x_region, y_region = zip(*pts_region)

#%%

fig = make_subplots(rows=3, cols=2,
                    vertical_spacing=0.030,
                    specs=[[{"type": "scatter"}, {"type": "scatter"}],
                           [{"colspan": 2}, None],
                           [{"colspan": 2}, None]], subplot_titles=(""))


fig.add_trace(go.Scatter(x=x_region, y=y_region, mode='lines', line_color='#999999', line_width=1.5, showlegend=False), row=1, col=1)



fig.add_trace(go.Scatter(x=x_prov, y= y_prov, mode='lines', line_color='#999999', line_width=1.5, showlegend=False), row=1, col=2)



for i in range(len(limits_prov)):
    lim = limits_prov[i]
    df_sub_province = df_province.loc[(df_province["totale_casi"] >= lim[0]) & (df_province["totale_casi"] <= lim[1])]
    fig.add_trace(go.Scatter(
        x=df_sub_province['long'],
        y=df_sub_province['lat'],
        text=df_sub_province['text'],
        mode='markers',
        marker=dict(size=df_sub_province['totale_casi'] / scale_factor, color=colors[i], sizemode='area'),
        name='{0} - {1}'.format(lim[0], lim[1]), showlegend=False), row=1, col=2)


for i in range(len(limits_regioni)):
    lim = limits_regioni[i]
    df_sub_regioni = df_regioni.loc[(df_regioni["totale_casi"] >= lim[0]) & (df_regioni["totale_casi"] <= lim[1])]
    fig.add_trace(go.Scatter(
        x=df_sub_regioni['long'],
        y=df_sub_regioni['lat'],
        text=df_sub_regioni['text'],
        mode='markers',
        marker=dict(size=df_sub_regioni['totale_casi'] / scale_factor, color=colors[i], sizemode='area'),
        name='{0} - {1}'.format(lim[0], lim[1])), row=1, col=1)


fig.update_layout(width=800,  height=1200, autosize=True, showlegend = True, template = "plotly_white", xaxis={"visible": False}, yaxis={"visible": False})

fig.add_trace(go.Scatter(x=df_andamento["data"], y= df_andamento["totale_casi"], mode='lines', line_width=1.5), row=2, col=1)

fig.add_trace(go.Scatter(x=df_andamento["data"], y= df_andamento["deceduti"], mode='lines', line_width=1.5), row=3, col=1)


plot(fig)
