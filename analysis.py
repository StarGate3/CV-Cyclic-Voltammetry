"""Pure numerical functions for CV peak analysis: smoothing, baseline evaluation, peak finding, and derivatives."""

from dataclasses import dataclass

import numpy as np
from scipy.signal import savgol_filter, find_peaks
from scipy.optimize import curve_fit


@dataclass
class CalibrationSettings:
    """User-configured current calibration: electrode area and analyte concentration normalization."""
    electrode_area: float = 1.0
    concentration: float = 1.0
    normalize_by_area: bool = False
    normalize_by_concentration: bool = False


def apply_calibration(y, settings):
    """Normalize a current array by electrode area and/or concentration.

    Returns (calibrated_y, unit_label). The input array is never modified in place.
    """
    divisor = 1.0
    if settings.normalize_by_area:
        divisor *= settings.electrode_area
    if settings.normalize_by_concentration:
        divisor *= settings.concentration

    calibrated = y / divisor if divisor != 1.0 else y.copy()

    if settings.normalize_by_area and settings.normalize_by_concentration:
        unit_label = "μA/(cm²·mM)"
    elif settings.normalize_by_area:
        unit_label = "μA/cm²"
    elif settings.normalize_by_concentration:
        unit_label = "μA/mM"
    else:
        unit_label = "μA"
    return calibrated, unit_label


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


def detect_peaks(x, y, mode, min_height=None, min_distance=None):
    """
    Detect peaks in y using scipy.signal.find_peaks.

    mode='oxidation': detects local maxima.
    mode='reduction': detects local minima (find_peaks on -y).
    min_height: minimum peak amplitude (absolute value); None disables filtering.
    min_distance: minimum separation between peaks in data points; None disables filtering.

    Returns list of dicts [{'x': float, 'y': float, 'height': float}, ...].
    """
    kwargs = {}
    if min_height is not None:
        kwargs['height'] = min_height
    if min_distance is not None:
        kwargs['distance'] = min_distance

    if mode == 'oxidation':
        indices, _ = find_peaks(y, **kwargs)
        return [{'x': float(x[i]), 'y': float(y[i]), 'height': float(y[i])} for i in indices]
    else:
        indices, _ = find_peaks(-y, **kwargs)
        return [{'x': float(x[i]), 'y': float(y[i]), 'height': float(-y[i])} for i in indices]


def gaussian(x, amplitude, center, sigma):
    """Symmetric Gaussian peak."""
    return amplitude * np.exp(-((x - center) ** 2) / (2.0 * sigma ** 2))


def lorentzian(x, amplitude, center, gamma):
    """Lorentzian (Cauchy) peak with half-width-at-half-maximum gamma."""
    return amplitude * (gamma ** 2 / ((x - center) ** 2 + gamma ** 2))


def asymmetric_gaussian(x, amplitude, center, sigma_left, sigma_right):
    """Gaussian with different widths on either side of the center."""
    sigma = np.where(x < center, sigma_left, sigma_right)
    return amplitude * np.exp(-((x - center) ** 2) / (2.0 * sigma ** 2))


def _empty_fit_result(error):
    return {
        'params': None, 'fwhm': None, 'asymmetry': None,
        'r_squared': None, 'x_fit': None, 'y_fit': None,
        'error': error,
    }


def fit_peak(x, y, model='gaussian', x_min=None, x_max=None):
    """
    Fit a peak-shape model to (x, y) after cropping to [x_min, x_max] and removing
    a linear baseline between the endpoints of the cropped range.

    model: 'gaussian', 'lorentzian', or 'asymmetric_gaussian'.
    Returns a dict with params, fwhm, asymmetry, r_squared, x_fit, y_fit, error.
    Never raises — failures come back in the 'error' field.
    """
    if x_min is None:
        x_min = float(np.min(x))
    if x_max is None:
        x_max = float(np.max(x))
    if x_min > x_max:
        x_min, x_max = x_max, x_min

    mask = (x >= x_min) & (x <= x_max)
    x_crop = np.asarray(x[mask], dtype=float)
    y_crop = np.asarray(y[mask], dtype=float)

    if len(x_crop) < 5:
        return _empty_fit_result("Zbyt mało punktów danych w wybranym zakresie (minimum 5).")

    # Detrend: subtract the straight line between the first and last points of the crop.
    if x_crop[-1] != x_crop[0]:
        slope = (y_crop[-1] - y_crop[0]) / (x_crop[-1] - x_crop[0])
    else:
        slope = 0.0
    intercept = y_crop[0] - slope * x_crop[0]
    baseline_crop = slope * x_crop + intercept
    y_det = y_crop - baseline_crop

    # Initial guesses
    abs_y = np.abs(y_det)
    idx_peak = int(np.argmax(abs_y))
    amp0 = float(y_det[idx_peak])
    if amp0 == 0.0:
        amp0 = float(np.max(abs_y)) or 1.0
    center0 = float(x_crop[idx_peak])
    width0 = (x_max - x_min) / 4.0 or 1.0

    try:
        if model == 'gaussian':
            popt, _ = curve_fit(gaussian, x_crop, y_det, p0=[amp0, center0, width0])
            amplitude, center, sigma = (float(v) for v in popt)
            fwhm = 2.0 * np.sqrt(2.0 * np.log(2.0)) * abs(sigma)
            asymmetry = None
            params = {'amplitude': amplitude, 'center': center, 'sigma': sigma}
            model_fn = gaussian
        elif model == 'lorentzian':
            popt, _ = curve_fit(lorentzian, x_crop, y_det, p0=[amp0, center0, width0])
            amplitude, center, gamma = (float(v) for v in popt)
            fwhm = 2.0 * abs(gamma)
            asymmetry = None
            params = {'amplitude': amplitude, 'center': center, 'gamma': gamma}
            model_fn = lorentzian
        elif model == 'asymmetric_gaussian':
            popt, _ = curve_fit(
                asymmetric_gaussian, x_crop, y_det,
                p0=[amp0, center0, width0, width0],
            )
            amplitude, center, sigma_left, sigma_right = (float(v) for v in popt)
            fwhm = np.sqrt(2.0 * np.log(2.0)) * (abs(sigma_left) + abs(sigma_right))
            asymmetry = abs(sigma_right) / abs(sigma_left) if sigma_left != 0 else None
            params = {
                'amplitude': amplitude, 'center': center,
                'sigma_left': sigma_left, 'sigma_right': sigma_right,
            }
            model_fn = asymmetric_gaussian
        else:
            return _empty_fit_result(f"Nieznany model: {model}")
    except Exception as exc:
        return _empty_fit_result(str(exc))

    y_model = model_fn(x_crop, *popt)
    ss_res = float(np.sum((y_det - y_model) ** 2))
    ss_tot = float(np.sum((y_det - np.mean(y_det)) ** 2))
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

    x_fit = np.linspace(float(x_crop[0]), float(x_crop[-1]), 500)
    y_fit = model_fn(x_fit, *popt) + (slope * x_fit + intercept)

    return {
        'params': params,
        'fwhm': float(fwhm),
        'asymmetry': float(asymmetry) if asymmetry is not None else None,
        'r_squared': float(r_squared),
        'x_fit': x_fit,
        'y_fit': y_fit,
        'error': None,
    }
