import folium
from folium import Choropleth
import geopandas as gpd
import pandas as pd
import numpy as np
import branca.colormap as cm

contagi = pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv')
province = gpd.read_file('https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_provinces.geojson')

province

date=list(contagi.data.unique())
contagi_cln=contagi.loc[(contagi.data==date[-1])&(contagi.denominazione_provincia!='In fase di definizione/aggiornamento')]

contagi_cln


sigle_pr=province.prov_acr.unique()
sigle_con=contagi_cln.sigla_provincia.unique()
list_dif = [i for i in sigle_pr if i not in sigle_con]    

list_dif

sigle_con

province.sort_values('prov_acr',axis=0,inplace=True)

province

contagi_cln.sigla_provincia.fillna('NA',inplace=True)

contagi_cln.sort_values("sigla_provincia", axis = 0, inplace=True)
contagi_cln

province_plt = province[["prov_acr", "geometry"]].set_index("prov_acr")
province_plt

contagi_dict=pd.Series(contagi_cln.totale_casi.values,index=contagi_cln['sigla_provincia'])
contagi_dict


linear = cm.linear.Paired_06.scale(contagi_cln.totale_casi.min(), contagi_cln.totale_casi.max()).to_step(n=15)
linear.caption = 'Numero di contagiati per provincia'
linear

cm.linear

m = folium.Map(location=[42.351032,14.167546], tiles='cartodbpositron', zoom_start=5)

folium.GeoJson(
    province_plt,
    style_function=lambda feature: {
    'fillColor': linear(contagi_dict[feature['id']]),
    'opacity':1,
    'fill_opacity':0.9,
    'color' : 'black',
    'weight' : 0.3,
    'dashArray' : 0,
        }
    ).add_to(m)
for idx, row in contagi_cln.iterrows():
    popup = 'Nella provincia di {} si sono registrati {} casi'.format(str(contagi_cln.denominazione_provincia.loc[idx]),
                                                                      str(contagi_cln.totale_casi.loc[idx]))
    folium.Marker([row['lat'], row['long']],
                        radius=5, color='green', opacity=0.6,
                 tooltip=popup).add_to(m)
m.add_child(linear)
m

m.save('province_interattiva_marker.html')


