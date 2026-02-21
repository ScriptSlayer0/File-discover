import psutil
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Header, Footer
from textual.containers import Container

class disk_partitions(App):

    CSS = """
    Screen {
        align: center middle;
    }
    """

    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            DataTable(id="partition_table")
        )
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#partition_table", DataTable)

        table.add_columns("Mountpoint", "Device", "Filesystem", "Options")

        partitions = psutil.disk_partitions()

        for partition in partitions:
            table.add_row(
                partition.mountpoint,
                partition.device,
                partition.fstype,
                partition.opts
            )

def print_partition_structure():
    app = disk_partitions()
    app.run()