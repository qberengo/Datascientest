
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import NLTKWordTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

# j'ai réduit la taille du fichier csv car il était trop gros pour l'importer dans Github
df = pd.read_csv(' DisneylandReviews.csv', encoding='cp1252')

# Préparation des données
df = df.drop(['Review_ID', 'Year_Month', 'Reviewer_Location'], axis=1)

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    stop_words.update(["'ve", "", "'ll", "'s", ".", ",", "?", "!", "(", ")", "..", "'m", "n", "u"])
    tokenizer = NLTKWordTokenizer()
    
    text = text.lower()
    
    tokens = tokenizer.tokenize(text)
    tokens = [t for t in tokens if t not in stop_words]
    
    return ' '.join(tokens)

df['Review_Text'] = df['Review_Text'].apply(preprocess_text)

# Premier Modele

features = df['Review_Text']
target = df['Rating']


X_train, X_test, y_train, y_test = train_test_split(features, target)

count_vectorizer_unique = CountVectorizer(max_features=2000)

X_train_cv = count_vectorizer_unique.fit_transform(X_train)
X_test_cv = count_vectorizer_unique.transform(X_test)
