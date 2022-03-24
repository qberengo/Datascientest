import pandas as pd
import numpy as np
from flask import render_template,request, Flask, make_response, abort
from werkzeug.exceptions import Unauthorized,BadRequest
from sklearn.model_selection import train_test_split as tts
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsRegressor


def prepa_data():
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
    
    #               Entrinement du modèle linéaire
    lr = LinearRegression() 
    # Entrainement du modèle
    Yfit_lr = lr.fit(X,y)
    #               Entrinement du modèle logistique
    logR = LogisticRegression(solver = "newton-cg")
    # Entrainement du modèle
    Yfit_logR = logR.fit(X, y)
    #               Entrinement du modèle voisinage
    knR = KNeighborsRegressor(n_neighbors = 5)
    # Entrainement du modèle
    Yfit_knR = knR.fit(X, y)

    return Yfit_lr, Yfit_logR, Yfit_knR

def linear_model(Yfit_lr, daily):
    # Prédiction de la variable cible pour le jeu de données TEST
    y_pred_lr = Yfit_lr.predict(daily)
    return y_pred_lr
def logistic_model(Yfit_logR, daily):
    # Prédiction de la variable cible pour le jeu de données TEST
    y_pred_lr = Yfit_logR.predict(daily)
    return y_pred_logR
def kneighbor_model(Yfit_knR, daily):
    # Prédiction de la variable cible pour le jeu de données TEST
    y_pred_lr = Yfit_knR.predict(daily)
    return y_pred_knR

def authenticate_user(username, password):
    authenticated_user = False
    if username in users.keys():
        if users[username] == password:
            authenticated_user = True
    return authenticated_user

@app.route("/status")
def status():
#Renvoie 1 si l'API fonctionne
    return "1\n"

@app.ruote('/biketomorrow')
def biketomorrow():
    return render_template('form.html')

@app.route('/biketomorrow/LR',methods=["POST"])
def biketomorrow_LR():
    form_data = request.form #form_data est un dictionnaire de forme {'nom input':'input'}
    data=request.get_json()
    if authenticate_user(data['username'],data['password'])==True:
        Yfit = prepa_data()
        result = linear_model(Yfit, data['daily'])
        return "There will be {} bike tomorrow".format(result)
    else:
        raise Unauthorized("Wrong Id")
