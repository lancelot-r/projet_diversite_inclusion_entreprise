from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from matplotlib import colormaps
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# Charger les données
df1 = pd.read_csv("data/salaire_effectifs.csv")
df2 = pd.read_csv("data/formation_evo.csv")
df3 = pd.read_csv("data/alternance.csv")
df4 = pd.read_csv("data/absence_conge_matpat.csv")
df5 = pd.read_csv("data/temps_partiel_final.csv")
df6 = pd.read_csv("data/maps.csv")
gdf1 = gpd.read_file("data/region.geojson")
gdf1.rename(columns={'nom': 'Région'}, inplace=True)
gdf1 = gdf1.merge(df6, on='Région', how='left')

# Extraire les évolutions uniques pour la liste déroulante
evolutions = df2["Evolution"].unique()
colleges = df1["Collège"].unique()
colleges_df4 = df4["Collège"].unique()
colleges_df5 = df5["Collège"].unique()
indicateur_df6 = ["Note Ecart rémunération", "Note Ecart taux de promotion", "Note Ecart taux d'augmentation (hors promotion)", 
                      "Note Ecart taux d'augmentation", "Note Ecart taux de promotion", "Note Hautes rémunérations",
                      "Note Retour congé maternité", "Note Index"]

app = Dash(suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1("Diversité et inclusion en entreprise évolution du bilan social chez EDF", style={'text-align': 'center', 'margin-top': '20px'}),

    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-7',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Disparité des effectifs femmes-hommes',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Formations et évolutions au sein de l\'entreprise',
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Contrats d\'apprentissage et d\'alternance',
                value='tab-3',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Evolution des prises de congés maternité / paternité',
                value='tab-4',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Proportion en temps partiel par genre',
                value='tab-5',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Indicateur',
                value='tab-6',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Tableau de bord',
                value='tab-7',
                className='custom-tab',
                selected_className='custom-tab--selected'
            )
        ]),
    html.Div(id='tabs-content-classes')
])

@callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'))

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
        html.H2("Disparité des effectifs et des salaires femmes-hommes", style={'text-align': 'center'}),
        dcc.Dropdown(
            id='effectifs-dropdown',
            options=[{'label': csp, 'value': csp} for csp in colleges],
            value=colleges[0],  # Valeur par défaut
            placeholder="Sélectionnez une catégorie socio-professionnelle"
        ),
        html.Div(id='graphs-container_1', style={'display': 'flex', 'justify-content': 'space-around', 'margin-top': '20px'})
    ], style={'padding': '20px', 'border-bottom': '2px solid #ccc'})

    elif tab == 'tab-2':
        return html.Div([
        html.H2("Évolution des formations", style={'text-align': 'center'}),
        dcc.Dropdown(
            id='evolution-dropdown',
            options=[{'label': evolution, 'value': evolution} for evolution in evolutions],
            value=evolutions[0],  # Valeur par défaut
            placeholder="Sélectionnez une évolution"
        ),
        html.Div(id='graphs-container_2', style={'display': 'flex', 'justify-content': 'space-around', 'margin-top': '20px'})
    ], style={'padding': '20px', 'border-bottom': '2px solid #ccc'})
    
    elif tab == 'tab-3':
        return html.Div([
        html.H2("Évolution des contrats d'alternance", style={'text-align': 'center'}),
        html.Div(id='graphs-container_3', style={'display': 'flex', 'justify-content': 'space-around', 'margin-top': '20px'})
    ], style={'padding': '20px'})

    elif tab == 'tab-4':
        return html.Div([
        html.H2("Evolution des prises de congés maternité / paternité", style={'text-align': 'center'}),
        dcc.Dropdown(
            id='conges-dropdown',
            options=[{'label': csp, 'value': csp} for csp in colleges_df4],
            value=colleges_df4[0],  # Valeur par défaut
            placeholder="Sélectionnez une catégorie socio-professionnelle"
        ),
        html.Div(id='graphs-container_4', style={'display': 'flex', 'justify-content': 'space-around', 'margin-top': '20px'})
    ], style={'padding': '20px', 'border-bottom': '2px solid #ccc'})
    
    elif tab == 'tab-5':
        return html.Div([
        html.H2("Proportion en temps-partiel par genre", style={'text-align': 'center'}),
        dcc.Dropdown(
            id='temps_partiel-dropdown',
            options=[{'label': csp, 'value': csp} for csp in colleges_df5],
            value=colleges_df5[0],  # Valeur par défaut
            placeholder="Sélectionnez une catégorie socio-professionnelle"
        ),
        html.Div(id='graphs-container_5', style={'display': 'flex', 'justify-content': 'space-around', 'margin-top': '20px'})
    ], style={'padding': '20px', 'border-bottom': '2px solid #ccc'})

    elif tab == 'tab-6':
        return html.Div([
        html.H2("Indicateur", style={'text-align': 'center'}),
        dcc.Dropdown(
            id='indicateur-dropdown',
            options=[{'label': indicateur, 'value': indicateur} for indicateur in indicateur_df6],
            value=indicateur_df6[0],  # Valeur par défaut
            placeholder="Sélectionnez un indicateur"
        ),
        html.Div(id='graphs-container_6', style={'display': 'flex', 'justify-content': 'space-around', 'margin-top': '20px'})
    ], style={'padding': '20px', 'border-bottom': '2px solid #ccc'})

    elif tab == 'tab-7':
        return html.Div([
        html.H2("Tableau de bord de l'évolution par genre chez EDF SA", style={'text-align': 'center'}),
        html.Div(id='graphs-container_7', style={'display': 'flex', 'justify-content': 'space-around', 'margin-top': '20px'})
    ], style={'padding': '20px'})


