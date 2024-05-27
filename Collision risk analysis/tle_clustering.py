'''
Author: Liew Ying Jia
Date: 16 Apr 2020
Description: This is a data clustering module for two-line elements.
Algorithm: Spectral Clustering/ KMeans Clustering
'''

import pandas as pd
import numpy as np
import seaborn as sns
import plotly as py
# import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from sklearn.cluster import KMeans, SpectralClustering
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats
from sklearn import metrics
from sklearn.metrics import silhouette_samples, silhouette_score, calinski_harabasz_score

def read_data(filepath, filename):
    folder_name = 'csv_file'
    csv_filepath = filepath + '/' + folder_name + '/' + filename
    tle_data = pd.read_csv(r"%s"%csv_filepath)
    
    return tle_data

def parameter_tuning(filepath, tle_data, method, module):
    # Create array
    num_clusters = np.arange(2, 11)

    # Create a list to store silhouette values
    sil_avg_data = []
    ch_score = []
    Sum_of_squared_distances = []

    for i in num_clusters:
        # Clustering model
        if method == 'KMeans':
            clusterer = KMeans(n_clusters = i, random_state = 40)
            cluster_labels = clusterer.fit_predict(tle_data)

            # Elbow method: Compute the inertia
            Sum_of_squared_distances.append(clusterer.inertia_)
        
        elif method == 'Spectral':
            clusterer = SpectralClustering(n_clusters=i, gamma = 1, assign_labels="kmeans", random_state=40).fit(tle_data)
            cluster_labels = clusterer.labels_

        # Silhouette score for all samples
        silhouette_avg = silhouette_score(tle_data, cluster_labels, metric = 'sqeuclidean')
        sil_avg_data.append(silhouette_avg)
         
        # Compute Calinski-Harabasz score
        ch = calinski_harabasz_score(tle_data, cluster_labels)
        ch_score.append(ch)
    
    if method == 'KMeans':
        sil_graph(num_clusters, sil_avg_data, filepath, 'KMeans', module)
        ch_graph(num_clusters, ch_score, filepath, 'KMeans', module)
        elbow_graph(num_clusters, Sum_of_squared_distances, filepath, 'KMeans', module)
    
    elif method == 'Spectral':
        sil_graph(num_clusters, sil_avg_data, filepath, 'Spectral', module)
        ch_graph(num_clusters, ch_score, filepath, 'Spectral', module)

    # Choose the optimum clusters number
    max_sil = max(sil_avg_data[1:len(sil_avg_data)])
    best_num_clusters = sil_avg_data.index(max_sil) + 2
    
    temp_folder = 'C:/temp_data/'
    if module == 'TLE':
        np.savetxt('%stle_sil_avg_data.txt'%temp_folder, sil_avg_data, delimiter=',')
        with open('%stle_best_num_clusters.txt'%temp_folder, 'w') as num_cluster_txt:
                num_cluster_txt.write(str(best_num_clusters))
    elif module == 'Dist':
        np.savetxt('%sdist_sil_avg_data.txt'%temp_folder, sil_avg_data, delimiter=',')
        with open('%sdist_best_num_clusters.txt'%temp_folder, 'w') as num_cluster_txt:
                num_cluster_txt.write(str(best_num_clusters))

    return sil_avg_data, ch_score, Sum_of_squared_distances, best_num_clusters

def sil_graph(num_clusters, sil_avg_data, filepath, method, module):
    # Plot silhouette graph
    plt.plot(num_clusters, sil_avg_data, 'bx-')
    plt.xlabel('Number of cluster')
    plt.ylabel('Silhouette Coefficient')
    plt.title('Silhouette Coefficient against Number of Cluster')
    plt.grid(True)
    
    if method == 'KMeans':
        if module == 'TLE':
            filename = 'TLE_kmeans_sil_graph_one.png'
        elif module == 'Dist':
            filename = 'Dist_kmeans_sil_graph_one.png'

    elif method == 'Spectral':
        if module == 'TLE':
            filename = 'TLE_spectral_sil_graph_one.png'
        elif module == 'Dist':
            filename = 'Dist_spectral_sil_graph_one.png'

    folder = 'Picture/'
    sil_filepath = filepath + '/' + folder + filename
    plt.savefig(sil_filepath)
    plt.tight_layout()
    plt.close()
    return 0

