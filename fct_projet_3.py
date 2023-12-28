#############################################################################################################################
### Fichier de fonction du projet 3 : Concevez une application au service de la santé publique.
#############################################################################################################################


#############################################################################################################################
# Importation des librairies : 

import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import numpy as np
from fuzzywuzzy import fuzz

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

#############################################################################################################################
def correlation_graph(pca, x_y, features) : 
    """
    Affiche le graphe des correlations

    Positional arguments : 
    -----------------------------------
    pca : sklearn.decomposition.PCA : notre objet PCA qui a été fit
    x_y : list ou tuple : le couple x,y des plans à afficher, exemple [0,1] pour F1, F2
    features : list ou tuple : la liste des features (ie des dimensions) à représenter
    """

    # Extrait x et y 
    x,y=x_y

    # Taille de l'image (en inches)
    fig, ax = plt.subplots(figsize=(10, 9))

    # Pour chaque composante : 
    for i in range(0, pca.components_.shape[1]):

        # Les flèches
        ax.arrow(0,0, 
                pca.components_[x, i],  
                pca.components_[y, i],  
                head_width=0.07,
                head_length=0.07, 
                width=0.02, )

        # Les labels
        plt.text(pca.components_[x, i] + 0.05,
                pca.components_[y, i] + 0.05,
                features[i])
        
    # Affichage des lignes horizontales et verticales
    plt.plot([-1, 1], [0, 0], color='grey', ls='--')
    plt.plot([0, 0], [-1, 1], color='grey', ls='--')

    # Nom des axes, avec le pourcentage d'inertie expliqué
    plt.xlabel('F{} ({}%)'.format(x+1, round(100*pca.explained_variance_ratio_[x],1)))
    plt.ylabel('F{} ({}%)'.format(y+1, round(100*pca.explained_variance_ratio_[y],1)))

    plt.title("Cercle des corrélations (F{} et F{})".format(x+1, y+1))

    # Le cercle 
    an = np.linspace(0, 2 * np.pi, 100)
    plt.plot(np.cos(an), np.sin(an))  # Add a unit circle for scale

    # Axes et display
    plt.axis('equal')
    plt.show(block=False)
    
    
#############################################################################################################################
def better_product(data, selected_product_code=None): 
    """
    Retourne le nom du produits sélectionné ainsi que ses score sante et environnement.
    
    Retourne s'il existe : 
       - une proposition du produit le plus similaire avec une meilleure note santé.
       - une proposition du produit le plus similaire avec une meilleure note environnement.
    
    Retourne le produit de la même catégorie avec la meilleure note globale.
   
    data : le dataframe avec les références des produits, data par défaut. 
    selected_product_code : le code du produit sélectionné, None par défaut. 
    """

    # Traitement des erreurs : 
    if selected_product_code is None: 
        raise ValueError('selected_product_code est vide.')
    elif selected_product_code not in data['code'].values : 
        print("Le produit sélectionné ne fait pas partie de la base de donnée.")
        return 

    # Création des données du produit sélectionné : 
    variables = ['label_bio', 'label_vege', 'energy_100g', 'fat_100g','saturated-fat_100g',
                 'salt_100g', 'sugars_100g', 'proteins_100g', 'fiber_100g', 'vitamin-a_100g',
                 'beta-carotene_100g', 'vitamin-d_100g', 'vitamin-e_100g', 'vitamin-k_100g',
                 'vitamin-c_100g', 'vitamin-b1_100g', 'vitamin-b2_100g', 'vitamin-pp_100g',
                 'vitamin-b6_100g', 'vitamin-b9_100g', 'vitamin-b12_100g', 'biotin_100g']
    
    selected_index = data.loc[data['code'] == selected_product_code].index
    selected_serie = data.loc[selected_index, variables].squeeze()

    selected_product = data.loc[selected_index]

    #______________________________________________________________________________________________________

    # Filtrage du dataset : 
    mask_1 = data['pnns_groups_1'] == selected_product['pnns_groups_1'].values[0]
    mask_2 = data['pnns_groups_2'] == selected_product['pnns_groups_2'].values[0]
    
    data = data.loc[mask_1 & mask_2].drop(selected_index)
    
    #______________________________________________________________________________________________________
    
    selected_name = selected_product['product_name'].values[0]
    data['similarity_name'] = data['product_name'].apply(lambda x: fuzz.token_set_ratio(x, selected_name))

    #______________________________________________________________________________________________________

    # Sélection des meilleurs produits tout confondu de la catégorie : 
    data_best_product = data.loc[data['score_tot'] == 'A']
    note_min = data_best_product['note_tot'].min()

        # Meilleur produit tout confondu de la catégorie :
    best_product_categ = data_best_product[data_best_product['note_tot'] == note_min]

    #______________________________________________________________________________________________________

    # Sélection du produit le plus similaire avec une meilleure note santé :
    mask_1 = data['note_sante'] < selected_product['note_sante'].values[0]
    data_sante = data[mask_1]
    
    mask_2 = data_sante['similarity_name'] == data_sante['similarity_name'].max()
    similar_product_best_sante = data_sante[mask_2]
    

    # Sélection du produit le plus similaire avec une meilleure note environnement :    
    mask_1 = data['note_environnement'] < selected_product['note_environnement'].values[0]
    data_envi = data[mask_1]
    
    mask_2 = data_envi['similarity_name'] == data_envi['similarity_name'].max()
    similar_product_best_environnement = data_envi[mask_2]

  #______________________________________________________________________________________________________

    # Retour du produits sélectionné : 
    print('--'*20+'\n')
    print("Vous avez choisi le produit :", selected_product['product_name'].values[0], '\n')
    print("Score santé du produit :", selected_product['score_sante'].values[0])
    print("Score environnement du produit :", selected_product['score_environnement'].values[0],'\n')
    print('--'*20+'\n')

    # Retour des produits similaires : 
    print("Proposition de produits similaires :\n")
    
    print(f"Le produit {similar_product_best_sante['product_name'].values[0]} "
          "sera le plus similaire avec un meilleur impact sur votre santé.")
    print("Score santé :", similar_product_best_sante['score_sante'].values[0], '\n')
    
    print(f"Le produit {similar_product_best_environnement['product_name'].values[0]} "
          "sera le plus similaire avec un meilleur impact sur l'environnement.")
    print("Score environnement :", similar_product_best_environnement['score_environnement'].values[0], '\n')

    print('--'*20+'\n')

    # Retour du meilleur produit de la catégorie : 
    print(f"Proposition du meilleur produit de la catégorie {best_product_categ['pnns_groups_1'].values[0]} | "
          f"{best_product_categ['pnns_groups_2'].values[0]} :\n")
    print(f"Le produit {best_product_categ['product_name'].values[0]} "
          "sera le produit avec le meilleur impact global de cette catégorie.")
    print(f"Score global : {best_product_categ['score_tot'].values[0]}")
    print(f"Score santé : {best_product_categ['score_sante'].values[0]}")
    print(f"Score environnement : {best_product_categ['score_environnement'].values[0]}")

    return