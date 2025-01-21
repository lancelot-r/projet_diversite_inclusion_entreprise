import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.markdown("<h1 style='text-align: center; color: black;'>Diversité et inclusion en entreprise évolution du bilan social chez EDF</h1>", unsafe_allow_html=True)
st.image("https://inclusivity.co.uk/wp-content/uploads/2022/04/EDF_Logo_RGB_COLOUR_LARGE-1.png")
st.markdown(" **Problématique** : quelles ont été les **principales évolutions** du bilan social d'**EDF SA** en terme d'**égalité**, d'**inclusion** et de **diversité** à travers le **temps** ? ")
st.markdown(" Afin de répondre à cette problématique, nous allons analyser le bilan social d'EDF SA autour de quatre graphiques sur les thèmes d'évolution des salaires, des employés, et des démissions en comparant différentes classes socio-professionnelles, différents types de contrats et en comparant les disparités inter-sexe. Ensuite, nous allons comparer EDF SA aux autres entreprises autour de quatre indicateurs (écart de rémunérations / ecart taux d'augmentation / hautes rémunération / index) au travers d'une heatmap représentant la moyenne du score des entreprises par région")
st.divider()

# Graphique 1 (barplot)
st.markdown("<h3 style='text-align: center; color: black;'> Evolution des salaires par catégorie socio-professionnelle et différence selon le genre </h3>", unsafe_allow_html=True)
st.markdown("Le barplot ci-dessous représente, pour chaque année, le salaire brut moyen pour les hommes et les femmes selon la catégorie socio-professionnelle choisie à l'aide du menu déroulant.")
# Traitement des données
salaire = pd.read_csv("data/promotion.csv", delimiter=";")
salaire = salaire[
    (salaire['Type de contrat'] == "Statutaire") &
    (salaire['Indicateur'] == 'Rémunération mensuelle moyenne brute') &
    (salaire['Collège'].isin(['Cadre', 'Maitrise', 'Execution']))
]
salaire = salaire.rename(columns={'Valeur': 'Salaire mensuel moyen brut'}).drop(columns=[
    'Perimètre juridique', 'Perimètre spatial', 'Spatial perimeter', 'Indicateur',
    'Indicator', 'Type de contrat', 'Type of contract', 'Employee category',
    'Plage M3E', 'M3E classification', 'Gender', 'Unité', 'Unit',
    'Chapitre du bilan social'
])

# Calcul de l'écart en pourcentage entre hommes et femmes
salaire_grouped = salaire.groupby(['Année', 'Collège', 'Genre'])['Salaire mensuel moyen brut'].mean().reset_index()
salaire_hommes = salaire_grouped[salaire_grouped['Genre'] == 'Homme']
salaire_femmes = salaire_grouped[salaire_grouped['Genre'] == 'Femme']
salaire_merged = pd.merge(salaire_hommes, salaire_femmes, on=['Année', 'Collège'], suffixes=('_hommes', '_femmes'))
salaire_merged['Ecart_pourcentage'] = ((salaire_merged['Salaire mensuel moyen brut_hommes'] -
                                        salaire_merged['Salaire mensuel moyen brut_femmes']) /
                                       salaire_merged['Salaire mensuel moyen brut_hommes']) * 100
salaire_final = pd.merge(salaire, salaire_merged[['Année', 'Collège', 'Ecart_pourcentage']], on=['Année', 'Collège'])

# Menu déroulant pour sélectionner un collège
colleges = salaire_final['Collège'].unique()
selected_college = st.selectbox("Choisissez la catégorie socio-professionnelle :", colleges)

df1 = salaire_final[salaire_final['Collège'] == selected_college]
def create_bar_chart(data, title):
    fig = px.bar(data, x='Année', y='Salaire mensuel moyen brut',
                 barmode='group', color='Genre',
                 color_discrete_map={"Homme": "#1b909a", "Femme": "#7900f1"},
                 category_orders={'Genre': ['Homme', 'Femme']})
    fig.update_traces(
        hovertemplate="<b>%{x}</b> <br>Salaire: %{y:.2f}<br> Écart entre hommes et femmes : %{customdata:.2f}%<br>",
        customdata=data['Ecart_pourcentage'],
        texttemplate='%{y}', textposition='outside'
    )
    fig.update_layout(
        title=title,
        width=800, height=500,
        legend_title="Genre",
        xaxis_title="Année",
        yaxis_title="Salaire mensuel moyen brut (€)"
    )
    return fig

