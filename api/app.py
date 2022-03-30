import pandas as pd
import numpy as np
from flask import render_template,request, Flask, make_response, abort
from werkzeug.exceptions import Unauthorized,BadRequest
from sklearn.model_selection import train_test_split as tts
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsRegressor


app = Flask(__name__)

#             Récupération des users et password
df_users=pd.read_csv('credentials.csv', sep =',')
users = dict([(i,j) for i,j in zip (df_users['username'],df_users['password'])])
print (users)

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
    
    #               Entrainement du modèle linéaire
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
    print(username,password)
    if username in users.keys():
        if users[username] == password:
            authenticated_user = True
    return authenticated_user

def check_data(data):
    # Vérification que les données récupérée soit cohérente avec celle que nous avons observées

    if data['meteo'] is in ['clear','cloudy', 'rainy', 'snowy']:
        meteo = ['clear','cloudy', 'rainy', 'snowy'].index(data['meteo'], 1, 4) # en supposant qu'une météo soit entrée parmis les 4 possible on ressort avec son mode
    else raise "Wrong Meteo"
    if data['day'] is in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]:
        day = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"].index(data['day'], 0, 6) #en supposant que qu'un jour de la semaine est entrée, on ressort avec son mode
    else raise "Wrong WeekDay"
    if -10.7 < data['temp'] < 39.4: #ici j'ai pris les min et max présent dans le DF bike
        temp = data['temp']
    else raise "Wrong Temperature"
    if 22 < data['bike'] < 8714: #idem
        bike = data['bike']
    else raise "Wrong bike number" #Si la vérification se conclue par une erreur alors ce sera la valeur de daily
    daily = [meteo, temp, bike, day] #les données sont rangée dans le même ordre que les colonnes du DF bike
    return daily

@app.route("/status")
def status():
#Renvoie 1 si l'API fonctionne
    return "1\n"

@app.route("/permissions",methods=["POST"])
def permissions():
    data=request.get_json()
    if authenticate_user(data['username'],data['password'])==True:
        return "Good Id"
    else:
        raise Unauthorized("Wrong Id")

@app.route('/biketomorrow/LR',methods=["POST"])
def biketomorrow_KGH():
    data=request.get_json()
    if authenticate_user(data['username'],data['password'])==True:
        daily = check_data(data)
        if type(daily) == list: 
            Yfit_lr, Yfit_logR, Yfit_knR = prepa_data()
            result = linear_model(Yfit_lr, daily)
            return "There will be {} bike predicted tomorrow with the Linear Regression model".format(result)
        else raise "Wrong daily data"
    else:
        raise Unauthorized("Wrong Id")

     
        
@app.route('/biketomorrow/LOGR',methods=["POST"])
def biketomorrow_LGST():
    form_data = request.form #form_data est un dictionnaire de forme {'nom input':'input'}
    data=request.get_json()
    if authenticate_user(data['username'],data['password'])==True:
        Yfit_lr, Yfit_logR, Yfit_knR = prepa_data()
        result = logistic_model(Yfit_logR, data['daily'])
        return "There will be {} bike predicted tomorrow with the Logistic Regression model".format(result)
    else:
        raise Unauthorized("Wrong Id")
        
                
@app.route('/biketomorrow/KNR',methods=["POST"])
def biketomorrow_LR():
    form_data = request.form #form_data est un dictionnaire de forme {'nom input':'input'}
    data=request.get_json()
    if authenticate_user(data['username'],data['password'])==True:
        Yfit_lr, Yfit_logR, Yfit_knR = prepa_data()
        result = kneighbor_model(Yfit_knR, data['daily'])
        return "There will be {} bike predicted tomorrow with the KNeighbors Regressor model".format(result)
    else:
        raise Unauthorized("Wrong Id")
        
        

