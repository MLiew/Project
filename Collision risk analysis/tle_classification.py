'''
Author: Liew Ying Jia
Date: 16 Apr 2020
Description:    This is a random forest classification module for two-line elements.
                If want to predict different value on the same random forest model, 
                call prediction(predict_input, random_forest).
Input value: New input data for prediction
Output variables:   accuracy, precision, recall, F1 score, max_estimators, 
                    random_forest model, rf_predict_input 
Output picture: Confusion matrix heatmap  
'''

import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier

def read_data(filepath):
    folder = 'csv_file'
    filename = 'TLE_Final_Cluster.csv'
    csv_filepath = filepath + '/' + folder + '/' + filename
    df = pd.read_csv(r"%s"%csv_filepath)
    df.head() 
    return df

def split_data(data):
    inputs = data.drop('Group', axis = 1)
    group_labels = data['Group']
    x_train, x_test, y_train, y_test = train_test_split(inputs, group_labels, test_size=0.2)
    print(inputs.head())
    
    return x_train, x_test, y_train, y_test

def kfold_tuning(x_train, y_train):
    rf_scores_cv = []
    num = [30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]

    for i in num:
        scores = cross_val_score(RandomForestClassifier(criterion = "gini", n_estimators = i, oob_score = True), x_train, y_train, cv = 10 )
        rf_scores_cv.append(np.average(scores))
        print("n_estimator:", i, "avg_val_score:", np.average(scores))

    max_index = rf_scores_cv.index(max(rf_scores_cv))
    max_cv_score = max(rf_scores_cv)
    print("Maximum average value is", max(rf_scores_cv), ", N-estimators is", num[max_index])

    max_estimators = num[max_index]
    print(max_estimators)

    temp_folder = 'C:/temp_data/'
    with open('%srf_max_estimators.txt'%temp_folder, 'w') as max_estimators_txt:
            max_estimators_txt.write(str(max_estimators))
    with open('%srf_max_cv_score.txt'%temp_folder, 'w') as max_cv_score_txt:
            max_cv_score_txt.write(str(max_cv_score))

    return max_estimators

def train_rf_model(x_train, x_test, y_train, y_test, max_estimators):
    # should return a model here
    random_forest = RandomForestClassifier(criterion = "gini", n_estimators= max_estimators, random_state = 40,  oob_score = True)
    random_forest.fit(x_train, y_train)
    acc_random_forest = round(random_forest.score(x_test, y_test)* 100, 4)
    print(acc_random_forest)
    
    return random_forest

def evaluation(random_forest, x_test, y_test,filepath):
    rf_acc = random_forest.score(x_test, y_test)
    print("Accuracy:", rf_acc)
    
    # Predictions
    rf_predictions = random_forest.predict(x_test)
    
    # Calculate recall, precision score and F1 score
    rf_precision = precision_score(y_test, rf_predictions, average='macro')
    rf_recall = recall_score(y_test, rf_predictions, average='macro')
    rf_f1_score = f1_score(y_test, rf_predictions, average = 'macro')

    print("Precision:", rf_precision)
    print("Recall:", rf_recall)
    print("F1 Score:", rf_f1_score)

    # Save evaluation score into txt file
    temp_folder = 'C:/temp_data/'
    with open('%srf_accuracy.txt'%temp_folder, 'w') as accuracy_txt:
            accuracy_txt.write(str(rf_acc))
    with open('%srf_precision.txt'%temp_folder, 'w') as precision_txt:
            precision_txt.write(str(rf_precision))
    with open('%srf_recall.txt'%temp_folder, 'w') as recall_txt:
            recall_txt.write(str(rf_recall))
    with open('%srf_f1.txt'%temp_folder, 'w') as f1_txt:
            f1_txt.write(str(rf_f1_score))

    # Confusion Matrix
    rf_con_matrix = confusion_matrix(y_test, rf_predictions)
    print(rf_con_matrix)

    # Plot heatmap for random forest confusion matrix
    folder = 'Picture'
    filename = 'Confusion_matrix.png'
    fig_path = filepath + '/' + folder + '/' + filename
    fig = sns.heatmap(rf_con_matrix, annot = True)
    con_heatmap = fig.get_figure()
    con_heatmap.savefig(fig_path, dpi = 400)
    plt.close()

    return rf_acc, rf_precision, rf_recall, rf_f1_score

def prediction(predict_input, random_forest):
    rf_predict_input = random_forest.predict(predict_input)[0]
    print(rf_predict_input)

    temp_folder = 'C:/temp_data/'
    with open('%srf_predict_input.txt'%temp_folder, 'w') as rf_predict_txt:
            rf_predict_txt.write(str(rf_predict_input))

    return rf_predict_input

def main_rf(filepath, predict_input):
    df = read_data(filepath)
    x_train, x_test, y_train, y_test = split_data(df)
    max_estimators = kfold_tuning(x_train, y_train)
    random_forest = train_rf_model(x_train, x_test, y_train, y_test, max_estimators)
    rf_acc, rf_precision, rf_recall, rf_f1_score = evaluation(random_forest, x_test, y_test, filepath)
    rf_predict_input = prediction(predict_input, random_forest)
    
    return random_forest, max_estimators, rf_acc, rf_precision, rf_recall, rf_f1_score, rf_predict_input

if __name__ == "__main__":
    filepath = 'C:/Users/LIEW YING JIA/Desktop/TLE_test_file'
    # Here should input a new input data for prediction
    predict_input = [[98.47462775,202.6435767,0.032286482,102.3841989,261.3666106,7231420.051]]
    random_forest, max_estimators, rf_acc, rf_precision, rf_recall, rf_f1_score, rf_predict_input = main_rf(filepath, predict_input)
    predict_input = [[150,150.55669 ,0.002286482,102.3841989,56.349,7500000.051]]
    prediction(predict_input, random_forest)