# Affichage du graphique
fig = create_bar_chart(df1, f"Évolution des salaires pour la catégorie socio-professionnelle : {selected_college}")
st.plotly_chart(fig)
st.markdown("Selon ce graphique, l'écart de salaire entre hommes et femmes est présent et constant selon les années (sauf en 2023 où l'écart subit une faible augmentation), quelque soit la catégorie socio-professionnelle. Cependant, cet écart est le plus faible pour les cadres et le plus haut pour les ouvriers. Enfin, le salaire brut moyen reste conséquent pour les ouvriers : ceci pourrait être expliqué par les différentes primes de risque, d'astreinte et de travail de nuit / week-ends.")

st.divider()
# Graphique 2 (Courbes)
st.markdown("<h3 style='text-align: center; color: black;'> Analyse du nombre d'évolutions et du nombre d'employés formés selon le genre </h3>", unsafe_allow_html=True)
st.markdown("Les deux graphiques ci-dessous représentent respectivement, pour chaque année, le nombre d'employés ayant suivi au moins une heure de formation et le nombre d'employés ayant évolué (selon l'évolution sélectionné à l'aide du menu déroulant). Pour chacun des graphiques, deux courbes sont tracées : l'une représentant les valeurs pour les hommes et l'autre pour les femmes. ")
# Traitement des données
promotion = pd.read_csv("data/promotion.csv", delimiter=";")
promotion = promotion[(promotion["Indicateur"] == "Promotions dans un collège supérieur") & 
                      (promotion["Type de contrat"] == "Statutaire")]
columns_to_drop = [
    'Perimètre juridique', 'Unité', 'Perimètre spatial', 'Spatial perimeter',
    'Indicator', 'Type of contract', 'Employee category', 'Plage M3E',
    'M3E classification', 'Gender', 'Unit', 'Chapitre du bilan social',
    'Type de contrat', 'Indicateur'
]
promotion = promotion.drop(columns=columns_to_drop)
promotion = promotion.groupby(["Année", "Collège", "Genre"]).sum().reset_index()
promotion = promotion.rename(columns={'Collège': 'Evolution'})
promotion['Collège'] = 'Exécution'
promotion.loc[promotion['Evolution'] == 'Maîtrise vers Cadre', 'Collège'] = 'Maitrise'

formation = pd.read_csv("data/formation.csv", delimiter=";")
formation = formation[
    (formation["Collège"].isin(["Maitrise", "Exécution"])) & 
    (formation["Indicateur"] == "Salariés ayant suivi au moins un stage")
]
formation = formation.drop(columns=[
    'Perimètre juridique', 'Unité', 'Perimètre spatial', 'Spatial perimeter',
    'Indicator', 'Employee category', 'Plage M3E', 'M3E classification',
    'Gender', 'Unit', 'Chapitre du bilan social'
])

df2 = pd.merge(promotion, formation, on=['Année', 'Collège', 'Genre'], how='inner')
df2 = df2.rename(columns={'Valeur_x': 'Nombre Evolutions', 'Valeur_y': 'Population formée'})

# Création de la liste déroulante pour sélectionner une évolution
evolutions = df2["Evolution"].unique()
selected_evolution = st.selectbox("Sélectionnez une évolution", evolutions)

# Filtrer les données en fonction de l'évolution sélectionnée
df2 = df2[df2["Evolution"] == selected_evolution]
selected_college = df2["Collège"].unique()
# Création des graphiques
def create_line_chart(data, y_value, title):
    return px.line(
        data,
        x='Année',
        y=y_value,
        color='Genre',
        title=title,
        labels={'Valeur': 'Valeur', 'Année': 'Année'},
        markers=True,
        color_discrete_map={
            'Homme': '#1b909a',  # Bleu
            'Femme': '#7900f1',  # Rose
        }
    )

fig_population_formee = create_line_chart(
    df2, 'Population formée', f"Population formée - {selected_college}"
)

fig_nombre_evolutions = create_line_chart(
    df2, 'Nombre Evolutions', f"Evolutions - {selected_evolution}"
)

# Superposition des graphiques
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_population_formee, use_container_width=True)
with col2:
    st.plotly_chart(fig_nombre_evolutions, use_container_width=True)

st.markdown("L'écart de population formée et évolutions est flagrant sur ce graphique : les femmes sont beaucoup moins formées que les hommes et leur nombre ne cesse de baisser depuis 2017. De plus, le nombre de femme évoluant au sein de l'entreprise est en moyenne deux fois plus faible que celui des hommes pour la même année. Le deuxième point important à relever sur ce graphique réside dans la différence de population formée entre les ouvriers et les managers : le nombre de managers formés est en moyenne 5 fois plus haut que le nombre d'ouvriers formés. Cependant, ce nombre très haut de managers formés n'induit pas un nombre conséquent d'évolutions par rapport aux ouvriers devenant managers. Ceci peut s'expliquer par le fait qu'il est beaucoup plus compliqué d'évoluer vers cadre que vers manager, mais aussi car la population formée n'est en fait que le nombre d'employés ayant suivi au moins une heure de formation : de là, nous pouvons déduire que les chiffres de population formée chez les managers sont influencés par ces derniers qui, en constante formation tout au long de l'année, ne visent pas forcément une évolution future vers le poste de cadre.")

























