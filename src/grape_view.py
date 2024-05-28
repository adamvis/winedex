import pandas as pd
import streamlit as st

from settings import db_conn
from src.raw_connections import get_raw_db_conn, insert_dict_sample

def get_grape_wine_region_summary(grape_code):
    if grape_code:
        query = f"""
            SELECT * 
            FROM app.grape_wine_region_summary gw
            WHERE gw.grape_code = {grape_code};
        """
        db_conn = st.connection("db", type="sql",ttl=1)
        data = db_conn.query(query, ttl=1)
    else:
        data = pd.DataFrame()
    return data

def get_grape_info(grape_code):
    if grape_code:
        try:
            description = get_grape_description(grape_code)['description'].to_list()[0]
        except IndexError:
            description = None
        return description

def get_linked_regions(grape_name):
    return pd.DataFrame()

def get_grape_description(grape_code):
    return db_conn.query(f"SELECT description FROM app.grapes_descriptions gd WHERE gd.grape_code = {grape_code}")

def insert_grape_description(grape_code, grape_description):
    insert_object = {"grape_code":grape_code,"description":grape_description}
    with get_raw_db_conn() as db_engine:
        insert_dict_sample(insert_object, 'app.grapes_descriptions', db_engine, upsert=True)
    
