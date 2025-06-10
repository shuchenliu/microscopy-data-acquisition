import os
import subprocess
from multiprocessing import Pool, cpu_count, dummy
from subprocess import CompletedProcess

from utils.keygen import keygen
from utils.display_results import display_table


TASKS = [
        # 'test',
        'empiar',
        'epfl',
        'janelia-openorganelle',
        'ome-idr',
        'hemibrain',
    ]

def get_output_dir(script_name: str) -> str:
    """
    Returns the output directory for the given script name
    """
    data_dir = os.path.join('../data')
    return os.path.join(data_dir, script_name)


def get_scripts_reference(script_name: str) -> str:
    """
    Returns the path to the script given a script name
    """
    scripts_dir = os.path.join('./query')
    ext = '.sh'

    if script_name == 'hemibrain':
        ext ='.py'
    return os.path.join(scripts_dir, script_name + ext)


def execute_script(args: str) -> (str, CompletedProcess | bool, str):
    """
    Execute individual query tasks, and pass payload to display renderer

    :param args: Script name
    :return:
        script: the script name
        completed_process: the results of completed subprocess task
        output_dir: the output directory
        size: size of the output dataset

    """

    script = args

    script_path = get_scripts_reference(script)
    result = subprocess.run(script_path, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    output_dir = get_output_dir(script)

    size_string = subprocess.run(
        ["du", "-sh", output_dir],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True  # ensures result.stdout is a string, not bytes
    )
    size = size_string.stdout.split()[0]

    return script, result, output_dir, size


def main():
    """
    Main driver function for the data acquisition pipeline.
    It generates a gcp credentials for later use with TensorStore, and start each query task in parallel.
    """

    # generate gcp cred
    keygen(255)

    with dummy.Pool(cpu_count()) as pool, \
        display_table(table_name="Microscopy Data Query Results", col_names=["Task", "Status"], labels=TASKS) as update_status:
            for sc in TASKS:
                pool.apply_async(execute_script, args=(sc,), callback=update_status)



if __name__ == "__main__":
    main()