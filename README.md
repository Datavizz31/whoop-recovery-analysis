# WHOOP Recovery Analysis — Do Lifestyle Habits Actually Work?

**By Lalithya Alapati** | [LinkedIn](https://linkedin.com/in/lalithyaalapati3108) |

---

## The Question

WHOOP's AI coaching recommends lifestyle habits to improve member recovery. But does following those recommendations actually work?

I used 48 days of real WHOOP member data to find out — and the answer is more interesting than a simple yes or no.

---

## What I Built

A full analytics pipeline on real WHOOP data:

```
Real WHOOP Export (Kaggle)
        ↓
Python — transform raw data into Amplitude event schema
        ↓
Rule-based AI recommendation engine
(personalized daily coaching based on recovery zone + HRV)
        ↓
Amplitude — feature engagement analytics
(recovery trends, HRV trends, deep sleep paradox)
```

---

## The Data

**Source:** Kaggle — [andrewcxjin/whoop-dataset](https://www.kaggle.com/datasets/andrewcxjin/whoop-dataset) (CC BY 4.0)  
**Size:** 48 days of real single-member WHOOP export  
**Fields:** Recovery score, HRV, resting heart rate, strain, sleep stages, SpO2, skin temperature  
**Experiment periods:**

| Period | Days | Description |
|--------|------|-------------|
| Baseline | 28 | Normal lifestyle, no changes |
| Coffee every morning | 8 | Coffee at 9am daily |
| Milk before bed | 8 | Milk 30 mins before sleep |
| Neutral | 4 | Transition between experiments |

> Note: Dates shifted forward 15 months for Amplitude free plan compatibility. Original data collected Oct–Dec 2024. All physiological values are unchanged.

---

## Key Findings

### Finding 1 — No statistically significant difference between periods

| Period | Avg Recovery | Avg HRV | Std Dev | Days |
|--------|-------------|---------|---------|------|
| Milk before bed | 56.8% | 62.4ms | 22.0 | 8 |
| Coffee every morning | 54.9% | 58.6ms | 18.2 | 8 |
| Baseline | 53.0% | 60.2ms | 18.9 | 28 |
| Neutral | 50.0% | 56.2ms | 36.7 | 4 |

The difference between best and worst period is **3.8 points.**  
Daily variation within periods is **18–22 points.**  
The signal is completely swallowed by the noise.

### Finding 2 — The Deep Sleep Paradox

Milk before bed shows:
- ✅ Highest recovery score (56.8%)
- ✅ Highest HRV (62.4ms)
- ❌ Lowest deep sleep % (18.8%)

This reveals something important about WHOOP's AI — **recovery score is driven primarily by HRV and resting heart rate, not deep sleep duration alone.** A member could have excellent recovery with less deep sleep if their nervous system is well-rested.

### Finding 3 — Sample size is the real problem

Each experiment ran for only 8 days. A proper power analysis suggests **64 days minimum** per condition to detect a meaningful effect at 80% statistical power.

---

## Product Insight

> WHOOP's AI coaching may be showing members habit recommendations before there is enough data to prove they work. Members need 64+ days of consistent habit logging — not 7 — to see statistically meaningful recovery improvement.

**Recommended metric for WHOOP's product team:**  
% of members who show statistically significant recovery improvement after 30, 60, and 90 days of consistent habit compliance.

---

## Amplitude Dashboards

### Chart 1 — Daily Recovery Score by Experiment Period
![Recovery Score Chart](charts/daily_recovery_score.png)

*Four experiment periods segmented. Baseline (blue) shows highest data density. All periods show similar average recovery with high daily variation.*

### Chart 2 — Daily HRV Trend by Experiment Period
![HRV Trend Chart](charts/daily_hrv_trend.png)

*HRV is the strongest predictor of recovery score. Milk before bed period shows marginally higher HRV (62.4ms) vs Baseline (60.2ms) — within normal daily variation.*

### Chart 3 — Deep Sleep % by Experiment Period — The Paradox
![Deep Sleep Chart](charts/deep_sleep_paradox.png)

*Milk before bed has highest recovery but lowest deep sleep. Challenges the assumption that more deep sleep always means better recovery.*

---

## AI Recommendation Engine

Each daily record receives a personalized coaching recommendation based on recovery zone, HRV, and active experiment period.

**Example outputs:**

> 🟢 *"Recovery strong at 72%. HRV 65ms indicates good nervous system readiness. Safe to take on high strain today. Milk experiment active — monitor if sleep quality improves tonight."*

> 🟡 *"Recovery moderate at 45%. HRV 58ms is within normal range. Moderate your training and prioritize sleep tonight."*

> 🔴 *"Recovery low at 31%. HRV 45ms suggests fatigue. Rest or light activity only. Coffee experiment active — note any changes in morning HRV trend."*

This mirrors the core logic of WHOOP's AI coaching feature.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python + Pandas | Data transformation + event schema creation |
| Rule-based AI engine | Personalized recovery recommendations |
| Amplitude | Feature engagement analytics + segmentation |
| WHOOP API schema | Data structured to match `/v2/recovery` endpoint |

---

## Files

```
whoop-recovery-analysis/
├── README.md
├── whoop_amplitude_prep.py     ← full pipeline code
├── whoop_amplitude_events.csv  ← transformed event data
├── data/
│   └── source.md               ← data attribution
└── charts/
    ├── daily_recovery_score.png
    ├── daily_hrv_trend.png
    └── deep_sleep_paradox.png
```

---

## What I Would Do With Real WHOOP API Access

```python
# Pull real recovery data from WHOOP API
GET https://api.prod.whoop.com/developer/v2/recovery
Headers: Authorization: Bearer {access_token}

# Returns exact fields used in this analysis:
# recovery_score, hrv_rmssd_milli, 
# resting_heart_rate, spo2_percentage,
# skin_temp_celsius, cycle_id, sleep_id
```

The Python pipeline in this repo connects directly to this schema. Swapping the Kaggle CSV for live API data requires changing one line.



