'''
Author: Liew Ying Jia
Date: 17 Apr 2020
Description:    This is a relative distance calculation module for two-line elements.
Input value: New input data for prediction, predicted class data
Output:   Total difference dataframe, 'Total_rel_dis.csv' file
'''

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

import math

class RelDistCal:
    @classmethod
    def eccen_anomaly(self, eccen, M):
        err_tol = 1e-10
        Ek = M

        Enew = Ek - ((Ek - eccen * math.sin(Ek) - M)/(1 - eccen * math.cos(Ek)))
        cnt = 0

        while(abs(Enew - Ek) > err_tol):
            Ek = Enew
            Enew = Ek - ((Ek - eccen * math.sin(Ek) - M)/(1 - eccen * math.cos(Ek)))
            cnt = cnt + 1

        return Enew

    @classmethod
    def true_anomaly(self, eccen, eccen_anomaly):
        true_anomaly_value = 2 * math.atan((math.pow((1 + eccen)/(1 - eccen), 0.5)) * math.tan(eccen_anomaly/2))
        
        if (true_anomaly_value < 0):
            true_anomaly_value  = true_anomaly_value + 2*math.pi
        
        return true_anomaly_value
    
    @classmethod
    def normal_vector(self, raan, inclin):
        nx = np.sin(raan) * np.sin(inclin)
        ny = -1 * np.cos(raan) * np.sin(inclin)
        nz = np.cos(inclin)
        norm_vector = np.array([nx, ny, nz])
        
        return norm_vector

    @classmethod
    def planes_angle(self, pri_norm_vector, sec_norm_value):
        # Angle between two planes         
        theta = np.arccos(np.inner(pri_norm_vector, sec_norm_value)/
                          (np.linalg.norm(pri_norm_vector) * np.linalg.norm(sec_norm_value)))
        
        return theta

    @classmethod
    def radius(self, eccen, smaxis, true_anomaly):
        radius_value = smaxis * (1 - math.pow(eccen,2)) / (1 + eccen * np.cos(true_anomaly))
   
        return radius_value

def read_data(filepath):
    folder = 'csv_file'
    filename = 'TLE_Final_Cluster.csv'
    csv_filepath = filepath + '/' + folder + '/' + filename
    df = pd.read_csv(r"%s"%csv_filepath)
    print(df.head())
    
    return df

def input_data(predict_input, rf_predict_input, df):
    input_predict = np.array(predict_input[0][:]).reshape(1,6)
    gr_predict = rf_predict_input

    # Create DataFrame for input_predict, same data format as predicted group
    input_predict_df = pd.DataFrame(input_predict, 
                                columns = ['Inclination', 'RAAN', 'Eccentricity', 
                                           'Argument of Perigee', 'Mean Anomaly', 'Semi Major Axis(m)'])
    # Get data from predicted class
    gr_predict_df = df.loc[df['Group'] == gr_predict]
    gr_predict_df = gr_predict_df.drop(['Group'], axis = 1)
    
    return input_predict_df, gr_predict_df

def pri_data(input_predict_df):
    # Extract all the primary object's data 
    pri_incline = input_predict_df.iloc[0]['Inclination']
    pri_raan = input_predict_df.iloc[0]['RAAN']
    pri_eccen = input_predict_df.iloc[0]['Eccentricity']
    pri_manomaly = input_predict_df.iloc[0]['Mean Anomaly']
    pri_smaxis = input_predict_df.iloc[0]['Semi Major Axis(m)']

    # Convert degree into radians
    pri_incline = np.radians(pri_incline)
    pri_raan = np.radians(pri_raan)
    pri_manomaly = np.radians(pri_manomaly)

    return pri_incline, pri_raan, pri_eccen, pri_manomaly, pri_smaxis

def sec_data(gr_predict_df):
    # Extract all the secondary object's data
    sec_incline = gr_predict_df['Inclination']
    sec_raan = gr_predict_df['RAAN']
    sec_eccen = gr_predict_df['Eccentricity']
    sec_manomaly = gr_predict_df['Mean Anomaly']
    sec_smaxis = gr_predict_df['Semi Major Axis(m)']
    
    # Convert degree into radians
    sec_incline = np.radians(sec_incline)
    sec_raan = np.radians(sec_raan)
    sec_manomaly = np.radians(sec_manomaly)

    return sec_incline, sec_raan, sec_eccen, sec_manomaly, sec_smaxis

def cal_phase(pri_eccen, pri_manomaly, pri_smaxis, sec_eccen, sec_manomaly, sec_smaxis):
    # Calculate phase difference (Mean Anomaly)
    # x-distance
    phase_diff = []
      
    # Eccentric anomaly, true anomaly and radius for primary orbit
    pri_eccen_anomaly = RelDistCal.eccen_anomaly(pri_eccen, pri_manomaly)
    pri_true_anomaly = RelDistCal.true_anomaly(pri_eccen, pri_eccen_anomaly)
    pri_radius = RelDistCal.radius(pri_eccen, pri_smaxis, pri_true_anomaly)
    
    # Eccentric anomaly for secondary orbit
    # Compute phase difference
    for eccen_data, manomaly_data, smaxis_data in zip(sec_eccen, sec_manomaly, sec_smaxis):
        sec_eccen_anomaly = RelDistCal.eccen_anomaly(eccen_data, manomaly_data)
        sec_true_anomaly = RelDistCal.true_anomaly(eccen_data, sec_eccen_anomaly)
        sec_radius = RelDistCal.radius(eccen_data, smaxis_data, sec_true_anomaly)
        
        if (pri_radius > sec_radius):
            largest_radius = pri_radius
        else:
            largest_radius = sec_radius
        
        diff = abs(pri_true_anomaly - sec_true_anomaly) * largest_radius
        phase_diff.append(diff)
    
    return phase_diff

