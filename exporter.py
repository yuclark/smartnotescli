import os
from datetime import datetime

def export_to_markdown(note_id: int, content: str, category: str, created_at: str) -> str:
    """Exports a single note into a nicely formatted Markdown file."""
    # Create an exports directory if it doesn't exist
    os.makedirs("exports", exist_ok=True)
    
    # Generate a clean filename
    filename = f"exports/note_{note_id}_{datetime.now().strftime('%Y%m%d')}.md"
    
    markdown_template = f"""# Note #{note_id}
**Category:** `{category}`  
**Created At:** {created_at}  

---

{content}
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_template)
        
    return filename