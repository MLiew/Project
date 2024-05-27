from pylatex import Document, Section, Subsection, Subsubsection, Command
from pylatex.section import Paragraph
from pylatex import Math, TikZ, Axis, Plot, Figure, Matrix, Alignat, Tabular, Table, Center, MultiColumn, MultiRow
from pylatex.utils import italic, NoEscape, bold
from pylatex.package import Package
from pylatex.basic import LineBreak, NewLine
from pylatex.position import FlushLeft, MiniPage

import numpy as np
import pandas as pd
import os

def get_data():
    folder_name = 'C:/temp_data/'

    input_data = np.loadtxt("%spredict_input.txt"%folder_name, delimiter = ',')

    tle_sil_score = list(np.around(np.loadtxt("%stle_sil_avg_data.txt"%folder_name), 3))

    best_clusters_orbit = int(np.loadtxt("%stle_best_num_clusters.txt"%folder_name))

    group_density_orbit = pd.read_csv("%stle_group_density.txt"%folder_name)
    
    tle_group_details = []
    for num in range(best_clusters_orbit):
        group = pd.read_csv("%stle_group_details_%s.csv"%(folder_name, num))
        tle_group_details.append(group)

    # Classification data
    max_cv_score = np.round(np.loadtxt("%srf_max_cv_score.txt"%folder_name), 3)
    max_estimators = int(np.loadtxt("%srf_max_estimators.txt"%folder_name))
    rf_acc = np.round(np.loadtxt("%srf_accuracy.txt"%folder_name), 3)
    rf_precision = np.round(np.loadtxt("%srf_precision.txt"%folder_name), 3)
    rf_recall = np.round(np.loadtxt("%srf_recall.txt"%folder_name), 3)
    rf_f1_score = np.round(np.loadtxt("%srf_f1.txt"%folder_name), 3)
    rf_group_result = int(np.loadtxt("%srf_f1.txt"%folder_name))

    # Relative distance clustering 
    dist_sil_score = list(np.around(np.loadtxt("%sdist_sil_avg_data.txt"%folder_name), 3))
    dist_best_clusters = int(np.loadtxt("%sdist_best_num_clusters.txt"%folder_name))
    dist_group_density = pd.read_csv("%sdist_group_density.txt"%folder_name)
    dist_group_details = []
    for num in range(dist_best_clusters):
        group = pd.read_csv("%sdist_group_details_%s.csv"%(folder_name, num))
        dist_group_details.append(group)

    return input_data, tle_sil_score, best_clusters_orbit, group_density_orbit, tle_group_details, max_cv_score, max_estimators,rf_acc, rf_precision, rf_recall, rf_f1_score, rf_group_result, dist_best_clusters, dist_sil_score, dist_group_density, dist_group_details

def create_tex(doc, filepath):
    newpath = filepath + '/Report'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    doc.generate_pdf('%s/testPylatex'%newpath,compiler='latexmk', compiler_args=['-xelatex'], clean_tex=False)

    tex = doc.dumps()

def table_input_data(doc, input_data):
    """Create table with given input data"""

    with doc.create(Table(position = "htb!")) as table1:
        table1.append(Command('centering'))
        table1.add_caption("输入的轨道数据")
        
        with table1.create(Tabular('c c c c c c')) as table:
            table.add_hline()
            table.add_row((bold('轨道倾角(°)'), bold('升交点赤经(°)'), bold('偏心率'), bold('近地点幅角(°)'), bold('平近点角(°)'), bold('轨道半长轴(m)')))
            table.add_hline()
            table.add_row((input_data))
            table.add_hline()

def table_sil_score(doc, sil_score, caption, module):
    num_clusters = ['聚类数目']
    num_clusters_list = list(np.arange(2, 11))
    num_clusters.extend(num_clusters_list)

    sil_score.insert(0, '轮廓系数')

    with doc.create(Table(position = "htb!")) as table1:
        table1.append(Command('centering'))
        table1.add_caption(caption)
        if module == 'TLE':
            table1.append(Command('label', 'table:TLESilscore'))   
 
        elif module == 'Dist':
            table1.append(Command('label', 'table:DistSilscore'))   
            
        with table1.create(Tabular('c c c c c c c c c c')) as table:
            table.add_hline()
            table.add_row(num_clusters)
            table.add_hline()
            table.add_row(sil_score)
            table.add_hline()

