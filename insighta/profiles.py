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


def list_profiles(gender, country, age_group, min_age, max_age,
                  sort_by, order, page, limit):
    params = {"page": page, "limit": limit}
    if gender: params["gender"] = gender
    if country: params["country"] = country
    if age_group: params["age_group"] = age_group
    if min_age: params["min_age"] = min_age
    if max_age: params["max_age"] = max_age
    if sort_by: params["sort_by"] = sort_by
    if order: params["order"] = order

    with console.status("[cyan]Fetching profiles...[/cyan]"):
        response = request("GET", "/api/profiles", params=params)

    if not response:
        return

    data = response.json()
    profiles = data.get("data", [])

    if not profiles:
        console.print("[yellow]No profiles found.[/yellow]")
        return

    display_table(profiles)
    console.print(
        f"\nPage [bold]{data.get('page')}[/bold] of "
        f"[bold]{data.get('total_pages')}[/bold] | "
        f"Total: [bold]{data.get('total')}[/bold]"
    )


def get_profile(profile_id: str):
    with console.status("[cyan]Fetching profile...[/cyan]"):
        response = request("GET", f"/api/profiles/{profile_id}")

    if not response:
        return

    if response.status_code == 404:
        console.print("[red]Profile not found.[/red]")
        return

    p = response.json().get("data", {})

    table = Table(show_header=False)
    table.add_column("Field", style="bold cyan")
    table.add_column("Value")

    for key, value in p.items():
        table.add_row(key, str(value))

    console.print(table)


def search_profiles(query: str):
    with console.status("[cyan]Searching...[/cyan]"):
        response = request("GET", "/api/profiles/search", params={"q": query})

    if not response:
        return

    profiles = response.json().get("data", [])

    if not profiles:
        console.print("[yellow]No results found.[/yellow]")
        return

    display_table(profiles)


def create_profile(name: str):
    with console.status(f"[cyan]Creating profile for '{name}'...[/cyan]"):
        response = request("POST", "/api/profiles", json={"name": name})

    if not response:
        return

    data = response.json()

    if data.get("status") == "success":
        console.print("[green]Profile created successfully.[/green]")
        get_profile(data["data"]["id"])
    else:
        console.print(f"[red]Error: {data.get('message')}[/red]")

