# Satellite collision risk analysis based on data mining with Python
<b>Aim and objective</b> <br>
The purpose of this study is to analyze the collision risk of orbiting spacecraft according to the density of spacecraft distribution in space.
This project uses data mining technology, which are clustering and classification method to filter out the spacecraft with higher collision risk with the target satellite, providing support for satellite initial orbit planning and collision avoidance. 
The methodology proposed in this paper consists following procedures: 
1. a clustering model and then a classification model are built on two-line element set(TLE).
2. orbital data for prediction is then input to the prediction model, spacecraft with similar orbital data will be output.
3. another clustering model is built after the computing of relative distances between data input and similar orbital data, returning the amount and relatives distances between data input and neighboring spacecraft.
The data mining models in this paper has shown the ability to select spacecraft which have high collision risk with the data input.
</br>

<b>Design the Python program</b>  
The flowchart of the program is as follows: 
![satelliteRiskFLowChart2](https://github.com/MLiew/Project/assets/30465494/4183e0c8-96a8-4984-83e6-43d995d33523)

<br>

## CODE
There are 11 Python source programs in the Python source program folder, which are:
1. web_crawl_test.py: crawler program;
2. data_prepro.py: Orbital data preprocessing program;
3. tle_clustering.py: clustering program;
4. tle_classification.py: classification program;
5. relative_distance.py: Spacecraft relative distance calculation module;
6.rel_dist_prepro_cluster.py: Spacecraft relative distance data preprocessing module;
7. produce_latex_report.py: Automatically generate report module;
8. HomePage.py: software main interface module;
9. SaveFilePage.py: the second interface module of the software;
10. PredictPage.py: The third interface module of the software;
11. PredictProgress.py: The fourth interface of the software.

<b> Requirements   </b>  
1. Software development language: Python;  
2. Editor: Visual Studio Code;  
3. Development environment: Anaconda (Python distribution)  
4. Python version: 3.6.8(64-bit)  
5. Libraries that need to be installed: PyQt5, Matplotlib, sklearn, PyLaTeX, bs4, pandas, numpy, csv, math, os, sys, time, functools, multiprocessing, seaborn, etc.

## HOW TO USE
1. Open HomePage.py and click Run;
2. The home page of the software interface pops up, click "Next";
3. The software enters the second interface and selects the file saving path and the clustering algorithm used in the orbit data clustering model;
4. Click the "Confirm" button and wait for the progress bar to reach 100% for the clustering model to complete training;
5. Click the "Next" button to enter the third interface;
6. According to the prompts on the interface, enter the satellite orbit data in the correct unit and format;
7. Click the "Predict" button to jump to the fourth interface;
8. Wait for the progress bar to run to 100%, and the analysis results are reported in the file saving path.

The GUI of this program is as follow:  
<img width="346" alt="satelliteCollisionGUI" src="https://github.com/MLiew/Project/assets/30465494/96466170-c221-4b6f-bbb6-29ddbdb48ce0">
