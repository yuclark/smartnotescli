import json
import os
from core.logger import log_error

CONFIG_PATH = os.path.join("config", "settings.json")

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        log_error(f"Error parsing configuration profile: {e}")
        return {"keywords": {}, "default_priority": "Medium"}

def analyze_content(content: str):
    config = load_config()
    content_lower = content.lower()
    
    # Heuristic category profiling
    detected_category = "General"
    for category, keywords in config.get("keywords", {}).items():
        if any(keyword.lower() in content_lower for keyword in keywords):
            detected_category = category
            break
            
    # Deterministic priority evaluation
    priority = config.get("default_priority", "Medium")
    if any(urgency in content_lower for urgency in ["urgent", "asap", "blocker", "critical", "deadline"]):
        priority = "High"
    elif any(low_priority in content_lower for low_priority in ["chill", "backlog", "someday"]):
        priority = "Low"
        
    return detected_category, priority