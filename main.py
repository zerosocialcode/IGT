from rich.console import Console
from rich.table import Table
from datetime import datetime
import sys

from platforms import load_platforms, get_platform_names, select_platforms, add_platform_cli
from scan import scan_all
from utils import save_html, log_error

DEFAULT_CONCURRENCY = 50

def print_summary_table(results, console):
    found = [r for r in results if r["found"]]
    notfound = [r for r in results if r["not found"]]
    table = Table(title="Scan Summary", show_lines=True)
    table.add_column("Platform", style="cyan", no_wrap=True)
    table.add_column("Found", justify="right", style="green")
    table.add_column("Not Found", justify="right", style="grey50")
    platforms = set(r["platform"] for r in results)
    for plat in sorted(platforms):
        found_n = sum(1 for r in found if r["platform"] == plat)
        notfound_n = sum(1 for r in notfound if r["platform"] == plat)
        table.add_row(plat.capitalize(), str(found_n), str(notfound_n))
    console.print(table)

def graceful_exit(console, message="", exit_code=0):
    if message:
        console.print(f"[bold yellow]{message}[/bold yellow]")
    console.print("\n[bold cyan]Thank you for using IGT Toolkit! Have a great day![/bold cyan]\n")
    sys.exit(exit_code)

def main():
    try:
        add_platform_cli()  # Handles add-platform command and exits if triggered

        banner = r"""
 _____ _____ _______ 
|_   _/ ____|__   __|
  | || |  __   | |   
  | || | |_ |  | |   
 _| || |__| |  | |   
|_____\_____|  |_|   
    """
        console = Console()
        console.print(f"[bold cyan]{banner}[/bold cyan]")
        console.print("[bold cyan]IGT: A Basic Information Gathering Toolkit v1[/bold cyan]")

        # Load platforms
        try:
            platforms = load_platforms()
        except Exception as e:
            graceful_exit(console, f"[red]{e}[/red]", exit_code=1)

        # Username input
        console.print("[grey58]Press Enter to use default username, or enter multiple usernames separated by comma/space.[/grey58]")
        user_input = console.input("[green]Enter username(s) to scan (default: admin):[/green] ").strip()
        if not user_input:
            usernames = ["admin"]
        else:
            # Split by comma or whitespace, clean up
            if "," in user_input:
                usernames = [u.strip() for u in user_input.split(",") if u.strip()]
            else:
                usernames = [u.strip() for u in user_input.split() if u.strip()]
        if not usernames:
            graceful_exit(console, "[red]No username(s) provided![/red]", exit_code=1)

        # Platform selection
        all_platform_names = get_platform_names(platforms)
        default_platform_label = "all"
        console.print("[grey58]Available platforms: " + ", ".join(all_platform_names) + "[/grey58]")
        console.print(f"[grey58]Press Enter to scan all platforms, or specify platform(s) (comma-separated) to scan.[/grey58]")
        plat_input = console.input(f"[green]Enter platform(s) to scan (default: {default_platform_label}):[/green] ").strip()
        if not plat_input:
            chosen_platforms = platforms
        else:
            plat_names = [p.strip().lower() for p in plat_input.split(",") if p.strip()]
            try:
                chosen_platforms = select_platforms(platforms, plat_names)
            except ValueError as e:
                graceful_exit(console, f"[red]{e}[/red]", exit_code=1)

        concurrency = DEFAULT_CONCURRENCY
        console.print(f"Scanning {', '.join(usernames)} across {len(chosen_platforms)} platform(s) ({len(chosen_platforms)*len(usernames)} checks)...\n")
        start = datetime.now()
        results = None
        try:
            results = scan_all(usernames, chosen_platforms, concurrency, log_error, console)
            if hasattr(results, '__await__'):  # If coroutine, run it
                import asyncio
                results = asyncio.run(results)
        except Exception as e:
            graceful_exit(console, f"[red]Error during scanning: {e}[/red]", exit_code=1)

        duration = (datetime.now() - start).total_seconds()
        save_html(usernames, results, stats={
            "platforms": len(chosen_platforms),
            "usernames": len(usernames),
            "duration": f"{duration:.1f}"
        })
        found_count = sum(r["found"] for r in results)
        print_summary_table(results, console)
        console.print(f"[bold green]{found_count} found[/bold green] / {len(results)} checked in {duration:.1f} seconds.")
        console.print("\n[bold cyan]Thank you for using IGT Toolkit! Have a great day![/bold cyan]\n")

    except KeyboardInterrupt:
        console = Console()
        graceful_exit(console, "[yellow]Scan interrupted by user (Ctrl+C).[/yellow]", exit_code=0)

if __name__ == "__main__":
    main()