st.divider()
# Graphique 3 (Courbes)
st.markdown("<h3 style='text-align: center; color: black;'> Analyse des différences d'évolutions du salaire moyen brut pour différents types de contrats, selon la catégorie socio-professionnelle </h3>", unsafe_allow_html=True)
st.markdown("Ce graphique nous montre l'évolution annuelle du salaire moyen brut pour les employés, tout genre confondu, de trois types de contrats : Statutaire, CDI et CDD non-statutaire. Avec l'aide du menu déroulant, il est possible d'afficher les courbes pour les ouvriers, managers et cadres.")
# Traitement des données
statut = pd.read_csv("data/promotion.csv", delimiter=";")
statut = statut[statut['Indicateur'] == 'Rémunération mensuelle moyenne brute']
statut = statut[statut["Plage M3E"].isna()]
statut = statut.drop(columns=['Perimètre juridique', 'Perimètre spatial',
       'Spatial perimeter', 'Indicateur', 'Indicator',
       'Type of contract', 'Employee category', 'Plage M3E',
       'M3E classification', 'Gender', 'Unité', 'Unit',
       'Chapitre du bilan social'])
statut = statut.groupby(["Année", "Type de contrat", "Collège"])["Valeur"].sum().reset_index()
statut = statut[statut["Valeur"] != 0]
statut = statut.rename(columns={'Valeur': 'Salaire mensuel brut moyen (€)'})

colleges = statut["Collège"].unique()
selected_college = st.selectbox("Sélectionnez un Collège", colleges)

df3 = statut[statut["Collège"] == selected_college]

# Création du graphique streamlit
fig3 = px.line(
    df3,
    x="Année",
    y="Salaire mensuel brut moyen (€)",
    color="Type de contrat",
    title=f"Salaire par année et type de contrat pour le Collège: {selected_college}",
    labels={"Salaire": "Salaire (€)", "Année": "Année"},
    markers=True,
    symbol='Type de contrat',
    color_discrete_map={
        'Statutaire': '#45992b',
        'Non statutaire CDD': '#c26a27', 
        'Non statutaire CDI': '#f07a1f',
    }
)

st.plotly_chart(fig3)
st.markdown("Selon ce graphique, les non-statutaires en CDD sont toujours moins payés que leurs collègues non-statutaires CDI ou statutaires, quelque soit la catégorie socio-professionnelle. Pour les ouvriers, les non-statutaires CDI ont vu leur salaire fortement augmenter, en moyenne, jusqu'à dépasser le salaire moyen des statutaires en 2021 (valeurs manquantes ensuite). Pour les managers, l'écart entre les non-statutaires CDI et statutaires est en constante augmentation depuis 2018 : le salaire moyen des statutaires n'a fait qu'augmenter alors que celui des non-statutaires CDI n'a augmenté qu'en 2018, avant de baisser et d'atteindre un niveau similaire en 2023. Pour les cadres en revanche, les non-statutaires CDI sont mieux payés que les statutaires, malgré un écart en baisse depuis 2018.")

st.divider()
# Graphique 4 (nuage de points)
st.markdown("<h3 style='text-align: center; color: black;'> Analyse de l'effet du salaire brut moyen sur le taux de démissions pour les différentes classes socio-professionnelles </h3>", unsafe_allow_html=True)
st.markdown("Ces 3 nuages de points représentent, pour chaque catégorie socio-professionnelle, le taux de démission (en %) selon le salaire brut moyen des statutaires, afin de chercher un lien entre salaire et démissions pour les employés d'EDF.")
# Traitement des données
demission = pd.read_csv("data/effectifs.csv", delimiter=";")
demission = demission[demission['Indicateur']=='Démissions']
demission = demission[demission["Plage M3E"].isna()]
demission = demission.drop(columns=['Perimètre juridique', 'Perimètre spatial',
       'Spatial perimeter', 'Indicateur', 'Indicator',
       'Type of contract', 'Employee category', 'Plage M3E',
       'M3E classification', 'Gender', 'Unité', 'Unit',
       'Chapitre du bilan social'])
demission = demission[demission['Type de contrat']=='Statutaires']
demission = demission.groupby(["Année", "Collège"])["Valeur"].sum().reset_index()
demission = demission[demission["Valeur"] != 0]
demission = demission.rename(columns={'Valeur': 'Démissions'})