def cal_height(pri_eccen, pri_manomaly, pri_smaxis, sec_eccen, sec_manomaly, sec_smaxis):
    height_diff = []
    
    # Eccentric anomaly, true anomaly and radius for primary orbit
    pri_eccen_anomaly = RelDistCal.eccen_anomaly(pri_eccen, pri_manomaly)
    pri_true_anomaly = RelDistCal.true_anomaly(pri_eccen, pri_eccen_anomaly)
    pri_radius = RelDistCal.radius(pri_eccen, pri_smaxis, pri_true_anomaly)
    
    # Perform calculation
    for eccen_data, smaxis_data, manomaly_data in zip(sec_eccen, sec_smaxis, sec_manomaly):
        sec_eccen_anomaly = RelDistCal.eccen_anomaly(eccen_data, manomaly_data)
        sec_true_anomaly = RelDistCal.true_anomaly(eccen_data, sec_eccen_anomaly)
        sec_radius = RelDistCal.radius(eccen_data, smaxis_data, sec_true_anomaly)
        
        height_diff_value = abs(pri_radius - sec_radius)
        height_diff.append(height_diff_value)
    
    return height_diff

def cal_incline(pri_incline, pri_raan, pri_eccen, pri_manomaly, pri_smaxis, sec_incline, sec_raan, sec_eccen, sec_manomaly,sec_smaxis):
    incline_diff = []
    sec_norm_vector = []  
    
    # Eccentric anomaly, true anomaly, radius and normal vector for primary orbit
    pri_eccen_anomaly = RelDistCal.eccen_anomaly(pri_eccen, pri_manomaly)
    pri_true_anomaly = RelDistCal.true_anomaly(pri_eccen, pri_eccen_anomaly)
    pri_radius = RelDistCal.radius(pri_eccen, pri_smaxis, pri_true_anomaly)
    pri_norm_vector = RelDistCal.normal_vector(pri_raan, pri_incline)
    
    for raan_data, incline_data, eccen_data, smaxis_data, manomaly_data in zip(sec_raan, sec_incline, sec_eccen, sec_smaxis, sec_manomaly):
        sec_norm_value = RelDistCal.normal_vector(raan_data, incline_data)
        sec_norm_vector.append(sec_norm_value)
        
        # Angle between two planes
        theta = RelDistCal.planes_angle(pri_norm_vector, sec_norm_value)         
        
        # Calculate the radius of secondary object
        sec_eccen_anomaly = RelDistCal.eccen_anomaly(eccen_data, manomaly_data)
        sec_true_anomaly = RelDistCal.true_anomaly(eccen_data, sec_eccen_anomaly)
        sec_radius = RelDistCal.radius(eccen_data, smaxis_data, sec_true_anomaly)
        
        # Distance between primary and secondary object
        distance = abs(np.sin(theta/2) * (pri_radius + sec_radius))
        incline_diff.append(distance)
    
    return incline_diff

def cal_final_dist(phase_diff, height_diff, incline_diff):
    total_dist = []
    
    for phase_data, height_data, incline_data in zip(phase_diff, height_diff, incline_diff):
        total_arr = np.array([phase_data, height_data, incline_data])
        total_diff = np.linalg.norm(total_arr)
        total_dist.append(total_diff)
    
    return total_dist

def final_dist_df(phase_diff, height_diff, incline_diff, total_diff):
    # Create a DataFrame with phase_diff, height_diff, incline_diff and total_diff
    total_diff_df = pd.DataFrame(zip(phase_diff, height_diff, incline_diff, total_diff),
                                columns = ['Phase difference', 'Height difference', 'Inclination difference', 'Total distance'])
    
    return total_diff_df

def save_csv(filepath, total_diff_df):
    # Save the total_diff_df into csv file
    folder = 'csv_file'
    filename = 'Total_rel_dis.csv'
    csv_filepath = filepath + '/' + folder + '/' + filename
    total_diff_df.to_csv(csv_filepath, index = False, header=True)

def main_rel_dist(filepath, predict_input, rf_predict_input):
    df = read_data(filepath)
    input_predict_df, gr_predict_df = input_data(predict_input, rf_predict_input, df)
    print(input_predict_df)
    print(gr_predict_df.head())
    pri_incline, pri_raan, pri_eccen, pri_manomaly, pri_smaxis = pri_data(input_predict_df)
    sec_incline, sec_raan, sec_eccen, sec_manomaly, sec_smaxis = sec_data(gr_predict_df)
    phase_diff = cal_phase(pri_eccen, pri_manomaly, pri_smaxis, sec_eccen, sec_manomaly, sec_smaxis)
    height_diff = cal_height(pri_eccen, pri_manomaly, pri_smaxis, sec_eccen, sec_manomaly, sec_smaxis)
    incline_diff = cal_incline(pri_incline, pri_raan, pri_eccen, pri_manomaly, pri_smaxis, sec_incline, sec_raan, sec_eccen, sec_manomaly, sec_smaxis)
    total_diff = cal_final_dist(phase_diff, height_diff, incline_diff)
    total_diff_df = final_dist_df(phase_diff, height_diff, incline_diff, total_diff)
    save_csv(filepath, total_diff_df)

    return total_diff_df
    
if __name__ == "__main__":
    filepath = 'C:/Users/LIEW YING JIA/Desktop/TLE_test_file'
    predict_input = [[98.47462775,202.6435767,0.032286482,102.3841989,261.3666106,7231420.051]]
    rf_predict_input = 1
    total_diff_df = main_rel_dist(filepath, predict_input, rf_predict_input)
