'''
Author: Liew Ying Jia
Date: 15 Apr 2020
Description: This is a data preprocessing module for two-line elements.
'''

import os
import pandas as pd
import numpy as np
import seaborn as sns
# import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from scipy import stats

def read_data(filepath):
    csv_filepath = filepath + '/' + 'csv_file/' + 'TLE_data.csv'
    tle_df = pd.read_csv(csv_filepath)
    tle_input = tle_df.drop(['Name', 'Mean Motion', 'Revolution Num', 'Period(s)'], axis=1)
    tle_input_desc = tle_input.describe()
    # print(tle_input_desc)
    
    return tle_input, tle_input_desc

# Z-score normalization
def z_score_norm(tle_input, filepath, seq):
    zscore_list = stats.zscore(tle_input)
    zscore_df = pd.DataFrame(zscore_list, columns = ['Inclination', 'RAAN', 'Eccentricity', 
                                    'ArgPerigee', 'MAnomaly', 'SMAxis'])

    zscore_df_des = zscore_df.describe()
    save_bxplot(zscore_df, filepath, seq)

    return zscore_df, zscore_df_des

def save_bxplot(data, filepath, seq):
    # Create a Picture folder to store all the pictures
    folder = 'Picture'
    newpath = filepath + '/' + folder

    if not os.path.exists(newpath):
        os.makedirs(newpath)

    fig_dims = (7.5, 4)
    fig, ax = plt.subplots(figsize=fig_dims)
    fig = sns.boxplot(data = data, ax = ax, orient="h", palette="Set2")
    # plt.show()
    boxplot = fig.get_figure()
    
    if seq == 0:
        boxplot.savefig('%s/boxplot1.png'%newpath, dpi=400)
    elif seq == 1:
        boxplot.savefig('%s/boxplot2.png'%newpath, dpi=400)
    
    plt.close()
    return 0

def remove_outlier(zscore, tle_input, filepath):
    # Get the index of the outliers
    # Consider zscore>3 is outlier
    # Only remove outliers from semi-major axis column
    index = zscore[(zscore['SMAxis']> 3)].index
    # print(index)

    # Remove outliers from original dataset: tle_input
    tle_r_outlier = tle_input
    tle_r_outlier.drop(index, inplace = True)
    tle_r_outlier_desc = tle_r_outlier.describe()
    # print(tle_r_outlier_desc)

    return tle_r_outlier, tle_r_outlier_desc

def save_csv(data, filepath, filename):
    csv_filepath = filepath + '/' + 'csv_file/' + filename 
    data.to_csv (r'%s'%csv_filepath, index = False, header=True)

def main_prepro_one(filepath):
    # filepath = 'C:/Users/LIEW YING JIA/Desktop/TLE_test_file'
    
    # Read in data
    tle_input, tle_input_desc = read_data(filepath)
    # Zscore normalized input data
    zscore_first, zscore_first_desc = z_score_norm(tle_input, filepath, 0)
    # Remove outliers
    tle_r_outlier, tle_r_outlier_desc = remove_outlier(zscore_first, tle_input, filepath)
    # Save removed outliers data into csv
    save_csv(tle_r_outlier, filepath, 'TLE_data_outlier_removed.csv')
    # Zscore normalized data without outliers
    zscore_sec, zscore_sec_desc = z_score_norm(tle_r_outlier, filepath, 1)
    # Save the zscore normalized data without outliers
    save_csv(zscore_sec, filepath, 'TLE_normalized_data.csv')
    
    return tle_input_desc, zscore_first_desc, tle_r_outlier_desc, zscore_sec_desc

if __name__ == "__main__":
    filepath = 'C:/Users/LIEW YING JIA/Desktop/TLE_test_file'
    main_prepro_one(filepath)