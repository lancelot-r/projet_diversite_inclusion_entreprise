from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

# Charger les données
df1 = pd.read_csv("effectifs.csv")
df2 = pd.read_csv("formation_evo.csv")
df3 = pd.read_csv("alternance.csv")
#df4 = pd.read_csv("")
df5 = pd.read_csv("temps_partiel.csv")

# Extraire les évolutions uniques pour la liste déroulante
evolutions = df2["Evolution"].unique()
colleges = df1["Collège"].unique()
#colleges_df4 = df4["Collège"].unique()
colleges_df5 = df5["Collège"].unique()

app = Dash(suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-2',
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
            )
        ]),
    html.Div(id='tabs-content-classes')
])

@callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'))

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
        html.H2("Disparité des effectifs hommes-femmes", style={'text-align': 'center'}),
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

@app.callback(
        Output('graphs-container_1', 'children'),
        Input('effectifs-dropdown', 'value')
)

# Graphique Tab 1 : Disparité des effectifs femmes-hommes
def update_graphs(selected_csp):

    filtered_df1 = df1[df1["Collège"] == selected_csp]

    #selected_csp = filtered_df1["Collège"].unique()

    fig_effectifs = px.bar(
        filtered_df1,
        x="Année",
        y="Nombre de salariés",
        color="Genre",
        barmode="group",
        text_auto='.2s',
        labels={'Nombre de salariés':'Nombre d\'employés', 'Année':'Année'},
        color_discrete_map={
            'Homme': '#1b909a',  # Bleu
            'Femme': '#7900f1',  # Rose
        }
    )

    return [
        html.Div(dcc.Graph(figure=fig_effectifs), style={'width': '80%'})
    ]

@app.callback(
    Output('graphs-container_2', 'children'),
    Input('evolution-dropdown', 'value')
)

def update_graphs(selected_evolution):
    # Filtrer les données en fonction de l'évolution sélectionnée
    filtered_df2 = df2[df2["Evolution"] == selected_evolution]

    # Extraire les collèges uniques pour le titre
    selected_college = filtered_df2["Collège"].unique()

    # Créer les graphiques
    fig_population_formee = px.line(
        filtered_df2,
        x='Année',
        y="Proportion d'employés formés (%)",
        color='Genre',
        title=f"Population formée - {selected_college}",
        labels={'Valeur': 'Valeur', 'Année': 'Année'},
        markers=True,
        color_discrete_map={
            'Homme': '#1b909a',  # Bleu
            'Femme': '#7900f1',  # Rose
        }
    )

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

    return [
        html.Div(dcc.Graph(figure=fig_apprentissage), style={'width': '48%'}),
        html.Div(dcc.Graph(figure=fig_professionnalisation), style={'width': '48%'})
    ]

# @app.callback(
#         Output('graphs-container_4', 'children'),
#         Input('conges-dropdown', 'value')
# )

# Graphique Tab 1 : Disparité des effectifs femmes-hommes
# def update_conges_graphs(selected_csp):

#     filtered_df4 = df4[df4["Collège"] == selected_csp]

#     #selected_csp = filtered_df1["Collège"].unique()

#     fig_conges_femme = px.bar(
#         filtered_df4,
#         x="Année",
#         y="",
#         text_auto='.2s',
#         labels={'Nombre de salariés':'Nombre d\'employés', 'Année':'Année'},
#         color_discrete_map={
#             'Homme': '#1b909a',  # Bleu
#             'Femme': '#7900f1',  # Rose
#         }
#     )

#     fig_conges_homme = px.bar(
#         filtered_df4,
#         x="Année",
#         y="Nombre de salariés",
#         text_auto='.2s',
#         labels={'Nombre de salariés':'Nombre d\'employés', 'Année':'Année'},
#         color_discrete_map={
#             'Homme': '#1b909a',  # Bleu
#             'Femme': '#7900f1',  # Rose
#         }
#     )

#     return [
#         html.Div(dcc.Graph(figure=mosaicplot_2017), style={'width': '48%'}),
#         html.Div(dcc.Graph(figure=mosaicplot_2023), style={'width': '48%'})
#     ]

@app.callback(
    Output('graphs-container_5', 'children'),
    Input('temps_partiel-dropdown', 'value')
)

def update_temps_partiel_graphs(selected_csp):

    filtered_df5 = df5[df5["Collège"] == selected_csp]

    # Extraire les collèges uniques pour le titre
    # selected_college = filtered_df5["Collège"].unique()

    # Créer les graphiques
    mosaicplot_2017 = px.treemap(
        filtered_df5[filtered_df5["Année"] == 2017],
        path=["Collège", "Genre"],
        values="Proportion de salariés en temps partiel en décembre (%)",
        color="Genre",
        title=f"Taux de Temps Partiel par Genre et CSP en 2017",
        labels={'Valeur': 'Valeur', 'Année': 'Année'},
        color_discrete_map={
            'Homme': '#1b909a',  # Bleu
            'Femme': '#7900f1',  # Rose
        }
    )

    mosaicplot_2023 = px.treemap(
        filtered_df5[filtered_df5["Année"] == 2023],
        path=["Collège", "Genre"],
        values="Proportion de salariés en temps partiel en décembre (%)",
        color="Genre",
        title=f"Taux de Temps Partiel par Genre et CSP en 2023",
        labels={'Valeur': 'Valeur', 'Année': 'Année'},
        color_discrete_map={
            'Homme': '#1b909a',  # Bleu
            'Femme': '#7900f1',  # Rose
        }
    )

    # Retourner les graphiques dans des divs côte à côte
    return [
        html.Div(dcc.Graph(figure=mosaicplot_2017), style={'width': '48%'}),
        html.Div(dcc.Graph(figure=mosaicplot_2023), style={'width': '48%'})
    ]

if __name__ == '__main__':
    app.run(debug=True)
