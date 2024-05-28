import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

def plot_geographical_references(data):
    fig = px.sunburst(
        data.groupby(['region', 'wine_region']).mean("punteggio").reset_index(),
        path=['region', 'wine_region'],
        values='punteggio',
        hover_name="punteggio",
        hover_data={"punteggio":True},
        custom_data='punteggio'
    )
    fig.update_traces(hovertemplate='Punteggio Medio: %{value:.2f}<br>')
    return fig


def plot_perfume_and_quality(data):
    perfume_columns = ['o_fruttato', 'o_floreale', 'o_vegetale', 'o_minerale', 'o_erbe_aromatiche',
                       'o_speziato', 'o_tostato', 'o_balsamico', 'o_etereo']
    quality_columns = {'o_qualita': 'Qualita', 'o_complessita': 'Complessita', 'g_equilibrio': 'Equilibrio',
                       'g_persistenza': 'Persistenza', 'g_dimensione': 'Dimensione'}
    
    # Calculate the number of perfume families
    data = data.set_index(["nome","produttore","annata"])
    data['N° Profumi'] = data[perfume_columns].sum(axis=1)

    # Melt the DataFrame for Plotly Express
    stacked_data_melted = pd.concat([data[['N° Profumi']], data[quality_columns.keys()]], axis=1)

    # Renaming Columns
    stacked_data_melted.columns = [quality_columns.get(c, c) for c in stacked_data_melted.columns]

    # Plot the stacked polar chart
    fig = px.line_polar(stacked_data_melted, line_group=data.index, color=data.index,
                        line_close=True, title='Wine Perfume Composition and Quality Indicators')
    
    return fig