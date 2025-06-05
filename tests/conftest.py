import sys
from pathlib import Path

# Add src directory to sys.path for tests
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
