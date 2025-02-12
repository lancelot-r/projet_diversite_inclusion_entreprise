from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from matplotlib import colormaps
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from folium.features import CustomIcon

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
                      "Note Ecart taux d'augmentation", "Note Hautes rémunérations",
                      "Note Retour congé maternité", "Note Index"]

app = Dash(suppress_callback_exceptions=True)

app.layout = html.Div([

    html.H1("Diversité et inclusion en entreprise : analyse de l'évolution du bilan social d'EDF SA", style={'text-align': 'center', 'margin-top': '20px'}),
    html.H1("sous l'angle des disparités de genre", style={'text-align': 'center'}),
    html.Img(
        src="https://upload.wikimedia.org/wikipedia/commons/1/12/%C3%89lectricit%C3%A9_de_France_logo.svg",
        style={
            "height": "100px",  # Ajuste la hauteur
            "marginBottom": "50px",  # Espacement sous l'image
            "display": "block",  # Pour rendre l'image en bloc
            "margin": "auto"  # Centre l'image horizontalement
        }
    ),
    html.Hr(style={"border": "1px solid #ccc", "margin": "20px 0"}),
    dcc.Tabs(
        id="tabs-with-classes",
        value='',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label="Métriques d'évolution 2017 - 2024",
                value='tab-0',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Disparité des effectifs et rémunerations femmes-hommes',
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
                label='Proportion en temps partiel par genre',
                value='tab-5',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label="Bilan d'EDF et moyennes régionales",
                value='tab-6',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
        ]),
    html.Div(id='tabs-content-classes')
])

@callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'))

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
        html.H2("Disparité des effectifs et des salaires femmes-hommes", style={'text-align': 'center'}),
        html.P("Sélectionnez une catégorie socio-professionnelle :", style={"fontSize": "16px", "fontWeight": "lighter", "marginBottom": "5px"}),
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
        html.P("Sélectionnez une évolution :", style={"fontSize": "16px", "fontWeight": "lighter", "marginBottom": "5px"}),
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

    elif tab == 'tab-5':
        return html.Div([
        html.H2("Proportion en temps-partiel par genre", style={'text-align': 'center'}),
        html.P("Sélectionnez une catégorie socio-professionnelle :", style={"fontSize": "16px", "fontWeight": "lighter", "marginBottom": "5px"}),
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
        html.H2("Carte intéractive : moyenne des scores d'entreprises par région et comparaison avec EDF SA", style={'text-align': 'center'}),
        html.P("Sélectionnez un indicateur :", style={"fontSize": "16px", "fontWeight": "lighter", "marginBottom": "5px"}),
        dcc.Dropdown(
            id='indicateur-dropdown',
            options=[{'label': indicateur, 'value': indicateur} for indicateur in indicateur_df6],
            value=indicateur_df6[0],  # Valeur par défaut
            placeholder="Sélectionnez un indicateur"
        ),
        html.Div(id='graphs-container_6', style={'display': 'flex', 'justify-content': 'space-around', 'margin-top': '20px'})
    ], style={'padding': '20px', 'border-bottom': '2px solid #ccc'})

    elif tab == 'tab-0':
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

indicateur_links = {
    "Note Ecart rémunération": "https://egapro.travail.gouv.fr/aide-index#indicateur-ecart-de-remuneration",
    "Note Ecart taux de promotion": "https://egapro.travail.gouv.fr/aide-index#indicateur-cart-de-taux-de-promotion-plus-de-250-salaries",
    "Note Ecart taux d'augmentation (hors promotion)": "https://egapro.travail.gouv.fr/aide-index#indicateur-cart-de-taux-d-augmentation-plus-de-250-salaries",
    "Note Ecart taux d'augmentation": "https://egapro.travail.gouv.fr/aide-index#indicateur-ecart-de-taux-d-augmentation-50-250-salaries",
    "Note Hautes rémunérations": "https://egapro.travail.gouv.fr/aide-index#indicateur-nombre-de-salaries-du-sexe-sous-represente-parmi-les-10-plus-hautes-remunerations",
    "Note Retour congé maternité": "https://egapro.travail.gouv.fr/aide-index#indicateur-pourcentage-de-salariees-augment-es-dans-l-ann-e-suivant-leur-retour-de-cong-maternite",
    "Note Index": "https://www.index-egapro.travail.gouv.fr/"
}

@app.callback(
    Output('graphs-container_6', 'children'),
    Input('indicateur-dropdown', 'value')
)
def update_output(selected_indicateur_df6):
    return update_map(selected_indicateur_df6)

