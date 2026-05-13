import numpy as np


def _metrics(experimental: np.ndarray, candidate: np.ndarray) -> dict:
    """Compute all fit metrics between two arrays of equal length."""
    if experimental.shape != candidate.shape:
        raise ValueError(
            f"Length mismatch: experimental has {len(experimental)} elements, "
            f"candidate has {len(candidate)}"
        )
    residuals = experimental - candidate
    ssr  = float(np.sum(residuals ** 2))
    mse  = float(np.mean(residuals ** 2))
    rmse = float(np.sqrt(mse))
    mae  = float(np.mean(np.abs(residuals)))
    ss_tot = float(np.sum((experimental - np.mean(experimental)) ** 2))
    r2   = 1.0 - ssr / ss_tot if ss_tot != 0 else float("nan")
    return dict(ssr=ssr, rmse=rmse, mae=mae, r2=r2,
                residuals=residuals, max_abs_res=float(np.max(np.abs(residuals))))


def _print_report(exp_arr: np.ndarray, candidates: tuple, all_metrics: list, best_idx: int) -> None:
    """Print a verbose project-report-style summary."""
    n = len(exp_arr)
    W = 68

    print("=" * W)
    print("  LEAST SQUARES FIT REPORT")
    print("=" * W)

    # Dataset summary
    print(f"\n  Data points used : {n}  (experimental origin point excluded)")
    print(f"  Experimental range: [{exp_arr.min():.4f}, {exp_arr.max():.4f}]")

    # Ranking table
    ranked = sorted(range(len(candidates)), key=lambda i: all_metrics[i]["ssr"])
    best_ssr = all_metrics[best_idx]["ssr"]

    print(f"\n{'─' * W}")
    print(f"  {'Rank':<6} {'Candidate':<14} {'SSR':>10} {'RMSE':>10} "
          f"{'MAE':>10} {'R²':>10} {'Rel. SSR':>10}")
    print(f"{'─' * W}")

    for rank, i in enumerate(ranked, start=1):
        m = all_metrics[i]
        rel = m["ssr"] / best_ssr
        marker = "  ◄ best" if i == best_idx else ""
        print(f"  {rank:<6} {'Candidate ' + str(i):<14} {m['ssr']:>10.4f} "
              f"{m['rmse']:>10.4f} {m['mae']:>10.4f} {m['r2']:>10.4f} "
              f"{rel:>10.2f}x{marker}")

    # Residual detail for best fit
    m = all_metrics[best_idx]
    print(f"\n{'─' * W}")
    print(f"  RESIDUALS — Candidate {best_idx} (best fit)")
    print(f"{'─' * W}")
    print(f"  {'Index':<8} {'Experimental':>14} {'Candidate':>14} {'Residual':>12}")
    print(f"  {'─'*50}")
    for i, (exp_val, res) in enumerate(zip(exp_arr, m["residuals"])):
        cand_val = exp_val - res
        print(f"  {i:<8} {exp_val:>14.4f} {cand_val:>14.4f} {res:>12.4f}")
    print(f"\n  Max absolute residual : {m['max_abs_res']:.4f}")
    print("=" * W)


# ── public API ────────────────────────────────────────────────────────────────

def best_fit(experimental: list, *candidates: list, verbose: bool = True) -> int:
    """
    Return the index of the candidate list that best fits the experimental
    data using the least squares method (lowest Sum of Squared Residuals).

    Parameters
    ----------
    experimental : list
        The reference / experimental data. The first element is treated as
        an artificial origin point and is excluded from the comparison.
    *candidates : list
        One or more candidate lists to compare against. Each must have the
        same length as experimental[1:].
    verbose : bool, optional
        If True, print a full report including ranking, per-candidate metrics,
        and a residuals table for the best fit. Default is False.

    Returns
    -------
    int
        The 0-based index of the candidate with the lowest SSR.
        (0 = first candidate, 1 = second, etc.)

    Raises
    ------
    ValueError
        If no candidates are provided, or if any candidate has a different
        length from experimental[1:].

    Example
    -------
    >>> best_fit(exp, model_a, model_b, verbose=True)
    """
    if not candidates:
        raise ValueError("At least one candidate list must be provided.")

    # Drop the first element — it is an artificially added origin point
    exp_arr = np.array(experimental[1:], dtype=float)
    all_metrics = [_metrics(exp_arr, np.array(c, dtype=float)) for c in candidates]
    best_idx = min(range(len(candidates)), key=lambda i: all_metrics[i]["ssr"])

    if verbose:
        _print_report(exp_arr, candidates, all_metrics, best_idx)

    return best_idx


