#!/usr/bin/env python3
"""Runner script for Counter-Party Lead Explorer."""

import sys
from pathlib import Path

# Add the project root to path so imports work correctly
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Now import and run the app
import streamlit.web.cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", str(project_root / "counter_party_explorer" / "app.py"), "--server.headless", "true"]
    sys.exit(stcli.main())
