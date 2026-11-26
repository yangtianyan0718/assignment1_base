# Wind, solar and storage · Team report

**Team / track / code revision / frozen artifact IDs**

## 1. System and information boundary
Identify the real measurements and the virtual equipment. Give units, UTC splits, snapshot hash, missing-window rule and information available at issue time.

## 2. Method
Describe your track and identify the frozen partner component. Record model settings, hardware, training or request budget and elapsed time.

## 3. Experiments
Give the baseline, episode-selection rule, initial states, repeats and one ablation. For each table identify who produced the evidence.

| Forecast | Wind / solar / load MAE (MW) | EENS (MWh) | Terminal deficits (MWh, m³) | Cost (CU) |
|---|---|---|---|---|
| A0 Seasonal | | | | |
| A1 Linear | | | | |
| A2 Deep | | | | |

| Supervisor | EENS (MWh) | Terminal deficits (MWh, m³) | Cost (CU) | Requests / tokens / latency | Fallbacks |
|---|---|---|---|---|---|
| B0 Deterministic | | | | | |
| B1 Single choice | | | | | |
| B2 Full harness | | | | | |

Expand the tables with the track metrics listed in the handout. Include all runs and give the range across LLM repeats.

## 4. Evidence
Plot a labelled time series. Recompute one hour of the ledger. Examine two forecast windows or two decisions and trace one failure from input through execution.

## 5. Interpretation and contributions
Explain what changed relative to the baseline and which conclusions the simulation supports. Identify individual contributions, AI assistance and reproduction commands. Target 3-5 pages.
