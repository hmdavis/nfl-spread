'''
Test our data with various machine learned models
''' 
import sys, math
import numpy as np 
from sklearn import cross_validation, neighbors
from sklearn.tree import DecisionTreeRegressor
from sklearn.grid_search import GridSearchCV
from sklearn.datasets import load_files 
import pylab as pl 


''' 
Prepare the dataset to be used in algorithms 
Params: 
	f: filepath 
Returns: 
	X: feature instances 
	y: label instances
'''
def load_data(f): 
	# read in the data as feature, label arrays 
	data = np.loadtxt(f, delimiter=',') 
	X = data[:,:-1]
	y = data[:,-1:]

	# normalize the data with l2 norm 
	row, col = X.shape 
	for r in range(row): 
		l2 = np.linalg.norm(X[r,:])
		X[r,:] /= l2 

	return X, y 


''' 
Calculate the average difference between predicted and expected spreads
Params: 
	pred: predicted spreads
	real: expected spreads
	multidimen: whether or not array shapes are (n,0) or (n,)
Returns: 
	avg: average difference 
'''
def avg_spread_difference(pred, real, multidimen): 
	diffs = [] 

	if multidimen: 
		row, col = pred.shape
		for x in range(row): 
			p = pred[x,0]
			r = real[x,0]
			diffs.append(abs(p-r))
	else: 
		row = len(pred)
		for x in range(row): 
			p = pred[x]
			r = real[x]
			diffs.append(abs(p-r))

	avg = sum(diffs) / len(diffs) 
	return avg 


''' 
Calculates the percentage of times we predict the correct winner
Params: 
	pred: predicted spreads
	real: expected spreads
	multidimen: whether or not array shapes are (n,0) or (n,)
Returns: 
	pctg: pctg of correct predictions 
'''
def percent_same_winner(pred, real, multidimen): 
	correct = 0.0

	if multidimen: 
		row, col = pred.shape
		for x in range(row): 
			p = pred[x,0]
			r = real[x,0]
			if (p > 0.0 and r > 0.0) or (p < 0.0 and r < 0.0) or (p == 0.0 and r == 0.0):
				correct += 1.0
	else: 
		row = len(pred)
		for x in range(row): 
			p = pred[x]
			r = real[x]
			if (p > 0.0 and r > 0.0) or (p < 0.0 and r < 0.0) or (p == 0.0 and r == 0.0):
				correct += 1.0

	pctg = correct / row 
	return pctg


''' 
Runs kNN regression over various k values 
Params: 
	X: features
	y: labels
'''
def knn(X,y):
	# split the data into train, test set 
	X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size=0.3, random_state=0)

	n_neighbors = [1,2,5,10,50,100]
	for k in n_neighbors: 
		knn = neighbors.KNeighborsRegressor(k)
		knn.fit(X_train, y_train)

		print "############## TRAINING ERROR, k=", k, "##############"
		pred = knn.predict(X_train)
		print "Spread:\t", avg_spread_difference(pred, y_train, True)
		print "Winner:\t", percent_same_winner(pred, y_train, True) 
		print "Score:\t", knn.score(X_train, y_train)

		print "############## TESTING ERROR, k=", k, "##############"
		pred = knn.predict(X_test)
		print "Spread:\t", avg_spread_difference(pred, y_test, True)
		print "Winner:\t", percent_same_winner(pred, y_test, True) 
		print "Score:\t", knn.score(X_test, y_test)


''' 
Runs decision tree regression over various depth values
Params: 
	X: features
	y: labels
'''
def dt(X,y): 
	# split data 
	X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size=0.3, random_state=0)

	max_depth = [1,2, 3, 5, 10, 50, 80, 100]
	
	for d in max_depth:
	# straight up, no funny business 
		dt = DecisionTreeRegressor(max_depth=d)
		dt.fit(X_train, y_train)
		
		print "############## TRAINING ERROR, d=", d, "##############"
		pred = dt.predict(X_train)[:]
		print "Spread:\t", avg_spread_difference(pred, y_train, False)
		print "Winner:\t", percent_same_winner(pred, y_train, False) 
		print "Score:\t", dt.score(X_train, y_train)

		print "############## TESTING ERROR, d=", d, "##############"
		pred = dt.predict(X_test)[:]
		print "Spread:\t", avg_spread_difference(pred, y_test, False)
		print "Winner:\t", percent_same_winner(pred, y_test, False) 
		print "Score:\t", dt.score(X_test, y_test)


X, y = load_data(sys.argv[1])
knn(X,y) 
dt(X,y)