def table_cluster_quantity_orbit(doc, group_density_orbit, best_clusters_orbit):
    with doc.create(Table(position = "htb!")) as table1:
        table1.append(Command('centering'))
        table1.add_caption('聚类类别与航天器数量')
        table1.append(Command('label', 'table2:ClusterQuantity1'))   
        
        with table1.create(Tabular('c c')) as table:
            table.add_hline()
            print(group_density_orbit)
            table.add_row(bold('聚类类别'), bold('航天器数量'))
            table.add_hline()
            for num in range(best_clusters_orbit):
                table.add_row(group_density_orbit.iloc[num])
            table.add_hline()

def table_group_details_orbit(doc, tle_group_details, best_clusters_orbit):
    for table_num in range(best_clusters_orbit):
        with doc.create(Table(position = "htb!")) as table1:
            table1.append(Command('centering'))
            table1.add_caption('聚类类别与轨道数据范围(类别%s)'%table_num)
            table1.append(Command('label', 'table:TleClusterRange%s'%table_num))   
            
        # for table_num in range(best_clusters_orbit):
            with table1.create(Tabular('c c c c c c c c')) as table:
                group_data = pd.DataFrame(tle_group_details[table_num])
                group_data = group_data.round({"Inclination":3, "RAAN":3, "Eccentricity":3, "Argument of Perigee":3, "Mean Anomaly":3, "Semi Major Axis(m)":3})
                table.add_hline()
                table.add_row('','轨道倾角','升交点赤经','偏心率','平近点角','近地点幅角','半长轴','类别')
                table.add_hline()
                for num in range(8):
                    table.add_row(group_data.iloc[num])

            table.add_hline()

def table_cluster_quantity_dist(doc, dist_group_density, dist_best_clusters):
    with doc.create(Table(position = "htb!")) as table1:
        table1.append(Command('centering'))
        table1.add_caption('相对距离聚类类别与航天器数量')
        table1.append(Command('label', 'table:DistClusterQuantity'))   
        
        with table1.create(Tabular('c c')) as table:
            table.add_hline()
            table.add_row(bold('聚类类别'), bold('航天器数量'))
            table.add_hline()
            for num in range(dist_best_clusters):
                table.add_row(dist_group_density.iloc[num])
            table.add_hline()

def table_group_details_dist(doc, dist_group_details, dist_best_clusters):
    for table_num in range(dist_best_clusters):
        with doc.create(Table(position = "htb!")) as table1:
            table1.append(Command('centering'))
            table1.add_caption('聚类类别与相对距离数据范围(类别%s)'%table_num)
            table1.append(Command('label', 'table:DistClusterRange%s'%table_num))   

            with table1.create(Tabular('c c c')) as table:
                group_data = pd.DataFrame(dist_group_details[table_num])
                group_data = group_data.round({"Total distance": 3})
                table.add_hline()
                table.add_row('', '相对距离(m)', '类别')
                table.add_hline()
                for num in range(8):
                    table.add_row(group_data.iloc[num])

            table.add_hline()

