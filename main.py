from rich.console import Console
from rich.table import Table
from datetime import datetime
import sys

from platforms import load_platforms, get_platform_names, select_platforms, add_platform_cli
from scan import scan_all
from utils import save_html, log_error

DEFAULT_CONCURRENCY = 50

def print_summary_table(results, console):
    # Safely filter results with .get() to avoid KeyError
    found = [r for r in results if r.get("found", False)]
    notfound = [r for r in results if r.get("not found", False)]
    
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

def validate_results(results):
    """Ensure all results have required keys."""
    validated = []
    for r in results:
        if not isinstance(r, dict):
            continue  # Skip invalid entries
        r.setdefault("found", False)
        r.setdefault("not found", not r["found"])
        validated.append(r)
    return validated

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
        usernames = ["admin"] if not user_input else [
            u.strip() for u in (user_input.split(",") if "," in user_input else user_input.split()) if u.strip()
        ]
        if not usernames:
            graceful_exit(console, "[red]No username(s) provided![/red]", exit_code=1)

        # Platform selection
        all_platform_names = get_platform_names(platforms)
        console.print("[grey58]Available platforms: " + ", ".join(all_platform_names) + "[/grey58]")
        console.print("[grey58]Press Enter to scan all platforms, or specify platform(s) (comma-separated) to scan.[/grey58]")
        plat_input = console.input("[green]Enter platform(s) to scan (default: all):[/green] ").strip()
        chosen_platforms = platforms if not plat_input else select_platforms(
            platforms, [p.strip().lower() for p in plat_input.split(",") if p.strip()]
        )

        # Scan execution
        console.print(f"Scanning {', '.join(usernames)} across {len(chosen_platforms)} platform(s)...\n")
        start = datetime.now()
        try:
            results = scan_all(usernames, chosen_platforms, DEFAULT_CONCURRENCY, log_error, console)
            if hasattr(results, '__await__'):
                import asyncio
                results = asyncio.run(results)
            results = validate_results(results)  # Validate before processing
        except Exception as e:
            graceful_exit(console, f"[red]Error during scanning: {e}[/red]", exit_code=1)

        # Save and display results
        duration = (datetime.now() - start).total_seconds()
        save_html(usernames, results, stats={
            "platforms": len(chosen_platforms),
            "usernames": len(usernames),
            "duration": f"{duration:.1f}"
        })
        found_count = sum(r.get("found", False) for r in results)
        print_summary_table(results, console)
        console.print(f"[bold green]{found_count} found[/bold green] / {len(results)} checked in {duration:.1f} seconds.")
        graceful_exit(console)  # Exit with success message

    except KeyboardInterrupt:
        graceful_exit(console, "[yellow]Scan interrupted by user (Ctrl+C).[/yellow]", exit_code=0)

if __name__ == "__main__":
    main()
