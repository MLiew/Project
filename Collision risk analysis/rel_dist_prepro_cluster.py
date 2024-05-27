'''
Author: Liew Ying Jia
Date: 17 Apr 2020
Description:    This is a data preprocessing and clustering module for relative distances.
Input value: Total relative distances
Output:   Two csv file
'''

import pandas as pd
import numpy as np
import seaborn as sns
# import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from sklearn.cluster import KMeans
from scipy import stats
from sklearn import metrics
from sklearn.metrics import silhouette_samples, silhouette_score

def read_data(filepath):
    folder_name = 'csv_file'
    filename = 'Total_rel_dis.csv'
    csv_filepath = filepath + '/' + folder_name + '/' + filename
    dist_data = pd.read_csv(r"%s"%csv_filepath)
    dist_data = dist_data.drop(['Phase difference', 'Height difference', 'Inclination difference'], axis=1)
    
    return dist_data

def z_score(dist_data, filepath,seq):
    zscore_df = dist_data.apply(stats.zscore)
    
    # zscore_df_des = zscore_df.describe()
    save_bxplot(zscore_df, filepath, seq)
    
    print(zscore_df)

    return zscore_df

def save_bxplot(data, filepath, seq):
    # Create a Picture folder to store all the pictures
    folder = 'Picture'
    newpath = filepath + '/' + folder

    fig_dims = (6, 4)
    fig, ax = plt.subplots(figsize = fig_dims)
    fig = sns.boxplot(x = data['Total distance'], ax = ax, orient="h", palette="Set2")
    # plt.show()
    boxplot = fig.get_figure()
    if seq == 0:
        boxplot.savefig('%s/rel_dist_boxplot1.png'%newpath, dpi=400)
    else:
        boxplot.savefig('%s/rel_dist_boxplot2.png'%newpath, dpi=400)
    plt.close()

def remove_outlier(zscore_df, dist_data, filepath):
    # Get the index of the outliers
    index = zscore_df[(zscore_df['Total distance']> 3)].index
    cnt = 3
    data_amount = zscore_df.size

    while len(index) >= (data_amount * 0.01):
        cnt += 1
        index = zscore_df[(zscore_df['Total distance']> cnt)].index

    # After finding out the outliers index, remove the outliers from zscore_df
    index = zscore_df[(zscore_df['Total distance']> cnt)].index
    removed_outlier_dist = dist_data.drop(index)
    removed_outlier_dist_desc = removed_outlier_dist.describe()

    return removed_outlier_dist, removed_outlier_dist_desc

def save_csv(data, filepath, filename):
    csv_filepath = filepath + '/' + 'csv_file/' + filename 
    data.to_csv (r'%s'%csv_filepath, index = False, header=True)

def main_dist_prepro(filepath):
    dist_data = read_data(filepath)
    z_score_df = z_score(dist_data, filepath, 0)
    removed_outlier_dist, removed_outlier_dist_desc = remove_outlier(z_score_df, dist_data, filepath)
    z_score_final_df = z_score(removed_outlier_dist, filepath, 1)

    # Save final normalized distance without outlier into csv file
    save_csv(z_score_final_df, filepath, 'Total_dist_preprocessed.csv')
    # Save original distance data without outliers
    save_csv(removed_outlier_dist, filepath, 'Total_dist_outlier_removed.csv')

    return z_score_df, removed_outlier_dist, removed_outlier_dist_desc, z_score_final_df

if __name__ == "__main__":
    filepath = 'C:/Users/LIEW YING JIA/Desktop/TLE_test_file'
    main_dist_prepro(filepath)