effectif=pd.read_csv("data/effectifs.csv", delimiter=";")
effectif=effectif[effectif["Type de contrat"] == "Statutaires"]
effectif=effectif.drop(columns= ['Perimètre juridique', 'Perimètre spatial',
                                  'Spatial perimeter', 'Indicator', 'Type of contract',
                                  'Employee category',
                                  'Nationality', 'Seniority', 'Employee subcategory',
                                  'M3E classification', "Plage M3E", "Ancienneté",
                                  "Unité", "Chapitre du bilan social"
                                 ])
effectif=effectif[effectif["Indicateur"] == "Effectif"]
effectif=effectif[effectif["Nationalité"] == "Française"]
effectif=effectif.rename(columns={"Valeur":"Nombre de salariés"})
effectif=effectif.groupby(['Année', 'Collège'])["Nombre de salariés"].sum().reset_index()

effectif["Collège"]=effectif["Collège"].str.replace("é","e")
effectif["Collège"]=effectif["Collège"].str.replace("î","i")
demission["Collège"]=demission["Collège"].str.replace("é","e")
demission["Collège"]=demission["Collège"].str.replace("î","i")

salaire_moyen = statut[statut["Type de contrat"]=="Statutaire"]
salaire_moyen = salaire_moyen.drop(columns="Type de contrat")
df4 = pd.merge(demission, salaire_moyen, on=['Année','Collège'], how='inner')
df4 = pd.merge(df4, effectif, on=['Année','Collège'], how='inner')
df4["Taux de démission (en %)"]=df4["Démissions"]/df4["Nombre de salariés"]*100

# Constitution du graphique streamlit
fig4 = px.scatter(
    df4,
    x="Salaire mensuel brut moyen (€)",
    y="Taux de démission (en %)",
    facet_col="Collège",
    color="Collège",
    labels={"Démissions": "Nombre de démissions", "Salaire mensuel brut moyen (€)": "Salaire moyen (€)"},
)

st.plotly_chart(fig4)
st.markdown("Les tendances des trois nuages de points semblent verticales : le taux de démission n'augmente que très peu en fonction du salaire. Ainsi, ce graphique ne permet pas de prouver un quelconque lien entre les variations du salaire brut moyen et des démissions pour les statutaires chez EDF, toutes CSP confondue.")



st.divider()
# Graphique 5 (carte interactive)
st.markdown("<h3 style='text-align: center; color: black;'> Carte intéractive : moyenne des scores d'entreprises par région et comparaison avec EDF SA en 2020 </h3>", unsafe_allow_html=True)
st.markdown("Afin de comparer EDF SA aux autres entreprises présentes sur les différentes régions du sol français, la carte intéractive ci-dessous indique, selon l'indicateur choisi à l'aide du menu déroulant, les valeurs moyennes de cet indicateur pour toutes les entreprises dont le siège social se trouve dans la région sélectionnée.")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Entreprise", "EDF SA")
col2.metric("Note Ecart Remuneration", "40")
col3.metric("Note Ecart taux d'augmentation", "20")
col4.metric("Note hautes rémunerations", "5")
col5.metric("Note index", "95")


# Préparation des données
egalite = pd.read_excel("data/egalite.xlsx")
egalité = egalite.copy()
egalité["Année"] = egalité["Année"].astype(str).str.strip()
egalité = egalité[egalité["Année"] == "2020"]
egalité.drop(columns=["Structure", "Tranche d'effectifs", "SIREN", "Raison Sociale",
                      "Nom UES", "Entreprises UES (SIREN)", "Département", "Pays",
                      "Note Ecart taux d'augmentation", "Note Ecart taux de promotion",
                      "Note Retour congé maternité", "Code NAF"], inplace=True)

outre_mer_regions = ["Guadeloupe", "Martinique", "Guyane", "La Réunion", "Mayotte"]
egalité = egalité[~egalité["Région"].isin(outre_mer_regions)]

egalité.replace("NC", np.nan, inplace=True)
colonnes_a_traiter = ["Note Ecart rémunération", "Note Ecart taux d'augmentation (hors promotion)", "Note Hautes rémunérations", "Note Index"]
egalité = egalité.groupby(["Région"])[colonnes_a_traiter].mean()
egalité = egalité.round(2)

# Charger le fichier GeoJSON et fusionner données
gdf1 = gpd.read_file("data/region.geojson")
gdf1.rename(columns={'nom': 'Région'}, inplace=True)
gdf1 = gdf1.merge(egalité, on='Région', how='left')

# App streamlit
selected_column = st.selectbox(
    "Choisissez un indicateur à afficher sur la carte :",
    colonnes_a_traiter,
    format_func=lambda x: x.replace("_", " ").capitalize()
)

maps = gdf1.explore(
    column=selected_column,
    cmap='YlOrRd',
    legend=True,
    legend_kwds={
        'label': f"{selected_column} par région",
        'orientation': "horizontal"
    },
    tooltip=['Région', selected_column]
)

# Afficher la carte dans Streamlit
st_folium(maps, width=700, height=500)