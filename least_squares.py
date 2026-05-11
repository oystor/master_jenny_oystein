"""
least_squares_fit.py
────────────────────
Public API — one function:

    best_fit(experimental, *candidates) -> list

Example
-------
    from least_squares_fit import best_fit

    exp   = [1.0, 2.1, 2.9, 4.2, 5.0]
    list1 = [1.1, 2.0, 3.1, 4.0, 5.2]
    list2 = [0.8, 1.9, 3.3, 4.5, 5.5]
    list3 = [1.0, 2.0, 3.0, 4.0, 5.0]

    result = best_fit(exp, list1, list2, list3)
    # → returns list3 (lowest sum of squared residuals)
"""

import numpy as np


# ── private helper ────────────────────────────────────────────────────────────

def _ssr(experimental: np.ndarray, candidate: np.ndarray) -> float:
    """Return the Sum of Squared Residuals between two arrays."""
    if experimental.shape != candidate.shape:
        raise ValueError(
            f"Length mismatch: experimental has {len(experimental)} elements, "
            f"candidate has {len(candidate)}"
        )
    return float(np.sum((experimental - candidate) ** 2))


# ── public API ────────────────────────────────────────────────────────────────

def best_fit(experimental: list, *candidates: list) -> list:
    """
    Return the candidate list that best fits the experimental data
    using the least squares method (lowest Sum of Squared Residuals).

    Parameters
    ----------
    experimental : list
        The reference / experimental data as a flat Python list of numbers.
    *candidates : list
        One or more candidate lists to compare against. Each must have
        the same length as `experimental`.

    Returns
    -------
    int
        The index of the candidate list with the lowest SSR (best fit).
        0-based, so 0 = first candidate, 1 = second, etc.

    Raises
    ------
    ValueError
        If no candidates are provided, or if any candidate has a different
        length from `experimental`.

    Example
    -------
    >>> result = best_fit(exp_data, model_a, model_b, model_c)
    """
    if not candidates:
        raise ValueError("At least one candidate list must be provided.")

    # Drop the first element — it is an artificially added origin point
    exp_arr = np.array(experimental[1:], dtype=float)
    return min(range(len(candidates)), key=lambda i: _ssr(exp_arr, np.array(candidates[i], dtype=float)))


