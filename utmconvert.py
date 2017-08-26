import utm
import csv
import pandas
import numpy as np
from numpy import array
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

path_to_dataset = '../data/Hawkins_Rumker/'
path_to_output = '../data/'

zone_number = 55
zone_letter = "H"
utm_list = []
points_utm_list = 0

def process(path_to_dataset, path_to_output, zone_number, zone_letter):
    data_file_name = 'KATSF.csv'
    data_file_output = 'Output_' + data_file_name

    with open(path_to_dataset + data_file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data_list = list(reader)
        xyz_columns = []
        # utm_list = []

        ##case 1
        firstRow = data_list[0]
        if "NAME" and "PART_ID" in firstRow:
            for row in data_list:
                xyz_columns = row[2:]
        else:
        ##case 2
            counter = 0
            for index, row in enumerate(data_list):
                counter +=1
                if "X" and "Y" and "Z" in data_list[index]:
                    xyz_columns = data_list[12:]
    ##convert csv to latlon
    for point in xyz_columns:
        x_coorindate = float(point[0])
        y_coorindate = float(point[1])
        z_coorindate = float(point[2])

        ##remove null points if they are 99999.00
        if z_coorindate != 99999.00:
            utm_tuple= list(utm.to_latlon(x_coorindate, y_coorindate, zone_number, zone_letter))
            utm_tuple.append(z_coorindate)
            utm_list.append(utm_tuple)
    length_utm_list = len(utm_list)

    # ##write and create cvs file
    # writer = csv.writer(open(path_to_output + data_file_output, 'w'))
    # for point in utm_list:
    #     writer.writerow(point)

process(path_to_dataset, path_to_output, zone_number, zone_letter)

points_utm_list = len(utm_list)

def convex_hull(utm_list):
    points = []
    ##Only output latitude and longitude from the utm_list
    for item in utm_list:
        points.append(item[:2])
    hull = ConvexHull(points)
    plot_convex_hull(points, hull)

def plot_convex_hull(points, hull):
    points = array(points)
    latitude = points[:,0]
    longitude = points[:,1]
    plt.plot(latitude, longitude, 'o')
    for simplex in hull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
    plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r--', lw=2)
    plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], 'ro')
    plt.show()

convex_hull(utm_list)