def main_report(filepath, method):
    input_data, tle_sil_score, best_clusters_orbit, group_density_orbit, tle_group_details, max_cv_score, max_estimators,rf_acc, rf_precision, rf_recall, rf_f1_score, rf_group_result, dist_best_clusters, dist_sil_score, dist_group_density, dist_group_details = get_data()

    geometry_options = {
    # "bottom": "1.0in",
    # "margin": "1.0in",
    "includeheadfoot": True
    }
        
    doc = Document(geometry_options = geometry_options)

    doc.packages.add(Package('ctex'))
    doc.preamble.append(Command('usepackage', 'float'))
    doc.preamble.append(Command('title', '基于数据挖掘的卫星运行碰撞风险分析报告'))
    doc.preamble.append(Command('author', '廖盈嘉'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))
    
    # Align left ： Introductory part
    with doc.create(FlushLeft()) as left_align:
        website = 'www.celestrak.com'
        left_align.append('轨道数据来源网站：%s'%website)
        left_align.append(NewLine())
        left_align.append('输入的轨道数据：')

        table_input_data(doc, input_data)

        left_align.append('本次分析将分为几个部分：轨道数据的聚类模型、轨道数据的分类预测模型、航天器相对距离计算、航天器相对距离聚类模型。')
    
    # Orbital data clustering part
    with doc.create(Section('轨道数据聚类模型')):
        with doc.create(Subsection('数据预处理')):
            doc.append(NoEscape(r'从轨道数据来源网站获得的轨道数据得知，轨道半长轴上等的离群值大大地影响到了半长轴数据的均值与标准差，因此，本分析根据3$\sigma$原则将Z值大于3的数据去除。'))
            doc.append('图')
            doc.append(Command('ref', 'fig:BoxPlot1'))
            doc.append('和图')
            doc.append(Command('ref', 'fig:BoxPlot2'))
            doc.append('分别为轨道数据在去除离群值之前与之后的箱型图。')

            with doc.create(Figure(position='H')) as box_plot:
                with box_plot.create(MiniPage(width=r'0.5\textwidth')) as mini_fig1:
                    box_plot.add_image('%s/Picture/boxplot1.png'%filepath)
                    box_plot.add_caption('去除离群值前的箱型图')
                    box_plot.append(Command('label', 'fig:BoxPlot1'))

                with box_plot.create(MiniPage(width=r'0.5\textwidth')) as mini_fig2:
                    box_plot.add_image('%s/Picture/boxplot2.png'%filepath)
                    box_plot.add_caption('去除离群值后的箱型图')
                    box_plot.append(Command('label', 'fig:BoxPlot2'))
        
        with doc.create(Subsection('聚类过程')):
            doc.append('算法：%s'% method)
            doc.append(NewLine())
            
            if method == 'KMeans':
                doc.append('这里选择使用的聚类算法为%s，而聚类评判指标为轮廓系数与手肘法。这里选择使轮廓系数最高的聚类数目为最佳聚类数目，同时也可以从手肘图中看见，在手肘处的聚类数目为最佳聚类数目。'%method)
                table_sil_score(doc, tle_sil_score, 'KMeans聚类算法下的轮廓系数', 'TLE')
                doc.append('从表')
                doc.append(Command('ref', 'table:TLESilscore'))
                doc.append('可知，获得轮廓系数最高的聚类数目为%s，聚类算法将轨道数据分为%s个聚类。'%(best_clusters_orbit, best_clusters_orbit))

                with doc.create(Figure(position='H')) as cluster_graph: 
                    with cluster_graph.create(MiniPage(width=r"0.5\textwidth")) as mini_fig1:
                        cluster_graph.add_image('%s/Picture/TLE_kmeans_sil_graph_one.png'%filepath) 
                        cluster_graph.add_caption('轮廓系数') 
                        cluster_graph.append(Command('label', 'fig:SilGraph1'))

                    with cluster_graph.create(MiniPage(width=r"0.5\textwidth")) as mini_fig2:
                        cluster_graph.add_image('%s/Picture/TLE_kmeans_elbow_graph_one.png'%filepath)
                        cluster_graph.add_caption('手肘图')
                        cluster_graph.append(Command('label', 'fig:ElbowMethod1'))
                    
        with doc.create(Subsection('数据结果')):
            doc.append(NoEscape(r'图\ref{fig:ClusterPairPlot}为多变量特征图，主要表示了轨道变量两两之间的关系。'))
            doc.append('表格') 
            doc.append(Command('ref', 'table2:ClusterQuantity1'))
            doc.append('为每个轨道聚类类别的卫星与空间碎片的密度。')
            doc.append('表格')
            for num in range(best_clusters_orbit):
                doc.append(Command('ref', 'table:TleClusterRange%s'%num))
                doc.append(',')
            doc.append(NoEscape(r'为每个聚类类别与轨道数据范围。'))
            
            with doc.create(Figure(position='H')) as pairplot_pic: 
                pairplot_pic.add_image('%s/Picture/Pairplot_clustering.png'%filepath) 
                pairplot_pic.add_caption('多变量特征图') 
                pairplot_pic.append(Command('label', 'fig:ClusterPairPlot'))
            
            # Orbital cluster group density 
            table_cluster_quantity_orbit(doc, group_density_orbit, best_clusters_orbit)
            table_group_details_orbit(doc, tle_group_details, best_clusters_orbit)
    
    with doc.create(Section('分类模型')): 
        doc.append('算法：随机森林算法')
        
        with doc.create(Subsection('分类过程')):
            pass
            doc.append('当分类树评估器数量为%s时，交叉验证率最大，即%s。' %(max_estimators, max_cv_score))

        with doc.create(Subsection('结果')):
            doc.append('本次分析选取%s为分类树评估器数量并建立随机森林模型。' %max_estimators)
            doc.append(NoEscape(r'表\ref{table:RandomForestIndicator}为随机森林模型的准确率、精确率、召回率和F1值。混淆模型见图\ref{fig:RFConfusionMatrix}。'))
            
            with doc.create(Table(position = "htb!")) as table1:
                table1.append(Command('centering'))
                table1.add_caption("随机森林数据")
                table1.append(Command('label', 'table:RandomForestIndicator'))
        
                with table1.create(Tabular('c c c c c')) as table:
                    table.add_hline()
                    table.add_row((bold('分类树评估数量'), bold('准确率'), bold('精确率'), bold('召回率'), bold('F1值')))
                    table.add_hline()
                    table.add_row((max_estimators, rf_acc, rf_precision, rf_recall, rf_f1_score))
                    table.add_hline()

            with doc.create(Figure(position='H')) as dist_pic: 
                        dist_pic.add_image('%s/Picture/Confusion_matrix.png'%filepath, width='7cm') 
                        dist_pic.add_caption('随机森林模型混淆矩阵')
                        dist_pic.append(Command('label', 'fig:RFConfusionMatrix'))
            
            doc.append('随后，根据所建立的随机森林分类预测模型，输入的轨道数据为聚类%s的数据。' %rf_group_result)

    with doc.create(Section('航天器相对距离聚类模型')):
        with doc.create(Subsection('过程')):
            doc.append('算法：K-Means++')
            with doc.create(Paragraph("")):
                doc.append(Command('indent'))
                doc.append('在计算完了输入的数据与其轨道聚类类别航天器之间的相对距离以后，这里选择使用的聚类算法为 KMeans，而聚类评判指标为轮廓系数与手肘法。这里选择使轮廓系数最高的聚类数目为最佳聚类数目，同时也可以从手肘图中看见，在手肘处的聚类数目为最佳聚类数目。')
                table_sil_score(doc, dist_sil_score, 'KMeans聚类算法下的航天器相对距离模型的轮廓系数', 'Dist')

            with doc.create(Figure(position='H')) as dist_cluster_graph: 
                    with dist_cluster_graph.create(MiniPage(width=r"0.5\textwidth")) as mini_fig3:
                        dist_cluster_graph.add_image('%s/Picture/Dist_kmeans_sil_graph_one.png'%filepath) 
                        dist_cluster_graph.add_caption('轮廓系数') 
                        dist_cluster_graph.append(Command('label', 'fig:SilGraph2'))
                        
                    with dist_cluster_graph.create(MiniPage(width=r"0.5\textwidth")) as mini_fig4:
                        dist_cluster_graph.add_image('%s/Picture/Dist_kmeans_elbow_graph_one.png'%filepath)
                        dist_cluster_graph.add_caption('手肘图')
                        dist_cluster_graph.append(Command('label', 'fig:ElbowMethod2'))
            
            doc.append(NoEscape(r'从表格\ref{table:DistSilscore}和图\ref{fig:SilGraph2}、图\ref{fig:ElbowMethod2}可知，')) #这里要加reference
            doc.append('最佳聚类数目为%s，将轨道数据分为了%s个聚类。' %(dist_best_clusters, dist_best_clusters))
        
        with doc.create(Subsection('数据结果')):
            doc.append('表格')
            doc.append(Command('ref', 'table:DistClusterQuantity'))
            doc.append('为每个轨道聚类类别与轨道航天器的数量。') 
            doc.append('表格')
            for num in range(dist_best_clusters):
                doc.append(Command('ref', 'table:DistClusterRange%s'%num))
                doc.append(',')
            doc.append(NoEscape(r'为每个聚类类别与相对距离的数据范围。'))
            
            # Relative distance cluster group density 
            table_cluster_quantity_dist(doc, dist_group_density, dist_best_clusters)
            table_group_details_dist(doc, dist_group_details, dist_best_clusters)
            
            with doc.create(Figure(position='H')) as dist_pic: 
                dist_pic.add_image('%s/Picture/Dist_scatterplot_clustering.png'%filepath, width='7cm') 
                dist_pic.add_caption('聚类类别与相对距离图')
                dist_pic.append(Command('label', 'fig:FinalClusterDistanceImage'))
            
            doc.append(NoEscape(r'图\ref{fig:FinalClusterDistanceImage}为主次航天器相对轨道距离的聚类结果图。'))

    create_tex(doc, filepath)

if __name__ == "__main__":
    filepath = 'C:/Users/LIEW YING JIA/Desktop/TLE_software'
    input_data = [[100, 202.6435767, 0.05, 103, 261.3666106, 7231420.051]]
    method = 'KMeans'
    main_report(filepath, method)