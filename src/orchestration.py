import os
import subprocess
from multiprocessing import Pool, cpu_count
from subprocess import CompletedProcess
from utils.display_results import display_table


TASKS = [
        # 'test',
        # 'empiar',
        # 'epfl',
        # 'janelia-openorganelle',
        # 'ome-idr'
        'hemibrain',
    ]

def get_output_dir(script_name: str):
    data_dir = os.path.join('./data')
    return os.path.join(data_dir, script_name)


def get_scripts_reference(script_name: str):
    scripts_dir = os.path.join('./query')
    ext = '.sh'

    if script_name == 'hemibrain':
        ext ='.py'
    return os.path.join(scripts_dir, script_name + ext)


def execute_script(args) -> (str, CompletedProcess | bool, str):
    script = args

    script_path = get_scripts_reference(script)
    result = subprocess.run(script_path, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # result = subprocess.run(script_path, shell=Tr ue, stdout=subprocess.DEVNULL,)

    return script, result, get_output_dir(script)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with Pool(cpu_count()) as pool, \
        display_table(table_name="Microscopy Data Query Results", col_names=["Task", "Status"], labels=TASKS) as update_status:
            for sc in TASKS:
                pool.apply_async(execute_script, args=(sc,), callback=update_status)



if __name__ == "__main__":
    main()