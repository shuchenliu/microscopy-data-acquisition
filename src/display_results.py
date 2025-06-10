import contextlib
from multiprocessing import Manager
from subprocess import CompletedProcess
from time import sleep

from rich.live import Live
from rich.table import Table

SPINNER_FRAMES = ["|", "/", "-", "\\"]

def render_table(table_name, col_names, labels, results, outputs, frame):
    table = Table(title=table_name)
    for col_name in col_names:
        table.add_column(col_name)

    if any(v is not None for v in outputs.values()):
        table.add_column('Output')

    for label in labels:
        result = results[label]
        spinner = SPINNER_FRAMES[frame % len(SPINNER_FRAMES)] if result.startswith("Running") else ''
        row = list([label, result + spinner])
        if outputs[label] is not None:
            row.append(outputs[label])
        table.add_row(*row)

    return table


@contextlib.contextmanager
def display_table(*, table_name, col_names, labels):
    # wrap frame so we can pass by reference
    frame = [0]

    def render_proxy(_status, _outputs):
        return render_table(table_name, col_names, labels, _status, _outputs, frame[0])

    with Manager() as manager:
        completed = manager.Value("i", 0)
        status = manager.dict({label: "Running..." for label in labels})
        outputs = manager.dict({label: None for label in labels})

        passed = [status, outputs]

        def update_status(result: CompletedProcess):
            label, res, output = result
            status[label] = f"[green]Done[/green]" if res.returncode == 0 else f"❌ Failed ({res.returncode})"
            outputs[label] = output
            completed.value += 1

        with Live(render_proxy(*passed), refresh_per_second=10) as live:
            yield update_status

            # Render loop
            while completed.value < len(labels):
                frame[0] += 1
                live.update(render_proxy(*passed))
                sleep(0.25)



            live.update(render_proxy(*passed))