def ch_graph(num_clusters, ch_score, filepath, method, module):
    # Plot ch graph
    plt.plot(num_clusters, ch_score, 'bx-')
    plt.xlabel('Number of cluster')
    plt.ylabel('Calinski-Harabasz Score')
    plt.title('Calinski-Harabasz Score against Number of Cluster')
    plt.grid(True)

    if method == 'KMeans':
        if module == 'TLE':
            filename = 'TLE_kmeans_ch_graph_one.png'
        elif module == 'Dist':
            filename = 'Dist_kmeans_ch_graph_one.png'

    elif method == 'Spectral':
        if module == 'TLE':
            filename = 'TLE_spectral_ch_graph_one.png'
        elif module == 'Dist':
            filename = 'Dist_spectral_ch_graph_one.png'

    folder = 'Picture/'
    ch_filepath = filepath + '/' + folder + filename
    plt.savefig(ch_filepath)
    plt.close()
    return 0

def elbow_graph(num_clusters, Sum_of_squared_distances, filepath, method, module):
    # Plot ch graph
    plt.plot(num_clusters, Sum_of_squared_distances, 'bx-')
    plt.xlabel('Number of cluster')
    plt.ylabel('Sum of squared dist')
    plt.title('Sum of squared dist against Number of Cluster')
    plt.grid(True)

    if method == 'KMeans':
        if module == 'TLE':
            filename = 'TLE_kmeans_elbow_graph_one.png'
        elif module == 'Dist':
            filename = 'Dist_kmeans_elbow_graph_one.png'

    folder = 'Picture/'
    elbow_filepath = filepath + '/' + folder + filename
    plt.savefig(elbow_filepath)
    plt.close()
    return 0

def kmeans_method(tle_data, best_num_clusters):
    # Create KMeans object
    train_clusterer = KMeans(n_clusters = best_num_clusters, random_state = 40)
    train_cluster_labels = train_clusterer.fit_predict(tle_data)
    
    return train_cluster_labels

def spectral_method(tle_data, best_num_clusters):
    train_clusterer = SpectralClustering(n_clusters = best_num_clusters, gamma = 1, assign_labels="kmeans", random_state=40).fit(tle_data)
    train_cluster_labels = train_clusterer.labels_
    
    return train_cluster_labels

def train_model(tle_data, method, best_num_clusters):
    if method == 'KMeans':
        train_cluster_labels = kmeans_method(tle_data, best_num_clusters)
    elif method == 'Spectral':
        train_cluster_labels = spectral_method(tle_data, best_num_clusters)
    
    return train_cluster_labels

def group_data(data, train_cluster_labels, filepath, module):
    if module == 'TLE':
        # Group normalized data and labels
        tle_norm_trained_data = data
        tle_norm_trained_data['Group'] = train_cluster_labels

        # Group original data and labels
        filename = 'TLE_data_outlier_removed.csv'
        tle_data = read_data(filepath, filename)
        tle_trained_data = tle_data
        tle_trained_data['Group'] = train_cluster_labels
        tle_trained_data.head()

        # Save the trained data into csv file
        folder = 'csv_file'
        filename = 'TLE_Final_Cluster.csv'
        csv_filepath = filepath + '/' + folder + '/' + filename
        tle_trained_data.to_csv(csv_filepath, index = False, header = True)

        return tle_norm_trained_data, tle_trained_data

    elif module == 'Dist':
        # Group normalized data and labels
        dist_norm_trained_data = data
        dist_norm_trained_data['Group'] = train_cluster_labels

        # Group original data and labels
        filename = 'Total_dist_outlier_removed.csv'
        dist_data = read_data(filepath, filename)
        dist_trained_data = dist_data
        dist_trained_data['Group'] = train_cluster_labels
        dist_trained_data.head()

        # Save the trained distance data into csv file
        folder = 'csv_file'
        filename = 'Dist_Final_Cluster.csv'
        csv_filepath = filepath + '/' + folder + '/' + filename
        dist_trained_data.to_csv(csv_filepath, index = False, header = True)
        
        return dist_norm_trained_data, dist_trained_data

