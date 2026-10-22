from pathlib import Path
import sys
import pandas as pd
import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "student-mat.csv"
INTERIM = ROOT / "data" / "interim"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

def cohens_d(a, b):
    """Cohen's d using pooled standard deviation."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    pooled_var = (((len(a) - 1) * np.var(a, ddof=1)) +
                  ((len(b) - 1) * np.var(b, ddof=1))) / (len(a) + len(b) - 2)
    if pooled_var <= 0:
        return float("nan")
    return (np.mean(a) - np.mean(b)) / np.sqrt(pooled_var)

def load_and_prepare(path=RAW):
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}\nDownload student-mat.csv from "
            "https://archive.ics.uci.edu/dataset/320/student+performance "
            "and place it in data/raw/."
        )
    # UCI Student Performance CSV uses semicolon-separated columns.
    df = pd.read_csv(path, sep=";")
    required = {"studytime", "G3"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    INTERIM.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(INTERIM / "loaded_data.csv", index=False)

    out = df[["studytime", "G3"]].copy()
    out["studytime"] = pd.to_numeric(out["studytime"], errors="coerce")
    out["G3"] = pd.to_numeric(out["G3"], errors="coerce")
    out = out.dropna(subset=["studytime", "G3"])
    out = out[out["studytime"].isin([1, 2, 3, 4])].copy()
    out["study_group"] = np.where(out["studytime"].isin([3, 4]), "higher", "lower")
    out.to_csv(PROCESSED / "analysis_data.csv", index=False)
    return out

def summarize(series):
    return {
        "n": int(series.count()),
        "mean": float(series.mean()),
        "sd": float(series.std(ddof=1)) if series.count() > 1 else float("nan"),
        "median": float(series.median()),
        "q1": float(series.quantile(0.25)),
        "q3": float(series.quantile(0.75)),
    }

def run_analysis(df):
    higher = df.loc[df["study_group"] == "higher", "G3"]
    lower = df.loc[df["study_group"] == "lower", "G3"]
    if len(higher) < 2 or len(lower) < 2:
        raise ValueError("Each group needs at least two records for the planned test.")
    test = stats.ttest_ind(higher, lower, equal_var=False, alternative="two-sided")
    diff = float(higher.mean() - lower.mean())
    d = cohens_d(higher, lower)

    # Sensitivity analysis excluding final grade zero.
    nonzero = df[df["G3"] != 0]
    hi_nz = nonzero.loc[nonzero["study_group"] == "higher", "G3"]
    lo_nz = nonzero.loc[nonzero["study_group"] == "lower", "G3"]
    if len(hi_nz) >= 2 and len(lo_nz) >= 2:
        sensitivity = stats.ttest_ind(hi_nz, lo_nz, equal_var=False, alternative="two-sided")
        sensitivity_text = (
            f"Non-zero G3 sensitivity: higher n={len(hi_nz)}, lower n={len(lo_nz)}, "
            f"mean difference={hi_nz.mean()-lo_nz.mean():.3f}, p={sensitivity.pvalue:.6g}"
        )
    else:
        sensitivity_text = "Non-zero G3 sensitivity not run: one group had fewer than two records."

    hs, ls = summarize(higher), summarize(lower)
    lines = [
        "Study Time and Final Mathematics Grade — Analysis Report",
        "NOTE: Results are observational associations, not proof of causation.",
        "",
        f"Rows in analysis dataset: {len(df)}",
        f"Higher study-time group (categories 3–4): n={hs['n']}, mean={hs['mean']:.3f}, "
        f"SD={hs['sd']:.3f}, median={hs['median']:.3f}, IQR={hs['q1']:.3f}–{hs['q3']:.3f}",
        f"Lower study-time group (categories 1–2): n={ls['n']}, mean={ls['mean']:.3f}, "
        f"SD={ls['sd']:.3f}, median={ls['median']:.3f}, IQR={ls['q1']:.3f}–{ls['q3']:.3f}",
        f"Mean difference (higher minus lower): {diff:.3f}",
        f"Welch two-sided t-test p-value: {test.pvalue:.6g}",
        f"Cohen's d: {d:.3f}",
        sensitivity_text,
        "",
        "Interpretation guide: compare the observed p-value with the preregistered 0.05 threshold. "
        "Report group summaries and effect size regardless of significance. Do not claim causation.",
    ]
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "analysis_report.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))

if __name__ == "__main__":
    try:
        data = load_and_prepare()
        run_analysis(data)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
