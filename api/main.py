import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split as tts
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold


#             Préparation des données
# On crée le data frame df à partir du fichier csv
df = pd.read_csv("bike.csv",sep=',', header=0)
# Remplacement des valeurs de météo par des catégories numériques
df = df.replace(to_replace = ['clear','cloudy', 'rainy', 'snowy'], value= [1, 2, 3,4])
# Conversion du type de colonne
df['weathersit'] = df['weathersit'].astype('int')
# Suppression des doublons
df = df.drop_duplicates()
# Définition du dictionnaire de fonctions à appliquer
function_to_apply = {
    'weathersit' : ['mean'],
    'hum' : ['min','max','mean'],
    'windspeed' : ['min','max','mean'],
    'temp' : ['min','max','mean'],
    'atemp' : ['min','max','mean'],
    'cnt' : ['sum'],
}
# Agrégation des données par jour et affichage
df_groupby=df.groupby("dteday").agg(function_to_apply).reset_index()
df_groupby.columns = df_groupby.columns.droplevel()
df_groupby.columns = ['dteday','mean_weathersit', 'min_hum', 'max_hum', 'mean_hum','min_windspeed','max_windspeed', 'mean_windspeed','min_temp','max_temp','mean_temp', 'min_atemp', 'max_atemp', 'mean_atemp', 'sum_cnt']
# Création colonne "weekday" dans le DataFrame contenant une catégorisation du jour de la semaine avec 0 = lundi ... et 6 = dimanche
df_["weekday"] = df_["dteday"].apply(lambda x : x.weekday())
# Définition du DataFrame définitif de travail selon les features séléctionnées : 
bike = df_.drop(["mean_windspeed", "dteday", "mean_temp", "mean_hum" ], axis = 1)
# Division du DataFrame en 2 autres : X pour les variables explicatives et y pour la cible
X = bike.drop([ "cnt_"], axis = 1)
y = bike["cnt_"]
# Division de ces deux nouveaux DataFrame en des jeux d'entrainements et de tests avec une conservation d'un tier des variables dans les jeux de tests. 
Xtrain, Xtest, Ytrain, Ytest = tts(X, y, test_size = 0.3)

#               Entrinement du modèle
lr = LinearRegression() 
# Entrainement du modèle
Yfit_lr = lr.fit(Xtrain,Ytrain)
# Prédiction de la variable cible pour le jeu de données TRAIN
y_pred_train_lr = lr.predict(Xtrain)
# Prédiction de la variable cible pour le jeu de données TEST
y_pred_test_lr = lr.predict(Xtest)