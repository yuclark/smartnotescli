import sys
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align

import core.database as database
import core.tagger as tagger
import core.exporter as exporter

console = Console()

def display_welcome():
    console.print(Panel.fit(
        "[bold cyan]⚡ ENTERPRISE SMART NOTES CLI v2.0[/bold cyan]\n[dim]Complete Task Pipelines, System Analytics & Embedded Testing[/dim]",
        border_style="cyan"
    ))

def handle_add():
    console.print("\n[bold green]📝 Ingest Note Content Context:[/bold green]")
    content = Prompt.ask("Enter content text structural input")
    if not content.strip():
        console.print("[bold red]Evaluation Error: Content buffer empty.[/bold red]\n")
        return
        
    category, priority = tagger.analyze_content(content)
    database.add_note(content, category, priority)
    console.print(f"\n[bold green]✓ Ingestion Complete.[/bold green] Tagged: [yellow]{category}[/yellow] | Priority: [magenta]{priority}[/magenta]\n")

def display_notes(notes_list):
    if not notes_list:
        console.print("[yellow]No active system notes match the requested stack tracking state.[/yellow]\n")
        return
    table = Table(show_header=True, header_style="bold cyan", expand=True)
    table.add_column("ID", width=4)
    table.add_column("Content Statement", width=45)
    table.add_column("Category", style="yellow")
    table.add_column("Priority", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Ingestion Time", style="dim")
    
    for row in notes_list:
        status_color = "green" if row[4] == "Done" else "orange3" if row[4] == "In Progress" else "white"
        table.add_row(str(row[0]), row[1], row[2], row[3], f"[{status_color}]{row[4]}[/{status_color}]", row[5])
    console.print(table)

def handle_status_update():
    note_id = Prompt.ask("\nEnter target Note ID to progress workflow state")
    status_choice = Prompt.ask("Select modern pipeline designation", choices=["Todo", "In Progress", "Done"])
    if note_id.isdigit():
        database.update_status(int(note_id), status_choice)
        console.print("[bold green]✓ System pipeline registry synced.[/bold green]\n")
    else:
        console.print("[bold red]Input parsing failure.[/bold red]\n")

def handle_soft_delete():
    note_id = Prompt.ask("\nEnter target Note ID to push to local tracking Trash Bin")
    if note_id.isdigit():
        database.soft_delete_note(int(note_id))
        console.print("[bold yellow]✓ Note soft-deleted and moved to trash folder.[/bold yellow]\n")

def handle_trash_bin():
    while True:
        trash = database.get_trash_notes()
        console.print("[bold red]🗑️ Trash Bin Configuration Tracking Dump:[/bold red]")
        for item in trash:
            console.print(f"  ID: {item[0]} | Cat: {item[2]} | Snippet: {item[1][:30]}...")
        console.print("\nOptions: 1. Restore Note | 2. Return to Central Monitor")
        choice = Prompt.ask("Action selection", choices=["1", "2"], default="2")
        if choice == "1":
            target = Prompt.ask("Enter ID to recover")
            if target.isdigit():
                database.restore_note(int(target))
                console.print("[bold green]✓ Record fully restored to active pool.[/bold green]\n")
        else:
            break

def handle_analytics():
    cat_stats, status_stats = database.get_analytics_payload()
    console.print("\n[bold cyan]📊 System Analytical Insights & Aggregations[/bold cyan]")
    
    table_cat = Table(title="Category Tracking Weights", header_style="bold yellow")
    table_cat.add_column("Category")
    table_cat.add_column("Logged Footprint Count")
    for item in cat_stats:
        table_cat.add_row(item[0], str(item[1]))
        
    table_status = Table(title="Pipeline Development States", header_style="bold green")
    table_status.add_column("Status State")
    table_status.add_column("Volume Metric")
    for item in status_stats:
        table_status.add_row(item[0], str(item[1]))
        
    console.print(table_cat)
    console.print(table_status)
    console.print()

def execute_automated_tests():
    console.print("\n[bold magenta]🧪 Initializing System Automated Testing Suite Engine...[/bold magenta]")
    import subprocess
    result = subprocess.run([sys.executable, "-m", "unittest", "tests/test_core.py"])
    if result.returncode == 0:
        console.print("[bold green]🏆 ALL SYSTEM UNIT TESTS PASSED SUCCESSFULLY![/bold green]\n")
    else:
        console.print("[bold red]❌ SYSTEM ERROR INDICATION: UNIT TEST FAILURE REPORTED.[/bold red]\n")

def main():
    database.init_db()
    display_welcome()
    
    while True:
        console.print("[bold white]System Operations Dashboard Menu Registry:[/bold white]")
        console.print("1. [green]Add Note / Objective Ingestion[/green]")
        console.print("2. [blue]Monitor Active Logs Table View[/blue]")
        console.print("3. [yellow]Execute Filter Pattern Text Query Search[/yellow]")
        console.print("4. [orange3]Progress Workflow System Pipeline Status[/orange3]")
        console.print("5. [red]Soft Delete Component Record Entry[/red]")
        console.print("6. [purple]Manage System Retention Trash Bin[/purple]")
        console.print("7. [cyan]View Enterprise Analytics Engine Output[/cyan]")
        console.print("8. [bold magenta]Run System Test Coverage Verification Suite[/bold magenta]")
        console.print("9. [bold white]Exit Terminal Program[/bold white]")
        
        choice = Prompt.ask("Choose operation pointer context", choices=[str(i) for i in range(1, 10)], default="2")
        
        if choice == "1": handle_add()
        elif choice == "2": display_notes(database.get_active_notes())
        elif choice == "3": display_notes(database.search_notes(Prompt.ask("Enter character array search matching pointer")))
        elif choice == "4": handle_status_update()
        elif choice == "5": handle_soft_delete()
        elif choice == "6": handle_trash_bin()
        elif choice == "7": handle_analytics()
        elif choice == "8": execute_automated_tests()
        elif choice == "9":
            console.print("[bold cyan]System shutdown safely completed. Goodbye.[/bold cyan]")
            sys.exit(0)

if __name__ == "__main__":
    main()