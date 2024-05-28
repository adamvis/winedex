import streamlit as st
from streamlit_modal import Modal
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Winedex - Terroirs", page_icon=":wine_glass:", layout='wide'
)
st.markdown(f"""
    <style>
        .reportview-container .main .block-container{{
            padding-top: {0}rem;
        }}
    </style>""",
    unsafe_allow_html=True,
)

from src.mapview import MapView
from settings import countries_options, region_ids

from src.wine_region_layer import create_wine_region
from src.regions_view import get_region_description, insert_region_description

area_properties_modal = Modal(
    "Save Area", 
    key="save-area",
)
area_delete_modal = Modal(
    "Delete Area", 
    key="delete-area",
)

edit_description_modal = Modal(
    "Edit Description", 
    key="edit-description"
)


def main():
    col1, col2 = st.columns([4,6])

    with col1:
        col3, col4 = st.columns([1,1])
        with col3:
            selected_country = st.selectbox(
                        label="Select a country",
                        options=countries_options,
                        index=5
                    )
            
            save_area = st.button(label='Save Area')
            # area_delete = st.button(label='Delete Area')
        with col4:
            region_options = [None]
            if ro:=countries_options.get(selected_country):
                region_options = region_options + ro
            selected_region = st.selectbox(
                        label="Select a region",
                        options=region_options
                    )
            if selected_region:
                description = get_region_description(region_ids[selected_region][0])
                if (description is None) or (description==''):
                    modify_description = st.button(label='Create Description')
                else:
                    modify_description = st.button(label='Modify Description')
            else:
                description = None
                modify_description = False

        if description:   
            with st.expander("Dettagli"):
                st.markdown(description)

    with col2:
        mv = MapView(selected_country, region=selected_region)
        returned_data = st_folium(mv.plot(), use_container_width=True, height=500, returned_objects=['last_active_drawing','last_object_clicked_tooltip'])
    
    # if area_delete and (returned_data['last_object_clicked_tooltip'] is not None):
    #     area_delete_modal.open()
    # if area_delete_modal.is_open():
    #     with area_delete_modal.container():
    #         st.markdown(f"Are you sure you want to delete {1} area?")
    #         proceed = st.button("Delete")
    #         abort = st.button("Cancel")

    #         if proceed:
    #             pass
    #         else:
    #             pass
    
    if save_area and (returned_data['last_active_drawing'] is not None):
        area_properties_modal.open()
    if area_properties_modal.is_open():
        with area_properties_modal.container():
            wine_region_name = st.text_input("Name")
            wine_region_type = st.radio("Area Type", ["Subregion","DOCG"])
            proceed = st.button("Save")
            abort = st.button("Cancel")
        
            if proceed:
                new_area_object = {
                    "geometry":returned_data['last_active_drawing']['geometry'] ,
                    "wine_region_name": wine_region_name, 
                    "wine_region_type": wine_region_type, 
                    "region_id":region_ids[selected_region][0]
                }
                wr_id = create_wine_region(new_area_object)
                area_properties_modal.close()
            elif abort:
                returned_data['last_active_drawing'] = None
                area_properties_modal.close()
                
    if modify_description:
            edit_description_modal.open()
    if edit_description_modal.is_open():
        with edit_description_modal.container():
            desc = st.text_area("Edit Text", description, height=200)
            save = st.button("Save")
            cancel = st.button("Cancel")
            if save:
                insert_region_description(region_ids[selected_region][0], desc)
            if save or cancel:
                edit_description_modal.close()
    
                    
    

if __name__ == "__main__":
    main()
