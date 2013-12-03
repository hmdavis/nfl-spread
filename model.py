import numpy as np 
from sklearn.tree import DecisionTreeRegressor
from sklearn.grid_search import GridSearchCV
import pylab as pl 

''' 
This file just shows three examples of simple ways to quickly check models
''' 

# split the data into train, test set 
X_train, y_train, X_test, y_test = cross_validation.train_test_split(X,y,test_size=0.3, random_state=0)


# straight up, no funny business 
dt = DecisionTreeRegressor(max_depth=10)
dt.fit(X_train, y_train)
print dt.score(X_test, y_test)


# see how model performs with cross validations 
scores = cross_validation.cross_val_score(dt, X, y, cv=5)
print scores.mean() 
print scores.std() 


# grid search will exhaustively evalulate model with supplied parameters
param_grid = [
	{'max_depth': [2, 3, 5, 10, 50, 80, 100]}
]
dtr = DecisionTreeRegressor() 
gs = GridSearchCV(dtr, param_grid, cv=5)
gs.fit(X_train, y_train)
print gs.score(X_test, y_test) 
# print gs.best_estimator_.get_params() 
# print gs.best_score_

