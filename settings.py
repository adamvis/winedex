
import os

import toml
import streamlit as st

data_path = 'data'
shapes_path = os.path.join(data_path, 'shapes')
countries_path = os.path.join(shapes_path, 'countries')
descriptions_path = os.path.join(data_path, 'descriptions')

def create_options_dict(data, key_column, option_column, distinct=True):
    key_option_dict = {}
    for idx, row in data.iterrows():
        key_name = row[key_column]
        option_name = row[option_column]

        if key_name in key_option_dict:
            key_option_dict[key_name].append(option_name)
        else:
            key_option_dict[key_name] = [option_name]
            
    if distinct:
        key_option_dict = {k:list(set(o)) for k, o in key_option_dict.items()}
            
    return key_option_dict
            
db_conn = st.connection("db", type="sql")
with open(".streamlit/secrets.toml", "r") as file:
    db_config = toml.load(file)["connections"]['db']


def get_grapes_dict():
    grapes_dict = db_conn.query(
        'SELECT distinct grape_code, grape FROM app.grapes;'
        ).set_index("grape_code").to_dict()['grape']
    return grapes_dict

def get_country_region_data():
    country_region_data = db_conn.query("""
        SELECT 
            distinct ct.country_id, 
            ct.country_name, 
            rg.region_id,
            rg.region_name,
            wr.wine_region_id, 
            wr.wine_region_name
        FROM 
            app.countries ct 
            LEFT JOIN app.regions rg 
            ON ct.country_id=rg.country_id
            left join app.wine_regions wr
            on rg.region_id =wr.region_id;
        """)
    return country_region_data

def get_regions_dict(country_region_data):
    regions_dict = country_region_data[["region_name","region_id"]].dropna().drop_duplicates().set_index("region_id").to_dict()['region_name']
    return regions_dict

def get_countries_options(country_region_data):
    countries_options = create_options_dict(country_region_data, "country_name", "region_name", distinct=True)
    return countries_options

def get_country_ids(country_region_data):
    country_ids = create_options_dict(country_region_data, "country_name", "country_id", distinct=True)
    return country_ids

def get_region_ids(country_region_data):
    region_ids = create_options_dict(country_region_data, "region_name", "region_id", distinct=True)
    return region_ids

grapes_dict = get_grapes_dict()
country_region_data = get_country_region_data()
regions_dict = get_regions_dict(country_region_data)
country_ids = get_country_ids(country_region_data)
region_ids = get_region_ids(country_region_data)
countries_options = get_countries_options(country_region_data)

def get_regions_options():
    data = db_conn.query("""
    SELECT 
        rg.region_name,
        wr.wine_region_name
    FROM 
        app.regions rg 
        left join app.wine_regions wr
        on rg.region_id =wr.region_id;
    """)
    regions_options = create_options_dict(data, "region_name", "wine_region_name", distinct=True)
    return regions_options

def get_wine_regions_dict():
    data = db_conn.query("""
    SELECT distinct 
        wr.wine_region_id, 
        wr.wine_region_name
    FROM 
        app.wine_regions wr
    """)
    
    wine_regions_dict = data[["wine_region_name","wine_region_id"]].dropna().drop_duplicates().set_index("wine_region_id").to_dict()['wine_region_name']
    return wine_regions_dict