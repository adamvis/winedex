import streamlit as st
from streamlit_tags import st_tags
from streamlit_searchbox import st_searchbox

st.set_page_config(
    page_title="Winedex - Cantina", page_icon=":wine_glass:", layout='wide'
)
st.markdown(f"""
    <style>
        .reportview-container .main .block-container{{
            padding-top: {0}rem;
        }}
    </style>""",
    unsafe_allow_html=True,
)

from src.wine_layer import create_wine, delete_wine, list_wine, dataframe_with_selections, compare_modal
from src.plots import plot_perfume_and_quality
from settings import grapes_dict, regions_dict, countries_options, get_regions_options, get_wine_regions_dict

import datetime as dt
map_dimensione = {
    "Strutturato":3,
    "Sottile":3,
    "Distinto":4,
    "Suggestivo":5
}


regions_options = get_regions_options()
wine_regions_dict = get_wine_regions_dict()

def main():
    
    listed_wines = list_wine()
    
    col1, col2 = st.columns([4,1])
    with col1:   
        selected_rows, selected_wines = dataframe_with_selections(listed_wines.set_index("wine_id"))
    with col2:
        st.button("Compare Selected", disabled=len(selected_rows)<2, on_click=compare_modal.open)
        st.button("Delete Selected", disabled=selected_rows.empty, on_click=delete_wine, kwargs={"wine_ids":selected_rows.index.to_list()})
    
    expander = st.expander("Aggiungi Vino")
    with expander:
        st.markdown("**Scheda di Degustazione**")
        cola, colb, colc = st.columns([1,1,1])
        with cola:
            country = st.selectbox(
                label="Country",
                options=countries_options,
                index=5,
            )
        with colb:
            # region_options = ([None] + countries_options[country])
            region_id = st_searchbox(
                lambda x:search_region(x,country),
                label="Regione",
                key="region-searchbox"
            )
            # wine_region_options = ([None] + region_options[regions_dict[region_id]])
        with colc:
            wine_region_id = st_searchbox(
                lambda x:search_wine_region(x,regions_dict[region_id]),
                label="Denominazione",
                key="wine-region-searchbox"
            )
        with st.form("wine_form", clear_on_submit=True):
            col1, col2, col3, col4 = st.columns([2,2,1,1])
            with col1:
                nome = st.text_area(label="Nome")
            with col2:
                produttore = st.text_area(label="Produttore")
            with col3:
                annata = st.number_input(label="Annata", min_value=1930, max_value=dt.date.today().year, step=1, value=2023)
            with col4:
                alchol = st.number_input(label="Alchol (%)", value=12.5, step=0.5)

            vitigni = st_tags([], suggestions=list(map(lambda x:x.lower().title(), grapes_dict.values())), label="Vititgni")
            st.markdown("------")
            v_colore = st.radio("**Colore**", ("Paglierino","Dorato","Aranciato","Cerasuolo","Ramato","Porpora","Rubino","Granato"), horizontal=True) 
            v_riflesso = st.radio("**Riflesso**", ("N/R","Verdolino","Dorato","Aranciato","Porpora","Granato"), horizontal=True)
            col5, col6, col7, col8 = st.columns([1,1,1,1])
            with col5:
                v_densita = st.radio("**Densità Cromatica**", ("Trasparente","Compatto"))
            with col6:
                v_limpidezza = st.radio("**Limpidezza**", ("Opaco","Limpido"))
            with col7:
                v_vivacità = st.radio("**Vivacità**", ("Cupo","Vivace","Luminoso"))
            with col8:
                v_perlage = st.radio("**Perlage**", ("N/R","Vivace","Fine"))
            
            st.markdown("------")
            st.markdown("**Profumi**")
            col9, col10, col11 = st.columns([1,1,1])
            with col9:
                o_fruttato = st.checkbox("Fruttato", label_visibility='visible')
                o_floreale = st.checkbox("Floreale", label_visibility='visible')
                o_vegetale = st.checkbox("Vegetale", label_visibility='visible')
                o_minerale = st.checkbox("Minerale", label_visibility='visible')
                o_erbe_aromatiche = st.checkbox("Erbe_aromatiche", label_visibility='visible')
            with col10:
                o_speziato = st.checkbox("Speziato", label_visibility='visible')
                o_tostato = st.checkbox("Tostato", label_visibility='visible')
                o_balsamico = st.checkbox("Balsamico", label_visibility='visible')
                o_etereo = st.checkbox("Etereo", label_visibility='visible')
            with col11:
                o_note = st.text_area("Note")
            
            col12, col13 = st.columns([1,1])
            with col12:
                o_complessita = st.slider("**Complessità Olfattiva**", min_value=12, max_value=16, step=1)
            with col13:
                o_qualita = st.slider("**Qualita Olfattiva**", min_value=14, max_value=20, step=1)
            
            col14, col15, col16, col17 = st.columns([1,1,1,1])
            with col14:
                g_zucchero = st.radio("**Zucchero**", ("Secco","Tendente al dolce","Dolce","Molto dolce"))
            with col15:
                g_alcol = st.radio("**Alcol**", ("Contenuto","Caldo","Più che caldo","Molto caldo"))
            with col16:
                g_acido = st.radio("**Acido**", ("Contenuto","Fresco","Più che Fresco","Molto Fresco"))
            with col17:
                g_tannino = st.radio("**Tannino**", ("N/R","Amaro","Vegetale","Maturo","Raffinato"))
            
            col18, col19 = st.columns([1,1])
            with col18:
                g_equilibrio = st.slider("**Equilibrio**", min_value=12, max_value=18, step=1)
                
            with col19:
                g_persistenza = st.slider("**Persistenza**", min_value=10, max_value=16, step=1)
            
            
            col20, col21 = st.columns([1,1])
            with col20:
                g_sapido = st.radio("**Sapidità percepita**", ("Non Avvertibile","Contenuto","Sapido","Più che Sapido"), horizontal=True)

            with col21:
                g_chiusura = st.radio("**Chiusura di bocca**", ("Imprecisa","Buona","Precisa","Elegante"), horizontal=True)
            
            st.markdown("------")
            col22, col23, col24 = st.columns([1,1,1])
            with col22:
                g_qualita = st.slider("**Qualità gustativa**", min_value=18, max_value=24, step=1)
            with col23:
                g_dimensione = map_dimensione[st.radio("**Dimensione**", ("Strutturato","Sottile","Distinto","Suggestivo"))]
            with col24:
                prospettive_di_consumo = st.radio("**Prospettive di consumo**", ("Da bere subito","Buone prospettive","Medie prospettive","Lunghe prospettive"))
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                submit_validated = True
                check_parameters = {"nome":nome,"produttore":produttore,"annata":annata,"alchol":alchol, "regione":region_id}
                for cp, v in check_parameters.items():
                    if v == '':
                        st.error(f"You are missing '{cp}' parameter")
                        submit_validated = False
                if submit_validated:
                    wine_obj = {
                        "nome":nome,"produttore":produttore,"annata":annata,"alchol":alchol,"v_colore":v_colore,"v_riflesso":v_riflesso,"v_densita":v_densita,"v_limpidezza":v_limpidezza,
                        "v_vivacità":v_vivacità,"v_perlage":v_perlage,"o_fruttato":o_fruttato,"o_floreale":o_floreale,"o_vegetale":o_vegetale,"o_minerale":o_minerale,"o_erbe_aromatiche":o_erbe_aromatiche,"o_speziato":o_speziato,
                        "o_tostato":o_tostato,"o_balsamico":o_balsamico,"o_etereo":o_etereo,"o_note":o_note,"o_complessita":o_complessita,"o_qualita":o_qualita,"g_zucchero":g_zucchero,"g_alcol":g_alcol,
                        "g_acido":g_acido,"g_tannino":g_tannino,"g_equilibrio":g_equilibrio,"g_persistenza":g_persistenza,"g_sapido":g_sapido,"g_chiusura":g_chiusura,"g_qualita":g_qualita,"g_dimensione":g_dimensione,
                        "prospettive_di_consumo":prospettive_di_consumo,"region_id":region_id,"wine_region_id":wine_region_id
                    }
                    punteggio = create_wine(wine_obj, vitigni, return_punteggio=True)
                    st.toast(f"Wine uploaded correctly! Final points: {punteggio}", icon='😍')
                # what will trigger one state or the other on re-run
            
    if compare_modal.is_open():
        with compare_modal.container():
            fig = plot_perfume_and_quality(selected_wines)
            st.plotly_chart(fig)
            finish = st.button("Finish")
            if finish:
                compare_modal.close()
    
# function with list of labels
def search_region(searchterm: str, country):
    filtered_options = dict(filter(lambda k: k[1] in countries_options[country], regions_dict.items()))
    return [(g.lower().title(), idx) for idx, g in filtered_options.items() if searchterm.upper() in g.upper()] if searchterm else []

def search_wine_region(searchterm: str, region):
    filtered_options = dict(filter(lambda k: k[1] in regions_options[region], wine_regions_dict.items()))
    return [(g.lower().title(), idx) for idx, g in filtered_options.items() if searchterm.upper() in g.upper()] if searchterm else []


if __name__ == "__main__":

    main()
