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

        "legend_baseline_ox": "Baseline Utlenienia",
        "legend_baseline_red": "Baseline Redukcji",
        "annot_oxidation": "Utlenienie",
        "annot_reduction": "Redukcja",

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

        "dlg_theory_title": "Teoria — podręcznik",

        "theory_tab1_title_pl": "Woltametria cykliczna",
        "theory_tab1_html_pl": """
        <h3>Woltametria cykliczna (CV)</h3>
        <p><b>Czym jest CV?</b> Woltametria cykliczna to technika elektroanalityczna,
        w której potencjał elektrody roboczej jest zmieniany liniowo w czasie między
        dwiema wartościami granicznymi, a następnie zawracany — tworząc cykl. Jednocześnie
        rejestrowany jest prąd płynący przez elektrodę.</p>

        <h3>Zasada działania</h3>
        <p>Potencjostat wymusza na elektrodzie roboczej zadany potencjał względem elektrody
        odniesienia, a prąd mierzy między elektrodą roboczą a pomocniczą. Zmiana potencjału
        wywołuje reakcje utleniania (na krzywej narastającej) i redukcji (na krzywej
        opadającej) substancji elektroaktywnej.</p>

        <h3>Opis woltamogramu</h3>
        <ul>
            <li><b>Oś X — potencjał E [mV lub V]:</b> narzucona siła elektrochemiczna.</li>
            <li><b>Oś Y — prąd I [μA]:</b> odpowiedź układu. Konwencja IUPAC: prądy
            anodowe (utlenianie) dodatnie, katodowe (redukcja) ujemne.</li>
        </ul>

        <h3>Piki utleniania i redukcji</h3>
        <p><b>Pik anodowy (ip,a)</b> pojawia się podczas skanu w kierunku dodatnich
        potencjałów i odpowiada utlenianiu analitu na elektrodzie. <b>Pik katodowy
        (ip,c)</b> pojawia się podczas skanu wstecznego i odpowiada redukcji produktu
        utlenienia. Obecność obu pików świadczy o procesie co najmniej quasi-odwracalnym.</p>

        <h3>Potencjał półfalowy E½</h3>
        <p>Dla procesu odwracalnego E½ definiuje się jako średnią arytmetyczną potencjałów
        piku anodowego i katodowego:</p>
        <p style="margin-left:2em;"><b>E½ = (E<sub>p,a</sub> + E<sub>p,c</sub>) / 2</b></p>
        <p>E½ jest bliski formalnemu potencjałowi redoks i charakteryzuje daną parę
        redoks niezależnie od szybkości skanowania (dla procesu odwracalnego).</p>

        <h3>ΔEp — rozdzielenie potencjałów pików</h3>
        <p>ΔEp to bezwzględna różnica potencjałów piku anodowego (utleniania) i katodowego
        (redukcji):</p>
        <p style="margin-left:2em;"><b>ΔEp = |E<sub>p,a</sub> − E<sub>p,c</sub>|</b></p>
        <p>ΔEp jest podstawowym kryterium odwracalności układu redoks. Dla procesu
        odwracalnego, jednoelektronowego, w temperaturze 25 °C teoretyczna wartość wynosi
        <b>ΔEp ≈ 59/n mV</b>, gdzie n to liczba wymienianych elektronów. Wartości ΔEp bliskie
        59/n mV wskazują na proces odwracalny; wyraźnie większe wartości świadczą o kinetyce
        quasi-odwracalnej lub nieodwracalnej, często związanej z wolnym transferem elektronu.
        W praktyce na ΔEp wpływa też opór roztworu (spadek omowy iR), co może zawyżać
        obserwowaną wartość.</p>
        """,

        "theory_tab2_title_pl": "Linia bazowa",
        "theory_tab2_html_pl": """
        <h3>Dlaczego korekcja linii bazowej jest konieczna</h3>
        <p>Zmierzony prąd piku to suma prądu faradajowskiego (reakcja redoks) oraz
        prądu tła — pojemnościowego ładowania podwójnej warstwy i prądów
        pochodzących od rozpuszczalnika/elektrolitu. Aby wyznaczyć prawdziwą
        wysokość piku (<b>H</b>) musimy odjąć prąd tła.</p>

        <h3>Jak prawidłowo wybrać punkty linii bazowej</h3>
        <p>Standardowa metoda korekcji linii bazowej w CV polega na wybraniu
        <b>obu</b> punktów na <b>liniowym fragmencie woltamogramu PRZED narastaniem
        piku</b> — po <i>lewej</i> stronie piku, w obszarze, w którym prąd jeszcze
        nie zaczął rosnąć na skutek reakcji redoks. Linia bazowa jest następnie
        <b>ekstrapolowana</b> jako prosta pod pikiem, aby oszacować prąd tła
        (niefaradajowski), który płynąłby, gdyby reakcja redoks nie zachodziła.</p>
        <ul>
            <li>Oba punkty (x<sub>1</sub>, y<sub>1</sub>) i (x<sub>2</sub>, y<sub>2</sub>)
            umieść na <b>płaskim, liniowym odcinku</b> woltamogramu poprzedzającym pik —
            tam, gdzie prąd zmienia się liniowo z potencjałem i nie ma jeszcze
            aktywności faradajowskiej.</li>
            <li>Prosta łącząca te dwa punkty reprezentuje prąd niefaradajowski
            (ładowanie podwójnej warstwy, tło rozpuszczalnika/elektrolitu) —
            jest ekstrapolowana pod pik do położenia E<sub>p</sub>.</li>
            <li>Wysokość piku H to odległość od piku do tej ekstrapolowanej linii
            w położeniu maksimum, a nie do prostej łączącej punkty po obu stronach piku.</li>
            <li>Oba punkty powinny leżeć na tej samej gałęzi woltamogramu
            (narastającej lub opadającej) i wystarczająco blisko siebie, aby
            zachować lokalne nachylenie tła.</li>
            <li>W CVision możesz wybrać punkty dwukrotnym kliknięciem lub edytować
            numerycznie w oknie „Edytuj linię bazową".</li>
        </ul>

        <h3>Wpływ złego doboru linii bazowej</h3>
        <ul>
            <li><b>Punkty po obu stronach piku</b> — linia przecina pik zamiast stanowić
            jego tło; wysokość H jest zaniżona, a jej wartość zależy arbitralnie od
            wybranego zakresu.</li>
            <li><b>Punkt w obszarze narastania piku</b> — ekstrapolacja jest nienaturalnie
            skośna, pozorny pik lub brak piku.</li>
            <li><b>Zbyt szeroki zakres obejmujący inne procesy</b> — nachylenie prostej
            zaburzone przez sąsiedni pik, H zawyżone lub zaniżone.</li>
            <li><b>Zbyt krótki odcinek liniowy</b> — punkty podatne na szum, duża
            niepewność ekstrapolacji.</li>
        </ul>
        <p>Dobra praktyka: zawsze wizualnie zweryfikuj, czy ekstrapolowana linia
        bazowa biegnie naturalnie pod pikiem, przed odczytem parametrów piku.</p>
        """,

        "theory_tab3_title_pl": "Parametry piku",
        "theory_tab3_html_pl": """
        <h3>Wysokość (H) i głębokość (D) piku</h3>
        <p>Wysokość piku anodowego <b>H = i<sub>p,a</sub> − i<sub>baseline</sub>(E<sub>p,a</sub>)</b>
        to odległość maksimum od linii bazowej w jego położeniu. Analogicznie
        głębokość piku katodowego <b>D = i<sub>baseline</sub>(E<sub>p,c</sub>) − i<sub>p,c</sub></b>.
        Obie wielkości są dodatnie i wyrażone w μA (lub — po kalibracji — w μA/cm²,
        μA/mM, μA/(cm²·mM)).</p>

        <h3>Stosunek prądów i<sub>p,a</sub> / i<sub>p,c</sub></h3>
        <p>Stosunek wysokości piku anodowego do katodowego informuje o odwracalności
        procesu elektrochemicznego:</p>
        <table border="1" cellpadding="6" cellspacing="0">
            <tr><th>i<sub>p,a</sub> / i<sub>p,c</sub></th><th>Interpretacja</th></tr>
            <tr><td>≈ 1,0</td><td>Proces odwracalny (forma utleniona i zredukowana stabilne)</td></tr>
            <tr><td>&lt; 1 lub &gt; 1</td><td>Proces quasi-odwracalny lub sprzężona reakcja chemiczna</td></tr>
            <tr><td>brak jednego z pików</td><td>Proces nieodwracalny</td></tr>
        </table>

        <h3>Równanie Randlesa-Ševčíka</h3>
        <p>Dla procesu odwracalnego, kontrolowanego dyfuzją, prąd piku wynosi:</p>
        <p style="margin-left:2em;"><b>i<sub>p</sub> = 0,4463 · n · F · A · C · √(n · F · v · D / (R · T))</b></p>
        <p>W 25 °C upraszcza się do i<sub>p</sub> = (2,69·10⁵) · n<sup>3/2</sup> · A · C · √(D · v).</p>
        <p><b>Znaczenie symboli:</b></p>
        <ul>
            <li><b>i<sub>p</sub></b> — prąd piku [A]</li>
            <li><b>n</b> — liczba elektronów biorących udział w reakcji</li>
            <li><b>F</b> — stała Faradaya (96 485 C/mol)</li>
            <li><b>A</b> — powierzchnia elektrody [cm²]</li>
            <li><b>C</b> — stężenie analitu w roztworze [mol/cm³]</li>
            <li><b>v</b> — szybkość skanowania potencjału [V/s]</li>
            <li><b>D</b> — współczynnik dyfuzji analitu [cm²/s]</li>
            <li><b>R</b> — stała gazowa (8,314 J/(mol·K))</li>
            <li><b>T</b> — temperatura [K]</li>
        </ul>
        <p>Liniowa zależność i<sub>p</sub> od √v jest diagnostyką procesu
        kontrolowanego dyfuzją.</p>
        <p>Ponieważ prąd piku i<sub>p</sub> jest wprost proporcjonalny do stężenia analitu C
        (zgodnie z równaniem Randlesa-Ševčíka), wysokość piku stanowi podstawę ilościowego
        oznaczania stężenia metodą krzywej kalibracyjnej.</p>

        <h3>Automatyczne wykrywanie pików</h3>
        <p>Program może automatycznie lokalizować piki metodą <b>find_peaks</b>, wykrywającą
        lokalne maksima/minima spełniające kryteria minimalnej wysokości i minimalnej odległości
        między pikami. Różni się to od ręcznego wyznaczania parametrów piku przez linię bazową:
        automatyczna detekcja szybko wskazuje położenie pików, natomiast dokładne parametry
        (wysokość względem tła, baseline) wyznacza się metodą linii bazowej. Kryteria minimalnej
        wysokości i odległości służą do odfiltrowania szumu i nieistotnych lokalnych ekstremów.</p>
        """,

        "theory_tab4_title_pl": "Pochodne i miejsca zerowe",
        "theory_tab4_html_pl": """
        <h3>Po co obliczać pochodną woltamogramu</h3>
        <p>Pochodne pomagają precyzyjnie zlokalizować cechy woltamogramu niewidoczne
        „gołym okiem" na surowym sygnale — szczególnie gdy piki są słabo
        rozdzielone, asymetryczne, lub proces jest nieodwracalny.</p>

        <h3>Pierwsza pochodna dI/dE</h3>
        <ul>
            <li>Miejsce zerowe pierwszej pochodnej odpowiada ekstremum prądu:
            <b>dI/dE = 0</b> → maksimum (pik utleniania) lub minimum (pik redukcji).</li>
            <li>Pozwala znaleźć dokładne E<sub>p</sub> bez wizualnego odgadywania.</li>
        </ul>

        <h3>Druga pochodna d²I/dE²</h3>
        <ul>
            <li>Miejsca zerowe drugiej pochodnej oznaczają punkty przegięcia krzywej CV —
            przydatne dla procesów <b>nieodwracalnych</b>, gdzie klasyczny pik nie tworzy
            wyraźnego maksimum (np. elektroutlenianie organiki).</li>
            <li>Pozwala oszacować potencjał półfalowy nawet przy braku piku redukcyjnego.</li>
        </ul>

        <h3>Wygładzanie Savitzky-Golay</h3>
        <p>Pochodne wzmacniają szum. Przed ich obliczaniem warto wygładzić sygnał filtrem
        Savitzky-Golay, który lokalnie dopasowuje wielomian niskiego stopnia metodą
        najmniejszych kwadratów, zachowując kształt piku lepiej niż średnia krocząca.</p>
        <p><b>Dobór parametrów:</b></p>
        <ul>
            <li><b>Okno</b> (liczba nieparzysta): im większe, tym silniejsze wygładzanie,
            ale ryzyko spłaszczenia piku. W praktyce 7–15 punktów dla typowego CV.</li>
            <li><b>Stopień wielomianu</b>: 2 lub 3 dla typowych kształtów, 4–5 dla
            bardziej złożonych sygnałów. Musi być <b>mniejszy</b> niż okno.</li>
            <li>Złota zasada: zwiększaj okno tylko na tyle, aby usunąć szum, i sprawdź,
            czy amplituda piku nie spada.</li>
        </ul>
        """,

        "theory_tab5_title_pl": "Dopasowanie krzywych",
        "theory_tab5_html_pl": """
        <h3>Kiedy stosować Gaussa, a kiedy Lorentza</h3>
        <table border="1" cellpadding="6" cellspacing="0">
            <tr><th>Model</th><th>Kształt</th><th>Zastosowanie</th></tr>
            <tr><td>Gaussowski</td>
                <td>szybko opadające ogony (exp(−x²))</td>
                <td>piki w miarę symetryczne, o wąskich ogonach</td></tr>
            <tr><td>Lorentzowski</td>
                <td>wolno opadające, szerokie ogony (1/(1+x²))</td>
                <td>piki z szerszymi ogonami/skrzydłami</td></tr>
            <tr><td>Asymetryczny Gaussowski</td>
                <td>różne σ z dwóch stron centrum</td>
                <td>piki wyraźnie niesymetryczne</td></tr>
        </table>
        <p>Modele te są funkcjami dopasowania matematycznego do wyznaczenia parametrów piku
        (FWHM, centrum, amplituda); wybór modelu to kwestia jakości dopasowania kształtu,
        nie interpretacji mechanizmu elektrodowego.</p>

        <h3>FWHM — szerokość połówkowa</h3>
        <p><b>FWHM</b> (Full Width at Half Maximum) to szerokość piku na wysokości
        równej połowie jego amplitudy. Wzory modelowe:</p>
        <ul>
            <li>Gauss: <b>FWHM = 2·√(2·ln2)·σ ≈ 2,3548·σ</b></li>
            <li>Lorentz: <b>FWHM = 2·γ</b></li>
            <li>Asymetryczny Gauss: <b>FWHM = √(2·ln2)·(σ<sub>L</sub> + σ<sub>R</sub>)</b></li>
        </ul>
        <p>Dla procesu odwracalnego w 25 °C teoretyczna FWHM piku wynosi ≈ 90,6/n mV
        (n — liczba elektronów). Znacznie szerszy pik świadczy o nieodwracalności lub
        powolnym transporcie.</p>

        <h3>Asymetria piku</h3>
        <p>Współczynnik <b>asymetrii = σ<sub>prawa</sub> / σ<sub>lewa</sub></b>:</p>
        <ul>
            <li><b>≈ 1,0</b> — pik symetryczny.</li>
            <li><b>&gt; 1</b> — prawa strona piku szersza.</li>
            <li><b>&lt; 1</b> — lewa strona piku szersza.</li>
        </ul>
        <p>Kierunek i stopień asymetrii mogą sygnalizować odstępstwa od idealnego,
        symetrycznego kształtu piku; ich interpretacja mechanistyczna wymaga jednak
        dodatkowej wiedzy o układzie i nie wynika jednoznacznie z samego dopasowania.</p>

        <h3>Współczynnik determinacji R²</h3>
        <p><b>R² = 1 − SS<sub>res</sub>/SS<sub>tot</sub></b> mierzy jaki procent zmienności
        danych wyjaśnia model:</p>
        <ul>
            <li><b>R² &gt; 0,99</b> — dopasowanie bardzo dobre, model adekwatny.</li>
            <li><b>0,95 – 0,99</b> — akceptowalne, ale warto sprawdzić inny model
            lub zmniejszyć zakres dopasowania.</li>
            <li><b>&lt; 0,95</b> — model niewłaściwy lub dane zaszumione; rozważ
            wygładzanie lub model asymetryczny.</li>
        </ul>
        """,

        "theory_tab6_title_pl": "Kalibracja jednostek",
        "theory_tab6_html_pl": """
        <h3>Normalizacja do powierzchni elektrody (standard publikacyjny)</h3>
        <p>Prąd zarejestrowany na elektrodzie zależy liniowo od jej powierzchni
        (patrz równanie Randlesa-Ševčíka). Porównywanie bezwzględnych wartości μA
        z różnych elektrod jest bezsensowne. Dlatego w publikacjach elektrochemicznych
        standardem jest <b>gęstość prądu j = i / A [μA/cm²]</b>.</p>

        <h3>Wyznaczanie rzeczywistej powierzchni elektrody (ECSA)</h3>
        <p><b>ECSA</b> (Electrochemically Active Surface Area) to powierzchnia faktycznie
        dostępna dla reakcji, zwykle większa niż powierzchnia geometryczna dla elektrod
        nanostrukturalnych. Typowe metody:</p>
        <ul>
            <li><b>Metoda Randlesa-Ševčíka:</b> wyznacz i<sub>p</sub> dla kilku szybkości
            skanowania z wzorcem o znanym D i C (np. [Fe(CN)<sub>6</sub>]³⁻/⁴⁻),
            dopasuj i<sub>p</sub> vs √v i oblicz A z nachylenia.</li>
            <li><b>Metoda pojemnościowa (double-layer):</b> z CV bez aktywnych par
            redoks oblicz pojemność C<sub>dl</sub> i podziel przez specyficzną pojemność
            materiału (zwykle 20–60 μF/cm² dla metali).</li>
            <li><b>Metoda utleniania H<sub>upd</sub></b> (dla Pt) — z ładunku pików
            desorpcji wodoru, 210 μC/cm² dla Pt(111).</li>
            <li><b>Metoda wzorca redoks</b> — z CV [Ru(NH<sub>3</sub>)<sub>6</sub>]³⁺ lub
            ferrocenu o znanym współczynniku dyfuzji.</li>
        </ul>

        <h3>Normalizacja do stężenia — czujniki elektrochemiczne</h3>
        <p>W analityce czujnikowej istotna jest <b>czułość na stężenie</b>, wyrażana
        w μA/mM lub (po dodatkowej normalizacji) μA/(cm²·mM). Pozwala porównywać
        różne konstrukcje czujników niezależnie od rozmiaru i stężenia kalibracyjnego.</p>

        <h3>Przelicznik jednostek w CVision</h3>
        <table border="1" cellpadding="6" cellspacing="0">
            <tr><th>Sytuacja</th><th>Operacja</th><th>Jednostka wynikowa</th></tr>
            <tr><td>Brak normalizacji</td><td>i</td><td>μA</td></tr>
            <tr><td>Normalizuj względem A</td><td>i / A</td><td>μA/cm²</td></tr>
            <tr><td>Normalizuj względem c</td><td>i / c</td><td>μA/mM</td></tr>
            <tr><td>Obie normalizacje</td><td>i / (A · c)</td><td>μA/(cm²·mM)</td></tr>
        </table>
        <p><b>Przykład:</b> pik o wysokości 168,175 μA dla elektrody o A = 0,071 cm²
        daje 168,175 / 0,071 ≈ <b>2368,66 μA/cm²</b>. Tę wartość można porównywać
        z literaturą niezależnie od wielkości elektrody.</p>
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

        "legend_baseline_ox": "Oxidation baseline",
        "legend_baseline_red": "Reduction baseline",
        "annot_oxidation": "Oxidation",
        "annot_reduction": "Reduction",

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
            will additionally show: <b>E½</b> (half-wave potential), <b>ΔEp</b> (peak-to-peak
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
            • Click "Fit". Results: <b>FWHM</b> (Full Width at Half Maximum — the width of the peak
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

        "dlg_theory_title": "Theory — handbook",

        "theory_tab1_title_en": "Cyclic voltammetry",
        "theory_tab1_html_en": """
        <h3>Cyclic voltammetry (CV)</h3>
        <p><b>What is CV?</b> Cyclic voltammetry is an electroanalytical technique in
        which the potential of the working electrode is swept linearly in time between
        two limiting values and then reversed — forming a cycle. At the same time,
        the current flowing through the electrode is recorded.</p>

        <h3>Operating principle</h3>
        <p>The potentiostat imposes a defined potential on the working electrode relative
        to the reference electrode, and measures the current between the working electrode
        and the auxiliary (counter) electrode. The change in potential drives oxidation
        (on the rising branch) and reduction (on the falling branch) of the electroactive
        species.</p>

        <h3>Reading a voltammogram</h3>
        <ul>
            <li><b>X axis — potential E [mV or V]:</b> the imposed electrochemical driving force.</li>
            <li><b>Y axis — current I [μA]:</b> the system's response. IUPAC convention:
            anodic currents (oxidation) are positive, cathodic currents (reduction) are negative.</li>
        </ul>

        <h3>Oxidation and reduction peaks</h3>
        <p>The <b>anodic peak (ip,a)</b> appears during the forward scan toward more
        positive potentials and corresponds to oxidation of the analyte at the electrode.
        The <b>cathodic peak (ip,c)</b> appears during the reverse scan and corresponds to
        reduction of the oxidation product. The presence of both peaks indicates a process
        that is at least quasi-reversible.</p>

        <h3>Half-wave potential E½</h3>
        <p>For a reversible process, E½ is defined as the arithmetic mean of the anodic
        and cathodic peak potentials:</p>
        <p style="margin-left:2em;"><b>E½ = (E<sub>p,a</sub> + E<sub>p,c</sub>) / 2</b></p>
        <p>E½ is close to the formal redox potential and characterizes a given redox
        couple independently of the scan rate (for a reversible process).</p>

        <h3>ΔEp — peak-to-peak separation</h3>
        <p>ΔEp is the absolute difference between the anodic (oxidation) and cathodic
        (reduction) peak potentials:</p>
        <p style="margin-left:2em;"><b>ΔEp = |E<sub>p,a</sub> − E<sub>p,c</sub>|</b></p>
        <p>ΔEp is the primary criterion for the reversibility of a redox couple. For a
        reversible, one-electron process at 25 °C, the theoretical value is
        <b>ΔEp ≈ 59/n mV</b>, where n is the number of electrons transferred. ΔEp values
        close to 59/n mV indicate a reversible process; markedly larger values point to
        quasi-reversible or irreversible kinetics, often associated with slow electron
        transfer. In practice, ΔEp is also affected by solution resistance — the ohmic
        (iR) drop — which can inflate the observed value.</p>
        """,

        "theory_tab2_title_en": "Baseline",
        "theory_tab2_html_en": """
        <h3>Why baseline correction is necessary</h3>
        <p>The measured peak current is the sum of the faradaic current (redox reaction)
        and the background current — capacitive charging of the double layer and
        currents originating from the solvent/electrolyte. To determine the true
        peak height (<b>H</b>) we must subtract the background current.</p>

        <h3>How to correctly choose the baseline points</h3>
        <p>The standard method for baseline correction in CV consists of choosing
        <b>both</b> points on a <b>linear segment of the voltammogram BEFORE the peak
        rises</b> — on the <i>left</i> side of the peak, in the region where the current
        has not yet begun to rise due to the redox reaction. The baseline is then
        <b>extrapolated</b> as a straight line under the peak to estimate the background
        (non-faradaic) current that would flow if the redox reaction were not
        occurring.</p>
        <ul>
            <li>Place both points (x<sub>1</sub>, y<sub>1</sub>) and (x<sub>2</sub>, y<sub>2</sub>)
            on a <b>flat, linear segment</b> of the voltammogram preceding the peak —
            where the current changes linearly with potential and there is no
            faradaic activity yet.</li>
            <li>The straight line connecting these two points represents the
            non-faradaic current (double-layer charging, solvent/electrolyte
            background) — it is extrapolated under the peak to the position E<sub>p</sub>.</li>
            <li>The peak height H is the distance from the peak to this extrapolated
            line at the position of the maximum, not to a straight line connecting
            points on both sides of the peak.</li>
            <li>Both points should lie on the same branch of the voltammogram
            (rising or falling) and be close enough together to preserve the local
            slope of the background.</li>
            <li>In CVision you can choose the points by double-clicking or edit them
            numerically in the "Edit baseline (numeric)" window.</li>
        </ul>

        <h3>Effect of poor baseline point selection</h3>
        <ul>
            <li><b>Points on both sides of the peak</b> — the line crosses the peak
            instead of forming its background; the height H is underestimated, and
            its value depends arbitrarily on the chosen range.</li>
            <li><b>A point within the rising part of the peak</b> — the extrapolation
            becomes unnaturally skewed, producing an apparent peak or no peak at all.</li>
            <li><b>Too wide a range spanning other processes</b> — the slope of the
            line is disturbed by a neighboring peak, overestimating or underestimating H.</li>
            <li><b>Too short a linear segment</b> — the points are susceptible to
            noise, leading to large extrapolation uncertainty.</li>
        </ul>
        <p>Good practice: always visually verify that the extrapolated baseline runs
        naturally under the peak before reading off the peak parameters.</p>
        """,

        "theory_tab3_title_en": "Peak parameters",
        "theory_tab3_html_en": """
        <h3>Peak height (H) and peak depth (D)</h3>
        <p>The anodic peak height <b>H = i<sub>p,a</sub> − i<sub>baseline</sub>(E<sub>p,a</sub>)</b>
        is the distance from the maximum to the baseline at its position. Similarly,
        the cathodic peak depth <b>D = i<sub>baseline</sub>(E<sub>p,c</sub>) − i<sub>p,c</sub></b>.
        Both quantities are positive and expressed in μA (or — after calibration — in μA/cm²,
        μA/mM, μA/(cm²·mM)).</p>

        <h3>Peak current ratio i<sub>p,a</sub> / i<sub>p,c</sub></h3>
        <p>The ratio of the anodic to cathodic peak height indicates the reversibility
        of the electrochemical process:</p>
        <table border="1" cellpadding="6" cellspacing="0">
            <tr><th>i<sub>p,a</sub> / i<sub>p,c</sub></th><th>Interpretation</th></tr>
            <tr><td>≈ 1.0</td><td>Reversible process (oxidized and reduced forms stable)</td></tr>
            <tr><td>&lt; 1 or &gt; 1</td><td>Quasi-reversible process or coupled chemical reaction</td></tr>
            <tr><td>one of the peaks absent</td><td>Irreversible process</td></tr>
        </table>

        <h3>The Randles–Ševčík equation</h3>
        <p>For a reversible, diffusion-controlled process, the peak current is:</p>
        <p style="margin-left:2em;"><b>i<sub>p</sub> = 0.4463 · n · F · A · C · √(n · F · v · D / (R · T))</b></p>
        <p>At 25 °C this simplifies to i<sub>p</sub> = (2.69·10⁵) · n<sup>3/2</sup> · A · C · √(D · v).</p>
        <p><b>Meaning of the symbols:</b></p>
        <ul>
            <li><b>i<sub>p</sub></b> — peak current [A]</li>
            <li><b>n</b> — number of electrons involved in the reaction</li>
            <li><b>F</b> — Faraday constant (96,485 C/mol)</li>
            <li><b>A</b> — electrode area [cm²]</li>
            <li><b>C</b> — analyte concentration in solution [mol/cm³]</li>
            <li><b>v</b> — potential scan rate [V/s]</li>
            <li><b>D</b> — analyte diffusion coefficient [cm²/s]</li>
            <li><b>R</b> — gas constant (8.314 J/(mol·K))</li>
            <li><b>T</b> — temperature [K]</li>
        </ul>
        <p>A linear relationship between i<sub>p</sub> and √v is diagnostic of a
        diffusion-controlled process.</p>
        <p>Because the peak current i<sub>p</sub> is directly proportional to the analyte
        concentration C (per the Randles–Ševčík equation), peak height provides the basis
        for quantitative concentration determination via a calibration curve.</p>

        <h3>Automatic peak detection</h3>
        <p>The program can automatically locate peaks using the <b>find_peaks</b> method,
        which detects local maxima/minima meeting the minimum peak height and minimum
        distance between peaks criteria. This differs from manually determining peak
        parameters via the baseline: automatic detection quickly indicates peak positions,
        whereas the exact parameters (height relative to the background, baseline) are
        determined using the baseline method. The minimum height and distance criteria
        are used to filter out noise and insignificant local extrema.</p>
        """,

        "theory_tab4_title_en": "Derivatives and zero-crossings",
        "theory_tab4_html_en": """
        <h3>Why compute the derivative of a voltammogram</h3>
        <p>Derivatives help precisely locate voltammogram features that are not visible
        "by eye" in the raw signal — especially when peaks are poorly resolved,
        asymmetric, or the process is irreversible.</p>

        <h3>First derivative dI/dE</h3>
        <ul>
            <li>A zero-crossing of the first derivative corresponds to a current extremum:
            <b>dI/dE = 0</b> → maximum (oxidation peak) or minimum (reduction peak).</li>
            <li>Allows the exact E<sub>p</sub> to be found without visual guesswork.</li>
        </ul>

        <h3>Second derivative d²I/dE²</h3>
        <ul>
            <li>Zero-crossings of the second derivative mark the inflection points of
            the CV curve — useful for <b>irreversible</b> processes, where the classic
            peak does not form a clear maximum (e.g., electro-oxidation of organics).</li>
            <li>Allows the half-wave potential to be estimated even in the absence of a
            reduction peak.</li>
        </ul>

        <h3>Savitzky-Golay smoothing</h3>
        <p>Derivatives amplify noise. Before computing them, it is worth smoothing the
        signal with a Savitzky-Golay filter, which locally fits a low-degree polynomial
        by least squares, preserving the peak shape better than a moving average.</p>
        <p><b>Choosing the parameters:</b></p>
        <ul>
            <li><b>Window</b> (an odd number): the larger it is, the stronger the
            smoothing, but with a risk of flattening the peak. In practice, 7–15 points
            for a typical CV.</li>
            <li><b>Polynomial order</b>: 2 or 3 for typical shapes, 4–5 for more
            complex signals. Must be <b>smaller</b> than the window.</li>
            <li>Golden rule: increase the window only as much as needed to remove
            noise, and check that the peak amplitude does not decrease.</li>
        </ul>
        """,

        "theory_tab5_title_en": "Curve fitting",
        "theory_tab5_html_en": """
        <h3>When to use a Gaussian vs. a Lorentzian</h3>
        <table border="1" cellpadding="6" cellspacing="0">
            <tr><th>Model</th><th>Shape</th><th>Application</th></tr>
            <tr><td>Gaussian</td>
                <td>fast-decaying tails (exp(−x²))</td>
                <td>reasonably symmetric peaks, with narrow tails</td></tr>
            <tr><td>Lorentzian</td>
                <td>slowly decaying, broad tails (1/(1+x²))</td>
                <td>peaks with wider tails/wings</td></tr>
            <tr><td>Asymmetric Gaussian</td>
                <td>different σ on each side of the center</td>
                <td>clearly asymmetric peaks</td></tr>
        </table>
        <p>These models are mathematical fitting functions used to determine peak
        parameters (FWHM, center, amplitude); the choice of model is a matter of
        shape-fitting quality, not interpretation of the electrode mechanism.</p>

        <h3>FWHM — full width at half maximum</h3>
        <p><b>FWHM</b> (Full Width at Half Maximum) is the width of the peak at a
        height equal to half its amplitude. Model formulas:</p>
        <ul>
            <li>Gaussian: <b>FWHM = 2·√(2·ln2)·σ ≈ 2.3548·σ</b></li>
            <li>Lorentzian: <b>FWHM = 2·γ</b></li>
            <li>Asymmetric Gaussian: <b>FWHM = √(2·ln2)·(σ<sub>L</sub> + σ<sub>R</sub>)</b></li>
        </ul>
        <p>For a reversible process at 25 °C, the theoretical peak FWHM is ≈ 90.6/n mV
        (n — number of electrons). A significantly wider peak indicates irreversibility
        or slow transport.</p>

        <h3>Peak asymmetry</h3>
        <p>The <b>asymmetry = σ<sub>right</sub> / σ<sub>left</sub></b> coefficient:</p>
        <ul>
            <li><b>≈ 1.0</b> — symmetric peak.</li>
            <li><b>&gt; 1</b> — the right side of the peak is wider.</li>
            <li><b>&lt; 1</b> — the left side of the peak is wider.</li>
        </ul>
        <p>The direction and degree of asymmetry may signal deviations from an
        ideal, symmetric peak shape; however, their mechanistic interpretation
        requires additional knowledge of the system and does not follow
        unambiguously from the fit alone.</p>

        <h3>Coefficient of determination R²</h3>
        <p><b>R² = 1 − SS<sub>res</sub>/SS<sub>tot</sub></b> measures what percentage
        of the data's variability the model explains:</p>
        <ul>
            <li><b>R² &gt; 0.99</b> — very good fit, model adequate.</li>
            <li><b>0.95 – 0.99</b> — acceptable, but it is worth checking another
            model or narrowing the fitting range.</li>
            <li><b>&lt; 0.95</b> — model unsuitable or data noisy; consider
            smoothing or the asymmetric model.</li>
        </ul>
        """,

        "theory_tab6_title_en": "Unit calibration",
        "theory_tab6_html_en": """
        <h3>Normalization by electrode area (publication standard)</h3>
        <p>The current recorded at an electrode depends linearly on its area
        (see the Randles–Ševčík equation). Comparing absolute μA values from
        different electrodes is meaningless. This is why, in electrochemical
        publications, the standard is the <b>current density j = i / A [μA/cm²]</b>.</p>

        <h3>Determining the true electrode area (ECSA)</h3>
        <p><b>ECSA</b> (Electrochemically Active Surface Area) is the surface actually
        available for the reaction, typically larger than the geometric area for
        nanostructured electrodes. Typical methods:</p>
        <ul>
            <li><b>Randles–Ševčík method:</b> determine i<sub>p</sub> at several scan
            rates using a standard with known D and C (e.g., [Fe(CN)<sub>6</sub>]³⁻/⁴⁻),
            fit i<sub>p</sub> vs √v, and calculate A from the slope.</li>
            <li><b>Capacitive (double-layer) method:</b> from a CV without active
            redox couples, calculate the double-layer capacitance C<sub>dl</sub> and
            divide by the material's specific capacitance (typically 20–60 μF/cm²
            for metals).</li>
            <li><b>H<sub>upd</sub> oxidation method</b> (for Pt) — from the charge of
            the hydrogen desorption peaks, 210 μC/cm² for Pt(111).</li>
            <li><b>Redox probe method</b> — from CV of [Ru(NH<sub>3</sub>)<sub>6</sub>]³⁺
            or ferrocene with a known diffusion coefficient.</li>
        </ul>

        <h3>Normalization by concentration — electrochemical sensors</h3>
        <p>In sensor analytics, what matters is <b>concentration sensitivity</b>,
        expressed in μA/mM or (after additional normalization) μA/(cm²·mM). It allows
        comparing different sensor designs independently of size and calibration
        concentration.</p>

        <h3>Unit conversion in CVision</h3>
        <table border="1" cellpadding="6" cellspacing="0">
            <tr><th>Situation</th><th>Operation</th><th>Resulting unit</th></tr>
            <tr><td>No normalization</td><td>i</td><td>μA</td></tr>
            <tr><td>Normalize by A</td><td>i / A</td><td>μA/cm²</td></tr>
            <tr><td>Normalize by c</td><td>i / c</td><td>μA/mM</td></tr>
            <tr><td>Both normalizations</td><td>i / (A · c)</td><td>μA/(cm²·mM)</td></tr>
        </table>
        <p><b>Example:</b> a peak with a height of 168.175 μA for an electrode with
        A = 0.071 cm² gives 168.175 / 0.071 ≈ <b>2368.66 μA/cm²</b>. This value can
        be compared with the literature independently of electrode size.</p>
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
