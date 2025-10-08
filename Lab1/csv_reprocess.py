import csv
import pandas

def reprocess_csv(csv_filename,
                  out_list,
                  out_list_ind):
    with open(csv_filename) as file:
        for i in range(4):
            line = file.readline()
            out_list[out_list_ind + i * 5] = float(line.split(sep=',')[1])
                  


               
    