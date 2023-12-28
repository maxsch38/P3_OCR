#############################################################################################################################
### Fichier de fonction du projet 3 : Concevez une application au service de la santé publique.
#############################################################################################################################


#############################################################################################################################
# Importation des librairies : 

import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox


#############################################################################################################################
def visu_graph_moy_nulle(liste_produits, liste_sante, liste_environnement, df_selection, save='n'):
    """
    Visualise les données moyennes nulles pour différentes catégories.

    Args:
        liste_produits (List[str]): Liste des noms de produits.
        liste_sante (List[str]): Liste des noms de variables liées à la santé.
        liste_environnement (List[str]): Liste des noms de variables liées à l'environnement.
        df_selection (DataFrame): DataFrame contenant les données sélectionnées.
        save (str, optionnel): Indique si la figure doit être enregistrée. 
                              'y' pour enregistrer, 'n' pour ne pas enregistrer. 
                              Par défaut, 'n'.
    """
    
    # Création des données : 
    axe_x_produits = list(x for x in range(1, len(liste_produits)+1))
    axe_x_sante = list(x+len(liste_produits) for x in range(1, len(liste_sante)+1))
    axe_x_environnement = list(x+len(liste_produits)+len(liste_sante) for x in range(1, len(liste_environnement)+1))

    donnees_produits = df_selection.loc[:, liste_produits].isna().mean().sort_values()
    donnes_sante = df_selection.loc[:, liste_sante].isna().mean().sort_values()
    donnes_environnement = df_selection.loc[:, liste_environnement].isna().mean().sort_values()

    legend_x = list(donnees_produits.index) + list(donnes_sante.index) + list(donnes_environnement.index)

    width = 0.4
    color_x = []
    limite_y_value = 0.8

    # Création de color_x, liste des couleurs conditionnelles des xticks : 
    for x in range(len(liste_produits)):
        if donnees_produits.iloc[x] < limite_y_value: 
            color_x.append('black')
        else:
            color_x.append('red')

    for x in range(len(liste_sante)):
        if donnes_sante.iloc[x] < limite_y_value: 
            color_x.append('black')
        else:
            color_x.append('red')      

    for x in range(len(liste_environnement)):
        if donnes_environnement.iloc[x] < limite_y_value: 
            color_x.append('black')
        else:
            color_x.append('red') 


    # Création de la figure 
    fig, ax1 = plt.subplots(figsize=(15,10))

    # Création graphique 1, sur les produits : 
    ax1.bar(x=axe_x_produits, height=donnees_produits, width=width, label='Données des produits', color='blue')

    # Création graphique 2, sur les données pour le score sante : 
    ax1.bar(x=axe_x_sante, height=donnes_sante, width=width, label='Données pour le score santé', color='orange')

    # Création du graphique 3, sur les données pour le score encironnement : 
    ax1.bar(x=axe_x_environnement, height=donnes_environnement, width=width, 
            label='Données pour le score environnement', color='green')

    # Noms des xticks: 
    ax1.set_xticks([x for x in range(1, len(legend_x)+1)], legend_x)


    # Couleurs conditionnelles des xticks : 
    for ticklabel, tickcolor in zip(ax1.get_xticklabels(), color_x):
        ticklabel.set_color(tickcolor)

    # Paramètre graphique : 
    plt.legend(fontsize=14)
    plt.xticks(rotation=90)
    plt.title("% données manquantes par variable pour l'ensemble des données sélectionnées", fontsize=18)
    plt.grid(axis='y')
    plt.tight_layout()

    
    if save == 'y': 
        bbox = Bbox.from_bounds(0, 0, 15, 10)
        plt.savefig('figure.png', bbox_inches=bbox)

    plt.show()
    
    
#############################################################################################################################
def val_nul_col(df, mot_col):
    """
    Affiche les statistiques des valeurs nulles pour les colonnes contenant un mot clé spécifié.

    Args:
        df (DataFrame): Le DataFrame contenant les données.
        mot_col (str): Le mot clé utilisé pour filtrer les colonnes.

    Returns:
        DataFrame: Les premières lignes du DataFrame avec des valeurs non nulles pour les colonnes spécifiées.
    """
    
    ls = list(df.filter(like=mot_col, axis=1).columns)
    
    col = ''
    for c in ls: 
        if col == '':
            col += c
        else: 
            col += ' / '+c
    print('nom des colonnes :',col )
    
    print('--'*50)

    serie = df[ls].isna().sum().sort_values(ascending=True)
    serie_index = serie.index
    
    for index in serie_index: 
        print(f'Nombre de {index} nul :', serie[index])
    
    print('--'*50)
    print('Visualisation des premières pour les colonnes non nulles : ')
    mask = df[ls].notna().sum(axis=1) == len(serie_index)
    return df[mask].head(10)


#############################################################################################################################
def fill_median(ser): 
    """
    Remplacement de chaque valeur manquante par la valeur médiane de la colonne
    """
    return ser.fillna(value=ser.median())
