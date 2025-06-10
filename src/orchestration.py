import os
import subprocess
from multiprocessing import Pool, cpu_count, Manager
from subprocess import CompletedProcess
from query.hemibrain import hemibrain
from display_results import display_table


SCRIPTS = [
        'empiar',
        'epfl',
        'janelia-openorganelle',
        'ome-idr'
    ]

def get_output_dir(script_name: str):
    data_dir = os.path.join('./data')
    return os.path.join(data_dir, script_name)


def get_scripts_reference(script_name: str):
    scripts_dir = os.path.join('./query')
    return os.path.join(scripts_dir, script_name + '.sh')


def execute_script(args) -> (str, CompletedProcess, str):
    script  = args
    script_path = get_scripts_reference(script)
    result = subprocess.run(script_path, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # result = subprocess.run(script_path, shell=True, stdout=subprocess.DEVNULL,)

    return script, result, get_output_dir(script)

def main():
    with Pool(cpu_count()) as pool, \
        display_table(table_name="Microscopy Data Query Results", col_names=["Task", "Status"], labels=SCRIPTS) as update_status:
            for sc in SCRIPTS:
                pool.apply_async(execute_script, args=(sc,), callback=update_status)




if __name__ == "__main__":
    main()