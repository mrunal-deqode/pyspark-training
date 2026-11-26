from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Output directory for generated CSV files
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# Reproducibility
RANDOM_SEED = 42

# Initial dataset sizes
NUM_CANDIDATES = 2_000
NUM_ADMINS = 5
NUM_JOBS = 200
NUM_APPLICATIONS = 5_000