@app.callback(
        Output('graphs-container_1', 'children'),
        Input('effectifs-dropdown', 'value')
)

# Graphique Tab 1 : Disparité des effectifs femmes-hommes
def update_graphs(selected_csp):

    filtered_df1 = df1[df1["Collège"] == selected_csp]

    fig_effectifs = px.bar(
        filtered_df1,
        x="Année",
        y="Nombre de salariés",
        color="Genre",
        title=f"Évolution de la masse salariale - {selected_csp}",
        barmode="group",
        text_auto='.2s',
        labels={'Nombre de salariés':'Nombre d\'employés', 'Année':'Année'},
        color_discrete_map={
            'Homme': '#1b909a',  # Bleu
            'Femme': '#7900f1',  # Rose
        }
    )
    fig_effectifs.update_traces(
        hovertemplate="<b>Année :</b> %{x}<br><b>Nombre de salariés :</b> %{y:.0f}")
    
    fig_salaires = px.line(
        filtered_df1,
        x='Année',
        y="Salaire mensuel moyen (€, brut)",
        color="Genre",
        title=f"Évolution de la rémuneration moyenne - {selected_csp}",
        markers=True,
        color_discrete_map={
            'Homme': '#1b909a',  # Bleu
            'Femme': '#7900f1',  # Rose
        }
    )
    fig_salaires.update_traces(
        hovertemplate="<br><b>Année :</b> %{x}<br><b>Salaire mensuel moyen brut :</b> %{y:.2f}€")
    
    fig_salaires.update_layout(yaxis_range=[0, 8000], hovermode = "x unified")

    return [
        html.Div(dcc.Graph(figure=fig_effectifs), style={'width': '60%'}),
        html.Div(dcc.Graph(figure=fig_salaires), style={'width': '40%'})
    ]

@app.callback(
    Output('graphs-container_2', 'children'),
    Input('evolution-dropdown', 'value')
)

