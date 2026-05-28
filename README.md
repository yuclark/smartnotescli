# Enterprise Smart Notes CLI (v2.0)

An enterprise-ready, robust Python CLI knowledge-base utility application implementing Clean Architecture guidelines, deterministic text-processing analytics, soft-deletion safety cycles, and a self-contained automation Unit Test validation layer.

## 🛠️ Architecture Structural Overview
The application isolates concerns completely across dedicated operational software patterns:
- `core/database.py`: Clean CRUD operations mapping directly to an embedded SQLite local architecture.
- `core/tagger.py`: Configurable heuristic categorization engine referencing JSON parameters.
- `core/logger.py`: Centralized logging interceptor emitting application execution updates to `app.log`.
- `tests/`: Automated verification suite using an isolated `:memory:` database system.

## ✨ Advanced Features
1. **Dynamic JSON Profiling Configurations:** Add words and manage metadata tags directly within `config/settings.json`.
2. **Deterministic Urgency Analysis:** Auto-assigns prioritization flags (High/Medium/Low) using language structural checks.
3. **Agile Workflow Pipelines:** Process note items through `Todo` -> `In Progress` -> `Done` milestones.
4. **Data Fail-safes:** Implements standard structural Soft-Deletions via an isolated, recoverable system trash bin.
5. **Integrated Verification Coverage:** Execute comprehensive software suite checks directly through the active interactive terminal window.

## 🚀 Setting Up & Executing Globally
1. Clone repository to your local target folder directory.
2. Complete environment setup and dependencies onboarding step:
   ```bash
   pip install -r requirements.txt