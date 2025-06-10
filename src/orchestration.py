import os
import random
import subprocess
from multiprocessing import Pool, cpu_count, Manager
from subprocess import CompletedProcess
from query.hemibrain import hemibrain
from display_results import display_table


def get_scripts_reference():
    # scripts = [
    #     'empiar',
    #     'epfl',
    #     'janelia-openorganelle',
    #     'ome-idr'
    # ]

    scripts = ['test'] * 4

    scripts_dir = os.path.join('./query')

    return [os.path.join(scripts_dir, sc + '.sh') for sc in scripts]


def execute_script(args) -> (str, CompletedProcess):
    index, script  = args
    random.seed(os.urandom(16))
    n = random.randint(0, 3)

    result = subprocess.run(f"{script} {n}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return f"{script}-{index}", result

def main():
    scripts = get_scripts_reference()
    # status = manager.dict({f"{s}-{i}": "Running..." for i, s in enumerate(scripts)})
    script_keys = [f"{s}-{i}" for i, s in enumerate(scripts)]

    with Pool(cpu_count()) as pool, \
        display_table(table_name="Results", col_names=["Task", "Status"], labels=script_keys) as update_status:
            for i, s in enumerate(scripts):
                pool.apply_async(execute_script, args=((i, s),), callback=update_status)




if __name__ == "__main__":
    main()