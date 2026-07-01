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

        "msg_no_data_title": "Brak danych",
        "msg_import_first": "Najpierw zaimportuj dane.",
        "msg_load_file_first": "Najpierw wczytaj plik danych.",
        "msg_error_title": "Błąd",

        "filedlg_open_title": "Wybierz plik z danymi",
        "filedlg_open_filter": "Pliki tekstowe (*.txt);;Wszystkie pliki (*)",
        "msg_file_error_title": "Błąd pliku",
        "msg_bad_columns": "Plik musi zawierać dokładnie 3 kolumny: E, I_ox, I_red.",
        "msg_import_failed": "Nie udało się zaimportować danych z pliku.\n",
        "msg_smoothing_failed": "Dane są zbyt krótkie do wygładzania z obecnymi ustawieniami okna/stopnia wielomianu:\n",
        "msg_calib_title": "Kalibracja",
        "msg_calib_applied": "Kalibracja została zastosowana. Kliknij 'Oblicz parametry piku' aby zaktualizować wyniki.",
        "msg_pick_ox_title": "Zakres utlenienia",
        "msg_pick_ox_instr": "Kliknij dwa razy w obszar wykresu, aby wybrać punkty (x1,y1) oraz (x2,y2) dla utlenienia.",
        "msg_pick_red_title": "Zakres redukcji",
        "msg_pick_red_instr": "Kliknij dwa razy w obszar wykresu, aby wybrać punkty (x1,y1) oraz (x2,y2) dla redukcji.",
        "msg_no_peaks_title": "Brak pików",
        "msg_no_peaks_found": "Nie wykryto żadnych pików przy podanych parametrach.",
        "msg_no_export_data": "Brak danych do eksportu.",
        "filedlg_save_title": "Zapisz do Excela",
        "filedlg_save_filter": "Excel Files (*.xlsx)",
        "msg_success_title": "Sukces",
        "msg_export_success": "Dane oraz wykres zostały zapisane do pliku ",
        "msg_missing_xlsxwriter": "Brak wymaganego pakietu 'xlsxwriter'. Zainstaluj go, aby eksportować do Excela.",
        "msg_export_error": "Wystąpił błąd podczas zapisu do pliku:\n",

        "status_peak_computed": "Policzono parametry piku",

        "msg_invalid_values_title": "Nieprawidłowe wartości",
        "msg_calib_nonzero": "Powierzchnia elektrody oraz stężenie muszą być różne od zera.",
        "msg_invalid_range_title": "Nieprawidłowy zakres",
        "msg_range_order": "Dolna granica zakresu X musi być mniejsza od górnej.",
        "msg_too_few_title": "Zbyt mało punktów",
        "msg_too_few_points": "Wybrany zakres zawiera tylko ",
        "msg_too_few_points_end": " punktów danych. Wymagane minimum: 5.",
        "msg_fit_failed_title": "Dopasowanie nieudane",
        "msg_fit_failed": "Nie udało się dopasować modelu: ",

        "msg_smoothing_error": "Nie udało się wygładzić danych: ",
        "msg_zeros_title": "Miejsca zerowe",
        "msg_zeros_found_header": "Znalezione miejsca zerowe:\n",
        "msg_zeros_none": "Brak miejsc zerowych w zadanym zakresie.",

        "dlg_help_title": "Help – instrukcja",
        "help_html_pl": """
        <html>
        <body style="font-family:Arial; font-size:10pt;">
            <p><b>1. Wybór typu pomiaru</b><br/>
            Z rozwijanego menu wybierz "Utlenianie" lub "Redukcja".</p>

            <p><b>2. Wczytanie danych</b><br/>
            Kliknij przycisk „Wybierz plik z danymi" i załaduj plik tekstowy (*.txt)
            zawierający trzy kolumny: E [mV], I_utlenianie [μA], I_redukcja [μA].</p>

            <p><b>3. Wygładzenie</b><br/>
            •! <i>W tym miejscu ustawienie wygładzania jest opcjonalne i zależy od jakości danych.</i><br/>
            • Zaznacz „Wygładzanie (Savitzky-Golay)".<br/>
            • <b>Okno</b>: liczba punktów uśrednianych przy wygładzaniu (musi być nieparzysta).
            <b>Stopień</b>: rząd wielomianu dopasowywanego lokalnie w oknie (typowo 2–3;
            musi być mniejszy niż okno).<br/>
            <i>Uwaga:</i> niezalecane jest zwiększanie okna powyżej 15.</p>

            <p><b>4. Wybór linii bazowej</b><br/>
            Linię bazową można ustawić lub skorygować na trzy sposoby:</p>
            <p>• <b>Dwukrotne kliknięcie:</b> <b>Utlenianie</b>: Kliknij „Zakres utlenienia
            (2× klik)" i wskaż dwa punkty. <b>Redukcja</b>: Kliknij „Zakres redukcji (2× klik)"
            i wskaż dwa punkty.

            <b>Oba punkty</b> umieść na <b>liniowym fragmencie woltamogramu PRZED narastaniem piku</b>
            (po lewej stronie piku) — tam, gdzie prąd zmienia się liniowo i nie ma jeszcze aktywności redoks.
            Prosta łącząca te punkty reprezentuje prąd tła (niefaradajowski) i zostanie
            <b>ekstrapolowana</b> pod pik, aby oszacować linię bazową w położeniu maksimum.
            Nie umieszczaj punktów po obu stronach piku — linia przecinałaby wtedy pik zamiast
            stanowić jego tło, co zafałszuje wysokość H.</p>
            <p>• <b>Przeciąganie myszą:</b> kolorowy pas bazy można chwycić klikając na jego pole
            i przesunąć go w całości, a następnie dostroić zakres precyzyjnie, przeciągając
            pionowe krawędzie (linie brzegowe) pasa.</p>
            <p>• <b>Dialog numeryczny „Edytuj linię bazową (numerycznie)":</b> pozwala wpisać
            wartości potencjału dla krawędzi zakresu. W praktyce: dla utleniania ustawia się
            prawą i lewą krawędź tak, aby zakres sięgał POZA maksimum piku; dla redukcji
            analogicznie (kluczowe jest, aby zakres bazy znalazł się poza maksimum piku).
            Wartości dobiera się orientacyjnie ("na oko"), pilnując, by baza obejmowała obszar
            poza pikiem.</p>

            <p><b>5. Obliczenie parametrów piku</b><br/>
            Kliknij „Oblicz parametry piku". Program wyznaczy x_peak, y_peak, linię bazową
            oraz wysokość/głębokość piku dla każdej z krzywych, a wyniki wyświetli na wykresie
            i w tabeli. Gdy policzone zostaną OBA piki (utlenianie i redukcja), w tabeli
            dodatkowo pojawią się: <b>E½</b> (potencjał półfalowy), <b>ΔEp</b> (rozdzielenie
            potencjałów pików, |E<sub>p,a</sub> − E<sub>p,c</sub>| — parametr odwracalności)
            oraz <b>Ipa/Ipc</b> (stosunek prądów pików anodowego i katodowego — również
            parametr odwracalności).</p>
            <p><i>Wizualizacja bazy po obliczeniu:</i> po kliknięciu tego przycisku kolorowy
            pas linii bazowej traci wypełnienie (krawędzie pozostają widoczne i przeciągalne),
            a w jego miejsce pojawia się wypełnienie obszaru między krzywą a linią bazową
            (pod krzywą utleniania / nad krzywą redukcji) — co czytelnie pokazuje wysokość
            piku. Przeciągnięcie krawędzi bazy, ponowny wybór zakresu (2× klik) lub użycie
            dialogu numerycznego przywraca tryb edycji (pas z wypełnieniem wraca).</p>

            <p><b>6. Pierwsza pochodna</b><br/>
            <i>Krok opcjonalny</i> — pomocniczy, służy do precyzyjnej lokalizacji ekstremów;
            nie jest wymagany do podstawowej analizy piku.<br/>
            • Kliknij „Oblicz pochodną" — otworzy się osobne okno z wykresem pierwszej
            pochodnej.<br/>
            • Okno ma własne kontrolki wygładzania (niezależne od ustawień w głównym oknie)
            oraz pole „Zakres miejsc zerowych od/do" z przyciskiem „Znajdź miejsca zerowe".<br/>
            • Miejsca zerowe pierwszej pochodnej odpowiadają ekstremom — wierzchołkom pików
            utleniania i redukcji.<br/>
            • Po zamknięciu okna znalezione miejsca zerowe zostają dopisane do tabeli wyników
            w głównym oknie.</p>

            <p><b>7. Druga pochodna</b><br/>
            <i>Krok opcjonalny</i> — szczególnie przydatny przy analizie procesów
            nieodwracalnych, gdzie brak pary pików utrudnia zwykłe wyznaczanie parametrów.<br/>
            • Kliknij „Oblicz drugą pochodną" — analogicznie jak przy pierwszej pochodnej,
            otworzy się osobne okno z wykresem drugiej pochodnej, własnym wygładzaniem,
            polem zakresu i przyciskiem „Znajdź miejsca zerowe".<br/>
            • Miejsca zerowe drugiej pochodnej odpowiadają punktom przegięcia woltamogramu,
            przydatnym zwłaszcza wtedy, gdy proces nieodwracalny nie tworzy wyraźnego piku.<br/>
            • Po zamknięciu okna znalezione miejsca zerowe zostają dopisane do tabeli wyników
            w głównym oknie.</p>

            <p><b>8. Eksport do Excela</b><br/>
            Kliknij „Eksport do Excela", wybierz nazwę pliku.
            Zapisane zostaną: surowe dane, dane wygładzone, pochodne, miejsca zerowe, wyniki piku i wykres.</p>

            <hr/>

            <p><b>9. Automatyczne wykrywanie pików</b><br/>
            • Kliknij „Wykryj piki automatycznie".<br/>
            • <b>Minimalna wysokość piku</b>: filtruje szum — tylko piki o amplitudzie
            większej lub równej tej wartości zostaną uznane za pik. Ustaw 0, aby wyłączyć filtr.<br/>
            • <b>Minimalna odległość między pikami</b>: podawana w <i>punktach danych</i>
            (nie w jednostkach osi X). Zapobiega wykrywaniu kilku pików w obrębie jednego
            szerokiego maksimum.<br/>
            • Zaznacz zakres(y) — utlenienia i/lub redukcji — dla których ma być uruchomione wyszukiwanie.<br/>
            • Wykryte piki są nanoszone na wykres jako <b>żółte kółka</b> oraz
            dopisywane do tabeli wyników jako „Pik auto (utl)" / „Pik auto (red)".</p>

            <p><b>10. Kalibracja jednostek</b><br/>
            • Kliknij „Kalibracja jednostek".<br/>
            • Podaj <b>powierzchnię elektrody</b> [cm²] oraz/lub <b>stężenie analitu</b> [mM].<br/>
            • Zaznacz odpowiednie checkboxy, aby znormalizować prąd.
            Normalizacja względem powierzchni (μA/cm²) jest standardem publikacyjnym
            i pozwala porównywać pomiary z elektrod o różnych rozmiarach. Normalizacja
            względem stężenia (μA/mM) stosowana jest w analizie czujników.<br/>
            • Podgląd jednostki wynikowej aktualizuje się na żywo.<br/>
            • Po zatwierdzeniu kalibracji tabela wyników jest czyszczona — <b>należy
            ponownie kliknąć „Oblicz parametry piku"</b>, aby uzyskać wartości wysokości
            i głębokości w nowych jednostkach. Surowe dane pozostają nietknięte — kalibracja
            jest zawsze stosowana jako krok post-processing.<br/>
            • Aktywna kalibracja jest widoczna w prawej części paska stanu.</p>

            <p><b>11. Dopasowanie krzywej</b><br/>
            • Kliknij „Dopasowanie krzywej".<br/>
            Modele te są funkcjami dopasowania matematycznego służącymi do wyznaczenia
            parametrów piku (FWHM, centrum, amplituda); nie są modelami fizycznymi opisującymi
            mechanizm elektrodowy — wybór modelu to kwestia jakości dopasowania kształtu,
            nie interpretacji procesu.<br/>
            • Wybierz <b>model</b>: <b>Gaussowski</b> — symetryczny, dzwonowy kształt; dobrze
            dopasowuje się do w miarę symetrycznych pików. Uwaga: rzeczywisty pik CV
            kontrolowany dyfuzją nie jest idealnie gaussowski (ma asymetryczny ogon), więc
            model traktuj jako przybliżenie empiryczne.<br/>
            <b>Lorentzowski</b> — symetryczny kształt o wolniej opadających (szerszych)
            ogonach niż Gauss; bywa lepszym dopasowaniem, gdy pik ma szersze skrzydła.<br/>
            <b>Asymetryczny Gaussowski</b> — dopuszcza różną szerokość po obu stronach piku
            (parametr asymetrii); przydatny, gdy pik jest wyraźnie niesymetryczny.<br/>
            • Wybierz <b>krzywą</b> (utlenianie/redukcja) — zakres X jest automatycznie
            wypełniany wartościami bieżącej linii bazowej, możesz go zmodyfikować.<br/>
            • Kliknij „Dopasuj". Wyniki: <b>FWHM</b> (szerokość połówkowa — szerokość piku
            na połowie jego wysokości), <b>amplituda</b>, <b>centrum piku</b>,
            <b>R²</b> (dopasowanie; &gt; 0,99 uznaje się za bardzo dobre), a dla modelu
            asymetrycznego — <b>asymetria</b> (σ_prawa/σ_lewa).<br/>
            • Zielona przerywana linia na wykresie dialogu to dopasowany model.<br/>
            • Przycisk „Dodaj do tabeli wyników" przenosi parametry do głównej tabeli.<br/>
            • Dialog jest niemodalny — możesz nadal pracować z głównym oknem.</p>

            <hr/>

            <p><b>Opcjonalne ustawienia</b><br/>
            • Tryb jasny/ciemny – przełącznik w górnym pasku.<br/>
            • Ręczna edycja osi – przycisk „Edytuj ustawienia osi".<br/>
            • Zakładka „Teoria" w górnym pasku — rozbudowany podręcznik teoretyczny.</p>
        </body>
        </html>
        """,
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

        "msg_no_data_title": "No data",
        "msg_import_first": "Please import data first.",
        "msg_load_file_first": "Please load a data file first.",
        "msg_error_title": "Error",

        "filedlg_open_title": "Open data file",
        "filedlg_open_filter": "Text files (*.txt);;All files (*)",
        "msg_file_error_title": "File error",
        "msg_bad_columns": "File must contain exactly 3 columns: E, I_ox, I_red.",
        "msg_import_failed": "Failed to import data from file.\n",
        "msg_smoothing_failed": "Data too short for smoothing with current window/polynomial order settings:\n",
        "msg_calib_title": "Calibration",
        "msg_calib_applied": "Calibration applied. Click 'Compute peak parameters' to update results.",
        "msg_pick_ox_title": "Oxidation range",
        "msg_pick_ox_instr": "Double-click on the plot to select points (x1,y1) and (x2,y2) for oxidation.",
        "msg_pick_red_title": "Reduction range",
        "msg_pick_red_instr": "Double-click on the plot to select points (x1,y1) and (x2,y2) for reduction.",
        "msg_no_peaks_title": "No peaks",
        "msg_no_peaks_found": "No peaks detected with the given parameters.",
        "msg_no_export_data": "No data to export.",
        "filedlg_save_title": "Save to Excel",
        "filedlg_save_filter": "Excel Files (*.xlsx)",
        "msg_success_title": "Success",
        "msg_export_success": "Data and plot saved to file ",
        "msg_missing_xlsxwriter": "Required package 'xlsxwriter' is missing. Install it to export to Excel.",
        "msg_export_error": "An error occurred while saving the file:\n",

        "status_peak_computed": "Peak parameters computed",

        "msg_invalid_values_title": "Invalid values",
        "msg_calib_nonzero": "Electrode area and concentration must be non-zero.",
        "msg_invalid_range_title": "Invalid range",
        "msg_range_order": "Lower X bound must be less than upper.",
        "msg_too_few_title": "Too few points",
        "msg_too_few_points": "Selected range contains only ",
        "msg_too_few_points_end": " data points. Minimum required: 5.",
        "msg_fit_failed_title": "Fit failed",
        "msg_fit_failed": "Failed to fit model: ",

        "msg_smoothing_error": "Failed to smooth data: ",
        "msg_zeros_title": "Zero-crossings",
        "msg_zeros_found_header": "Zero-crossings found:\n",
        "msg_zeros_none": "No zero-crossings in the given range.",

        "dlg_help_title": "Help – instructions",
        "help_html_en": """
        <html>
        <body style="font-family:Arial; font-size:10pt;">
            <p><b>1. Select measurement type</b><br/>
            From the dropdown menu, choose "Oxidation" or "Reduction".</p>

            <p><b>2. Load data</b><br/>
            Click the "Open data file" button and load a text file (*.txt)
            containing three columns: E [mV], I_oxidation [μA], I_reduction [μA].</p>

            <p><b>3. Smoothing</b><br/>
            •! <i>Smoothing is optional here and depends on the quality of the data.</i><br/>
            • Check "Smoothing (Savitzky-Golay)".<br/>
            • <b>Window</b>: the number of points averaged during smoothing (must be odd).
            <b>Order</b>: the degree of the polynomial fitted locally within the window (typically 2–3;
            must be smaller than the window).<br/>
            <i>Note:</i> increasing the window above 15 is not recommended.</p>

            <p><b>4. Set the baseline</b><br/>
            The baseline can be set or adjusted in three ways:</p>
            <p>• <b>Double-click:</b> <b>Oxidation</b>: Click "Oxidation range
            (2x click)" and pick two points. <b>Reduction</b>: Click "Reduction range (2x click)"
            and pick two points.

            Place <b>both points</b> on a <b>linear segment of the voltammogram BEFORE the peak rises</b>
            (on the left side of the peak) — where the current changes linearly and there is no redox activity yet.
            The straight line connecting these points represents the background (non-faradaic) current and
            will be <b>extrapolated</b> under the peak to estimate the baseline at the position of the maximum.
            Do not place points on both sides of the peak — the line would then cross the peak instead of
            forming its background, which would distort the height H.</p>
            <p>• <b>Dragging with the mouse:</b> the colored baseline band can be grabbed by clicking on its area
            and moved as a whole, then fine-tuned precisely by dragging its
            vertical edges (border lines).</p>
            <p>• <b>Numeric dialog "Edit baseline (numeric)":</b> lets you type
            the potential values for the range edges. In practice: for oxidation, set the right
            and left edge so the range extends BEYOND the peak maximum; for reduction,
            likewise (the key point is that the baseline range must lie beyond the peak maximum).
            Values are chosen roughly ("by eye"), making sure the baseline covers the area
            outside the peak.</p>

            <p><b>5. Compute peak parameters</b><br/>
            Click "Compute peak parameters". The program will determine x_peak, y_peak, the baseline
            value, and the height/depth of the peak for each curve, and display the results on the plot
            and in the table. When BOTH peaks (oxidation and reduction) have been computed, the table
            will additionally show: <b>E½</b> (half-wave potential), <b>ΔEp</b> (peak potential
            separation, |E<sub>p,a</sub> − E<sub>p,c</sub>| — a reversibility parameter)
            and <b>Ipa/Ipc</b> (the ratio of the anodic and cathodic peak currents — also a
            reversibility parameter).</p>
            <p><i>Baseline visualization after computation:</i> after clicking this button, the
            colored baseline band loses its fill (the edges remain visible and draggable),
            and a filled area appears in its place between the curve and the baseline
            (below the oxidation curve / above the reduction curve) — clearly showing the
            peak height. Dragging a baseline edge, re-selecting the range (2x click), or using
            the numeric dialog restores edit mode (the filled band returns).</p>

            <p><b>6. First derivative</b><br/>
            <i>Optional step</i> — a helper tool for precisely locating extrema;
            not required for basic peak analysis.<br/>
            • Click "Compute derivative" — a separate window with the first-derivative
            plot will open.<br/>
            • The window has its own smoothing controls (independent of the settings in the
            main window) and a "Zero-crossing range from:" / "to:" field with a "Find zero-crossings" button.<br/>
            • The zero-crossings of the first derivative correspond to extrema — the apexes of the
            oxidation and reduction peaks.<br/>
            • When the window is closed, the found zero-crossings are appended to the results table
            in the main window.</p>

            <p><b>7. Second derivative</b><br/>
            <i>Optional step</i> — especially useful when analyzing irreversible
            processes, where the lack of a peak pair makes standard parameter determination difficult.<br/>
            • Click "Compute second derivative" — just like with the first derivative,
            a separate window with the second-derivative plot will open, with its own smoothing,
            a range field, and a "Find zero-crossings" button.<br/>
            • The zero-crossings of the second derivative correspond to the inflection points of the
            voltammogram, useful especially when an irreversible process does not form a clear peak.<br/>
            • When the window is closed, the found zero-crossings are appended to the results table
            in the main window.</p>

            <p><b>8. Export to Excel</b><br/>
            Click "Export to Excel", choose a file name.
            The following will be saved: raw data, smoothed data, derivatives, zero-crossings, peak results, and the chart.</p>

            <hr/>

            <p><b>9. Automatic peak detection</b><br/>
            • Click "Auto-detect peaks".<br/>
            • <b>Minimum peak height</b>: filters out noise — only peaks with an amplitude
            greater than or equal to this value are counted as a peak. Set to 0 to disable the filter.<br/>
            • <b>Minimum distance between peaks</b>: given in <i>data points</i>
            (not in X-axis units). Prevents detecting several peaks within a single
            broad maximum.<br/>
            • Check the range(s) — oxidation and/or reduction — for which detection should run.<br/>
            • Detected peaks are marked on the plot as <b>yellow circles</b> and
            appended to the results table as "Pik auto (utl)" / "Pik auto (red)".</p>

            <p><b>10. Unit calibration</b><br/>
            • Click "Unit calibration".<br/>
            • Enter the <b>electrode area</b> [cm²] and/or the <b>analyte concentration</b> [mM].<br/>
            • Check the relevant checkboxes to normalize the current.
            Normalization by area (μA/cm²) is a publication standard and allows
            comparing measurements from electrodes of different sizes. Normalization
            by concentration (μA/mM) is used in sensor analysis.<br/>
            • The resulting-unit preview updates live.<br/>
            • After confirming the calibration, the results table is cleared — <b>you need to
            click "Compute peak parameters" again</b> to obtain the height and depth values
            in the new units. The raw data remains untouched — calibration is always applied
            as a post-processing step.<br/>
            • The active calibration is shown on the right side of the status bar.</p>

            <p><b>11. Curve fitting</b><br/>
            • Click "Curve fitting".<br/>
            These models are mathematical fitting functions used to determine
            peak parameters (FWHM, center, amplitude); they are not physical models describing
            the electrode mechanism — the choice of model is a matter of shape-fitting quality,
            not process interpretation.<br/>
            • Choose a <b>model</b>: <b>Gaussian</b> — a symmetric, bell-shaped curve; fits
            reasonably symmetric peaks well. Note: a real diffusion-controlled CV peak is
            not perfectly Gaussian (it has an asymmetric tail), so treat the
            model as an empirical approximation.<br/>
            <b>Lorentzian</b> — a symmetric shape with more slowly decaying (wider)
            tails than the Gaussian; can be a better fit when the peak has wider wings.<br/>
            <b>Asymmetric Gaussian</b> — allows a different width on each side of the peak
            (an asymmetry parameter); useful when the peak is clearly non-symmetric.<br/>
            • Choose the <b>curve</b> (oxidation/reduction) — the X range is automatically
            filled with the values of the current baseline; you can modify it.<br/>
            • Click "Fit". Results: <b>FWHM</b> (full width at half maximum — the width of the peak
            at half its height), <b>amplitude</b>, <b>peak center</b>,
            <b>R²</b> (goodness of fit; &gt; 0.99 is considered very good), and for the
            asymmetric model — <b>asymmetry</b> (σ_right/σ_left).<br/>
            • The green dashed line on the dialog's plot is the fitted model.<br/>
            • The "Add to results table" button transfers the parameters to the main table.<br/>
            • The dialog is non-modal — you can keep working with the main window.</p>

            <hr/>

            <p><b>Optional settings</b><br/>
            • Light/dark theme – switch in the top toolbar.<br/>
            • Manual axis editing – "Edit axis settings" button.<br/>
            • The "Theory" tab in the top toolbar — an extensive theoretical handbook.</p>
        </body>
        </html>
        """,
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
