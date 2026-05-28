# Smart Notes CLI

A beautiful, modular command-line interface application written in Python that automatically categorizes notes based on keyword patterns using a local SQLite database.

## Features
- **Smart Auto-Categorization:** Detects keywords to group notes into Work, Coding, Personal, or Ideas.
- **Local Persistence:** Powered by an embedded SQLite database.
- **Rich Visual CLI:** Beautifully rendered UI elements, panels, and data tables.
- **Markdown Export:** Clean structural export capabilities for local notation archiving.

## Architecture Highlights
- Fully separated layers: Presentation (CLI), Business Logic (Tagger), Database Logic, and File Handling.

## Getting Started
1. Clone the repo.
2. Initialize virtual environment: `python -m venv venv`
3. Activate environment and install dependencies: `pip install -r requirements.txt`
4. Run the application: `python notes.py`