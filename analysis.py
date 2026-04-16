"""Pure numerical functions for CV peak analysis: smoothing, baseline evaluation, peak finding, and derivatives."""

import numpy as np
from scipy.signal import savgol_filter


def apply_smoothing(raw_y, window_length, polyorder):
    """Apply Savitzky-Golay filter; auto-corrects window_length to satisfy scipy constraints."""
    if window_length % 2 == 0:
        window_length += 1
    if window_length > len(raw_y):
        window_length = len(raw_y) if len(raw_y) % 2 == 1 else len(raw_y) - 1
    if window_length <= polyorder:
        window_length = polyorder + 1
        if window_length % 2 == 0:
            window_length += 1
    return savgol_filter(raw_y, window_length, polyorder)


def compute_baseline_value(x_point, x1, y1, x2, y2):
    """Return the y value of the linear baseline at x_point."""
    if x2 != x1:
        return y1 + (y2 - y1) * (x_point - x1) / (x2 - x1)
    return float(y1)


def compute_baseline_curve(x_region, x1, y1, x2, y2):
    """Return baseline y values over x_region via linear interpolation between (x1,y1) and (x2,y2)."""
    if x2 != x1:
        return y1 + (y2 - y1) * (x_region - x1) / (x2 - x1)
    return np.full_like(x_region, float(y1))


def compute_oxidation_peak(x, y_ox, ox_settings):
    """
    Find the oxidation (maximum) peak within the baseline region.

    Returns a dict with x_peak, y_peak, baseline_val, height, x_region,
    peak_height_curve, and summary string — or None if no data falls in the region.
    """
    x1, y1_b = ox_settings['x1'], ox_settings['y1']
    x2, y2_b = ox_settings['x2'], ox_settings['y2']
    mask = (x >= min(x1, x2)) & (x <= max(x1, x2))
    if not np.any(mask):
        return None
    x_region = x[mask]
    y_region = y_ox[mask]
    idx_peak = np.argmax(y_region)
    x_peak = float(x_region[idx_peak])
    y_peak = float(y_region[idx_peak])
    baseline_val = compute_baseline_value(x_peak, x1, y1_b, x2, y2_b)
    height = y_peak - baseline_val
    baseline_curve = compute_baseline_curve(x_region, x1, y1_b, x2, y2_b)
    peak_height_curve = y_region - baseline_curve
    return {
        'x_peak': x_peak,
        'y_peak': y_peak,
        'baseline_val': baseline_val,
        'height': height,
        'x_region': x_region,
        'peak_height_curve': peak_height_curve,
        'summary': (
            f"Utlenienie: x_peak={x_peak:.3f}, y_peak={y_peak:.3f}, "
            f"baseline={baseline_val:.3f}, height={height:.3f}\n"
        ),
    }


def compute_reduction_peak(x, y_red, red_settings):
    """
    Find the reduction (minimum) peak within the baseline region.

    Returns a dict with x_peak, y_peak, baseline_val, depth, x_region,
    peak_height_curve, and summary string — or None if no data falls in the region.
    """
    x1, y1_b = red_settings['x1'], red_settings['y1']
    x2, y2_b = red_settings['x2'], red_settings['y2']
    mask = (x >= min(x1, x2)) & (x <= max(x1, x2))
    if not np.any(mask):
        return None
    x_region = x[mask]
    y_region = y_red[mask]
    idx_peak = np.argmin(y_region)
    x_peak = float(x_region[idx_peak])
    y_peak = float(y_region[idx_peak])
    baseline_val = compute_baseline_value(x_peak, x1, y1_b, x2, y2_b)
    depth = baseline_val - y_peak
    baseline_curve = compute_baseline_curve(x_region, x1, y1_b, x2, y2_b)
    peak_height_curve = y_red[mask] - baseline_curve
    return {
        'x_peak': x_peak,
        'y_peak': y_peak,
        'baseline_val': baseline_val,
        'depth': depth,
        'x_region': x_region,
        'peak_height_curve': peak_height_curve,
        'summary': (
            f"Redukcja: x_peak={x_peak:.3f}, y_peak={y_peak:.3f}, "
            f"baseline={baseline_val:.3f}, depth={depth:.3f}\n"
        ),
    }


def compute_e_half(x_ox_peak, x_red_peak):
    """Return the half-wave potential E½ as the midpoint of the two peak x-positions."""
    return (x_ox_peak + x_red_peak) / 2.0


def compute_derivatives(x, y1, y2):
    """Return first numerical derivatives of y1 and y2 with respect to x."""
    return np.gradient(y1, x), np.gradient(y2, x)


def compute_second_derivatives(x, y1, y2):
    """Return second numerical derivatives of y1 and y2 with respect to x."""
    d1, d2 = compute_derivatives(x, y1, y2)
    return np.gradient(d1, x), np.gradient(d2, x)