def update_graphs(selected_evolution):
    # Filtrer les données en fonction de l'évolution sélectionnée
    filtered_df2 = df2[df2["Evolution"] == selected_evolution]

    # Extraire les collèges uniques pour le titre
    college_df2 = filtered_df2["Collège"].unique()

    # Créer les graphiques
    fig_population_formee = px.line(
        filtered_df2,
        x='Année',
        y="Proportion d'employés formés (%)",
        color='Genre',
        title=f"Population formée - {college_df2}",
        labels={'Valeur': 'Valeur', 'Année': 'Année'},
        markers=True,
        color_discrete_map={
            'Homme': '#1b909a',  # Bleu
            'Femme': '#7900f1',  # Rose
        }
    )
    fig_population_formee.update_traces(
        hovertemplate="<br><b>Année :</b> %{x}<br><b>Proportion d'employés formés :</b> %{y:.2f}%")
    
    fig_nombre_evolutions = px.line(
        filtered_df2,
        x='Année',
        y="Proportion d'évolutions (%)",
        color='Genre',
        title=f"Evolutions - {selected_evolution}",
        labels={'Valeur': 'Valeur', 'Année': 'Année'},
        markers=True,
        color_discrete_map={
            'Homme': '#1b909a',  # Bleu
            'Femme': '#7900f1',  # Rose
        }
    )
    fig_nombre_evolutions.update_traces(
        hovertemplate="<br><b>Année :</b> %{x}<br><b>Proportion d'évolutions :</b> %{y:.2f}%")
    
    fig_population_formee.update_layout(yaxis_range=[0, 40], hovermode = "x unified")
    fig_nombre_evolutions.update_layout(yaxis_range=[0, 40], hovermode = "x unified")

    # Retourner les graphiques dans des divs côte à côte
    return [
        html.Div(dcc.Graph(figure=fig_population_formee), style={'width': '48%'}),
        html.Div(dcc.Graph(figure=fig_nombre_evolutions), style={'width': '48%'})
    ]

@app.callback(
    Output('graphs-container_3', 'children'),
    Input('tabs-with-classes', 'value')
)

def display_alternance_graphs(_):
    df3_apprentissage = df3[df3["Indicateur"] == "Contrats d'apprentissage conclus dans l'année"]
    df3_pro = df3[df3["Indicateur"] == "Contrats de professionnalisation conclus dans l'année"]

    fig_apprentissage = px.line(
        df3_apprentissage,
        x='Année',
        y="Nombre de contrats",
        color="Genre",
        title="Évolution du nombre de contrats d'apprentissages",
        markers=True,
        color_discrete_map={
            'Homme': '#1b909a',  # Bleu
            'Femme': '#7900f1',  # Rose
        }
    )
    fig_apprentissage.update_traces(
        hovertemplate="<br><b>Année :</b> %{x}<br><b>Nombre de contrats :</b> %{y:.0f}")
    
    fig_professionnalisation = px.line(
        df3_pro,
        x='Année',
        y="Nombre de contrats",
        color="Genre",
        title="Évolution du nombre de contrats de professionnalisation",
        markers=True,
        color_discrete_map={
            'Homme': '#1b909a',  # Bleu
            'Femme': '#7900f1',  # Rose
        }
    )
    fig_professionnalisation.update_traces(
        hovertemplate="<br><b>Année :</b> %{x}<br><b>Nombre de contrats :</b> %{y:.0f}")
    
    fig_apprentissage.update_layout(yaxis_range=[0, 1500], hovermode = "x unified")
    fig_professionnalisation.update_layout(yaxis_range=[0, 1500], hovermode = "x unified")

    return [
        html.Div(dcc.Graph(figure=fig_apprentissage), style={'width': '48%'}),
        html.Div(dcc.Graph(figure=fig_professionnalisation), style={'width': '48%'})
    ]

@app.callback(
        Output('graphs-container_4', 'children'),
        Input('conges-dropdown', 'value')
)

