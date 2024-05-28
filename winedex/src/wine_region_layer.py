import pandas as pd
import geopandas as gpd
import shapely.geometry as sg

from src.raw_connections import get_raw_db_conn


def create_wine_region(wine_obj):
    wine_obj['geometry'] = sg.Polygon(wine_obj['geometry']['coordinates'][0])
    with get_raw_db_conn() as db_engine:
        gpd.GeoDataFrame.from_dict([wine_obj],geometry='geometry', crs=4326).to_postgis('wine_regions', db_engine, 'app', if_exists='append')
    return None


def list_wine_regions(region_id=None):
    query="""
    SELECT * from app.wine_regions ORDER BY wine_region_id;
    """
    if region_id is not None:
        query = query.replace(" ORDER BY wine_region_id;",f" WHERE region_id={region_id} ORDER BY wine_region_id;")
    with get_raw_db_conn() as db_engine:
        data = gpd.GeoDataFrame.from_postgis(query, db_engine, geom_col='geometry', crs=4326)
    return data

def get_wine_region_stats(wine_region_ids):
    if len(wine_region_ids)== 1:
        query=f"""
        SELECT * from app.wine_region_summary wrs WHERE wrs.wine_region_id = {wine_region_ids[0]};
        """
        
    else:
        query=f"""
        SELECT * from app.wine_region_summary wrs WHERE wrs.wine_region_id IN {tuple(wine_region_ids)};
        """
    with get_raw_db_conn() as db_engine:
        data = pd.read_sql_query(query, db_engine)
    return data

def update_wine_region():
    pass

def delete_wine_region(wine_region_ids):
    with get_raw_db_conn() as db_engine:
        wine_region_ids(db_engine, 'app.wine_regions', wine_region_ids)

