import psutil
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Header, Footer
from textual.containers import Container


# =========================
# CONFIGURACIÓN GLOBAL
# =========================

SIZE_MODE = "auto"  # auto | gb | tb | binary


# =========================
# Formateo de tamaños
# =========================

def format_size(size: int, mode: str = "auto") -> str:

    if mode == "gb":
        return f"{size / (1024 ** 3):.2f} GB"

    if mode == "tb":
        return f"{size / (1024 ** 4):.2f} TB"

    if mode == "binary":
        units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
        power = 1024
    else:
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        power = 1024

    n = 0
    while size >= power and n < len(units) - 1:
        size /= power
        n += 1

    return f"{size:.2f} {units[n]}"


# =========================
# APP TEXTUAL
# =========================

class PartitionApp(App):

    CSS = """
    Screen {
        align: center middle;
    }

    DataTable {
        width: 100%;
        height: 100%;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            DataTable(id="partition_table")
        )
        yield Footer()

    def on_mount(self) -> None:
        self.table = self.query_one("#partition_table", DataTable)

        # Crear columnas una sola vez
        self.table.add_columns(
            "Mountpoint",
            "Device",
            "Filesystem",
            "Total",
            "Used",
            "Free",
            "Usage %"
        )

        self.refresh_table()

    def action_refresh(self) -> None:
        self.refresh_table()

    def refresh_table(self) -> None:
        # Limpiar tabla (compatible con versiones antiguas y nuevas)
        self.table.clear()

        partitions = psutil.disk_partitions()

        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                percent = usage.percent

                if percent >= 80:
                    percent_str = f"[bold red]{percent}%[/bold red]"
                elif percent >= 60:
                    percent_str = f"[yellow]{percent}%[/yellow]"
                else:
                    percent_str = f"[green]{percent}%[/green]"

                self.table.add_row(
                    partition.mountpoint,
                    partition.device,
                    partition.fstype,
                    format_size(usage.total, SIZE_MODE),
                    format_size(usage.used, SIZE_MODE),
                    format_size(usage.free, SIZE_MODE),
                    percent_str
                )

            except PermissionError:
                continue
            except Exception:
                continue


# =========================
# API pública
# =========================

def print_partition_structure(mode: str = "auto"):
    global SIZE_MODE
    SIZE_MODE = mode

    app = PartitionApp()
    app.run()