# Graphique Tab 1 : Disparité des effectifs femmes-hommes
def update_conges_graphs(selected_csp):

    filtered_df4 = df4[df4["Collège"] == selected_csp]

    fig_conges_femme = px.bar(
        filtered_df4,
        x="Année",
        y="Nombre d'heures moyen de congé maternité par salariée",
        title=f"Prise de congés maternité - {selected_csp}",
        text_auto='.2s',
        labels={"Nombre d'heures moyen de congé maternité par salariée":'Durée moyenne de congé maternité (heures)', 'Année':'Année'},
        color_discrete_sequence=["#7900f1"]
    )
    fig_conges_femme.update_traces(
        hovertemplate="<b>Année :</b> %{x}<br><b>Durée moyenne de congé maternité :</b> %{y:.0f}h")
    
    fig_conges_homme = px.bar(
        filtered_df4,
        x="Année",
        y="Nombre d'heures moyen de congé paternité par salarié",
        title=f"Prise de congés paternité - {selected_csp}",
        text_auto='.2s',
        labels={"Nombre d'heures moyen de congé paternité par salarié":'Durée moyenne de congé paternité (heures)', 'Année':'Année'},
        color_discrete_sequence=["#1b909a"]
    )
    fig_conges_homme.update_traces(
        hovertemplate="<b>Année :</b> %{x}<br><b>Durée moyenne de congé paternité :</b> %{y:.0f}h")
    
    fig_conges_homme.update_layout(yaxis_range=[0, 60])
    fig_conges_femme.update_layout(yaxis_range=[0, 60])

    return [
        html.Div(dcc.Graph(figure=fig_conges_femme), style={'width': '48%'}),
        html.Div(dcc.Graph(figure=fig_conges_homme), style={'width': '48%'})
    ]

@app.callback(
    Output('graphs-container_5', 'children'),
    Input('temps_partiel-dropdown', 'value')
)

def update_temps_partiel_graphs(selected_csp):

    filtered_df5 = df5[df5["Collège"] == selected_csp].round(2)

    # Créer les graphiques
    mosaicplot_2017 = px.treemap(
        filtered_df5[filtered_df5["Année"] == 2017],
        path=["Genre", "Metrique"],
        values="Valeur",
        color="Genre",
        title=f"Proportion d'employés en temps partiel par genre en 2017 - {selected_csp}",
        labels={'Valeur': 'Valeur', 'Année': 'Année'},
        color_discrete_map={
            'Homme': '#1b909a',
            'Femme': '#7900f1',
        }
    )
    mosaicplot_2017.update_traces(
        hovertemplate="%{label} : %{value:.0f} %")
    
    mosaicplot_2023 = px.treemap(
        filtered_df5[filtered_df5["Année"] == 2023],
        path=["Genre", "Metrique"],
        values="Valeur",
        color="Genre",
        title=f"Proportion d'employés en temps partiel par genre en 2023 - {selected_csp}",
        labels={'Valeur': 'Valeur', 'Année': 'Année'},
        color_discrete_map={
            'Homme': '#1b909a',
            'Femme': '#7900f1',
        },
    )
    mosaicplot_2023.update_traces(
        hovertemplate="%{label} : %{value:.0f} %")
    # Retourner les graphiques dans des divs côte à côte
    return [
        html.Div(dcc.Graph(figure=mosaicplot_2017), style={'width': '48%'}),
        html.Div(dcc.Graph(figure=mosaicplot_2023), style={'width': '48%'})
    ]


@app.callback(
    Output('graphs-container_6', 'children'),
    Input('indicateur-dropdown', 'value')
)
def update_output(selected_indicateur_df6):
    return update_map(selected_indicateur_df6)

