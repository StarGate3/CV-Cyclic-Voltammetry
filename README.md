# CVision

![Version](https://img.shields.io/badge/version-3.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

Desktop application for **cyclic voltammetry (CV)** analysis — a Qt-based tool for importing voltammograms, selecting baselines, computing peak parameters, fitting peak shapes, calibrating currents to publication units, and exporting results to Excel.

![Screenshot](screenshot.png)

---

## Features

- **Data loading** — three-column whitespace-separated `.txt` files (E, I_ox, I_red).
- **Interactive baseline selection** — drag the blue/red baseline regions on the plot, or enter coordinates numerically via the baseline dialog.
- **Savitzky-Golay smoothing** — toggleable, with adjustable window length and polynomial order.
- **Peak parameter calculation** — x_peak, y_peak, baseline value, peak height (H) / depth (D), plotted on the chart and listed in the results table.
- **Half-wave potential E½** — automatically computed as the midpoint of the oxidation and reduction peak potentials.
- **1st and 2nd derivative analysis** — separate windows with zero-crossing detection over a user-selected range.
- **Automatic peak detection** — `scipy.signal.find_peaks` with minimum-height and minimum-distance filters; detected peaks marked as yellow circles.
- **Curve fitting** — Gaussian, Lorentzian, and asymmetric-Gaussian models via `scipy.optimize.curve_fit`; reports FWHM, amplitude, center, R², and asymmetry ratio.
- **Current calibration and unit normalization** — divide current by electrode area (cm²) and/or analyte concentration (mM) to obtain μA/cm², μA/mM, or μA/(cm²·mM); raw data is never modified.
- **Excel export** — `.xlsx` with raw data, smoothed data, derivatives, zero crossings, parameters, calibration settings, and an embedded line chart.
- **Dark / Light theme toggle** — switch instantly from the toolbar.
- **Built-in Help, Theory handbook (6 tabs), and About dialog** — practical how-to plus a theoretical reference covering CV fundamentals, baseline correction, peak parameters, derivatives, curve fitting, and unit calibration.
- **Live mouse coordinate display** — current (x, y) shown in the status bar.

---

## Installation

**Requirements:** Python 3.8+

```bash
# 1. Clone the repository
git clone https://github.com/StarGate3/CV-Cyclic-Voltammetry.git
cd CV-Cyclic-Voltammetry

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python main.py
```

---

## Input file format

CVision expects a plain-text file with **three numeric columns** separated by whitespace:

| Column | Quantity           | Typical unit |
|-------:|--------------------|--------------|
|      1 | Potential *E*      | mV           |
|      2 | Oxidation current  | μA           |
|      3 | Reduction current  | μA           |

Example:

```
-200.0   0.12    0.15
-180.0   0.18    0.14
-160.0   0.31    0.12
-140.0   0.55    0.09
-120.0   1.12    0.04
...
```

Rows are loaded with `numpy.loadtxt`; the "Utlenianie / Redukcja" combo box decides which column is treated as the primary curve. If rows are not sorted by potential they are reordered on load.

---

## Project structure

| File                      | Role                                                                                       |
|---------------------------|--------------------------------------------------------------------------------------------|
| `main.py`                 | Application entry point — creates the `QApplication` and shows the main window.             |
| `main_window.py`          | `MainWindow` class — toolbar, plot widget, signal wiring, results table, Help/Theory/About. |
| `analysis.py`             | Pure numerical functions — smoothing, baseline math, peak finding, derivatives, calibration, curve fitting. |
| `dialogs.py`              | Auxiliary `QDialog` classes — axis settings, baseline settings, peak detection, calibration, curve fitting. |
| `derivative_windows.py`   | 1st and 2nd derivative windows with interactive zero-crossing search.                       |
| `export.py`               | Excel export — pandas DataFrames + XlsxWriter embedded chart, calibration section.          |
| `utils.py`                | Small helpers (e.g. zero-crossing detection used by derivative windows).                    |

---

## Usage workflow

A typical analysis session follows these steps:

1. **Select measurement type** — choose "Utlenianie" or "Redukcja" from the combo box (this decides which column of the input file is primary).
2. **Load data** — click **"Wybierz plik z danymi"** and pick a 3-column `.txt` file.
3. **(Optional) Calibrate units** — click **"Kalibracja jednostek"**, enter electrode area and/or analyte concentration, toggle the normalization checkboxes. The Y axis and status bar update immediately.
4. **(Optional) Enable smoothing** — check **"Wygładzanie (Savitzky-Golay)"** and adjust window / polynomial order if the data is noisy.
5. **Pick the baseline** — click **"Zakres utlenienia (2× klik)"** (or "Zakres redukcji") and click twice on the **linear region to the left of the peak**. The baseline is extrapolated as a straight line under the peak. Fine-tune numerically via **"Edytuj linię bazową"** if needed.
6. **Compute peak parameters** — click **"Oblicz parametry piku"** to obtain E_peak, I_peak, baseline, H/D, and E½. Results are annotated on the plot and added to the results table.
7. **(Optional) Detect peaks automatically** — click **"Wykryj piki automatycznie"** and set minimum height / distance.
8. **(Optional) Derivative analysis** — click **"Oblicz pochodną"** or **"Oblicz drugą pochodną"** and select the search range for zero crossings.
9. **(Optional) Curve fitting** — click **"Dopasowanie krzywej"**, pick a model (Gaussian / Lorentzian / Asymmetric Gaussian), confirm the range, and press **"Dopasuj"**. Review FWHM and R², then **"Dodaj do tabeli wyników"** to persist.
10. **Export** — click **"Eksport do Excela"** to save raw data, smoothed data, derivatives, zero crossings, peak parameters, the calibration block, and an embedded chart into a single `.xlsx` file.

For background theory on any of the above, open the **"Teoria"** dialog from the toolbar.

---

## Author and License

- **Author:** [Author Name]
- **License:** [License]
