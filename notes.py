import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
# NEW IMPORTS FOR THE DASHBOARD
from rich.align import Align
from rich.columns import Columns

import database
import tagger
import exporter

console = Console()

def display_welcome():
    console.print(Panel.fit(
        "[bold cyan]🧠 SMART NOTES CLI[/bold cyan]\n[dim]Your local, auto-tagging knowledge base[/dim]",
        border_style="magenta"
    ))

def handle_add():
    console.print("\n[bold green]📝 Create a New Note:[/bold green]")
    content = Prompt.ask("Enter your note content")
    
    if not content.strip():
        console.print("[bold red]Error: Note content cannot be empty.[/bold red]")
        return
        
    category = tagger.auto_categorize(content)
    database.add_note(content, category)
    
    console.print(f"\n[bold green]✓ Note saved successfully![/bold green]")
    console.print(f"Auto-categorized as: [bold yellow]{category}[/bold yellow]\n")

def display_notes_table(notes):
    if not notes:
        console.print("[yellow]No notes found.[/yellow]\n")
        return

    table = Table(title="Your Notes", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Content", width=50)
    table.add_column("Category", style="yellow")
    table.add_column("Created At", style="green")

    for row in notes:
        table.add_row(str(row[0]), row[1], row[2], row[3])

    console.print(table)
    console.print()

def handle_view():
    notes = database.get_all_notes()
    display_notes_table(notes)

def handle_search():
    query = Prompt.ask("\nEnter search keyword (content or category)")
    notes = database.search_notes(query)
    display_notes_table(notes)

def handle_export():
    note_id_str = Prompt.ask("\nEnter the ID of the note you want to export to Markdown")
    if not note_id_str.isdigit():
        console.print("[bold red]Invalid ID format.[/bold red]\n")
        return
        
    note = database.get_note_by_id(int(note_id_str))
    if not note:
        console.print("[bold red]Note not found.[/bold red]\n")
        return
        
    filepath = exporter.export_to_markdown(note[0], note[1], note[2], note[3])
    console.print(f"[bold green]✓ Successfully exported to {filepath}[/bold green]\n")

# NEW FEATURE: ANALYTICS DASHBOARD
def handle_analytics():
    stats = database.get_category_stats()
    all_notes = database.get_all_notes()
    total_notes = len(all_notes)
    
    if total_notes == 0:
        console.print("[yellow]\nAdd some notes first to see analytics![/yellow]\n")
        return
        
    console.print("\n[bold cyan]📊 Knowledge Base Analytics[/bold cyan]")
    
    # Summary Box
    summary_text = f"[bold white]Total Notes Saved:[/bold white] [bold green]{total_notes}[/bold green]"
    console.print(Panel(Align.center(summary_text), border_style="cyan"))
    
    # Text-based Distribution Chart
    console.print("[bold]Category Distribution:[/bold]")
    for category, count in stats:
        percentage = (count / total_notes) * 100
        # Create a visual block bar representation
        bar_length = int(percentage / 5)  # 1 block per 5%
        bar = "■" * max(bar_length, 1)
        console.print(f"  [yellow]{category:<12}[/yellow] | [magenta]{bar:<20}[/magenta] {count} note(s) ({percentage:.1f}%)")
    console.print()

def main():
    database.init_db()
    display_welcome()
    
    while True:
        console.print("[bold white]Options:[/bold white]")
        console.print("1. [bold green]Add Note[/bold green]")
        console.print("2. [bold blue]View All Notes[/bold blue]")
        console.print("3. [bold yellow]Search Notes[/bold yellow]")
        console.print("4. [bold magenta]Export Note to MD[/bold magenta]")
        console.print("5. [bold cyan]View Analytics Dashboard[/bold cyan]") # New Menu item
        console.print("6. [bold red]Exit[/bold red]")
        
        choice = Prompt.ask("Choose an action", choices=["1", "2", "3", "4", "5", "6"], default="1")
        
        if choice == "1":
            handle_add()
        elif choice == "2":
            handle_view()
        elif choice == "3":
            handle_search()
        elif choice == "4":
            handle_export()
        elif choice == "5":
            handle_analytics()
        elif choice == "6":
            console.print("[bold cyan]Goodbye![/bold cyan]")
            sys.exit(0)

if __name__ == "__main__":
    main()