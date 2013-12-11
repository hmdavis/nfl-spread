'''
Test our data with various machine learned models
''' 
import sys, math
import numpy as np
from sklearn import cross_validation, neighbors, feature_selection, svm
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.grid_search import GridSearchCV
from sklearn.datasets import load_files 
import pylab as pl 
import argparse

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

def f_regression(X,y):
   return feature_selection.f_regression(X,y,center=False)

''' 
Runs kNN regression over various k values 
Params: 
	X: features
	y: labels
'''
def knn(X_train,y_train,X_test,y_test):
	#feature selection
	#featureSelector = feature_selection.SelectKBest(score_func=f_regression,k=10)
	#Xselected = featureSelector.fit_transform(X,y)

	# split the data into train, test set 
	#X_train, X_test, y_train, y_test = cross_validation.train_test_split(Xselected,y,test_size=0.3, random_state=0)

	n_neighbors = [1,2,5,10,20,30,40,50,60,70,80,100]
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
def dt(X_train,y_train,X_test,y_test): 
	# split data 
	#X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size=0.3, random_state=0)

	max_depth = [3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20]
	
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

'''
SVM regression
'''
def svmTest(X_train,y_train,X_test,y_test): 
	y_train_composed = [x for [x] in y_train]

	C_range = 10.0 ** np.arange(-3, 6)
	gamma_range = 10.0 ** np.arange(-5, 4)

	best_spread_difference = 1000

	for c in C_range:
		for gamma in gamma_range:
			svmRegressor = svm.SVR(kernel='rbf', C=c, gamma=gamma)
			svmRegressor.fit(X_train, y_train_composed)
			pred = svmRegressor.predict(X_test)[:]
			curr_spread_difference = avg_spread_difference(pred, y_test, False)

			try:
				if curr_spread_difference < best_spread_difference:
					print "############## TESTING ERROR C=",c," gamma=",gamma,"##############"
					print "Spread:\t", curr_spread_difference
					print "Winner:\t", percent_same_winner(pred, y_test, False) 
					best_spread_difference = curr_spread_difference
			except:
				best_spread_difference = curr_spread_difference

argparser = argparse.ArgumentParser()
argparser.add_argument('testing', type=file)
argparser.add_argument('training', type=file) 
argparser.add_argument('--knn', action='store_true', default=False)
argparser.add_argument('--dt', action='store_true', default=False)
argparser.add_argument('--svm', action='store_true', default=False)


args = argparser.parse_args()

X_train, y_train = load_data(args.testing)
X_test, y_test = load_data(args.training)

print X_test.shape, X_train.shape

if args.knn:
	knn(X_train,y_train,X_test,y_test)
if args.dt:
	dt(X_train,y_train,X_test,y_test)
if args.svm:
	svmTest(X_train,y_train,X_test,y_test)
