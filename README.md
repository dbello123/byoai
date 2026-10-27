# BYOAI: Governance Model Code and Review Data

Supporting materials for *"Governing Bring Your Own AI: A Parameterized Maturity Model."*

| File | What it is |
|---|---|
| `sensitivity.py` | Sensitivity analysis for the parameterized governance model |
| `data/CARS_IEEE_Paper_Reported_Results.xlsx` | Literature-review coding behind the paper's reported results |
| `requirements.txt` | Python dependencies (numpy) |

## Sensitivity analysis

`sensitivity.py` shows that the monotonic trends in the Framework Gap Index (FGI)
and the Composite Governance Score (CGS) across the five-level maturity ladder
are structural, not artifacts of one parameter choice.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 sensitivity.py
```

The baseline (alpha = 0.25, weights 0.40/0.30/0.30) reproduces the published
endpoints: FGI 0.77 -> 0.08 and CGS 1.3 -> 4.3. The script then sweeps alpha and
the weight vectors and confirms the direction holds for every combination.

## Literature-review results

`data/CARS_IEEE_Paper_Reported_Results.xlsx` has three sheets:

- **Paper results**: the counts reported in Tables I and II. Risk categories are
  out of 24 studies and framework families out of 30. A study can fall under more
  than one category.
- **References**: each cited source with its title, citation, link, source type,
  assigned risk categories and frameworks, review status and the material reviewed
  (full text, abstract only, and so on).
- **Category index**: one row per source and category, for tracing each count back
  to the studies behind it.

**Status:** the totals follow the paper. Paper-by-paper coding has not been fully
verified. Rows marked "Review needed" or "To confirm" are still being checked.
