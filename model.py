'''
Test our data with various machine learned models
''' 

import sys, math, argparse
import numpy as np
import pylab as pl 
from sklearn import cross_validation, neighbors, feature_selection, svm
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.grid_search import GridSearchCV
from sklearn.datasets import load_files 
from sklearn.ensemble import RandomForestRegressor



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
    X = data[:,:-2]
    y = data[:,-2:-1]
    y_vegas = data[:,-1:]

    # normalize the data with l2 norm 
    row, col = X.shape 
    for r in range(row): 
        l2 = np.linalg.norm(X[r,:])
        X[r,:] /= l2 

    return X, y, y_vegas


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

def percent_vegas_winner(pred, real, vegas, multidimen): 
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
            v = vegas[x]
            actual_diff = r - v
            pred_diff = p - v
            if math.copysign(1,actual_diff) == math.copysign(1,pred_diff):
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

    # X, X_val, y, y_val = cross_validation.train_test_split(X,y,test_size=0.2, random_state=0)
    k_fold = cross_validation.KFold(n=len(y), n_folds=5, indices=True, shuffle=True)
    n_neighbors = [1,2,5,10,50,100]

    for k in n_neighbors: 
        for train, test in k_fold:

            spreads_train = []
            spreads_test = []
            acc_train = [] 
            acc_test = [] 
            score_train = [] 
            score_test = [] 
            
            X_train , y_train = (X[train], y[train])
            X_test, y_test = (X[test], y[test])
            knn = neighbors.KNeighborsRegressor(k)
            knn.fit(X_train, y_train)

            # calculate training errors 
            pred = knn.predict(X_train)
            spreads_train.append(avg_spread_difference(pred, y_train, True))
            acc_train.append(percent_same_winner(pred, y_train, True)) 
            score_train.append(knn.score(X_train, y_train))

            # calculate test errors 
            pred = knn.predict(X_test)
            spreads_test.append(avg_spread_difference(pred, y_test, True))
            acc_test.append(percent_same_winner(pred, y_test, True)) 
            score_test.append(knn.score(X_test, y_test))

        print "\n>> TRAIN, k=", k 
        print "Avg. Spread:\t", sum(spreads_train) / float(len(spreads_train))
        print "Avg. Winner:\t", sum(acc_train) / float(len(acc_train))
        print "Avg. R^2 Score:\t", sum(score_train) / float(len(score_train))

        print "\n>> TEST, k=", k 
        print "Avg. Spread:\t", sum(spreads_test) / float(len(spreads_test))
        print "Avg. Winner:\t", sum(acc_test) / float(len(acc_test))
        print "Avg. R^2 Score:\t", sum(score_test) / float(len(score_test))


''' 
Runs random forest regression over various forest sizes
Params: 
    X: features
    y: labels
'''
def rf(X,y): 
    k_fold = cross_validation.KFold(n=len(y), n_folds=5, indices=True, shuffle=True)
    size_forest = [10, 25, 50, 100]

    for n in size_forest: 
        for train, test in k_fold: 

            spreads_train = []
            spreads_test = []
            acc_train = [] 
            acc_test = [] 
            score_train = [] 
            score_test = []
            
            X_train, y_train = (X[train], y[train])
            X_test, y_test = (X[test], y[test])
            rf = RandomForestRegressor(n_estimators=n)
            rf.fit(X_train, y_train)
            
            # calculate training errors 
            pred = rf.predict(X_train)[:]
            spreads_train.append(avg_spread_difference(pred, y_train, False))
            acc_train.append(percent_same_winner(pred, y_train, False)) 
            score_train.append(rf.score(X_train, y_train))

            # calculate test errors 
            pred = rf.predict(X_test)[:]
            spreads_test.append(avg_spread_difference(pred, y_test, False))
            acc_test.append(percent_same_winner(pred, y_test, False)) 
            score_test.append(rf.score(X_test, y_test))

        print "\n>> TRAIN, size_forest=", n 
        print "Avg. Spread:\t", sum(spreads_train) / float(len(spreads_train))
        print "Avg. Winner:\t", sum(acc_train) / float(len(acc_train))
        print "Avg. R^2 Score:\t", sum(score_train) / float(len(score_train))

        print "\n>> TEST, size_forest=", n
        print "Avg. Spread:\t", sum(spreads_test) / float(len(spreads_test))
        print "Avg. Winner:\t", sum(acc_test) / float(len(acc_test))
        print "Avg. R^2 Score:\t", sum(score_test) / float(len(score_test))
        
        
