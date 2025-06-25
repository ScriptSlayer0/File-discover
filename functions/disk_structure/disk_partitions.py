import psutil

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

def print_partition_structure():
    console = Console()
    table = Table(title="Disk Partitions")
    table.add_column("Mountpoint", style="green")
    table.add_column("Device", style="magenta")
    table.add_column("Filesystem", style="blue")
    table.add_column("Options", style="cyan")

    # Define the partitions list
    partitions = psutil.disk_partitions()  # Add this line

    for partition in partitions:
        table.add_row(
            partition.mountpoint,
            partition.device,
            partition.fstype,
            partition.opts
        )

    panel = Panel(table, title="Disk Partitions", style="bold")
    console.print(panel)
