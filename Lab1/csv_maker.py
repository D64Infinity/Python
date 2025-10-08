import csv
import random

def make_csv(filename_prefix="numData",
             filename_suffix_num=1,
             num_rows=100):
    filename = f"{filename_prefix}_{filename_suffix_num}.csv"

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for _ in range(num_rows):
            category = random.choice(['A', 'B', 'C', 'D'])
            value = random.uniform(0, 100)
            writer.writerow([category, value])
