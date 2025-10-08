import csv_maker, csv_process, csv_reprocess
import csv
import multiprocessing
import pandas
from concurrent.futures import ProcessPoolExecutor as pExec  

if __name__ == "__main__":
    manage = multiprocessing.Manager()
    results_list = manage.list([0] * 20)

    with pExec(max_workers=5) as exec:
        gen_tasks = [exec.submit(csv_maker.make_csv, filename_suffix_num=i) for i in range(1, 6)]
        [task.result() for task in gen_tasks]

    with pExec(max_workers=5) as exec:
        proc_tasks = [exec.submit(csv_process.process_csv, filename_suffix_num=i, csv_filename=f"numData_{i}.csv") for i in range(1, 6)]
        [task.result() for task in proc_tasks]

    with pExec(max_workers=5) as exec:
        reproc_tasks = [exec.submit(csv_reprocess.reprocess_csv, csv_filename=f"numData_{i}_processed.csv",
                                    out_list=results_list, out_list_ind=i-1) for i in range(1, 6)]
        [task.result() for task in reproc_tasks]

    print(list(results_list))

    with open("final_results.csv", 'w', newline='') as results_file:
        writer = csv.writer(results_file)

        for i in range(4):
            start_ind = i*5
            end_ind = start_ind+5
            data_frame = pandas.DataFrame(list(results_list)[start_ind:end_ind])
            writer.writerow([chr(ord('A')+i), data_frame.median()[0], data_frame.std()[0]])

        