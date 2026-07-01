"""
Moduł translations.py
----------------------
Słowniki tłumaczeń UI (PL/EN) oraz wspólny mechanizm tłumaczenia dla całego programu
(główne okno i dialogi). Etap 0: klucze toolbara (trzy rzędy, w tym Help/Teoria/About jako
zwykłe przyciski), obu combo (motyw, pomiar) i tytułu okna. Etap 1a: etykiety Okno/Stopień,
nagłówki tabeli wyników, tytuł wykresu i domyślne etykiety osi. Etap 1b-1: proste dialogi
(PeakDetectionDialog, AxisSettingsDialog, okna pochodnych). Kolejne etapy dołożą resztę
kluczy (pozostałe dialogi, komunikaty błędów, treść Help/Teoria/About).

Mechanizm bieżącego języka: MainWindow trzyma swój własny `self.current_language` (bo
retranslate_ui() go potrzebuje), ale dialogi to osobne klasy bez dostępu do MainWindow —
nie mogą wołać `self.tr_`. Dlatego bieżący język jest też trzymany tu, modułowo
(`_current_language`), aktualizowany przez `set_language()` w tych samych miejscach, gdzie
zmienia się `self.current_language` w main_window.py. Dialogi wołają `tr(key)` przy budowie
UI i odczytują ten sam, aktualny język — jedno źródło prawdy, zsynchronizowane przez
`set_language()`.
"""

