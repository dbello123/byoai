# BYOAI Governance Model: Sensitivity Analysis

Companion code for *"Governing Bring Your Own AI: A Parameterized Maturity Model."*

`sensitivity.py` shows that the monotonic trends in the Framework Gap Index (FGI)
and the Composite Governance Score (CGS) across the five-level maturity ladder
are structural, not artifacts of one parameter choice.

## Run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 sensitivity.py
```

The baseline (alpha = 0.25, weights 0.40/0.30/0.30) reproduces the published
endpoints: FGI 0.77 -> 0.08 and CGS 1.3 -> 4.3. The script then sweeps alpha and
the weight vectors and confirms the direction holds for every combination.
