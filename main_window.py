"""
Moduł main_window.py
--------------------
Główne okno aplikacji CVision: budowa interfejsu Qt, obsługa sygnałów i interakcji
użytkownika. Obliczenia numeryczne delegowane do analysis.py, eksport do export.py.
"""

import numpy as np
from PyQt6 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg

from dialogs import AxisSettingsDialog, BaselineSettingsDialog
from derivative_windows import DerivativeWindow, SecondDerivativeWindow
import analysis
import export as _export_module


class MainWindow(QtWidgets.QMainWindow):
    """
    Główne okno aplikacji do analizy woltamogramu cyklicznego.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CVision: Analiza woltamogramu cyklicznego")
        self.E_half_line = None
        self._e_half_value = None  # stores full-precision E½ for export (BUG-07)
        self.plot_widget = pg.PlotWidget(title="Woltamogram")
        self.plot_widget.addLegend()
        self.apply_theme("Ciemny")
        self.is_updating_baseline = False
        self.baseline_mode = None
        self.num_clicks = 0
        self.axis_settings = {
            'x_label': 'E [mV]',
            'y_label': 'I [μA]',
            'x_min': 0,
            'x_max': 10,
            'y_min': 0,
            'y_max': 10,
            'font': QtGui.QFont("Arial", 12)
        }
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
        self.resultsTable.setHorizontalHeaderLabels(["Typ", "x_peak", "y_peak", "Baseline", "H/D"])
        self.centralLayout.addWidget(self.resultsTable)
        self.setStatusBar(QtWidgets.QStatusBar())
        self.proxy = pg.SignalProxy(self.plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        self.plot_widget.scene().sigMouseClicked.connect(self.on_mouse_click)

    def _build_toolbar_row1(self, row):
        """Fills the first toolbar row: measurement type, file, baseline/axis settings, export, help."""
        self.measurement_type_combo = QtWidgets.QComboBox()
        self.measurement_type_combo.addItems(["Utlenianie", "Redukcja"])
        for i in range(self.measurement_type_combo.count()):
            self.measurement_type_combo.setItemData(
                i,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                QtCore.Qt.ItemDataRole.TextAlignmentRole
            )
        row.addWidget(self.measurement_type_combo)
        btn_select_file = QtWidgets.QPushButton("Wybierz plik z danymi")
        btn_select_file.clicked.connect(self.open_file)
        row.addWidget(btn_select_file)
        btn_baseline_settings = QtWidgets.QPushButton("Edytuj linię bazową (numerycznie)")
        btn_baseline_settings.clicked.connect(self.edit_baseline_settings)
        row.addWidget(btn_baseline_settings)
        btn_clear = QtWidgets.QPushButton("Wyczyść wykres")
        btn_clear.clicked.connect(self.clear_plot)
        row.addWidget(btn_clear)
        btn_axis_settings = QtWidgets.QPushButton("Edytuj ustawienia osi")
        btn_axis_settings.clicked.connect(self.edit_axis_settings)
        row.addWidget(btn_axis_settings)
        btn_export = QtWidgets.QPushButton("Eksport do Excela")
        btn_export.clicked.connect(self.export_to_excel)
        row.addWidget(btn_export)
        btn_help = QtWidgets.QPushButton("Help")
        btn_help.clicked.connect(self.show_help)
        row.addWidget(btn_help)
        btn_about = QtWidgets.QPushButton("About")
        btn_about.clicked.connect(self.show_about)
        row.addWidget(btn_about)

    def _build_toolbar_row2(self, row):
        """Fills the second toolbar row: baseline pick, peak analysis, derivatives, theme, smoothing."""
        btn_pick_ox = QtWidgets.QPushButton("Zakres utlenienia (2x klik)")
        btn_pick_ox.clicked.connect(self.pick_baseline_oxidation)
        row.addWidget(btn_pick_ox)
        btn_pick_red = QtWidgets.QPushButton("Zakres redukcji (2x klik)")
        btn_pick_red.clicked.connect(self.pick_baseline_reduction)
        row.addWidget(btn_pick_red)
        btn_compute_peak = QtWidgets.QPushButton("Oblicz parametry piku")
        btn_compute_peak.clicked.connect(self.compute_peak_parameters)
        row.addWidget(btn_compute_peak)
        btn_derivative = QtWidgets.QPushButton("Oblicz pochodną")
        btn_derivative.clicked.connect(self.compute_derivative)
        row.addWidget(btn_derivative)
        btn_second_derivative = QtWidgets.QPushButton("Oblicz drugą pochodną")
        btn_second_derivative.clicked.connect(self.compute_second_derivative)
        row.addWidget(btn_second_derivative)
        self.combo_theme = QtWidgets.QComboBox()
        self.combo_theme.addItems(["Ciemny", "Jasny"])
        for i in range(self.combo_theme.count()):
            self.combo_theme.setItemData(
                i,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                QtCore.Qt.ItemDataRole.TextAlignmentRole
            )
        self.combo_theme.currentTextChanged.connect(self.apply_theme)
        row.addWidget(self.combo_theme)
        row.addWidget(self.smoothingCheckBox)
        row.addWidget(QtWidgets.QLabel("Okno:"))
        row.addWidget(self.windowSpinBox)
        row.addWidget(QtWidgets.QLabel("Stopień:"))
        row.addWidget(self.polySpinBox)

    def setup_layout(self):
        """Assembles the main window layout from toolbar rows and the plot widget."""
        top_row1 = QtWidgets.QHBoxLayout()
        top_row2 = QtWidgets.QHBoxLayout()
        self._build_toolbar_row1(top_row1)
        self._build_toolbar_row2(top_row2)
        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(top_row1)
        top_layout.addLayout(top_row2)
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

    def apply_theme(self, theme):
        """Zmienia motyw aplikacji na ciemny lub jasny."""
        if theme == "Ciemny":
            self.setStyleSheet("QWidget { background-color: #2e2e2e; color: white; }")
            self.plot_widget.setBackground('k')
            self.plot_widget.setStyleSheet("border: 1px solid white;")
        else:
            self.setStyleSheet("")
            self.plot_widget.setBackground('w')
            self.plot_widget.setStyleSheet("border: 1px solid black;")

    def open_file(self):
        """Otwiera okno wyboru pliku i importuje dane z wybranego pliku."""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Wybierz plik z danymi", "", "Pliki tekstowe (*.txt);;Wszystkie pliki (*)"
        )
        if file_name:
            try:
                data = np.loadtxt(file_name)
                if data.ndim != 2 or data.shape[1] < 3:
                    QtWidgets.QMessageBox.critical(
                        self, "Błąd pliku",
                        "Plik musi zawierać dokładnie 3 kolumny: E, I_ox, I_red."
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
                QtWidgets.QMessageBox.critical(self, "Błąd", f"Nie udało się zaimportować danych z pliku.\n{str(e)}")

    def update_plot_from_raw_data(self):
        """Aktualizuje wykres główny na podstawie danych surowych i opcjonalnie stosuje wygładzanie."""
        if self.x is None or self.raw_y1 is None or self.raw_y2 is None:
            return
        if self.smoothingCheckBox.isChecked():
            window_length = self.windowSpinBox.value()
            polyorder = self.polySpinBox.value()
            self.y1 = analysis.apply_smoothing(self.raw_y1, window_length, polyorder)
            self.y2 = analysis.apply_smoothing(self.raw_y2, window_length, polyorder)
        else:
            self.y1 = self.raw_y1.copy()
            self.y2 = self.raw_y2.copy()
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
        self.baseline_settings = settings
        self.update_baseline_lines()

    def pick_baseline_oxidation(self):
        """Aktywuje tryb wyboru zakresu dla utlenienia poprzez dwukrotne kliknięcie."""
        if self.x is None:
            QtWidgets.QMessageBox.warning(self, "Brak danych", "Najpierw wczytaj plik danych.")
            return
        self.baseline_mode = "oxidation"
        self.num_clicks = 0
        QtWidgets.QMessageBox.information(
            self, "Zakres utlenienia",
            "Kliknij dwa razy w obszar wykresu, aby wybrać punkty (x1,y1) oraz (x2,y2) dla utlenienia."
        )

    def pick_baseline_reduction(self):
        """Aktywuje tryb wyboru zakresu dla redukcji poprzez dwukrotne kliknięcie."""
        if self.x is None:
            QtWidgets.QMessageBox.warning(self, "Brak danych", "Najpierw wczytaj plik danych.")
            return
        self.baseline_mode = "reduction"
        self.num_clicks = 0
        QtWidgets.QMessageBox.information(
            self, "Zakres redukcji",
            "Kliknij dwa razy w obszar wykresu, aby wybrać punkty (x1,y1) oraz (x2,y2) dla redukcji."
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
        x_min, x_max = self.baseline_region_reduction.getRegion()
        # Snap y-values to the actual reduction curve at the new boundary positions
        y1 = float(np.interp(x_min, self.x, self.y2))
        y2 = float(np.interp(x_max, self.x, self.y2))
        self.baseline_settings['reduction'] = {'x1': x_min, 'y1': y1, 'x2': x_max, 'y2': y2}
        self.update_baseline_lines()

    def _compute_single_peak(self, y_data, baseline_settings, mode):
        """
        Compute one peak (oxidation or reduction), draw its Qt annotations, and insert a table row.

        Returns the analysis result dict (with x_peak, y_peak, baseline_val, height/depth,
        x_region, peak_height_curve, summary), or None when no data falls in the region.
        The relevant PlotDataItem/TextItem references are stored as instance attributes.
        """
        if mode == 'oxidation':
            result = analysis.compute_oxidation_peak(self.x, y_data, baseline_settings)
            label, text_color, line_color, curve_color = "Utlenienie", 'b', 'b', 'c'
            h_key, ip_name, curve_name = 'height', "Ip,a", "Peak Height Ox"
            ip_y = lambda r: [r['baseline_val'], r['y_peak']]
        else:
            result = analysis.compute_reduction_peak(self.x, y_data, baseline_settings)
            label, text_color, line_color, curve_color = "Redukcja", 'r', 'r', 'm'
            h_key, ip_name, curve_name = 'depth', "Ip,c", "Peak Height Red"
            ip_y = lambda r: [r['y_peak'], r['baseline_val']]

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
        peak_curve = self.plot_widget.plot(
            result['x_region'], result['peak_height_curve'],
            pen=pg.mkPen(color=curve_color, width=2), name=curve_name
        )
        self.insert_result_row(label, result['x_peak'], result['y_peak'], result['baseline_val'], h_or_d)

        if mode == 'oxidation':
            self.peak_text_oxidation = peak_text
            self.ip_a_line = ip_line
            self.peak_curve_oxidation = peak_curve
        else:
            self.peak_text_reduction = peak_text
            self.ip_c_line = ip_line
            self.peak_curve_reduction = peak_curve

        return result

    def compute_peak_parameters(self):
        """Oblicza parametry piku na podstawie danych i aktualnych ustawień linii bazowych."""
        if self.x is None:
            QtWidgets.QMessageBox.warning(self, "Brak danych", "Najpierw zaimportuj dane.")
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
        # Clear all previous results before re-inserting.
        self.resultsTable.setRowCount(0)

        ox_result = self._compute_single_peak(self.y1, self.baseline_settings['oxidation'], 'oxidation')
        red_result = self._compute_single_peak(self.y2, self.baseline_settings['reduction'], 'reduction')
        results = (ox_result['summary'] if ox_result else "Utlenienie: brak danych w zadanym zakresie.\n\n")
        results += (red_result['summary'] if red_result else "Redukcja: brak danych w zadanym zakresie.\n")

        if ox_result and red_result:
            E_half = analysis.compute_e_half(ox_result['x_peak'], red_result['x_peak'])
            self._e_half_value = E_half  # store full-precision float for export (BUG-07)
            self.insert_result_row("E1/2", E_half, "", "", "")
            self.E_half_line = pg.InfiniteLine(
                pos=E_half, angle=90,
                pen=pg.mkPen(color='g', width=2, style=QtCore.Qt.PenStyle.DashLine)
            )
            self.plot_widget.addItem(self.E_half_line)
            results += f"E1/2: {E_half:.3f}\n"

        QtWidgets.QMessageBox.information(self, "Parametry piku", results)

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
            QtWidgets.QMessageBox.warning(self, "Brak danych", "Najpierw zaimportuj dane.")
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
            QtWidgets.QMessageBox.warning(self, "Brak danych", "Najpierw zaimportuj dane.")
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

    def export_to_excel(self):
        """Eksportuje dane, parametry i wykres do pliku Excel."""
        if self.x is None:
            QtWidgets.QMessageBox.warning(self, "Brak danych", "Brak danych do eksportu.")
            return
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Zapisz do Excela", "", "Excel Files (*.xlsx)"
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
            )
            QtWidgets.QMessageBox.information(
                self, "Sukces", f"Dane oraz wykres zostały zapisane do pliku {filename}"
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas zapisu do pliku:\n{str(e)}")

    def show_help(self):
        help_text = """
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
            <i>Uwaga:</i> niezalecane jest zwiększanie okna powyżej 15.</p>

            <p><b>4. Wybór linii bazowej</b><br/>
            <b>Utlenianie</b>: Kliknij „Zakres utlenienia (2× klik)" i wskaż dwa punkty.
            <b>Redukcja</b>: Kliknij „Zakres redukcji (2× klik)" i wskaż dwa punkty.

            Po wybraniu liniowego fragmentu należy ręcznie dostosować współrzędne punktów linii bazowej w taki sposób,
            aby obejmowała ona cały pik.</p>

            <p><b>5. Obliczenie parametrów piku</b><br/>
            Kliknij „Oblicz parametry piku". Program wyznaczy x_peak, y_peak, linię bazową, wysokość/głębokość piku i E₁/₂,
            a wyniki wyświetli na wykresie i w tabeli.</p>

            <p><b>6. Druga pochodna (procesy nieodwracalne)</b><br/>
            • Kliknij „Oblicz drugą pochodną".<br/>
            • Opcja wygładzania jest opcjonalna, ale zalecana.<br/>
            • Podaj zakres poszukiwania miejsc zerowych.<br/>
            • Kliknij „Znajdź miejsca zerowe" – punkty zostaną pokazane na wykresie i zapisane w tabeli.</p>

            <p><b>7. Eksport do Excela</b><br/>
            Kliknij „Eksport do Excela", wybierz nazwę pliku.
            Zapisane zostaną: surowe dane, dane wygładzone, pochodne, miejsca zerowe, wyniki piku i wykres.</p>

            <hr/>

            <p><b>Opcjonalne ustawienia</b><br/>
            • Tryb jasny/ciemny – przełącznik w górnym pasku.<br/>
            • Ręczna edycja osi – przycisk „Edytuj ustawienia osi".</p>
        </body>
        </html>
        """
        QtWidgets.QMessageBox.information(self, "Help – instrukcja", help_text)

    def show_about(self):
        about_text = """
        <html>
        <body>
            <h4 align="center">CVision</h4>
            <h4>Analiza woltamogramu cyklicznego</h4>
            <p>Wersja: 2.0.0</p>
            <p>Autor: <b>StarGate3</b><br/>
            GitHub: <a href='https://github.com/StarGate3'>github.com/StarGate3</a>
            </p>
        </body>
        </html>
        """
        QtWidgets.QMessageBox.about(self, "About", about_text)