def update_map(selected_indicateur_df6):
    # Créer la carte centrée sur la France
    m = folium.Map(location=[46.157880, 2.488444], zoom_start=5)
    
    # Créer la choroplèthe en utilisant votre GeoDataFrame (converti en GeoJSON)
    folium.Choropleth(
        geo_data=gdf1.to_json(),  # convertir en JSON
        data=gdf1,
        columns=["Région", selected_indicateur_df6],
        key_on="feature.properties.Région",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=selected_indicateur_df6,
    ).add_to(m)
    
    # Optionnel : ajouter les labels pour chaque région
    style_function = lambda x: {
        'fillColor': '#ffffff',
        'color': '#000000',
        'fillOpacity': 0.1,
        'weight': 0.1
    }
    
    highlight_function = lambda x: {'fillColor': '#000000', 'color': '#000000', 'fillOpacity': 0.50, 'weight': 0.1}
    
    folium.GeoJson(
        gdf1.to_json(),
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=["Région", selected_indicateur_df6],
            aliases=["Région:", f"{selected_indicateur_df6}:"],
            localize=True
        )
    ).add_to(m)
    
    # Récupérer le code HTML de la carte
    map_html = m._repr_html_()
    
    # Afficher la carte dans un Iframe
    return html.Iframe(srcDoc=map_html, width='60%', height='700', style={'border': '0'})

@app.callback(
    Output('graphs-container_7', 'children'),
    Input('tabs-with-classes', 'value')
)