def update_map(selected_indicateur_df6):
    # Créer la carte centrée sur la France
    m = folium.Map(location=[46.157880, 2.488444], zoom_start=6)
    
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

        # Définition des coordonnées et valeur de l'indicateur pour une entreprise
    entreprise_data = {
        "nom": "EDF SA",
        "latitude": 48.8566,  # Paris
        "longitude": 2.3522,
        "Note Ecart rémunération":40,
        "Note Ecart taux de promotion":15,
        "Note Ecart taux d'augmentation (hors promotion)":"Non communiqué", 
        "Note Ecart taux d'augmentation":20,
        "Note Hautes rémunérations":5,
        "Note Retour congé maternité":15,
        "Note Index": 75
    }

    logo_url = "https://upload.wikimedia.org/wikipedia/commons/1/12/%C3%89lectricit%C3%A9_de_France_logo.svg"
    icon = CustomIcon(
    logo_url,
    icon_size=(40, 40)  # Ajuste la taille du logo
)
    folium.Marker(
        location=[entreprise_data["latitude"], entreprise_data["longitude"]],
        popup=f"<b>{entreprise_data['nom']}</b><br>{selected_indicateur_df6}: {entreprise_data[selected_indicateur_df6]}",
        tooltip=f"{entreprise_data['nom']} - {selected_indicateur_df6}: {entreprise_data[selected_indicateur_df6]}",
        icon=icon
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

    # 📌 Sélecteur d'indicateur (Dropdown)
    dropdown = dbc.Select(
        id="select-indicateur",
        options=[{"label": k, "value": k} for k in indicateur_links.keys()],
        value=None,
        placeholder="Définitions des indicateurs"
    )

    # 📌 Conteneur de la définition du lien
    definition_link = html.Div(id="definition-link")

    # 📌 Titre de la carte
    header_section = dbc.Row(
        dbc.Col(
            html.H3(f"Indicateur selectionné : {selected_indicateur_df6} (Les scores régionaux correspondent aux moyennes des scores des entreprises dont le siège social se situe dans la région)", style={"textAlign": "center", "fontSize": "16px", "fontWeight": "lighter", "marginBottom": "20px"})
        )
    )

    # 📌 Agencement avec sélection d'indicateur et lien au-dessus de la carte
    layout = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(dropdown, width=6),
                    dbc.Col(definition_link, width=6)
                ],
                className="mb-3"
            ),
            header_section,
            dbc.Row(
                dbc.Col(html.Iframe(srcDoc=map_html, width='1200', height='700', style={'center': '0'}))
            )
        ],
        fluid=True
    )

    return layout

# 📌 Callback pour mettre à jour le lien de définition en fonction de l'indicateur sélectionné
@app.callback(
    Output("definition-link", "children"),
    [Input("select-indicateur", "value")]
)
def update_link(selected_indicateur):
    if selected_indicateur:
        return dbc.Alert(
            html.A(
                f"Lien vers la définition - {selected_indicateur}",
                href=indicateur_links[selected_indicateur],
                target="_blank",
                style={"text-decoration": "none", "color": "blue"}
            ),
            color="info"
        )
    return ""

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
                value=-59,
                number = {"suffix": "%"},
                title= {'text': "<br><span style='font-size:0.6em;color:gray'>Ecart</span>"},
                delta={'reference': -57.13, "suffix": "%"},
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
                value=-11.84,
                number = {"suffix": "%"},
                title= {'text': "<br><span style='font-size:0.6em;color:gray'>Ecart</span>"},
                delta={'reference': -13.35, "suffix": "%"},
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
                number = {"suffix": "%"},
                title= {'text': "<br><span style='font-size:0.8em;color:#7900f1'>Femmes</span>"},
                delta={'reference': 47.86, "suffix":"%"},
                mode="number+delta",
                domain={'x': [0.1, 0.3], 'y': [0.4, 0.6]}))

    fig_formation.add_trace(go.Indicator(
                value=43.85,
                number = {"suffix": "%"},
                title= {'text': "<br><span style='font-size:0.8em;color:#1b909a'>Hommes</span>"},
                delta={'reference': 47.2, "suffix":"%"},
                mode="number+delta",
                domain={'x': [0.7, 0.9], 'y': [0.4, 0.6]}))

    fig_formation.add_trace(go.Indicator(
                value=-12.56,
                number = {"suffix": "%"},
                title= {'text': "<br><span style='font-size:0.6em;color:gray'>Ecart</span>"},
                delta={'reference': 1.39, "suffix": "%"},
                mode="number+delta",
                domain={'x': [0.4, 0.6], 'y': [0.4, 0.6]}))
    
    fig_effectif.update_layout(margin=dict(l=0, r=0, t=100, b=0))
    fig_salaire.update_layout(margin=dict(l=0, r=0, t=100, b=0))
    fig_formation.update_layout(margin=dict(l=0, r=0, t=100, b=0))

    return html.Div([
    # Conteneur pour l'effectif
        html.Div([
            dcc.Graph(id='fig-effectif', figure=fig_effectif, style={'height': '350px', 'width': '400px'})
        ], style={
            'backgroundColor': '#f9f9f9',
            'borderRadius': '15px',
            'padding': '20px',
            'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)',
            'margin': '10px auto',
            'textAlign': 'center'
        }),

        # Conteneur pour le salaire
        html.Div([
            dcc.Graph(id='fig-salaire', figure=fig_salaire, style={'height': '350px', 'width': '400px'})
        ], style={
            'backgroundColor': '#f9f9f9',
            'borderRadius': '15px',
            'padding': '20px',
            'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)',
            'margin': '10px auto',
            'textAlign': 'center'
        }),

        # Conteneur pour la formation
        html.Div([
            dcc.Graph(id='fig-formation', figure=fig_formation, style={'height': '350px', 'width': '400px'})
        ], style={
            'backgroundColor': '#f9f9f9',
            'borderRadius': '15px',
            'padding': '20px',
            'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)',
            'margin': '10px auto',
            'textAlign': 'center'
        }),
    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'alignItems': 'center',
        'justifyContent': 'center',
        'gap': '20px'
    })



if __name__ == '__main__':
    app.run(debug=True)
