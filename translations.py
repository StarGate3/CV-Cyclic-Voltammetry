"""
Moduł translations.py
----------------------
Słowniki tłumaczeń UI (PL/EN). Czysty moduł danych — brak zależności od Qt ani od reszty
programu. Etap 0: klucze toolbara (trzy rzędy, w tym Help/Teoria/About jako zwykłe
przyciski), obu combo (motyw, pomiar) i tytułu okna. Kolejne etapy dołożą resztę kluczy
(etykiety, nagłówki tabeli, osie, dialogi, treść Help/Teoria/About).
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
    },
}
