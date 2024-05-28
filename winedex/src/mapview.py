import os
import numpy as np
import pandas as pd
import geopandas as gpd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import Draw
from src.raw_connections import get_raw_db_conn


from settings import shapes_path, country_ids, region_ids
from src.wine_region_layer import list_wine_regions, get_wine_region_stats

sns.set_theme(style="whitegrid", palette="pastel", color_codes=True) 
sns.mpl.rc("figure", figsize=(10,6))

def get_contours_data(country):
    query=f"""
    SELECT rg.region_name, rg.geometry FROM app.regions rg WHERE rg.country_id = {country_ids[country][0]}; 
    """
    with get_raw_db_conn() as db_engine:
        data = gpd.GeoDataFrame.from_postgis(query, db_engine, geom_col='geometry', crs=4326)
    return data
    
class MapView:

    def __init__(self, country, region=None) -> None:
        self.country = country
        self.region = region
        self.plot_cities = False
        self.contours_data = get_contours_data(country)
       
        if region: 
            try: 
                self.wine_region_data = list_wine_regions(region_id=region_ids[region][0])
                if not self.wine_region_data.empty:    
                    wine_region_stats = get_wine_region_stats(self.wine_region_data['wine_region_id'].to_list())
                    self.wine_region_data = self.wine_region_data.set_index('wine_region_id').join(wine_region_stats.set_index('wine_region_id'), how='left', rsuffix='_r')
                    self.wine_region_data = self.wine_region_data[self.wine_region_data.columns[~self.wine_region_data.columns.str.endswith('_r')]]
                    self.docg_data = self.wine_region_data[self.wine_region_data['wine_region_type'] == 'DOCG']
                    self.wine_region_data = self.wine_region_data[self.wine_region_data['wine_region_type'] == 'Subregion']
                else:
                    self.docg_data = gpd.GeoDataFrame()
                    self.wine_region_data = gpd.GeoDataFrame()
            except ValueError:
                self.docg_data = gpd.GeoDataFrame()
                self.wine_region_data = gpd.GeoDataFrame()
        else:
            self.docg_data = gpd.GeoDataFrame()
            self.wine_region_data = gpd.GeoDataFrame()

    def plot_contours(self):
        contours_index = self.contours_data.region_name == self.region
        if sum(contours_index)>0:
            m = self.contours_data[contours_index].explore(name="Contours", tiles="OpenStreetMap", labels=False)
        else:
            m = self.contours_data.explore(name="Contours", tiles="OpenStreetMap", labels=False)
        return m

    def plot_subareas(self, m, data, name):
        layer_group = folium.FeatureGroup(name=name)
        color_map = {}
        # Iterate over each subarea and add it to the layer group with a unique color
        for _, row in data.iterrows():
            subarea = row['geometry']
            # Create a color dictionary to assign a unique color to each subarea
            color = f'hsl({_ * (360 // len(data["geometry"].unique()))}, 90%, 60%)'
            color_map[row['wine_region_name']]=color
            folium.GeoJson(
                gpd.GeoDataFrame.from_dict({_:row.to_dict()}, orient='index', crs='EPSG:4326').to_crs(epsg='4326').to_json(),
                style_function=lambda feature, color=color: {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.5
                },
                tooltip = folium.features.GeoJsonTooltip(fields=['wine_region_name','wine_count', 'best_wine', 'best_produttore', 'best_punteggio', 'avg_punteggio'],
                                            aliases=["", "Vini in Cantina", "Miglior Vino", "Miglior Produttore ", "Miglior Punteggio", "Punteggio Medio"],
                                            sticky=True
                                            ), 
                show=True
            ).add_to(layer_group)

        layer_group.add_to(m)
        # Create a custom legend with area names and colors
        legend_html = '<div style="position:fixed; bottom:10px; left:10px; z-index:9999; background-color:white; padding:6px; border-radius:4px; border:1px solid gray;">'
        legend_html += '<b>Legend</b><br>'
        for area, color in color_map.items():
            legend_html += f'<div style="margin-bottom: 5px;"><span style="display:inline-block; width: 15px; height: 15px; background-color:{color}; border: 1px solid black;"></span> {area}</div>'
        legend_html += '</div>'

        # Add the legend to the map
        m.get_root().html.add_child(folium.Element(legend_html))
        

    def plot(self):
        plt.clf()
        m = self.plot_contours()
        if self.region:
            Draw(export=True).add_to(m)
        if not self.wine_region_data.empty:
            self.plot_subareas(m, self.wine_region_data, 'SubRegion')
        if not self.docg_data.empty:
            self.plot_subareas(m, self.docg_data, 'DOCG')
        
        # Add layers to the map and set overlay parameter to False for default selection
        layer_control = folium.LayerControl(position='topleft', collapsed=True)
        layer_control.add_to(m)
        
        return m