''' 
Runs decision tree regression over various depth values
Params: 
    X: features
    y: labels
'''
def dt(X_train,y_train,X_test,y_test): 
    # split data 

    # X, X_val, y, y_val = cross_validation.train_test_split(X,y,test_size=0.2, random_state=0)
    k_fold = cross_validation.KFold(n=len(y), n_folds=5, indices=True, shuffle=True)
    max_depth = [1,2, 3, 5, 10, 50, 80, 100]
    
    for d in max_depth:
        for train, test in k_fold:

            spreads_train = []
            spreads_test = []
            acc_train = [] 
            acc_test = [] 
            score_train = [] 
            score_test = [] 
            
            X_train , y_train = (X[train], y[train])
            X_test, y_test = (X[test], y[test])
            dt = DecisionTreeRegressor(max_depth=d)
            dt.fit(X_train, y_train)
        
            # calculate training error 
            pred = dt.predict(X_train)[:]
            spreads_train.append(avg_spread_difference(pred, y_train, False))
            acc_train.append(percent_same_winner(pred, y_train, False)) 
            score_train.append(dt.score(X_train, y_train))

            pred = dt.predict(X_test)[:]
            spreads_test.append(avg_spread_difference(pred, y_test, False))
            acc_test.append(percent_same_winner(pred, y_test, False)) 
            score_test.append(dt.score(X_test, y_test))

        print "\n>> TRAIN, d=", d 
        print "Avg. Spread:\t", sum(spreads_train) / float(len(spreads_train))
        print "Avg. Winner:\t", sum(acc_train) / float(len(acc_train))
        print "Avg. R^2 Score:\t", sum(score_train) / float(len(score_train))

        print "\n>> TEST, d=", d 
        print "Avg. Spread:\t", sum(spreads_test) / float(len(spreads_test))
        print "Avg. Winner:\t", sum(acc_test) / float(len(acc_test))
        print "Avg. R^2 Score:\t", sum(score_test) / float(len(score_test))

'''
SVM regression
'''
def svmTest(X_train,y_train,X_test,y_test,y_vegas_test): 
    y_train_composed = [x for [x] in y_train]

    C_range = 10.0 ** np.arange(2, 6)
    gamma_range = 10.0 ** np.arange(-5, 4)

    best_spread_difference = 1000

    for c in C_range:
        for gamma in gamma_range:
            svmRegressor = svm.SVR(kernel='rbf', C=c, gamma=gamma)
            svmRegressor.fit(X_train, y_train_composed)
            pred = svmRegressor.predict(X_test)[:]
            curr_spread_difference = avg_spread_difference(pred, y_test, False)

            # try:
            #     if curr_spread_difference < best_spread_difference:
            #         print "############## TESTING ERROR C=",c," gamma=",gamma,"##############"
            #         print "Spread:\t", curr_spread_difference
            #         print "Winner:\t", percent_same_winner(pred, y_test, False) 
            #         best_spread_difference = curr_spread_difference
            # except:
            #     best_spread_difference = curr_spread_difference

            print "############## TESTING ERROR C=",c," gamma=",gamma,"##############"
            print "Winner against the Line:\t", percent_vegas_winner(pred, y_test, y_vegas_test,False) 
            best_spread_difference = curr_spread_difference



###############################################################################
argparser = argparse.ArgumentParser()
argparser.add_argument('training', type=file)
argparser.add_argument('testing', type=file) 
argparser.add_argument('--knn', action='store_true', default=False)
argparser.add_argument('--dt', action='store_true', default=False)
argparser.add_argument('--svm', action='store_true', default=False)
argparser.add_argument('--rf', action='store_true', default=False)

args = argparser.parse_args()

X_train, y_train, y_vegas_train = load_data(args.training)
X_test, y_test, y_vegas_test = load_data(args.testing)

#X,y = load_data(args.training)

#print X_train.shape, X_test.shape

if args.knn:
    knn(X_train,y_train,X_test,y_test)
elif args.dt:
    dt(X_train,y_train,X_test,y_test)
elif args.svm:
    svmTest(X_train,y_train,X_test,y_test,y_vegas_test)
elif args.rf:
    rf(X,y)
else: 
    print "Usage: [--knn] [--dt] [--rf] [--svm]"
