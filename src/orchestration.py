import os
import subprocess
import time
from multiprocessing import Pool, cpu_count, dummy, Manager
from subprocess import CompletedProcess

from utils.keygen import keygen
from utils.display_results import display_table


TASKS = [
        # 'test',
        'hemibrain',
        'ome-idr',
        'janelia-openorganelle',
        'empiar',
        'epfl',
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

    with Manager() as manager, \
        dummy.Pool(cpu_count()) as pool, \
        display_table(table_name="Microscopy Data Query Results", col_names=["Task", "Status"], labels=TASKS) as (mark_start, update_status):

            # we separate tasks into 3 groups and run them sequentially
            group0 = TASKS[0:2]
            group1 = TASKS[2:4]

            # we isolate EPFL since it's VERY slow and does need the full bandwidth
            group2 = TASKS[4:]


            groups = [group0, group1, group2]
            lock = manager.Lock()

            # when a group finishes, kick off the next group if possible
            def launch_group(index: int):
                remaining = manager.Value(int, len(groups[index]))

                def on_task_complete(res):
                    with lock:
                        remaining.value -= 1

                    if remaining.value == 0 and index < len(groups) - 1:
                        launch_group(index + 1)

                    update_status(res)

                for i, sc in enumerate(groups[index]):
                    mark_start(sc)
                    pool.apply_async(execute_script, args=(sc,), callback=on_task_complete)


            # start the first group
            launch_group(0)

if __name__ == "__main__":
    main()