def scatter_graph(dist_data, filepath):
    folder = 'Picture'
    fig_name = 'Dist_scatterplot_clustering.png'
    fig_path = filepath + '/' + folder + '/' + fig_name
    fig = sns.scatterplot(x = dist_data['Group'], y = dist_data['Total distance'], hue = 'Group', 
                data = dist_data, palette='Set1', s = 100)
    scatter_fig = fig.get_figure()
    scatter_fig.savefig(fig_path, dpi = 400)

def pairplot_graph(tle_trained_data, filepath):
    folder = 'Picture'
    fig_name = 'Pairplot_clustering.png'
    fig_path = filepath + '/' + folder + '/' + fig_name
    pairplot_fig = sns.pairplot(tle_trained_data, kind='scatter', hue="Group", palette="Set2", height=2.5, plot_kws=dict(s=50, alpha=0.4))
    pairplot_fig.savefig(fig_path, dpi = 400)
    plt.close()

def cluster_intuition(tle_trained_data, best_num_clusters, module):
    # Get the density of each group
    groups = tle_trained_data['Group']
    group_density = groups.value_counts() 

    # Get the information for each group
    group_details = [tle_trained_data.loc[tle_trained_data['Group'] == num] for num in range(best_num_clusters)]

    if module == 'TLE':
        for i in range(best_num_clusters):
            filename = 'C:/temp_data/tle_group_details_%s.csv'%i
            test = group_details[i].describe()
            test.to_csv(filename, index = True, header=True)

        group_density.to_csv('C:/temp_data/tle_group_density.txt', index = True, header = True)
    elif module == 'Dist':
        for i in range(best_num_clusters):
            filename = 'C:/temp_data/dist_group_details_%s.csv'%i
            test = group_details[i].describe()
            test.to_csv(filename, index = True, header=True)

        group_density.to_csv('C:/temp_data/dist_group_density.txt', index = True, header = True)

    return group_density, group_details

def main_tle_cluster(filepath, method):
    module = 'TLE'
    tle_data = read_data(filepath, 'TLE_normalized_data.csv')
    
    if method == 'KMeans':
        sil_avg_data, ch_score, Sum_of_squared_distances, best_num_clusters = parameter_tuning(filepath, tle_data, method, module)
    elif method == 'Spectral':
        sil_avg_data, ch_score, Sum_of_squared_distances, best_num_clusters = parameter_tuning(filepath, tle_data, method, module)

    # Build clustering model
    train_cluster_labels = train_model(tle_data, method, best_num_clusters)
    tle_norm_trained_data, tle_trained_data = group_data(tle_data, train_cluster_labels, filepath, module)
    pairplot_graph(tle_norm_trained_data, filepath)
    group_density, group_details = cluster_intuition(tle_trained_data, best_num_clusters, module)

    return sil_avg_data, ch_score, Sum_of_squared_distances, best_num_clusters, tle_norm_trained_data, tle_trained_data, group_density, group_details

def main_dist_cluster(filepath, method):
    module = 'Dist'
    # Get the preprocessed relative distances data
    dist_data = read_data(filepath, 'Total_dist_preprocessed.csv')

    # Distinguish clustering algorithm and do parameter tuning
    if method == 'KMeans':
        sil_avg_data, ch_score, Sum_of_squared_distances, best_num_clusters = parameter_tuning(filepath, dist_data, method, module)
    elif method == 'Spectral':
        sil_avg_data, ch_score, Sum_of_squared_distances, best_num_clusters = parameter_tuning(filepath, dist_data, method, module)
    
    # Build clustering model
    train_cluster_labels = train_model(dist_data, method, best_num_clusters)
    # Group data
    dist_norm_trained_data, dist_trained_data = group_data(dist_data, train_cluster_labels, filepath, module)
    
    # seaborn scatterplot
    scatter_graph(dist_trained_data, filepath)

    # cluster_intuition()
    group_density, group_details = cluster_intuition(dist_trained_data, best_num_clusters, module)

    return sil_avg_data, Sum_of_squared_distances, best_num_clusters, dist_norm_trained_data, dist_trained_data

if __name__ == "__main__":
    filepath = 'C:/Users/LIEW YING JIA/Desktop/TLE_test_file'
    method = 'KMeans'
    main_tle_cluster(filepath, method)

    # main_dist_cluster(filepath, method)