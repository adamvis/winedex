

from settings import grapes_dict
from src.raw_connections import get_raw_db_conn, insert_dict_sample, delete_rows


from streamlit_modal import Modal

compare_modal = Modal(
    "Compare Wines", 
    key="compare",
)

def create_wine(wine_obj, vitigni, return_punteggio=False):
    
    punteggio = wine_obj["o_complessita"] + wine_obj["o_qualita"] + wine_obj["g_equilibrio"] + wine_obj["g_persistenza"] + wine_obj["g_qualita"] + wine_obj["g_dimensione"]
    query = f"""
        INSERT INTO app.wines (
        "nome","produttore","annata","alchol","v_colore","v_riflesso","v_densita","v_limpidezza","v_vivacità","v_perlage","o_fruttato","o_floreale","o_vegetale","o_minerale","o_erbe_aromatiche","o_speziato","o_tostato","o_balsamico","o_etereo","o_note","o_complessita", 
        "o_qualita","g_zucchero","g_alcol","g_acido","g_tannino","g_equilibrio","g_persistenza","g_sapido","g_chiusura","g_qualita","g_dimensione","prospettive_di_consumo","punteggio"
    ) 
    VALUES (
        '{wine_obj["nome"]}',
        '{wine_obj["produttore"]}',
        {wine_obj["annata"]},
        {wine_obj["alchol"]},
        '{wine_obj["v_colore"]}',
        '{wine_obj["v_riflesso"]}',
        '{wine_obj["v_densita"]}',
        '{wine_obj["v_limpidezza"]}',
        '{wine_obj["v_vivacità"]}',
        '{wine_obj["v_perlage"]}',
        {wine_obj["o_fruttato"]},
        {wine_obj["o_floreale"]},
        {wine_obj["o_vegetale"]},
        {wine_obj["o_minerale"]},
        {wine_obj["o_erbe_aromatiche"]},
        {wine_obj["o_speziato"]},
        {wine_obj["o_tostato"]},
        {wine_obj["o_balsamico"]},
        {wine_obj["o_etereo"]},
        '{wine_obj["o_note"]}',
        {wine_obj["o_complessita"]},
        {wine_obj["o_qualita"]},
        '{wine_obj["g_zucchero"]}',
        '{wine_obj["g_alcol"]}',
        '{wine_obj["g_acido"]}',
        '{wine_obj["g_tannino"]}',
        {wine_obj["g_equilibrio"]},
        {wine_obj["g_persistenza"]},
        '{wine_obj["g_sapido"]}',
        '{wine_obj["g_chiusura"]}',
        {wine_obj["g_qualita"]},
        {wine_obj["g_dimensione"]},
        '{wine_obj["prospettive_di_consumo"]}',
        {punteggio}
    ) RETURNING wine_id;
    """
    
    wine_obj['punteggio']=punteggio
    
    with get_raw_db_conn() as db_engine:
        id = insert_dict_sample(wine_obj, 'app.wines',  db_engine, return_creation_id=True)
    
    for k,v in grapes_dict.items():
        if v in [i.upper() for i in vitigni]:
            insert_dict_sample({"wine_id":id,"grape_code":k}, 'app.grapes_wines', db_engine)
    
    if return_punteggio:
        return punteggio


def list_wine():
    query="""
    SELECT * from app.wines;
    """
    db_conn = st.connection("db", type="sql",ttl=1)
    data = db_conn.query(query, ttl=1)
    return data

def update_wine():
    pass

def delete_wine(wine_ids):
    with get_raw_db_conn() as db_engine:
        try:
            delete_rows(db_engine, 'app.grapes_wines', wine_ids)
        except IndexError:
            pass

import streamlit as st

@st.cache_data
def dataframe_with_selections(df):
    df_with_selections = df[["nome","produttore","annata","punteggio"]].astype(str).copy()
    df_with_selections.insert(0, "✔", False) 
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"✔": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
        height=min(200, int((len(df_with_selections.reset_index(drop=True))+1) * 35.5)),
        use_container_width = True
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df['✔']]
    
    return selected_rows, df.loc[selected_rows.index]