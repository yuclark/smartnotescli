# Simple keyword mapping for auto-categorization
KEYWORDS = {
    "Work": ["meeting", "deadline", "project", "task", "client", "manager", "todo"],
    "Coding": ["code", "bug", "python", "javascript", "git", "github", "api", "database", "sqlite"],
    "Personal": ["gym", "grocery", "buy", "health", "workout", "reminder", "call"],
    "Ideas": ["innovate", "brainstorm", "app", "business", "concept", "draft"]
}

def auto_categorize(content: str) -> str:
    """Scans the text content and returns a matching category, defaulting to 'General'."""
    content_lower = content.lower()
    
    for category, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in content_lower:
                return category
                
    return "General"