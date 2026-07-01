"""
Moduł main_window.py
--------------------
Główne okno aplikacji CVision: budowa interfejsu Qt, obsługa sygnałów i interakcji
użytkownika. Obliczenia numeryczne delegowane do analysis.py, eksport do export.py.
"""

import numpy as np
from PyQt6 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg

from dialogs import (AxisSettingsDialog, BaselineSettingsDialog, PeakDetectionDialog,
                     CalibrationDialog, CurveFittingDialog)
from derivative_windows import DerivativeWindow, SecondDerivativeWindow
import analysis
from analysis import CalibrationSettings
import export as _export_module
from export import MissingXlsxwriterError
from translations import translate, set_language


class MainWindow(QtWidgets.QMainWindow):
    """
    Główne okno aplikacji do analizy woltamogramu cyklicznego.
    """
    def __init__(self):
        super().__init__()
        self.current_language = "pl"  # set early so retranslate_ui() can use it right away
        set_language(self.current_language)  # keep the module-level language (dialogs) in sync
        self.setWindowTitle(self.tr_("window_title"))
        self.E_half_line = None
        self._e_half_value = None  # stores full-precision E½ for export (BUG-07)
        self.plot_widget = pg.PlotWidget(title="Woltamogram")
        self.plot_widget.addLegend()
        self.apply_theme(0)  # index 0 = dark theme; independent of combo_theme, created later
        self.is_updating_baseline = False
        self.baseline_mode = None
        self.num_clicks = 0
        self.axis_settings = {
            'x_label': self.tr_('axis_x'),
            'y_label': 'I [μA]',
            'x_min': 0,
            'x_max': 10,
            'y_min': 0,
            'y_max': 10,
            'font': QtGui.QFont("Arial", 12)
        }
        self.calibration_settings = CalibrationSettings()
        self.current_unit_label = "μA"
        self.update_axis_settings()
        self.baseline_settings = {
            'oxidation': {'x1': 0, 'y1': 0, 'x2': 10, 'y2': 0},
            'reduction': {'x1': 0, 'y1': 0, 'x2': 10, 'y2': 0}
        }
        self.baseline_region_oxidation = None
        self.baseline_region_reduction = None
        self.baseline_line_oxidation = None
        self.baseline_line_reduction = None
        self.peak_text_oxidation = None
        self.peak_text_reduction = None
        self.ip_a_line = None
        self.ip_c_line = None
        self.peak_curve_oxidation = None
        self.peak_curve_reduction = None
        self.curve_oxidation = None   # main oxidation PlotDataItem (PERF-02)
        self.curve_reduction = None   # main reduction PlotDataItem (PERF-02)
        self.x = None
        self.y1 = None
        self.y2 = None
        self.measurement_type = 0
        self.smoothingCheckBox = QtWidgets.QCheckBox("Wygładzanie (Savitzky-Golay)")
        self.windowSpinBox = QtWidgets.QSpinBox()
        self.windowSpinBox.setRange(3, 101)
        self.windowSpinBox.setSingleStep(2)
        self.windowSpinBox.setValue(15)
        self.polySpinBox = QtWidgets.QSpinBox()
        self.polySpinBox.setRange(1, 5)
        self.polySpinBox.setValue(3)
        self.raw_y1 = None
        self.raw_y2 = None
        self.deriv_y1 = None
        self.deriv_y2 = None
        self.second_deriv_y1 = None
        self.second_deriv_y2 = None
        self.deriv_intersections = None
        self.second_deriv_intersections = None
        self.auto_peak_scatter_items = []
        self._curve_fit_dialog = None
        self.smoothingCheckBox.stateChanged.connect(self.update_plot_from_raw_data)
        # Only redraw when smoothing is actually active (QUAL-04).
        self.windowSpinBox.valueChanged.connect(
            lambda: self.update_plot_from_raw_data() if self.smoothingCheckBox.isChecked() else None
        )
        self.polySpinBox.valueChanged.connect(
            lambda: self.update_plot_from_raw_data() if self.smoothingCheckBox.isChecked() else None
        )
        self.setup_layout()
        self.resultsTable = QtWidgets.QTableWidget()
        self.resultsTable.setColumnCount(5)
        self.resultsTable.setHorizontalHeaderLabels(
            [self.tr_("col_type"), self.tr_("col_xpeak"), self.tr_("col_ypeak"),
             self.tr_("col_baseline"), self.tr_("col_hd")]
        )
        self.centralLayout.addWidget(self.resultsTable)
        self.setStatusBar(QtWidgets.QStatusBar())
        self.calibration_status_label = QtWidgets.QLabel("")
        self.statusBar().addPermanentWidget(self.calibration_status_label)
        self.proxy = pg.SignalProxy(self.plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        self.plot_widget.scene().sigMouseClicked.connect(self.on_mouse_click)
        self.retranslate_ui()  # apply the starting language (pl) to all translated widgets

    def _build_toolbar_row1(self, row):
        """Fills the first toolbar row: measurement type, file, baseline/axis settings, export."""
        self.measurement_type_combo = QtWidgets.QComboBox()
        self.measurement_type_combo.addItems(["Utlenianie", "Redukcja"])
        for i in range(self.measurement_type_combo.count()):
            self.measurement_type_combo.setItemData(
                i,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                QtCore.Qt.ItemDataRole.TextAlignmentRole
            )
        row.addWidget(self.measurement_type_combo)
        self.btn_open_file = QtWidgets.QPushButton("Wybierz plik z danymi")
        self.btn_open_file.clicked.connect(self.open_file)
        row.addWidget(self.btn_open_file)
        self.btn_baseline_edit = QtWidgets.QPushButton("Edytuj linię bazową (numerycznie)")
        self.btn_baseline_edit.clicked.connect(self.edit_baseline_settings)
        row.addWidget(self.btn_baseline_edit)
        self.btn_clear = QtWidgets.QPushButton("Wyczyść wykres")
        self.btn_clear.clicked.connect(self.clear_plot)
        row.addWidget(self.btn_clear)
        self.btn_axis_settings = QtWidgets.QPushButton("Edytuj ustawienia osi")
        self.btn_axis_settings.clicked.connect(self.edit_axis_settings)
        row.addWidget(self.btn_axis_settings)
        self.btn_calibration = QtWidgets.QPushButton("Kalibracja jednostek")
        self.btn_calibration.clicked.connect(self.edit_calibration_settings)
        row.addWidget(self.btn_calibration)
        self.btn_export = QtWidgets.QPushButton("Eksport do Excela")
        self.btn_export.clicked.connect(self.export_to_excel)
        row.addWidget(self.btn_export)
        row.addStretch()

    def _build_toolbar_row2(self, row):
        """Fills the second toolbar row: baseline pick, peak analysis, derivatives, curve fit."""
        self.btn_pick_ox = QtWidgets.QPushButton("Zakres utlenienia (2x klik)")
        self.btn_pick_ox.clicked.connect(self.pick_baseline_oxidation)
        row.addWidget(self.btn_pick_ox)
        self.btn_pick_red = QtWidgets.QPushButton("Zakres redukcji (2x klik)")
        self.btn_pick_red.clicked.connect(self.pick_baseline_reduction)
        row.addWidget(self.btn_pick_red)
        self.btn_compute_peak = QtWidgets.QPushButton("Oblicz parametry piku")
        self.btn_compute_peak.clicked.connect(self.compute_peak_parameters)
        row.addWidget(self.btn_compute_peak)
        self.btn_auto_peaks = QtWidgets.QPushButton("Wykryj piki automatycznie")
        self.btn_auto_peaks.clicked.connect(self.open_peak_detection_dialog)
        row.addWidget(self.btn_auto_peaks)
        self.btn_derivative = QtWidgets.QPushButton("Oblicz pochodną")
        self.btn_derivative.clicked.connect(self.compute_derivative)
        row.addWidget(self.btn_derivative)
        self.btn_second_deriv = QtWidgets.QPushButton("Oblicz drugą pochodną")
        self.btn_second_deriv.clicked.connect(self.compute_second_derivative)
        row.addWidget(self.btn_second_deriv)
        self.btn_curve_fit = QtWidgets.QPushButton("Dopasowanie krzywej")
        self.btn_curve_fit.clicked.connect(self.open_curve_fitting_dialog)
        row.addWidget(self.btn_curve_fit)
        row.addStretch()

    def _build_toolbar_row3(self, row):
        """Fills the third toolbar row: smoothing controls, theme, language, help/theory/about."""
        row.addWidget(self.smoothingCheckBox)
        self.label_window = QtWidgets.QLabel("Okno:")
        row.addWidget(self.label_window)
        row.addWidget(self.windowSpinBox)
        self.label_polyorder = QtWidgets.QLabel("Stopień:")
        row.addWidget(self.label_polyorder)
        row.addWidget(self.polySpinBox)
        self.combo_theme = QtWidgets.QComboBox()
        self.combo_theme.addItems(["Ciemny", "Jasny"])
        for i in range(self.combo_theme.count()):
            self.combo_theme.setItemData(
                i,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                QtCore.Qt.ItemDataRole.TextAlignmentRole
            )
        self.combo_theme.currentIndexChanged.connect(self.apply_theme)
        row.addWidget(self.combo_theme)
        self.combo_language = QtWidgets.QComboBox()
        self.combo_language.addItems(["Polski", "English"])
        for i in range(self.combo_language.count()):
            self.combo_language.setItemData(
                i,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                QtCore.Qt.ItemDataRole.TextAlignmentRole
            )
        self.combo_language.currentIndexChanged.connect(self.on_language_changed)
        row.addWidget(self.combo_language)
        self.btn_help = QtWidgets.QPushButton("Help")
        self.btn_help.clicked.connect(self.show_help)
        row.addWidget(self.btn_help)
        self.btn_theory = QtWidgets.QPushButton("Teoria")
        self.btn_theory.clicked.connect(self.show_theory)
        row.addWidget(self.btn_theory)
        self.btn_about = QtWidgets.QPushButton("About")
        self.btn_about.clicked.connect(self.show_about)
        row.addWidget(self.btn_about)
        row.addStretch()

    def setup_layout(self):
        """Assembles the main window layout from toolbar rows and the plot widget."""
        top_row1 = QtWidgets.QHBoxLayout()
        top_row2 = QtWidgets.QHBoxLayout()
        top_row3 = QtWidgets.QHBoxLayout()
        self._build_toolbar_row1(top_row1)
        self._build_toolbar_row2(top_row2)
        self._build_toolbar_row3(top_row3)
        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(top_row1)
        top_layout.addLayout(top_row2)
        top_layout.addLayout(top_row3)
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        self.centralLayout = QtWidgets.QVBoxLayout(central_widget)
        self.centralLayout.addLayout(top_layout)
        self.centralLayout.addWidget(self.plot_widget)

    def mouseMoved(self, evt):
        """Wyświetla bieżące współrzędne kursora w pasku stanu."""
        pos = evt[0]
        if self.plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self.plot_widget.getViewBox().mapSceneToView(pos)
            self.statusBar().showMessage(f"x = {mouse_point.x():.3f}, y = {mouse_point.y():.3f}")

    def apply_theme(self, index):
        """Zmienia motyw aplikacji na ciemny (indeks 0) lub jasny (indeks 1) w combo_theme.

        Rozpoznawanie po indeksie (nie po widocznym tekście pozycji) — tekst pozycji combo
        będzie w przyszłości tłumaczony, a indeks 0/1 pozostanie stały niezależnie od języka.
        """
        if index == 0:
            self.setStyleSheet("QWidget { background-color: #2e2e2e; color: white; }")
            self.plot_widget.setBackground('k')
            self.plot_widget.setStyleSheet("border: 1px solid white;")
        else:
            self.setStyleSheet("")
            self.plot_widget.setBackground('w')
            self.plot_widget.setStyleSheet("border: 1px solid black;")

    def tr_(self, key):
        """Zwraca tekst dla klucza w self.current_language; brakujący klucz -> sam klucz.

        Deleguje do translations.translate(), żeby główne okno i dialogi (które wołają
        translations.tr() bezpośrednio) czytały z jednego, wspólnego źródła prawdy.
        """
        return translate(key, self.current_language)

    def on_language_changed(self, index):
        """Przełącza język UI na podstawie indeksu combo_language (0=pl, 1=en), nie tekstu.

        Wzorowane na measurement_type_combo (odczyt currentIndex), a nie na dawnym sposobie
        działania apply_theme (który porównywał widoczny tekst pozycji).
        """
        self.current_language = "pl" if index == 0 else "en"
        set_language(self.current_language)  # keep the module-level language (dialogs) in sync
        self.retranslate_ui()

    def _set_combo_item_texts(self, combo, texts):
        """Podmienia tekst pozycji combo bez zmiany currentIndex i bez efektów ubocznych.

        setItemText nie emituje currentIndexChanged w PyQt6 (zweryfikowane), ale sygnały są
        blokowane na czas podmiany jako dodatkowe zabezpieczenie przed skutkami ubocznymi
        (np. przypadkowym przełączeniem motywu przez apply_theme).
        """
        combo.blockSignals(True)
        for i, text in enumerate(texts):
            combo.setItemText(i, text)
        combo.blockSignals(False)

    def retranslate_ui(self):
        """Ustawia teksty wszystkich widżetów przetłumaczonych do Etapu 1a, wg self.current_language.

        Etap 0: tytuł okna, 16 przycisków toolbara (rzędy 1-3), checkbox wygładzania,
        pozycje obu combo (pomiar, motyw).
        Etap 1a: etykiety „Okno:”/„Stopień:”, nagłówki tabeli wyników, tytuł wykresu.

        UWAGA — etykiety osi (x_label/y_label w self.axis_settings) celowo NIE są tu
        ustawiane. Są edytowalne przez użytkownika (AxisSettingsDialog) i w kodzie nie ma
        żadnej flagi rozróżniającej „wartość domyślna” od „wartość ustawiona ręcznie” —
        wymuszenie retłumaczenia tutaj nadpisywałoby ręczne ustawienia użytkownika przy
        każdej zmianie języka. Zamiast tego domyślne etykiety osi są tłumaczone tylko przy
        ich naturalnym (od)tworzeniu: self.tr_('axis_x') w konstruktorze (__init__) oraz
        self.tr_('axis_y_current') w dynamicznym f"{...} [{jednostka}]" w
        update_plot_from_raw_data()/on_calibration_confirmed(). Rozróżnienie default-vs-user
        dla osi nie istnieje w kodzie i wymaga osobnej decyzji projektowej, jeśli ma być
        w pełni poprawne przy przełączaniu języka.
        """
        self.setWindowTitle(self.tr_("window_title"))
        self.plot_widget.setTitle(self.tr_("plot_title"))

        self.btn_open_file.setText(self.tr_("btn_open_file"))
        self.btn_baseline_edit.setText(self.tr_("btn_baseline_edit"))
        self.btn_clear.setText(self.tr_("btn_clear"))
        self.btn_axis_settings.setText(self.tr_("btn_axis_settings"))
        self.btn_calibration.setText(self.tr_("btn_calibration"))
        self.btn_export.setText(self.tr_("btn_export"))

        self.btn_pick_ox.setText(self.tr_("btn_pick_ox"))
        self.btn_pick_red.setText(self.tr_("btn_pick_red"))
        self.btn_compute_peak.setText(self.tr_("btn_compute_peak"))
        self.btn_auto_peaks.setText(self.tr_("btn_auto_peaks"))
        self.btn_derivative.setText(self.tr_("btn_derivative"))
        self.btn_second_deriv.setText(self.tr_("btn_second_deriv"))
        self.btn_curve_fit.setText(self.tr_("btn_curve_fit"))

        self.smoothingCheckBox.setText(self.tr_("check_smoothing"))
        self.label_window.setText(self.tr_("label_window"))
        self.label_polyorder.setText(self.tr_("label_polyorder"))
        self.btn_help.setText(self.tr_("btn_help"))
        self.btn_theory.setText(self.tr_("btn_theory"))
        self.btn_about.setText(self.tr_("btn_about"))

        self._set_combo_item_texts(
            self.measurement_type_combo, [self.tr_("combo_oxidation"), self.tr_("combo_reduction")]
        )
        self._set_combo_item_texts(
            self.combo_theme, [self.tr_("combo_theme_dark"), self.tr_("combo_theme_light")]
        )

        self.resultsTable.setHorizontalHeaderLabels(
            [self.tr_("col_type"), self.tr_("col_xpeak"), self.tr_("col_ypeak"),
             self.tr_("col_baseline"), self.tr_("col_hd")]
        )

    def open_file(self):
        """Otwiera okno wyboru pliku i importuje dane z wybranego pliku."""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, self.tr_("filedlg_open_title"), "", self.tr_("filedlg_open_filter")
        )
        if file_name:
            try:
                data = np.loadtxt(file_name)
                if data.ndim != 2 or data.shape[1] < 3:
                    QtWidgets.QMessageBox.critical(
                        self, self.tr_("msg_file_error_title"),
                        self.tr_("msg_bad_columns")
                    )
                    return
                self.measurement_type = self.measurement_type_combo.currentIndex()
                if self.measurement_type == 0:
                    self.x = data[:, 0]
                    self.raw_y1 = data[:, 1]
                    self.raw_y2 = data[:, 2]
                else:
                    self.x = data[:, 0]
                    self.raw_y1 = data[:, 2]
                    self.raw_y2 = data[:, 1]
                if np.any(np.diff(self.x) < 0):
                    idx_sort = np.argsort(self.x)
                    self.x = self.x[idx_sort]
                    self.raw_y1 = self.raw_y1[idx_sort]
                    self.raw_y2 = self.raw_y2[idx_sort]
                # Set default baseline positions once on load so smoothing
                # parameter changes later do not silently reset them (BUG-02).
                new_x_min = np.min(self.x)
                new_x_max = np.max(self.x)
                new_y_min = min(np.min(self.raw_y1), np.min(self.raw_y2))
                mid_x = (new_x_min + new_x_max) / 2
                self.baseline_settings['oxidation'] = {'x1': new_x_min, 'y1': new_y_min, 'x2': mid_x,     'y2': new_y_min}
                self.baseline_settings['reduction']  = {'x1': mid_x,     'y1': new_y_min, 'x2': new_x_max, 'y2': new_y_min}
                self.update_plot_from_raw_data()
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self, self.tr_("msg_error_title"),
                    f"{self.tr_('msg_import_failed')}{str(e)}"
                )

    def update_plot_from_raw_data(self):
        """Aktualizuje wykres główny na podstawie danych surowych i opcjonalnie stosuje wygładzanie."""
        if self.x is None or self.raw_y1 is None or self.raw_y2 is None:
            return
        if self.smoothingCheckBox.isChecked():
            window_length = self.windowSpinBox.value()
            polyorder = self.polySpinBox.value()
            try:
                self.y1 = analysis.apply_smoothing(self.raw_y1, window_length, polyorder)
                self.y2 = analysis.apply_smoothing(self.raw_y2, window_length, polyorder)
            except Exception as e:
                QtWidgets.QMessageBox.warning(
                    self, self.tr_("msg_error_title"),
                    f"{self.tr_('msg_smoothing_failed')}{str(e)}"
                )
                self.y1 = self.raw_y1.copy()
                self.y2 = self.raw_y2.copy()
        else:
            self.y1 = self.raw_y1.copy()
            self.y2 = self.raw_y2.copy()
        self.y1, self.current_unit_label = analysis.apply_calibration(self.y1, self.calibration_settings)
        self.y2, _ = analysis.apply_calibration(self.y2, self.calibration_settings)
        self.axis_settings['y_label'] = f"{self.tr_('axis_y_current')} [{self.current_unit_label}]"
        self._refresh_calibration_status()
        if self.curve_oxidation is None:
            # First draw after a load or clear: rebuild the widget from scratch.
            # Also null the baseline refs so update_baseline_lines re-adds them
            # to the fresh widget rather than calling setRegion on stale items.
            self.plot_widget.clear()
            self.plot_widget.addLegend()
            self.baseline_region_oxidation = None
            self.baseline_region_reduction = None
            self.baseline_line_oxidation = None
            self.baseline_line_reduction = None
            self.curve_oxidation = self.plot_widget.plot(
                self.x, self.y1, pen=pg.mkPen(color='b', width=2), name='Utlenianie'
            )
            self.curve_reduction = self.plot_widget.plot(
                self.x, self.y2, pen=pg.mkPen(color='r', width=2), name='Redukcja'
            )
        else:
            # Subsequent smoothing changes: update data in-place to preserve zoom/pan.
            self.curve_oxidation.setData(self.x, self.y1)
            self.curve_reduction.setData(self.x, self.y2)
        self.axis_settings['x_min'] = np.min(self.x)
        self.axis_settings['x_max'] = np.max(self.x)
        self.axis_settings['y_min'] = min(np.min(self.y1), np.min(self.y2))
        self.axis_settings['y_max'] = max(np.max(self.y1), np.max(self.y2))
        self.update_axis_settings()
        # Baseline defaults are set once in open_file(); only redraw them here.
        self.update_baseline_lines()

    def clear_plot(self):
        """Czyści wykres oraz resetuje wszystkie dane i elementy graficzne."""
        self.plot_widget.clear()
        self.plot_widget.addLegend()
        self.update_axis_settings()
        for item in [self.baseline_region_oxidation, self.baseline_region_reduction,
                     self.baseline_line_oxidation, self.baseline_line_reduction,
                     self.peak_text_oxidation, self.peak_text_reduction,
                     self.ip_a_line, self.ip_c_line, self.peak_curve_oxidation, self.peak_curve_reduction]:
            if item is not None:
                self.plot_widget.removeItem(item)
        if self.E_half_line is not None:
            self.plot_widget.removeItem(self.E_half_line)
            self.E_half_line = None
        self.baseline_region_oxidation = None
        self.baseline_region_reduction = None
        self.baseline_line_oxidation = None
        self.baseline_line_reduction = None
        self.peak_text_oxidation = None
        self.peak_text_reduction = None
        self.ip_a_line = None
        self.ip_c_line = None
        self.peak_curve_oxidation = None
        self.peak_curve_reduction = None
        self.curve_oxidation = None   # null so next load triggers a full redraw (PERF-02)
        self.curve_reduction = None
        for item in self.auto_peak_scatter_items:
            self.plot_widget.removeItem(item)
        self.auto_peak_scatter_items = []
        self.resultsTable.setRowCount(0)
        self.x = None
        self.raw_y1 = None
        self.raw_y2 = None
        self.y1 = None
        self.y2 = None
        self.deriv_y1 = None
        self.deriv_y2 = None
        self.second_deriv_y1 = None
        self.second_deriv_y2 = None
        self.deriv_intersections = None
        self.second_deriv_intersections = None
        self.measurement_type = 0

    def edit_axis_settings(self):
        """Otwiera dialog edycji ustawień osi."""
        dialog = AxisSettingsDialog(self.axis_settings, self)
        dialog.applied.connect(self.on_axis_settings_applied)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.axis_settings = dialog.get_settings()
            self.update_axis_settings()

    def on_axis_settings_applied(self, settings):
        """Aktualizuje ustawienia osi po zatwierdzeniu zmian w dialogu."""
        self.axis_settings = settings
        self.update_axis_settings()

    def edit_calibration_settings(self):
        """Otwiera dialog kalibracji jednostek prądu."""
        dialog = CalibrationDialog(self.calibration_settings, self)
        dialog.calibration_confirmed.connect(self.on_calibration_confirmed)
        dialog.exec()

    def on_calibration_confirmed(self, settings):
        """Zapisuje nowe ustawienia kalibracji i odświeża wykres."""
        self.calibration_settings = settings
        if self.x is not None:
            self.update_plot_from_raw_data()
            # Drop stale peak rows — they still carry the pre-calibration numbers
            # until the user re-runs compute_peak_parameters against calibrated y.
            self.resultsTable.setRowCount(0)
            QtWidgets.QMessageBox.information(
                self, self.tr_("msg_calib_title"),
                self.tr_("msg_calib_applied")
            )
        else:
            # No data loaded yet: still refresh status label and Y axis preview.
            _, self.current_unit_label = analysis.apply_calibration(np.array([0.0]), settings)
            self.axis_settings['y_label'] = f"{self.tr_('axis_y_current')} [{self.current_unit_label}]"
            self.update_axis_settings()
            self._refresh_calibration_status()

    def _refresh_calibration_status(self):
        """Aktualizuje etykietę statusu kalibracji (ukrywa ją przy ustawieniach domyślnych)."""
        s = self.calibration_settings
        if not s.normalize_by_area and not s.normalize_by_concentration:
            self.calibration_status_label.setText("")
            return
        parts = []
        if s.normalize_by_area:
            parts.append(f"A={s.electrode_area:g} cm²")
        if s.normalize_by_concentration:
            parts.append(f"c={s.concentration:g} mM")
        self.calibration_status_label.setText(
            f"Kalibracja aktywna: {', '.join(parts)} → {self.current_unit_label}"
        )

    def edit_baseline_settings(self):
        """Otwiera dialog edycji ustawień linii bazowej."""
        dialog = BaselineSettingsDialog(self.baseline_settings, self)
        dialog.baseline_applied.connect(self.on_baseline_settings_applied)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.baseline_settings = dialog.get_settings()
            self.update_baseline_lines()

    def on_baseline_settings_applied(self, settings):
        """Aktualizuje linię bazową na podstawie ustawień z dialogu.

        The dialog (BaselineSettingsDialog) already recomputes y-values to match the
        new x positions before emitting this signal, so we trust the values as-is.
        """
        self._reset_baseline_to_edit_mode('oxidation')
        self._reset_baseline_to_edit_mode('reduction')
        self.baseline_settings = settings
        self.update_baseline_lines()

    def pick_baseline_oxidation(self):
        """Aktywuje tryb wyboru zakresu dla utlenienia poprzez dwukrotne kliknięcie."""
        if self.x is None:
            QtWidgets.QMessageBox.warning(self, self.tr_("msg_no_data_title"), self.tr_("msg_load_file_first"))
            return
        self._reset_baseline_to_edit_mode('oxidation')
        self.baseline_mode = "oxidation"
        self.num_clicks = 0
        QtWidgets.QMessageBox.information(
            self, self.tr_("msg_pick_ox_title"),
            self.tr_("msg_pick_ox_instr")
        )

    def pick_baseline_reduction(self):
        """Aktywuje tryb wyboru zakresu dla redukcji poprzez dwukrotne kliknięcie."""
        if self.x is None:
            QtWidgets.QMessageBox.warning(self, self.tr_("msg_no_data_title"), self.tr_("msg_load_file_first"))
            return
        self._reset_baseline_to_edit_mode('reduction')
        self.baseline_mode = "reduction"
        self.num_clicks = 0
        QtWidgets.QMessageBox.information(
            self, self.tr_("msg_pick_red_title"),
            self.tr_("msg_pick_red_instr")
        )

    def on_mouse_click(self, event):
        """Obsługuje kliknięcia myszą w celu wyboru punktów dla linii bazowej."""
        if self.baseline_mode is None:
            return
        if self.x is None:
            # Guard: no data loaded yet — np.interp would crash on None.
            return
        pos = event.scenePos()
        mouse_point = self.plot_widget.getViewBox().mapSceneToView(pos)
        x_click = mouse_point.x()
        y_curve = float(np.interp(x_click, self.x, self.y1 if self.baseline_mode == "oxidation" else self.y2))
        pt_key = 'x1' if self.num_clicks == 0 else 'x2'
        self.baseline_settings[self.baseline_mode][pt_key] = x_click
        self.baseline_settings[self.baseline_mode][pt_key.replace('x', 'y')] = y_curve
        if self.num_clicks == 0:
            self.num_clicks = 1
        else:
            self.num_clicks = 0
            self.baseline_mode = None
            self.update_baseline_lines()

    def update_axis_settings(self):
        """Aktualizuje etykiety oraz zakresy osi wykresu."""
        x_label = self.axis_settings.get('x_label', 'Oś X')
        y_label = self.axis_settings.get('y_label', 'Prąd')
        font = self.axis_settings.get('font', QtGui.QFont("Arial", 12))
        self.plot_widget.setLabel('bottom', text=x_label, **{'font': font})
        self.plot_widget.setLabel('left', text=y_label, **{'font': font})
        self.plot_widget.setXRange(self.axis_settings.get('x_min', 0), self.axis_settings.get('x_max', 10))
        self.plot_widget.setYRange(self.axis_settings.get('y_min', 0), self.axis_settings.get('y_max', 10))

    def update_baseline_lines(self):
        """Aktualizuje linie bazowe i regiony interaktywne.

        Na pierwszym wywołaniu (lub po wyczyszczeniu wykresu) tworzy obiekty Qt
        i podłącza sygnały. Przy kolejnych wywołaniach używa setRegion()/setData()
        zamiast usuwać i tworzyć nowe obiekty (PERF-01).
        """
        self.is_updating_baseline = True

        ox = self.baseline_settings['oxidation']
        x1_ox, y1_ox, x2_ox, y2_ox = ox['x1'], ox['y1'], ox['x2'], ox['y2']

        if self.baseline_region_oxidation is None:
            self.baseline_region_oxidation = pg.LinearRegionItem(
                values=[min(x1_ox, x2_ox), max(x1_ox, x2_ox)],
                brush=(0, 0, 255, 50),
                hoverBrush=pg.mkBrush(0, 0, 255, 20),
                movable=True
            )
            self.baseline_region_oxidation.sigRegionChanged.connect(self.on_oxidation_region_changed)
            self.plot_widget.addItem(self.baseline_region_oxidation)
        else:
            self.baseline_region_oxidation.setRegion([min(x1_ox, x2_ox), max(x1_ox, x2_ox)])

        if self.baseline_line_oxidation is None:
            self.baseline_line_oxidation = self.plot_widget.plot(
                [x1_ox, x2_ox], [y1_ox, y2_ox],
                pen=pg.mkPen(color='b', width=2, style=QtCore.Qt.PenStyle.DashLine),
                name="Baseline Utlenienia"
            )
        else:
            self.baseline_line_oxidation.setData([x1_ox, x2_ox], [y1_ox, y2_ox])

        red = self.baseline_settings['reduction']
        x1_red, y1_red, x2_red, y2_red = red['x1'], red['y1'], red['x2'], red['y2']

        if self.baseline_region_reduction is None:
            self.baseline_region_reduction = pg.LinearRegionItem(
                values=[min(x1_red, x2_red), max(x1_red, x2_red)],
                brush=(255, 0, 0, 50),
                hoverBrush=pg.mkBrush(255, 0, 0, 20),
                movable=True
            )
            self.baseline_region_reduction.sigRegionChanged.connect(self.on_reduction_region_changed)
            self.plot_widget.addItem(self.baseline_region_reduction)
        else:
            self.baseline_region_reduction.setRegion([min(x1_red, x2_red), max(x1_red, x2_red)])

        if self.baseline_line_reduction is None:
            self.baseline_line_reduction = self.plot_widget.plot(
                [x1_red, x2_red], [y1_red, y2_red],
                pen=pg.mkPen(color='r', width=2, style=QtCore.Qt.PenStyle.DashLine),
                name="Baseline Redukcji"
            )
        else:
            self.baseline_line_reduction.setData([x1_red, x2_red], [y1_red, y2_red])

        self.is_updating_baseline = False

    def on_oxidation_region_changed(self):
        """Obsługuje zmianę regionu interaktywnego dla utlenienia."""
        if self.is_updating_baseline:
            return
        self._reset_baseline_to_edit_mode('oxidation')
        x_min, x_max = self.baseline_region_oxidation.getRegion()
        # Snap y-values to the actual oxidation curve at the new boundary positions
        y1 = float(np.interp(x_min, self.x, self.y1))
        y2 = float(np.interp(x_max, self.x, self.y1))
        self.baseline_settings['oxidation'] = {'x1': x_min, 'y1': y1, 'x2': x_max, 'y2': y2}
        self.update_baseline_lines()

    def on_reduction_region_changed(self):
        """Obsługuje zmianę regionu interaktywnego dla redukcji."""
        if self.is_updating_baseline:
            return
        self._reset_baseline_to_edit_mode('reduction')
        x_min, x_max = self.baseline_region_reduction.getRegion()
        # Snap y-values to the actual reduction curve at the new boundary positions
        y1 = float(np.interp(x_min, self.x, self.y2))
        y2 = float(np.interp(x_max, self.x, self.y2))
        self.baseline_settings['reduction'] = {'x1': x_min, 'y1': y1, 'x2': x_max, 'y2': y2}
        self.update_baseline_lines()

    def _reset_baseline_to_edit_mode(self, kind):
        """
        Restore the edit-phase look for one baseline ('oxidation' or 'reduction'): drop its
        post-peak curve fill (if any) and make the LinearRegionItem's fill visible again,
        without touching its draggable edges. Called whenever the user starts editing that
        baseline again (drag, numeric dialog, or a fresh 2x-click pick) so a leftover fill
        never keeps referring to a baseline that is no longer current.
        """
        if kind == 'oxidation':
            fill_item, region, edit_brush = self.peak_curve_oxidation, self.baseline_region_oxidation, (0, 0, 255, 50)
        else:
            fill_item, region, edit_brush = self.peak_curve_reduction, self.baseline_region_reduction, (255, 0, 0, 50)

        if fill_item is not None:
            self.plot_widget.removeItem(fill_item)
            if kind == 'oxidation':
                self.peak_curve_oxidation = None
            else:
                self.peak_curve_reduction = None
        if region is not None:
            region.setBrush(pg.mkBrush(*edit_brush))

    def _compute_single_peak(self, y_data, baseline_settings, mode):
        """
        Compute one peak (oxidation or reduction), draw its Qt annotations, and insert a table row.

        Returns the analysis result dict (with x_peak, y_peak, baseline_val, height/depth,
        x_region, peak_height_curve, summary), or None when no data falls in the region.
        The relevant PlotDataItem/TextItem references are stored as instance attributes.

        On success, this also switches that baseline's LinearRegionItem into "post-peak"
        display: its fill becomes transparent (the draggable edges are untouched) and a
        FillBetweenItem shades the actual area between the curve and the baseline over the
        region the height/depth was measured on.
        """
        if mode == 'oxidation':
            result = analysis.compute_oxidation_peak(self.x, y_data, baseline_settings)
            label, text_color, line_color = "Utlenienie", 'b', 'b'
            h_key, ip_name = 'height', "Ip,a"
            ip_y = lambda r: [r['baseline_val'], r['y_peak']]
            fill_brush = (0, 0, 255, 60)
            region = self.baseline_region_oxidation
        else:
            result = analysis.compute_reduction_peak(self.x, y_data, baseline_settings)
            label, text_color, line_color = "Redukcja", 'r', 'r'
            h_key, ip_name = 'depth', "Ip,c"
            ip_y = lambda r: [r['y_peak'], r['baseline_val']]
            fill_brush = (255, 0, 0, 60)
            region = self.baseline_region_reduction

        if result is None:
            return None

        h_or_d = result[h_key]
        text = (f"{label}:\nx_peak = {result['x_peak']:.3f}\ny_peak = {result['y_peak']:.3f}\n"
                f"baseline = {result['baseline_val']:.3f}\n{h_key} = {h_or_d:.3f}")
        peak_text = pg.TextItem(text=text, color=text_color, anchor=(0.5, -1.0))
        peak_text.setPos(result['x_peak'], result['y_peak'])
        self.plot_widget.addItem(peak_text)
        ip_line = self.plot_widget.plot(
            [result['x_peak'], result['x_peak']], ip_y(result),
            pen=pg.mkPen(color=line_color, width=2, style=QtCore.Qt.PenStyle.DashLine), name=ip_name
        )

        # Shade the exact area height/depth was measured over (curve vs baseline), at the
        # real y-coordinates. Replaces the old "Peak Height" line, which plotted the
        # baseline-subtracted values (peak_height_curve) and so floated near y=0,
        # disconnected from where the peak actually sits on the plot.
        x1, y1_b = baseline_settings['x1'], baseline_settings['y1']
        x2, y2_b = baseline_settings['x2'], baseline_settings['y2']
        baseline_curve = analysis.compute_baseline_curve(result['x_region'], x1, y1_b, x2, y2_b)
        y_curve_region = result['peak_height_curve'] + baseline_curve
        curve_item = pg.PlotCurveItem(result['x_region'], y_curve_region)
        baseline_item = pg.PlotCurveItem(result['x_region'], baseline_curve)
        peak_fill = pg.FillBetweenItem(curve_item, baseline_item, brush=pg.mkBrush(*fill_brush))
        self.plot_widget.addItem(peak_fill)

        if region is not None:
            region.setBrush(pg.mkBrush(0, 0, 0, 0))  # transparent: edges stay draggable

        self.insert_result_row(label, result['x_peak'], result['y_peak'], result['baseline_val'], h_or_d)

        if mode == 'oxidation':
            self.peak_text_oxidation = peak_text
            self.ip_a_line = ip_line
            self.peak_curve_oxidation = peak_fill
        else:
            self.peak_text_reduction = peak_text
            self.ip_c_line = ip_line
            self.peak_curve_reduction = peak_fill

        return result

    def compute_peak_parameters(self):
        """Oblicza parametry piku na podstawie danych i aktualnych ustawień linii bazowych."""
        if self.x is None:
            QtWidgets.QMessageBox.warning(self, self.tr_("msg_no_data_title"), self.tr_("msg_import_first"))
            return
        # Remove all previous peak annotations and the E½ line so a partial
        # re-computation cannot leave a stale line from the prior run (BUG-06).
        if self.E_half_line is not None:
            self.plot_widget.removeItem(self.E_half_line)
            self.E_half_line = None
        self._e_half_value = None
        for item in [self.peak_text_oxidation, self.peak_text_reduction, self.ip_a_line,
                     self.ip_c_line, self.peak_curve_oxidation, self.peak_curve_reduction]:
            if item is not None:
                self.plot_widget.removeItem(item)
        self.peak_text_oxidation = None
        self.peak_text_reduction = None
        self.ip_a_line = None
        self.ip_c_line = None
        self.peak_curve_oxidation = None
        self.peak_curve_reduction = None
        # Restore both regions to the visible edit-mode fill; _compute_single_peak makes a
        # region transparent again only if it actually finds a peak on that side, so a side
        # that fails this time doesn't stay stuck transparent with nothing drawn over it.
        for region, edit_brush in (
            (self.baseline_region_oxidation, (0, 0, 255, 50)),
            (self.baseline_region_reduction, (255, 0, 0, 50)),
        ):
            if region is not None:
                region.setBrush(pg.mkBrush(*edit_brush))
        # Clear all previous results before re-inserting.
        self.resultsTable.setRowCount(0)

        ox_result = self._compute_single_peak(self.y1, self.baseline_settings['oxidation'], 'oxidation')
        red_result = self._compute_single_peak(self.y2, self.baseline_settings['reduction'], 'reduction')

        if ox_result and red_result:
            E_half = analysis.compute_e_half(ox_result['x_peak'], red_result['x_peak'])
            self._e_half_value = E_half  # store full-precision float for export (BUG-07)
            self.insert_result_row("E1/2", E_half, "", "", "")
            self.E_half_line = pg.InfiniteLine(
                pos=E_half, angle=90,
                pen=pg.mkPen(color='g', width=2, style=QtCore.Qt.PenStyle.DashLine)
            )
            self.plot_widget.addItem(self.E_half_line)

            delta_ep = analysis.compute_delta_ep(ox_result['x_peak'], red_result['x_peak'])
            peak_ratio = analysis.compute_peak_current_ratio(ox_result['height'], red_result['depth'])
            self.insert_result_row("ΔEp [mV]", delta_ep, "", "", "")
            self.insert_result_row("Ipa/Ipc", peak_ratio, "", "", "")

        if ox_result or red_result:
            self.statusBar().showMessage(self.tr_("status_peak_computed"), 5000)

    def open_peak_detection_dialog(self):
        """Otwiera dialog automatycznego wykrywania pików."""
        if self.x is None:
            QtWidgets.QMessageBox.warning(self, self.tr_("msg_no_data_title"), self.tr_("msg_import_first"))
            return
        dialog = PeakDetectionDialog(self)
        dialog.detection_confirmed.connect(self._on_peak_detection_confirmed)
        dialog.exec()

    def _on_peak_detection_confirmed(self, min_height, min_distance, detect_ox, detect_red):
        """Uruchamia detekcję pików i nanosi wyniki na wykres oraz do tabeli."""
        for item in self.auto_peak_scatter_items:
            self.plot_widget.removeItem(item)
        self.auto_peak_scatter_items = []

        height_filter = min_height if min_height > 0.0 else None
        total_found = 0

        if detect_ox:
            ox_peaks = analysis.detect_peaks(self.x, self.y1, 'oxidation',
                                             min_height=height_filter,
                                             min_distance=min_distance)
            for peak in ox_peaks:
                scatter = self.plot_widget.plot(
                    [peak['x']], [peak['y']],
                    pen=None, symbol='o',
                    symbolBrush=pg.mkBrush(255, 255, 0, 220),
                    symbolSize=10,
                )
                self.auto_peak_scatter_items.append(scatter)
                self.insert_result_row("Pik auto (utl)", peak['x'], peak['y'], "", peak['height'])
            total_found += len(ox_peaks)

        if detect_red:
            red_peaks = analysis.detect_peaks(self.x, self.y2, 'reduction',
                                              min_height=height_filter,
                                              min_distance=min_distance)
            for peak in red_peaks:
                scatter = self.plot_widget.plot(
                    [peak['x']], [peak['y']],
                    pen=None, symbol='o',
                    symbolBrush=pg.mkBrush(255, 255, 0, 220),
                    symbolSize=10,
                )
                self.auto_peak_scatter_items.append(scatter)
                self.insert_result_row("Pik auto (red)", peak['x'], peak['y'], "", peak['height'])
            total_found += len(red_peaks)

        if total_found == 0:
            QtWidgets.QMessageBox.information(
                self, self.tr_("msg_no_peaks_title"),
                self.tr_("msg_no_peaks_found")
            )

    def insert_result_row(self, peak_type, x_peak, y_peak, baseline, h_or_d):
        """Wstawia nowy wiersz do tabeli wyników."""
        row = self.resultsTable.rowCount()
        self.resultsTable.insertRow(row)
        self.resultsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(peak_type)))
        self.resultsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(f"{x_peak:.3f}" if isinstance(x_peak, (int, float)) else ""))
        self.resultsTable.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{y_peak:.3f}" if isinstance(y_peak, (int, float)) else ""))
        self.resultsTable.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{baseline:.3f}" if isinstance(baseline, (int, float)) else ""))
        self.resultsTable.setItem(row, 4, QtWidgets.QTableWidgetItem(f"{h_or_d:.3f}" if isinstance(h_or_d, (int, float)) else ""))

    def compute_derivative(self):
        """Oblicza pierwsze pochodne i otwiera okno analizy pochodnych."""
        if self.x is None or self.y1 is None or self.y2 is None:
            QtWidgets.QMessageBox.warning(self, self.tr_("msg_no_data_title"), self.tr_("msg_import_first"))
            return
        self.deriv_y1, self.deriv_y2 = analysis.compute_derivatives(self.x, self.y1, self.y2)
        derivative_window = DerivativeWindow(self.x, self.deriv_y1, self.deriv_y2, self)
        derivative_window.exec()
        zeros = derivative_window.intersections
        if zeros:
            for x0, y0 in zeros:
                self.insert_result_row("Zero crossing", x0, y0, "", "")
        self.deriv_intersections = zeros

    def compute_second_derivative(self):
        """Oblicza drugie pochodne i otwiera okno analizy drugich pochodnych."""
        if self.x is None or self.y1 is None or self.y2 is None:
            QtWidgets.QMessageBox.warning(self, self.tr_("msg_no_data_title"), self.tr_("msg_import_first"))
            return
        self.second_deriv_y1, self.second_deriv_y2 = analysis.compute_second_derivatives(
            self.x, self.y1, self.y2
        )
        second_derivative_window = SecondDerivativeWindow(
            self.x, self.second_deriv_y1, self.second_deriv_y2, self
        )
        second_derivative_window.exec()
        zeros2 = second_derivative_window.intersections
        if zeros2:
            for x0, y0 in zeros2:
                self.insert_result_row("Zero crossing 2nd", x0, y0, "", "")
        self.second_deriv_intersections = zeros2

    def open_curve_fitting_dialog(self):
        """Otwiera niemodalny dialog dopasowania krzywej (Gauss/Lorentz/asymetryczny)."""
        if self.x is None or self.y1 is None or self.y2 is None:
            QtWidgets.QMessageBox.warning(self, self.tr_("msg_no_data_title"), self.tr_("msg_import_first"))
            return
        if self._curve_fit_dialog is not None:
            self._curve_fit_dialog.close()
        self._curve_fit_dialog = CurveFittingDialog(
            x=self.x, y1=self.y1, y2=self.y2,
            baseline_settings=self.baseline_settings,
            x_label=self.axis_settings.get('x_label', 'E [mV]'),
            y_unit_label=self.current_unit_label,
            parent=self,
        )
        self._curve_fit_dialog.fit_added_to_table.connect(self._on_curve_fit_added)
        self._curve_fit_dialog.show()

    def _on_curve_fit_added(self, label, center, amplitude, r_squared, fwhm):
        """Dodaje wiersz z parametrami dopasowania do tabeli wyników."""
        self.insert_result_row(label, center, amplitude, r_squared, fwhm)

    def export_to_excel(self):
        """Eksportuje dane, parametry i wykres do pliku Excel."""
        if self.x is None:
            QtWidgets.QMessageBox.warning(self, self.tr_("msg_no_data_title"), self.tr_("msg_no_export_data"))
            return
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, self.tr_("filedlg_save_title"), "", self.tr_("filedlg_save_filter")
        )
        if not filename:
            return
        # Read table contents here so export.py receives plain data, not Qt widgets.
        table_data = []
        for row in range(self.resultsTable.rowCount()):
            row_data = {}
            for col in range(self.resultsTable.columnCount()):
                header = self.resultsTable.horizontalHeaderItem(col).text()
                item = self.resultsTable.item(row, col)
                row_data[header] = item.text() if item is not None else ""
            table_data.append(row_data)
        try:
            _export_module.export_to_excel(
                filename=filename,
                x=self.x,
                raw_y1=self.raw_y1,
                raw_y2=self.raw_y2,
                y1=self.y1,
                y2=self.y2,
                smoothing_active=self.smoothingCheckBox.isChecked(),
                deriv_y1=self.deriv_y1,
                deriv_y2=self.deriv_y2,
                second_deriv_y1=self.second_deriv_y1,
                second_deriv_y2=self.second_deriv_y2,
                table_data=table_data,
                deriv_intersections=self.deriv_intersections,
                second_deriv_intersections=self.second_deriv_intersections,
                e_half_value=self._e_half_value,
                measurement_type=self.measurement_type,
                calibration_settings=self.calibration_settings,
                calibration_unit_label=self.current_unit_label,
            )
            QtWidgets.QMessageBox.information(
                self, self.tr_("msg_success_title"), f"{self.tr_('msg_export_success')}{filename}"
            )
        except MissingXlsxwriterError:
            QtWidgets.QMessageBox.critical(
                self, self.tr_("msg_error_title"), self.tr_("msg_missing_xlsxwriter")
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, self.tr_("msg_error_title"), f"{self.tr_('msg_export_error')}{str(e)}"
            )

    def show_help(self):
        # Reads the current language once, at open time (no live retranslation),
        # same convention as the standalone dialogs.
        help_text = self.tr_(f"help_html_{self.current_language}")
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(self.tr_("dlg_help_title"))
        dialog.setMinimumSize(400, 300)
        dialog.resize(700, 600)
        layout = QtWidgets.QVBoxLayout(dialog)
        browser = QtWidgets.QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setHtml(help_text)
        layout.addWidget(browser)
        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch(1)
        close_btn = QtWidgets.QPushButton(self.tr_("btn_close"))
        close_btn.clicked.connect(dialog.accept)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)
        # Center the dialog on the main window before showing it.
        geom = dialog.frameGeometry()
        geom.moveCenter(self.geometry().center())
        dialog.move(geom.topLeft())
        dialog.exec()

    def show_about(self):
        about_text = """
        <html>
        <body>
            <h4 align="center">CVision</h4>
            <h4>Analiza woltamogramu cyklicznego</h4>
            <p>Wersja: 3.2</p>
            <p><b>Nowości w wersji 3.2:</b></p>
            <ul>
                <li>Czytelniejsza wizualizacja linii bazowej — po obliczeniu parametrów piku
                    zakres bazy jest pokazywany jako wypełnienie obszaru pod/nad krzywą
                    względem linii bazowej (zamiast pełnego pionowego pasa)</li>
                <li>Poprawki stabilności: obsługa błędu wygładzania dla krótkich serii danych,
                    bezpieczny zapis pliku Excel</li>
            </ul>
            <p><b>Nowości w wersji 3.1:</b></p>
            <ul>
                <li>ΔEp — rozdzielenie potencjałów pików (parametr diagnostyczny odwracalności)</li>
                <li>Ipa/Ipc — stosunek prądów pików anodowego i katodowego (parametr odwracalności)</li>
            </ul>
            <p><b>Nowości w wersji 3.0:</b></p>
            <ul>
                <li>Automatyczne wykrywanie pików (scipy.signal.find_peaks)</li>
                <li>Kalibracja jednostek — normalizacja prądu względem powierzchni
                    elektrody i/lub stężenia analitu (μA → μA/cm², μA/mM, μA/(cm²·mM))</li>
                <li>Dopasowanie krzywej — modele Gaussowski, Lorentzowski
                    oraz asymetryczny Gaussowski z wyznaczaniem FWHM i R²</li>
            </ul>
            <p>Autor: <b>StarGate3</b><br/>
            GitHub: <a href='https://github.com/StarGate3'>github.com/StarGate3</a>
            </p>
        </body>
        </html>
        """
        QtWidgets.QMessageBox.about(self, "About", about_text)

    def show_theory(self):
        """Otwiera okno z podręcznikiem teoretycznym CV (6 zakładek)."""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(self.tr_("dlg_theory_title"))
        dialog.resize(780, 620)
        layout = QtWidgets.QVBoxLayout(dialog)
        tabs = QtWidgets.QTabWidget()
        tabs.setStyleSheet("""
            QTabBar::tab {
                background-color: #555555;
                color: #ffffff;
                padding: 6px 12px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #0078d4;
                color: #ffffff;
            }
            QTabBar::tab:hover {
                background-color: #666666;
                color: #ffffff;
            }
        """)
        for title, html in self._theory_tabs():
            scroll = QtWidgets.QScrollArea()
            scroll.setWidgetResizable(True)
            label = QtWidgets.QLabel(html)
            label.setWordWrap(True)
            label.setTextFormat(QtCore.Qt.TextFormat.RichText)
            label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
            label.setOpenExternalLinks(True)
            label.setMargin(12)
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
            scroll.setWidget(label)
            tabs.addTab(scroll, title)
        layout.addWidget(tabs)
        close_btn = QtWidgets.QPushButton(self.tr_("btn_close"))
        close_btn.clicked.connect(dialog.accept)
        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch(1)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)
        dialog.exec()

    def _theory_tabs(self):
        """Zwraca listę krotek (tytuł_zakładki, html) z treścią teoretyczną, wg bieżącego języka.

        Każda zakładka ma klucze theory_tabN_title_{lang}/theory_tabN_html_{lang} w
        translations.py. Na razie tylko zakładka 1 ma prawdziwe tłumaczenie EN — zakładki
        2-6 mają _en identyczne z _pl (placeholder do przetłumaczenia w kolejnych krokach),
        więc mechanizm jest już wspólny dla wszystkich sześciu i nie wymaga zmian, gdy
        kolejne zakładki dostaną właściwe tłumaczenia.
        """
        lang = self.current_language
        return [
            (self.tr_(f"theory_tab{n}_title_{lang}"), self.tr_(f"theory_tab{n}_html_{lang}"))
            for n in range(1, 7)
        ]
