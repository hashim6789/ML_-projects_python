import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

matches = pd.read_csv('ipl_2008_2023.csv')

# replace duplicates of team names
matches.batting_team = matches.batting_team.str.replace('Gujarat Lions','Gujarat Titans')
matches.bowling_team = matches.bowling_team.str.replace('Gujarat Lions','Gujarat Titans')

matches.batting_team = matches.batting_team.str.replace('Rising Pune Supergiant','Pune Warriors')
matches.bowling_team = matches.bowling_team.str.replace('Rising Pune Supergiant','Pune Warriors')

matches.batting_team = matches.batting_team.str.replace('Rising Pune Supergiants','Pune Warriors')
matches.bowling_team = matches.bowling_team.str.replace('Rising Pune Supergiants','Pune Warriors')

matches.batting_team = matches.batting_team.str.replace('Pune Warriorss','Pune Warriors')
matches.bowling_team = matches.bowling_team.str.replace('Pune Warriorss','Pune Warriors')


teams = ['Gujarat Titans', 'Rajasthan Royals', 'Lucknow Super Giants',
       'Punjab Kings', 'Mumbai Indians', 'Royal Challengers Bangalore',
       'Kolkata Knight Riders', 'Sunrisers Hyderabad', 'Delhi Capitals',
       'Chennai Super Kings', 'Pune Warriors', 'Kochi Tuskers Kerala']


#remove unwanted coloumns
unwanted = ['city', 'crr', 'rrr','id']
matches.drop(unwanted, axis=1, inplace=True)


#encode the chategorical data

#encoding the batting team column
matches.replace({'batting_team':{'Gujarat Titans': 12, 'Rajasthan Royals':1, 'Lucknow Super Giants':2,'Punjab Kings': 3, 'Mumbai Indians':4, 'Royal Challengers Bangalore':5,'Kolkata Knight Riders': 6, 'Sunrisers Hyderabad':7, 'Delhi Capitals':8,'Chennai Super Kings':9, 'Pune Warriors':10, 'Kochi Tuskers Kerala':11}},inplace=True)
#encoding the bowling team column
matches.replace({'bowling_team':{'Gujarat Titans': 12, 'Rajasthan Royals':1, 'Lucknow Super Giants':2,'Punjab Kings': 3, 'Mumbai Indians':4, 'Royal Challengers Bangalore':5,'Kolkata Knight Riders': 6, 'Sunrisers Hyderabad':7, 'Delhi Capitals':8,'Chennai Super Kings':9, 'Pune Warriors':10, 'Kochi Tuskers Kerala':11}},inplace=True)



#splitting data and target
X = matches.drop(columns=['results'])
Y = matches.results

#splitting X,Y into training and testing.
from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2)

# Initialize the Random Forest classifier
random_forest = RandomForestClassifier()

# Train the model
random_forest.fit(X_train, Y_train)

# Predict on the test set
Y_pred = random_forest.predict(X_test)

#model deployment
pickle.dump(random_forest,open('./random_forest_model.sav', 'wb'))