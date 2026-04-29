import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from .api import request

console = Console()


def display_table(profiles: list):
    table = Table(show_header=True, header_style="bold cyan")
    for col in ["ID", "Name", "Gender", "Age", "Age Group", "Country", "Created At"]:
        table.add_column(col)

    for p in profiles:
        table.add_row(
            str(p.get("id", "")),
            p.get("name", ""),
            p.get("gender", ""),
            str(p.get("age", "")),
            p.get("age_group", ""),
            p.get("country_name", ""),
            p.get("created_at", ""),
        )

    console.print(table)