def tableau_de_bord(_):

    # Créer la figure avec un grid de 6 lignes et 3 colonnes
    fig_effectif = go.Figure()
    
    # Colonne 1 : Effectifs
    fig_effectif.add_trace(go.Indicator(
                value=243003,
                title = {'text': "Effectif<br><span style='font-size:0.6em;color:gray'>Total</span>"},
                delta={'reference': 248953, 'relative': True},
                mode="number+delta",
                domain={'x': [0.4, 0.6], 'y': [0.8, 1.0]}))
    
    fig_effectif.add_trace(go.Indicator(
                value=70653,
                title= {'text': "<br><span style='font-size:0.8em;color:#7900f1'>Femmes</span>"},
                delta={'reference': 74691, 'relative': True},
                mode="number+delta",
                domain={'x': [0.1, 0.3], 'y': [0.4, 0.6]}))
    
    fig_effectif.add_trace(go.Indicator(
                value=172350,
                title= {'text': "<br><span style='font-size:0.8em;color:#1b909a'>Hommes</span>"},
                delta={'reference': 174262, 'relative': True},
                mode="number+delta",
                domain={'x': [0.7, 0.9], 'y': [0.4, 0.6]}))
    
    fig_effectif.add_trace(go.Indicator(
                value=11.85,
                number = {"suffix": "%"},
                title= {'text': "<br><span style='font-size:0.6em;color:gray'>Ecart</span>"},
                delta={'reference': 13.36, "suffix": "%"},
                mode="number+delta",
                domain={'x': [0.4, 0.6], 'y': [0.4, 0.6]}))

    
    # Colonne 2 : Salaires
    fig_salaire = go.Figure()

    fig_salaire.add_trace(go.Indicator(
                value=5245,
                number = {"suffix": "€"},
                title = {'text': "Salaire moyen<br><span style='font-size:0.6em;color:gray'>Total</span>"},
                delta={'reference': 4318.33, 'relative': True},
                mode="number+delta",
                domain={'x': [0.4, 0.6], 'y': [0.8, 1.0]}))
    
    fig_salaire.add_trace(go.Indicator(
                value=4914.67,
                number = {"suffix": "€"},
                title= {'text': "<br><span style='font-size:0.8em;color:#7900f1'>Femmes</span>"},
                delta={'reference': 4009.33, 'relative': True},
                mode="number+delta",
                domain={'x': [0.1, 0.3], 'y': [0.4, 0.6]}))

    fig_salaire.add_trace(go.Indicator(
                value=5575.33,
                number = {"suffix": "€"},
                title= {'text': "<br><span style='font-size:0.8em;color:#1b909a'>Hommes</span>"},
                delta={'reference': 4627.33, 'relative': True},
                mode="number+delta",
                domain={'x': [0.7, 0.9], 'y': [0.4, 0.6]}))

    fig_salaire.add_trace(go.Indicator(
                value=11.85,
                number = {"suffix": "%"},
                title= {'text': "<br><span style='font-size:0.6em;color:gray'>Ecart</span>"},
                delta={'reference': 13.36, "suffix": "%"},
                mode="number+delta",
                domain={'x': [0.4, 0.6], 'y': [0.4, 0.6]}))
    
    # Colonne 3 : Formation
    fig_formation = go.Figure()

    fig_formation.add_trace(go.Indicator(
                value=42.25,
                number = {"suffix": "%"},
                title = {'text': "Salariés formés<br><span style='font-size:0.6em;color:gray'>Total</span>"},
                delta={'reference': 47.39, "suffix":"%"},
                mode="number+delta",
                domain={'x': [0.4, 0.6], 'y': [0.8, 1.0]}))
    
    fig_formation.add_trace(go.Indicator(
                value = 38.34,
                number = {"suffix": "€"},
                title= {'text': "<br><span style='font-size:0.8em;color:#7900f1'>Femmes</span>"},
                delta={'reference': 47.86, "suffix":"%"},
                mode="number+delta",
                domain={'x': [0.1, 0.3], 'y': [0.4, 0.6]}))

    fig_formation.add_trace(go.Indicator(
                value=43.85,
                number = {"suffix": "€"},
                title= {'text': "<br><span style='font-size:0.8em;color:#1b909a'>Hommes</span>"},
                delta={'reference': 47.2, "suffix":"%"},
                mode="number+delta",
                domain={'x': [0.7, 0.9], 'y': [0.4, 0.6]}))

    fig_formation.add_trace(go.Indicator(
                value=11.85,
                number = {"suffix": "%"},
                title= {'text': "<br><span style='font-size:0.6em;color:gray'>Ecart</span>"},
                delta={'reference': 13.36, "suffix": "%"},
                mode="number+delta",
                domain={'x': [0.4, 0.6], 'y': [0.4, 0.6]}))
       
    # Colonne 4 : Congés maaternité / paternité
    fig_conges = go.Figure()
    
    fig_conges.add_trace(go.Indicator(
                value=32,
                number = {"suffix": "h"},
                title = {'text': "Congés parental<br><span style='font-size:0.6em;color:gray'>Total</span>"},
                delta={'reference': 45, "relative":True},
                mode="number+delta",
                domain={'x': [0.4, 0.6], 'y': [0.8, 1.0]}))
    
    fig_conges.add_trace(go.Indicator(
                value = 26,
                number = {"suffix": " h"},
                title= {'text': "<br><span style='font-size:0.8em;color:#7900f1'>Congés maternité</span>"},
                delta={'reference': 42, "relative":True},
                mode="number+delta",
                domain={'x': [0.1, 0.3], 'y': [0.4, 0.6]}))

    fig_conges.add_trace(go.Indicator(
                value=6,
                number = {"suffix": " h"},
                title= {'text': "<br><span style='font-size:0.8em;color:#1b909a'>Congés paternité</span>"},
                delta={'reference': 3, "relative":True},
                mode="number+delta",
                domain={'x': [0.7, 0.9], 'y': [0.4, 0.6]}))

    fig_conges.add_trace(go.Indicator(
                value=20,
                number = {"suffix": "h"},
                title= {'text': "<br><span style='font-size:0.6em;color:gray'>Ecart</span>"},
                delta={'reference': 39, "relative": True},
                mode="number+delta",
                domain={'x': [0.4, 0.6], 'y': [0.4, 0.6]}))

    return html.Div([
        dcc.Graph(figure=fig_effectif),
        dcc.Graph(figure=fig_salaire),
        dcc.Graph(figure=fig_formation),
        dcc.Graph(figure=fig_conges)
    ], style={
        'display': 'grid',
        'gridTemplateColumns': '1fr 1fr',  # Deux colonnes de largeur égale
        'gridAutoRows': '300px',          # Définit la hauteur des lignes
        'justifyItems': 'center',         # Centrer les graphiques horizontalement
        'alignItems': 'center',           # Centrer les graphiques verticalement
        'padding': '0',                   # Supprimer tout padding global
        'margin': '0'                     # Supprimer tout margin global
    })


if __name__ == '__main__':
    app.run(debug=True)
