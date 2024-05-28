import streamlit as st
from streamlit_searchbox import st_searchbox
from streamlit_modal import Modal

st.set_page_config(
    page_title="Winedex - Vitigni", page_icon=":wine_glass:", layout='wide'
)
st.markdown(f"""
    <style>
        .reportview-container .main .block-container{{
            padding-top: {0}rem;
        }}
    </style>""",
    unsafe_allow_html=True,
)

from settings import grapes_dict
from src.grape_view import get_grape_wine_region_summary, get_grape_info, get_linked_regions, insert_grape_description
from src.plots import plot_geographical_references

edit_description_modal = Modal(
    "Edit Description", 
    key="edit-description",
)

def main():
    grape_options = (list(grapes_dict.values()))
    selected_grape_code = st_searchbox(
        search_vitigno,
        key="Cerca Vitigno",
    )
    if selected_grape_code:
        grape_wine_region_summary = get_grape_wine_region_summary(selected_grape_code)
        linked_wines = grape_wine_region_summary[["wine_region","region","nome","produttore","annata","punteggio"]]
        grape_info = get_grape_info(selected_grape_code)
        col1, col2 = st.columns([1,1])
        with col1:
            st.markdown("**Riferimenti Geografici**")
            if not grape_wine_region_summary.empty:
                fig = plot_geographical_references(grape_wine_region_summary)
                st.plotly_chart(fig, use_container_width=True)  # Adjusted to use_container_width
            else:
                st.markdown("Nessun riferimento geografico rilevato.")
        with col2:
            st.markdown("**Riferimenti in Cantina**")
            if not linked_wines.empty:
                st.table(linked_wines[["nome","produttore","annata","punteggio"]].sort_values("punteggio", ascending=False))
            else:
                st.markdown("Nessun riferimento in cantina rilevato")
        if grape_info:
            with st.expander("Informazioni sul vitigno"):
                st.markdown(grape_info)
                update_info = st.button("Modifica Info")
                if update_info:
                    edit_description_modal.open()
        else:
            st.markdown("Nessuna informazione relativa al vitigno")
            add_info = st.button("Aggiungi Info")
            if add_info:
                edit_description_modal.open()
        
        if edit_description_modal.is_open():
            with edit_description_modal.container():
                description = st.text_area("Edit Text", grape_info, height=200)
                save = st.button("Save")
                cancel = st.button("Cancel")
                if save:
                    insert_grape_description(selected_grape_code,description)
                if save or cancel:
                    edit_description_modal.close()

# function with list of labels
def search_vitigno(searchterm: str):
    return [(g.lower().title(), idx) for idx, g in grapes_dict.items() if searchterm.upper() in g] if searchterm else []

if __name__ == "__main__":
    main()
