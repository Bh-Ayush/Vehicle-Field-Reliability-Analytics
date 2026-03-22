"""
Configuration for Vehicle Field Reliability Analytics.
Centralizes vehicle definitions, API endpoints, file paths, and analysis parameters.
"""

from pathlib import Path
from datetime import date

# ──────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────
ROOT_DIR = Path(__file__).parent
DATA_RAW = ROOT_DIR / "data" / "raw"
DATA_PROCESSED = ROOT_DIR / "data" / "processed"
OUTPUT_FIGURES = ROOT_DIR / "outputs" / "figures"

for d in [DATA_RAW, DATA_PROCESSED, OUTPUT_FIGURES]:
    d.mkdir(parents=True, exist_ok=True)

# ──────────────────────────────────────────────
# NHTSA API
# ──────────────────────────────────────────────
NHTSA_COMPLAINTS_URL = "https://api.nhtsa.gov/complaints/complaintsByVehicle"

# ──────────────────────────────────────────────
# Vehicle scope
# ──────────────────────────────────────────────
VEHICLES: dict[str, list[dict]] = {
    "TESLA": [
        {"model": "MODEL 3", "years": list(range(2017, 2026))},
        {"model": "MODEL Y", "years": list(range(2020, 2026))},
        {"model": "MODEL S", "years": list(range(2012, 2026))},
        {"model": "MODEL X", "years": list(range(2016, 2026))},
    ],
    "RIVIAN": [
        {"model": "R1T", "years": list(range(2022, 2026))},
        {"model": "R1S", "years": list(range(2022, 2026))},
    ],
    "LUCID": [
        {"model": "AIR", "years": list(range(2022, 2026))},
    ],
    "FORD": [
        {"model": "MUSTANG MACH-E", "years": list(range(2021, 2026))},
        {"model": "F-150 LIGHTNING", "years": list(range(2022, 2026))},
    ],
}

# Model-year launch dates (approx.) — used for time-to-failure calc
MODEL_YEAR_START: dict[str, dict[str, dict[int, date]]] = {
    "TESLA": {
        "MODEL 3": {yr: date(yr - 1, 7, 1) for yr in range(2017, 2026)},
        "MODEL Y": {yr: date(yr - 1, 10, 1) for yr in range(2020, 2026)},
        "MODEL S": {yr: date(yr - 1, 6, 1) for yr in range(2012, 2026)},
        "MODEL X": {yr: date(yr - 1, 9, 1) for yr in range(2016, 2026)},
    },
    "RIVIAN": {
        "R1T": {yr: date(yr - 1, 12, 1) for yr in range(2022, 2026)},
        "R1S": {yr: date(yr - 1, 12, 1) for yr in range(2022, 2026)},
    },
    "LUCID": {
        "AIR": {yr: date(yr - 1, 10, 1) for yr in range(2022, 2026)},
    },
    "FORD": {
        "MUSTANG MACH-E": {yr: date(yr - 1, 11, 1) for yr in range(2021, 2026)},
        "F-150 LIGHTNING": {yr: date(yr - 1, 12, 1) for yr in range(2022, 2026)},
    },
}

# ──────────────────────────────────────────────
# Analysis parameters
# ──────────────────────────────────────────────
WEIBULL_COMPONENTS = [
    "ELECTRICAL SYSTEM",
    "POWER TRAIN",
    "SERVICE BRAKES",
    "STEERING",
    "AIR BAGS",
    "SUSPENSION",
    "VISIBILITY/WIPER",
    "EXTERIOR LIGHTING",
    "SEATS",
    "STRUCTURE",
    "WHEELS",
    "LATCHES/LOCKS/LINKAGES",
    "VEHICLE SPEED CONTROL",
    "ELECTRONIC STABILITY CONTROL",
    "FORWARD COLLISION AVOIDANCE",
    "LANE DEPARTURE",
    "AUTOMATIC EMERGENCY BRAKING",
    "FUEL/PROPULSION SYSTEM",
    "TRACTION CONTROL SYSTEM",
]

# Minimum complaint count per group for Weibull fit
WEIBULL_MIN_SAMPLES = 15

# EDA: top N components to visualize
EDA_TOP_N_COMPONENTS = 15

# Random seed for reproducibility
RANDOM_SEED = 42
