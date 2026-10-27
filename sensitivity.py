#!/usr/bin/env python3
"""
Sensitivity analysis for the BYOAI parameterized governance model.

Companion to: "Governing Bring Your Own AI: A Parameterized Maturity Model."
Demonstrates that the monotonic trends in FGI and CGS across the five-level
maturity ladder are structural, not artifacts of a single parameter choice.

The model uses the enforceability form of the Framework Gap Index:
    FGI0     = 1 - alpha * (covered_nominal / total)          (Eq. 2, alpha = 0.25)
    FGI(l)   = FGI0 * (1 - 0.90 * TCCS(l))                    (Eq. 3)
    C(l)     = 1 - FGI(l)
    R(l)     = mean fractional reduction across three outcome axes
    T(l)     = TCCS(l)
    CGS(l)   = 1 + 4 * (w1*R + w2*C + w3*T)                   (Eq. 4)

Baseline parameters (alpha = 0.25, weights = 0.40/0.30/0.30) reproduce the
published endpoints: FGI 0.77 -> 0.08, CGS 1.3 -> 4.3.

Run:  python3 sensitivity.py
"""

import numpy as np

# ---------------------------------------------------------------------------
# Fixed model inputs (from the maturity mapping, Table III, and outcome axes)
# ---------------------------------------------------------------------------

# Technical Control Coverage Score by level.
# Seven canonical families (DSPM, CASB, DLP, SSPM, IAM, CIEM, SWG); the count
# active at each level is 0, 1, 3, 6, 7  ->  TCCS = count / 7.
TCCS = np.array([0.00, 1/7, 3/7, 6/7, 7/7])   # 0, .14, .43, .86, 1.00

# Normalized security-outcome residuals per level (lower = better).
# Axes: exfiltration risk, detection-latency index, attack-surface breadth.
EXFIL   = np.array([1.00, 0.90, 0.506, 0.346, 0.329])
LATENCY = np.array([1.00, 0.80, 0.612, 0.419, 0.398])
SURFACE = np.array([1.00, 0.90, 0.769, 0.442, 0.353])

# R = mean fractional risk reduction across the three axes.
RESID = (EXFIL + LATENCY + SURFACE) / 3.0
R = 1.0 - RESID

# Nominal coverage ratio: chosen so that FGI0 = 0.77 at the baseline alpha=0.25,
# i.e. covered_nominal/total = (1 - 0.77) / 0.25.
COV_RATIO = (1.0 - 0.77) / 0.25            # ~= 0.92

LEVELS = ["L1", "L2", "L3", "L4", "L5"]


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

def fgi(alpha):
    """Residual Framework Gap Index across the five levels for a given alpha."""
    fgi0 = 1.0 - alpha * COV_RATIO
    return fgi0 * (1.0 - 0.90 * TCCS)

def cgs(alpha, w):
    """Composite Governance Score across the five levels for alpha and weights w."""
    C = 1.0 - fgi(alpha)
    T = TCCS
    w1, w2, w3 = w
    return 1.0 + 4.0 * (w1 * R + w2 * C + w3 * T)


# ---------------------------------------------------------------------------
# Sweep configuration
# ---------------------------------------------------------------------------

ALPHAS = [0.15, 0.20, 0.25, 0.30, 0.40]

# Weight vectors on the valid simplex (non-negative, sum to 1):
# baseline plus the three single-axis-heavy extremes and an equal split.
WEIGHT_SETS = {
    "baseline (.40,.30,.30)": (0.40, 0.30, 0.30),
    "R-heavy  (.60,.20,.20)": (0.60, 0.20, 0.20),
    "C-heavy  (.20,.60,.20)": (0.20, 0.60, 0.20),
    "T-heavy  (.20,.20,.60)": (0.20, 0.20, 0.60),
    "equal    (.34,.33,.33)": (0.34, 0.33, 0.33),
}


def _fmt(row, nd):
    return "  ".join(f"{v:.{nd}f}" for v in row)


def main():
    # ---- Baseline reproduction check -------------------------------------
    w0 = WEIGHT_SETS["baseline (.40,.30,.30)"]
    print("=" * 62)
    print("BASELINE CHECK  (alpha=0.25, weights=0.40/0.30/0.30)")
    print("Expected from paper:  FGI 0.77 -> 0.08 ;  CGS 1.3 -> 4.3")
    print("-" * 62)
    print(f"  levels : {'  '.join(LEVELS)}")
    print(f"  TCCS   : {_fmt(TCCS, 2)}")
    print(f"  R      : {_fmt(R, 3)}")
    print(f"  FGI    : {_fmt(fgi(0.25), 3)}")
    print(f"  CGS    : {_fmt(cgs(0.25, w0), 2)}")
    print()

    # ---- FGI envelope over alpha -----------------------------------------
    fgi_stack = np.array([fgi(a) for a in ALPHAS])
    fgi_mono = all(np.all(np.diff(fgi(a)) < 0) for a in ALPHAS)

    print("=" * 62)
    print(f"FGI ENVELOPE  over alpha in {ALPHAS}")
    print("-" * 62)
    print(f"  levels : {'  '.join(LEVELS)}")
    print(f"  min    : {_fmt(fgi_stack.min(0), 2)}")
    print(f"  max    : {_fmt(fgi_stack.max(0), 2)}")
    print(f"  monotonically decreasing for every alpha : {fgi_mono}")
    print()

    # ---- CGS envelope over alpha x weight sets ---------------------------
    cgs_rows = [cgs(a, w) for a in ALPHAS for w in WEIGHT_SETS.values()]
    cgs_stack = np.array(cgs_rows)
    cgs_mono = all(np.all(np.diff(c) > 0) for c in cgs_stack)

    print("=" * 62)
    print(f"CGS ENVELOPE  over alpha x {len(WEIGHT_SETS)} weight vectors")
    print("-" * 62)
    print(f"  levels : {'  '.join(LEVELS)}")
    print(f"  min    : {_fmt(cgs_stack.min(0), 2)}")
    print(f"  max    : {_fmt(cgs_stack.max(0), 2)}")
    print(f"  monotonically increasing for every combination : {cgs_mono}")
    print()

    # ---- One-line verdict ------------------------------------------------
    print("=" * 62)
    verdict = ("INVARIANT: direction holds across all sampled parameters; "
               "only magnitude varies.") if (fgi_mono and cgs_mono) else \
              ("WARNING: a monotonic trend broke under some parameter set.")
    print(verdict)
    print("=" * 62)


if __name__ == "__main__":
    main()