TRANSLATIONS = {
    "pl": {
        "window_title": "CVision: Analiza woltamogramu cyklicznego",

        "btn_open_file": "Wybierz plik z danymi",
        "btn_baseline_edit": "Edytuj linię bazową (numerycznie)",
        "btn_clear": "Wyczyść wykres",
        "btn_axis_settings": "Edytuj ustawienia osi",
        "btn_calibration": "Kalibracja jednostek",
        "btn_export": "Eksport do Excela",
        "btn_help": "Help",
        "btn_theory": "Teoria",
        "btn_about": "About",

        "btn_pick_ox": "Zakres utlenienia (2x klik)",
        "btn_pick_red": "Zakres redukcji (2x klik)",
        "btn_compute_peak": "Oblicz parametry piku",
        "btn_auto_peaks": "Wykryj piki automatycznie",
        "btn_derivative": "Oblicz pochodną",
        "btn_second_deriv": "Oblicz drugą pochodną",
        "btn_curve_fit": "Dopasowanie krzywej",
        "check_smoothing": "Wygładzanie (Savitzky-Golay)",

        "combo_oxidation": "Utlenianie",
        "combo_reduction": "Redukcja",

        "combo_theme_dark": "Ciemny",
        "combo_theme_light": "Jasny",

        "label_language": "Język",

        "label_window": "Okno:",
        "label_polyorder": "Stopień:",
        "plot_title": "Woltamogram",
        "axis_x": "E [mV]",
        "axis_y_current": "Prąd",

        "col_type": "Typ",
        "col_xpeak": "x_peak",
        "col_ypeak": "y_peak",
        "col_baseline": "Baseline",
        "col_hd": "H/D",

        "dlg_peakdet_title": "Automatyczne wykrywanie pików",
        "lbl_min_height": "Minimalna wysokość piku:",
        "lbl_min_distance": "Minimalna odległość między pikami:",
        "suffix_datapoints": " punktów danych",
        "chk_detect_ox": "Zakres utlenienia",
        "chk_detect_red": "Zakres redukcji",

        "dlg_axis_title": "Ustawienia osi",
        "lbl_axis_x_label": "Etykieta osi X:",
        "lbl_axis_y_label": "Etykieta osi Y:",
        "lbl_axis_x_range": "Zakres osi X:",
        "lbl_axis_y_range": "Zakres osi Y:",
        "lbl_font": "Czcionka:",
        "lbl_min": "Min:",
        "lbl_max": "Max:",
        "btn_choose_font": "Wybierz czcionkę",
        "axis_default_x": "Oś X",
        "axis_default_y": "Wartości",

        "dlg_deriv_title": "Pochodne utlenienia i redukcji",
        "dlg_deriv2_title": "Druga pochodna utlenienia i redukcji",
        "plot_deriv_title": "Wykres pochodnych",
        "plot_deriv2_title": "Wykres drugiej pochodnej",
        "legend_deriv_ox": "Pochodna utleniania",
        "legend_deriv_red": "Pochodna redukcji",
        "legend_deriv2_ox": "Druga pochodna utleniania",
        "legend_deriv2_red": "Druga pochodna redukcji",
        "lbl_zero_range_from": "Zakres miejsc zerowych od:",
        "lbl_zero_range_to": "do:",
        "btn_find_zeros": "Znajdź miejsca zerowe",

        "dlg_baseline_title": "Ustawienia linii bazowej (numerycznie)",
        "lbl_oxidation": "Utlenienie:",
        "lbl_reduction": "Redukcja:",
        "baseline_preview_uninit": "Podgląd wartości: Punkty nie są jeszcze zainicjalizowane",

        "dlg_calibration_title": "Kalibracja jednostek",
        "lbl_electrode_area": "Powierzchnia elektrody [cm²]:",
        "lbl_analyte_conc": "Stężenie analitu [mM]:",
        "chk_normalize_area": "Normalizuj względem powierzchni elektrody",
        "chk_normalize_conc": "Normalizuj względem stężenia",
        "btn_cancel": "Anuluj",
        "btn_reset": "Resetuj",
        "lbl_unit_result": "Jednostka wynikowa:",

        "dlg_curvefit_title": "Dopasowanie krzywej",
        "lbl_model": "Model:",
        "lbl_curve": "Krzywa:",
        "lbl_xrange_from": "Zakres X — od:",
        "lbl_xrange_to": "Zakres X — do:",
        "model_gaussian": "Gaussowski",
        "model_lorentzian": "Lorentzowski",
        "model_asym_gaussian": "Asymetryczny Gaussowski",
        "btn_fit": "Dopasuj",
        "grp_results": "Wyniki",
        "lbl_fwhm": "FWHM:",
        "lbl_peak_center": "Centrum piku:",
        "lbl_amplitude": "Amplituda:",
        "lbl_asymmetry": "Asymetria:",
        "lbl_r_squared": "R²:",
        "lbl_fwhm_unit": "Jednostka FWHM:",
        "btn_add_to_results": "Dodaj do tabeli wyników",
        "btn_close": "Zamknij",
        "legend_fit": "Dopasowanie",
    },
    "en": {
        "window_title": "CVision: Cyclic Voltammogram Analysis",

        "btn_open_file": "Open data file",
        "btn_baseline_edit": "Edit baseline (numeric)",
        "btn_clear": "Clear plot",
        "btn_axis_settings": "Edit axis settings",
        "btn_calibration": "Unit calibration",
        "btn_export": "Export to Excel",
        "btn_help": "Help",
        "btn_theory": "Theory",
        "btn_about": "About",

        "btn_pick_ox": "Oxidation range (2x click)",
        "btn_pick_red": "Reduction range (2x click)",
        "btn_compute_peak": "Compute peak parameters",
        "btn_auto_peaks": "Auto-detect peaks",
        "btn_derivative": "Compute derivative",
        "btn_second_deriv": "Compute second derivative",
        "btn_curve_fit": "Curve fitting",
        "check_smoothing": "Smoothing (Savitzky-Golay)",

        "combo_oxidation": "Oxidation",
        "combo_reduction": "Reduction",

        "combo_theme_dark": "Dark",
        "combo_theme_light": "Light",

        "label_language": "Language",

        "label_window": "Window:",
        "label_polyorder": "Order:",
        "plot_title": "Voltammogram",
        "axis_x": "E [mV]",
        "axis_y_current": "Current",

        "col_type": "Type",
        "col_xpeak": "x_peak",
        "col_ypeak": "y_peak",
        "col_baseline": "Baseline",
        "col_hd": "H/D",

        "dlg_peakdet_title": "Automatic peak detection",
        "lbl_min_height": "Minimum peak height:",
        "lbl_min_distance": "Minimum distance between peaks:",
        "suffix_datapoints": " data points",
        "chk_detect_ox": "Oxidation range",
        "chk_detect_red": "Reduction range",

        "dlg_axis_title": "Axis settings",
        "lbl_axis_x_label": "X axis label:",
        "lbl_axis_y_label": "Y axis label:",
        "lbl_axis_x_range": "X axis range:",
        "lbl_axis_y_range": "Y axis range:",
        "lbl_font": "Font:",
        "lbl_min": "Min:",
        "lbl_max": "Max:",
        "btn_choose_font": "Choose font",
        "axis_default_x": "X axis",
        "axis_default_y": "Values",

        "dlg_deriv_title": "Oxidation and reduction derivatives",
        "dlg_deriv2_title": "Second derivative of oxidation and reduction",
        "plot_deriv_title": "Derivative plot",
        "plot_deriv2_title": "Second derivative plot",
        "legend_deriv_ox": "Oxidation derivative",
        "legend_deriv_red": "Reduction derivative",
        "legend_deriv2_ox": "Second oxidation derivative",
        "legend_deriv2_red": "Second reduction derivative",
        "lbl_zero_range_from": "Zero-crossing range from:",
        "lbl_zero_range_to": "to:",
        "btn_find_zeros": "Find zero-crossings",

        "dlg_baseline_title": "Baseline settings (numeric)",
        "lbl_oxidation": "Oxidation:",
        "lbl_reduction": "Reduction:",
        "baseline_preview_uninit": "Value preview: Points not initialized yet",

        "dlg_calibration_title": "Unit calibration",
        "lbl_electrode_area": "Electrode area [cm²]:",
        "lbl_analyte_conc": "Analyte concentration [mM]:",
        "chk_normalize_area": "Normalize by electrode area",
        "chk_normalize_conc": "Normalize by concentration",
        "btn_cancel": "Cancel",
        "btn_reset": "Reset",
        "lbl_unit_result": "Resulting unit:",

        "dlg_curvefit_title": "Curve fitting",
        "lbl_model": "Model:",
        "lbl_curve": "Curve:",
        "lbl_xrange_from": "X range — from:",
        "lbl_xrange_to": "X range — to:",
        "model_gaussian": "Gaussian",
        "model_lorentzian": "Lorentzian",
        "model_asym_gaussian": "Asymmetric Gaussian",
        "btn_fit": "Fit",
        "grp_results": "Results",
        "lbl_fwhm": "FWHM:",
        "lbl_peak_center": "Peak center:",
        "lbl_amplitude": "Amplitude:",
        "lbl_asymmetry": "Asymmetry:",
        "lbl_r_squared": "R²:",
        "lbl_fwhm_unit": "FWHM unit:",
        "btn_add_to_results": "Add to results table",
        "btn_close": "Close",
        "legend_fit": "Fit",
    },
}


_current_language = "pl"


def set_language(lang):
    """Ustawia bieżący język modułu (widoczny globalnie dla tr()/translate())."""
    global _current_language
    _current_language = lang


def get_language():
    """Zwraca aktualnie ustawiony język modułu."""
    return _current_language


def translate(key, lang):
    """Zwraca tekst dla klucza w podanym języku; brakujący klucz -> sam klucz."""
    return TRANSLATIONS[lang].get(key, key)


def tr(key):
    """Zwraca tekst dla klucza w bieżącym języku modułu (ustawianym przez set_language()).

    Używane przez dialogi (dialogs.py, derivative_windows.py), które nie mają dostępu do
    MainWindow.tr_ — czytają ten sam, współdzielony stan języka.
    """
    return translate(key, _current_language)
