import csv
import pandas

def process_csv(csv_filename,
                filename_suffix_num):
    data_frame = pandas.read_csv(csv_filename, names=["cat", "val"])

    with open(f"numData_{filename_suffix_num}_processed.csv", 'w') as res_file:
        for category in ['A', 'B', 'C', 'D']:
            category_data = data_frame[data_frame["cat"] == category]["val"]
        
            if not category_data.empty:
                median = category_data.median()
                standart = category_data.std()
                csv.DictWriter(res_file, fieldnames=["cat", "med", "std"], lineterminator='\n').writerow({"cat": category, "med": median, "std": standart})
    