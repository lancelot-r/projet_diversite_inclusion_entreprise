from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Charger les données
df1 = pd.read_csv("effectifs.csv")
df2 = pd.read_csv("formation_evolution.csv")
df4 = pd.read_csv("alternance.csv")

# Extraire les évolutions uniques pour la liste déroulante
evolutions = df2["Evolution"].unique()
colleges = df1["Collège"].unique()

# Créer l'application Dash
app = Dash(__name__)

# Layout de l'application
app.layout = html.Div([
    html.H1("Tableaux de bord sur l'évolution des formations et des alternances", style={'text-align': 'center'}),

    # Section 0 : Nombre de salariés homme-femme
   html.Div([
        html.H2("Disparité des effectifs hommes-femmes", style={'text-align': 'center'}),
        dcc.Dropdown(
            id='effectifs-dropdown',
            options=[{'label': csp, 'value': csp} for csp in colleges],
            value=colleges[0],  # Valeur par défaut
            placeholder="Sélectionnez une catégorie socio-professionnelle"
        ),
        html.Div(id='graphs-container_1', style={'display': 'flex', 'justify-content': 'space-around', 'margin-top': '20px'})
    ], style={'padding': '20px', 'border-bottom': '2px solid #ccc'}),

    # Section 1 : Evolution des formations
    html.Div([
        html.H2("Évolution des formations", style={'text-align': 'center'}),
        dcc.Dropdown(
            id='evolution-dropdown',
            options=[{'label': evolution, 'value': evolution} for evolution in evolutions],
            value=evolutions[0],  # Valeur par défaut
            placeholder="Sélectionnez une évolution"
        ),
        html.Div(id='graphs-container_2', style={'display': 'flex', 'justify-content': 'space-around', 'margin-top': '20px'})
    ], style={'padding': '20px', 'border-bottom': '2px solid #ccc'}),

    # Section 2 : Evolution des alternances
    html.Div([
        html.H2("Évolution des contrats d'alternance", style={'text-align': 'center'}),
        html.Div(id='alternance-graphs', style={'display': 'flex', 'justify-content': 'space-around', 'margin-top': '20px'})
    ], style={'padding': '20px'})
])

@app.callback(
        Output('graphs-container_1', 'children'),
        Input('effectifs-dropdown', 'value')
)

def update_graphs(selected_csp):

    filtered_df1 = df1[df1["Collège"] == selected_csp]

    selected_csp = filtered_df1["Collège"].unique()

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


# Callback pour mettre à jour les graphiques de la première section
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
        y='Population formée',
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
        y='Evolutions',
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

# Callback pour afficher les graphiques de la deuxième section
@app.callback(
    Output('alternance-graphs', 'children'),
    Input('evolution-dropdown', 'value')  # Pas réellement dépendant de l'input, mais requis pour callback
)
def display_alternance_graphs(_):
    df4_apprentissage = df4[df4["Indicateur"] == "Contrats d'apprentissage conclus dans l'année"]
    df4_pro = df4[df4["Indicateur"] == "Contrats de professionnalisation conclus dans l'année"]

    fig_apprentissage = px.line(
        df4_apprentissage,
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
        df4_pro,
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

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)