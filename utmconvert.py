import utm
import csv
import pandas

# print(utm.to_latlon(340000, 5710000, 55, 'J'))

path_to_dataset = '../data/'
path_to_output = '../data/'

zone_number = 55
zone_letter = "J"

def process(path_to_dataset, path_to_output, zone_number, zone_letter):
    data_file_name = 'Top_Illawarra.csv'
    data_file_output = 'Output_' + data_file_name
    utm_list = []

    with open(path_to_dataset + data_file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data_list = list(reader)

    ##convert csv to latlon
    for point in data_list[1:]:
        data_name = point[0]
        x_coorindate = float(point[2])
        y_coorindate = float(point[3])
        z_coorindate = float(point[4])
        utm_tuple= list(utm.to_latlon(x_coorindate, y_coorindate, zone_number, zone_letter))
        utm_tuple.append(z_coorindate)
        utm_list.append(utm_tuple)

    ##write and create cvs file
    writer = csv.writer(open(path_to_output + data_file_output, 'w'))
    for point in utm_list:
        writer.writerow(point)

process(path_to_dataset, path_to_output, zone_number, zone_letter)
