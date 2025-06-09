import os
import random
import subprocess
from multiprocessing import Pool, cpu_count, Manager
from time import sleep, time

from rich.live import Live
from rich.table import Table

from query.hemibrain import hemibrain

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


def execute_script(args):
    index, script  = args
    random.seed(os.urandom(16))
    n = random.randint(0, 10)

    result = subprocess.run(f"{script} {n}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    status = f"[green]Done[/green] (n = {n})" if result.returncode == 0 else f"❌ Failed ({result.returncode})"
    return f"{script}-{index}", status

def render_table(scripts, status, frame):
    SPINNER_FRAMES = ["|", "/", "-", "\\"]
    table = Table(title="Script Status")
    table.add_column("Script")
    table.add_column("Status", overflow="ellipsis")
    for i, s in enumerate(scripts):
        spinner = SPINNER_FRAMES[frame % len(SPINNER_FRAMES)] if status[f"{s}-{i}"].startswith('Run') else ''
        table.add_row(s, status[f"{s}-{i}"] + spinner)
    return table

def main():
    scripts = get_scripts_reference()
    # status = manager.dict({f"{s}-{i}": "Running..." for i, s in enumerate(scripts)})
    script_keys = [f"{s}-{i}" for i, s in enumerate(scripts)]
    status = {k: "Running..." for k in script_keys}

    frame = 0
    with Manager() as manager:
        completed = manager.Value("i", 0)

        def update_status(result):
            script_key, result_status = result
            status[script_key] = result_status
            completed.value += 1

        with Pool(cpu_count()) as pool, Live(render_table(scripts, status, frame), refresh_per_second=4) as live:
            for i, s in enumerate(scripts):
                pool.apply_async(execute_script, args=((i, s),), callback=update_status)

            # Render loop
            while completed.value < len(scripts):
                frame += 1
                live.update(render_table(scripts, status, frame))
                sleep(0.25)

            live.update(render_table(scripts, status, frame))




if __name__ == "__main__":
    main()