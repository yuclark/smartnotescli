import os
from datetime import datetime
from core.logger import log_info

def export_note(note_id, content, category, priority, status, created_at) -> str:
    os.makedirs("exports", exist_ok=True)
    filename = f"exports/archived_note_{note_id}.md"
    
    document = f"""# Systems Backup: Note #{note_id}
- **Metadata Classification:** `{category}`  
- **System Priority Rating:** `{priority}`  
- **Functional Progress State:** `{status}`  
- **Captured Generation Ingestion:** {created_at}  

---

## Content Statement
{content}
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(document)
    log_info(f"System Note ID {note_id} exported to clean markdown at {filename}")
    return filename