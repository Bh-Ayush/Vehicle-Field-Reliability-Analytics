#!/usr/bin/env python3
"""
Vehicle Field Reliability Analytics — Phase 1 Pipeline

Orchestrates:
  1. Data ingestion  (NHTSA API or synthetic)
  2. Cleaning + feature engineering
  3. Exploratory data analysis
  4. Weibull survival analysis

Usage:
    python run_pipeline.py                  # full pipeline, synthetic data
    python run_pipeline.py --mode api       # full pipeline, live NHTSA data
    python run_pipeline.py --step eda       # run only EDA (assumes cleaned data exists)
"""

import argparse
import logging
import sys
import time
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent))

from config import DATA_RAW, DATA_PROCESSED, OUTPUT_FIGURES

logger = logging.getLogger("pipeline")


def main():
    parser = argparse.ArgumentParser(
        description="Vehicle Field Reliability Analytics — Phase 1 Pipeline"
    )
    parser.add_argument(
        "--mode",
        choices=["synthetic", "api"],
        default="synthetic",
        help="Data source: 'synthetic' (default) or 'api' (live NHTSA)",
    )
    parser.add_argument(
        "--step",
        choices=["all", "ingest", "clean", "eda", "weibull"],
        default="all",
        help="Run a specific step or 'all' (default)",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=5000,
        help="Number of synthetic records (default: 5000)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)-10s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    t0 = time.time()
    logger.info("=" * 60)
    logger.info("Vehicle Field Reliability Analytics — Phase 1")
    logger.info("=" * 60)

    steps = [args.step] if args.step != "all" else ["ingest", "clean", "eda", "weibull"]

    # ── Step 1: Ingest ──
    if "ingest" in steps:
        logger.info("\n▶ STEP 1: Data Ingestion")
        from src.ingest import fetch_from_api, generate_synthetic

        if args.mode == "api":
            fetch_from_api()
        else:
            generate_synthetic(n_records=args.n)

    # ── Step 2: Clean ──
    if "clean" in steps:
        logger.info("\n▶ STEP 2: Data Cleaning")
        from src.clean import clean

        raw_file = DATA_RAW / (
            "nhtsa_complaints_raw.csv" if args.mode == "api"
            else "nhtsa_complaints_synthetic.csv"
        )
        clean(input_path=raw_file)

    # ── Step 3: EDA ──
    if "eda" in steps:
        logger.info("\n▶ STEP 3: Exploratory Data Analysis")
        from src.eda import run_eda
        run_eda()

    # ── Step 4: Weibull ──
    if "weibull" in steps:
        logger.info("\n▶ STEP 4: Weibull Survival Analysis")
        from src.weibull import run_weibull
        results = run_weibull()

        # Print key findings
        by_make = results["by_make"]
        logger.info("\n" + "=" * 60)
        logger.info("KEY FINDINGS — Weibull Parameters by Manufacturer")
        logger.info("=" * 60)
        for _, row in by_make.iterrows():
            logger.info(
                f"  {row['maketxt']:8s} │ β={row['beta']:.3f} │ η={row['eta']:>7.0f}d │ "
                f"MTTF={row['mttf']:>7.0f}d │ B10={row['b10']:>6.0f}d │ n={row['n']}"
            )
            logger.info(f"           │ → {row['interpretation']}")

    elapsed = time.time() - t0
    logger.info(f"\n✓ Pipeline complete in {elapsed:.1f}s")
    logger.info(f"  Figures → {OUTPUT_FIGURES}/")
    logger.info(f"  Data    → {DATA_PROCESSED}/")


if __name__ == "__main__":
    main()
