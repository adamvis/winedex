import streamlit as st

from src.raw_connections import get_raw_db_conn, insert_dict_sample


def get_region_description(region_id):
    db_conn = st.connection("db", type="sql",ttl=1)
    return db_conn.query(f"SELECT region_name, description FROM app.regions rg WHERE rg.region_id = {region_id}")["description"].to_list()[0]
    

def insert_region_description(region_id, region_description):
    insert_object = {"region_id":region_id,"description":region_description}
    with get_raw_db_conn() as db_engine:
        insert_dict_sample(insert_object, 'app.regions', db_engine, upsert=True)