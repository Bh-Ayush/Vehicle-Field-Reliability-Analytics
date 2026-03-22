# Vehicle-Field-Reliability-Analytics

**An end-to-end analytics platform that ingests NHTSA consumer complaint data, performs statistical reliability analysis using Weibull survival models, and surfaces actionable failure patterns across EV manufacturers — Tesla, Rivian, Lucid, and Ford's EV lineup.**



---

## Architecture

```
NHTSA API ─→ Ingest ─→ Clean ─→ EDA ─→ Weibull Analysis
                │          │        │           │
                ▼          ▼        ▼           ▼
           data/raw/   data/proc/  outputs/   outputs/
           *.csv       *.parquet   figures/   results/
```

## Key Analyses

| Analysis | Method | Output |
|----------|--------|--------|
| **Failure Distribution** | Weibull MLE (β, η) per make & component | Survival curves, hazard rates |
| **B-Life Estimates** | B10/B50 from fitted parameters | Time at which 10%/50% fail |
| **Component Ranking** | Complaint volume + severity scoring | Heatmaps, grouped bars |
| **Trend Detection** | Time-series complaint volume | Monthly trend lines by make |
| **Severity Assessment** | Composite score (crash/fire/injury) | Manufacturer comparison |

### Weibull Shape Parameter (β) Interpretation

| β Range | Failure Pattern | Engineering Action |
|---------|-----------------|-------------------|
| β < 1 | Infant mortality — early-life defects | Improve QC, burn-in testing |
| β ≈ 1 | Random failures — constant rate | Condition monitoring |
| 1 < β ≤ 2 | Early wear-out beginning | Preventive maintenance scheduling |
| β > 2 | Wear-out / fatigue failures | Component redesign, material upgrade |

## How to Run 

```bash
# Clone and setup
git clone https://github.com/Bh-Ayush/Vehicle-Field-Reliability-Analytics.git
cd Vehicle-Field-Reliability-Analytics
pip install -r requirements.txt

# Run full pipeline (synthetic data — no API key needed)
python run_pipeline.py

# Run with live NHTSA data
python run_pipeline.py --mode api

# Run individual steps
python run_pipeline.py --step eda
python run_pipeline.py --step weibull
```

## Project Structure

```
Vehicle-Field-Reliability-Analytics/
├── config.py                 # Vehicle definitions, paths, parameters
├── run_pipeline.py           # Main orchestrator
├── requirements.txt
├── src/
│   ├── ingest.py            # NHTSA API client + synthetic data generator
│   ├── clean.py             # Cleaning, type casting, feature engineering
│   ├── eda.py               # 10 exploratory visualizations
│   └── weibull.py           # MLE fitting, survival/hazard curves, B-life
├── data/
│   ├── raw/                 # Raw ingested CSV files
│   └── processed/           # Cleaned parquet files
├── outputs/
│   ├── figures/             # PNG visualizations (EDA + Weibull)
│   └── results/             # Weibull parameter tables (CSV)
├── notebooks/               # Jupyter exploration (optional)
└── tests/
```

## Output Figures

### EDA (10 outputs)
1. Complaint volume by manufacturer
2. Component failure heatmap (make × component)
3. Monthly complaint trend
4. Mileage distribution at failure (violin)
5. Time-to-failure by component (box)
6. Severity breakdown (crash/fire/injury)
7. Geographic distribution (top 15 states)
8. Top 5 components per manufacturer
9. Vehicle age at complaint
10. Summary statistics table

### Weibull Analysis (5+ outputs)
11. Survival curves by manufacturer
12. Hazard rate curves by manufacturer
13. Survival curves by component
14. β comparison charts (manufacturers & components)
15. Weibull probability plots (per make)

## Data Sources

- **Primary**: [NHTSA Vehicle Complaints Database](https://www.nhtsa.gov/recalls-complaints/complaints) 
- **Scope**: Tesla (Model 3/Y/S/X), Rivian (R1T/R1S), Lucid Air, Ford (Mach-E, F-150 Lightning)
- **Synthetic mode**: Generates 5,000 records with statistically plausible Weibull-distributed failure times per component, for development and demonstration

## Methodology

**Weibull Distribution** is the standard reliability engineering model for time-to-failure analysis. The 2-parameter form:

- **Reliability function**: `R(t) = exp(-(t/η)^β)`
- **β (shape)**: Determines failure rate behavior — see interpretation table above
- **η (scale)**: Characteristic life — the time at which 63.2% of units have failed
- **MTTF**: `η · Γ(1 + 1/β)` — mean time to failure

Parameters are estimated via Maximum Likelihood Estimation (MLE) using `scipy.stats.weibull_min.fit()`.

**References**:
- Abernethy, R.B. *The New Weibull Handbook* (5th ed.)
- O'Connor, P.D.T. & Kleyner, A. *Practical Reliability Engineering* (5th ed.)


## License

MIT
