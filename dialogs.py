"""
Moduł dialogs.py
-----------------
Zawiera klasy dialogowe do ustawień osi oraz linii bazowej.
"""

import re

import numpy as np
import pyqtgraph as pg
from PyQt6 import QtWidgets, QtGui, QtCore

from analysis import CalibrationSettings, apply_calibration, fit_peak


class AxisSettingsDialog(QtWidgets.QDialog):
    """
    Dialog umożliwiający ustawienia parametrów osi wykresu.
    """
    applied = QtCore.pyqtSignal(dict)

    def __init__(self, current_settings, parent=None):
        """
        Inicjalizacja dialogu z aktualnymi ustawieniami.
        """
        super().__init__(parent)
        self.setWindowTitle("Ustawienia osi")
        self.current_settings = current_settings
        self.init_ui()

    def init_ui(self):
        """Tworzy interfejs dialogu z polami do edycji ustawień osi."""
        layout = QtWidgets.QFormLayout(self)
        self.x_label_edit = QtWidgets.QLineEdit(self.current_settings.get('x_label', 'Oś X'))
        layout.addRow("Etykieta osi X:", self.x_label_edit)
        self.y_label_edit = QtWidgets.QLineEdit(self.current_settings.get('y_label', 'Wartości'))
        layout.addRow("Etykieta osi Y:", self.y_label_edit)

        # Ustawienia zakresu osi X
        self.x_min_spin = QtWidgets.QDoubleSpinBox()
        self.x_min_spin.setRange(-1e9, 1e9)
        self.x_min_spin.setDecimals(3)
        self.x_min_spin.setValue(self.current_settings.get('x_min', 0))
        self.x_max_spin = QtWidgets.QDoubleSpinBox()
        self.x_max_spin.setRange(-1e9, 1e9)
        self.x_max_spin.setDecimals(3)
        self.x_max_spin.setValue(self.current_settings.get('x_max', 10))
        x_range_layout = QtWidgets.QHBoxLayout()
        x_range_layout.addWidget(QtWidgets.QLabel("Min:"))
        x_range_layout.addWidget(self.x_min_spin)
        x_range_layout.addWidget(QtWidgets.QLabel("Max:"))
        x_range_layout.addWidget(self.x_max_spin)
        layout.addRow("Zakres osi X:", x_range_layout)

        # Ustawienia zakresu osi Y
        self.y_min_spin = QtWidgets.QDoubleSpinBox()
        self.y_min_spin.setRange(-1e9, 1e9)
        self.y_min_spin.setDecimals(3)
        self.y_min_spin.setValue(self.current_settings.get('y_min', 0))
        self.y_max_spin = QtWidgets.QDoubleSpinBox()
        self.y_max_spin.setRange(-1e9, 1e9)
        self.y_max_spin.setDecimals(3)
        self.y_max_spin.setValue(self.current_settings.get('y_max', 10))
        y_range_layout = QtWidgets.QHBoxLayout()
        y_range_layout.addWidget(QtWidgets.QLabel("Min:"))
        y_range_layout.addWidget(self.y_min_spin)
        y_range_layout.addWidget(QtWidgets.QLabel("Max:"))
        y_range_layout.addWidget(self.y_max_spin)
        layout.addRow("Zakres osi Y:", y_range_layout)

        # Wybór czcionki
        self.font = self.current_settings.get('font', QtGui.QFont("Arial", 12))
        self.font_button = QtWidgets.QPushButton("Wybierz czcionkę")
        self.font_button.clicked.connect(self.choose_font)
        self.font_label = QtWidgets.QLabel(self.font.toString())
        font_layout = QtWidgets.QHBoxLayout()
        font_layout.addWidget(self.font_button)
        font_layout.addWidget(self.font_label)
        layout.addRow("Czcionka:", font_layout)

        # Przyciski OK, Anuluj, Apply
        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok |
            QtWidgets.QDialogButtonBox.StandardButton.Cancel |
            QtWidgets.QDialogButtonBox.StandardButton.Apply,
            parent=self
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Apply).clicked.connect(self.on_apply)
        layout.addRow(self.button_box)

    def choose_font(self):
        """Otwiera okno wyboru czcionki i aktualizuje etykietę czcionki."""
        font, ok = QtWidgets.QFontDialog.getFont(self.font, self, "Wybierz czcionkę")
        if ok:
            self.font = font
            self.font_label.setText(self.font.toString())

    def on_apply(self):
        """Emituje sygnał z nowymi ustawieniami bez zamykania dialogu."""
        self.applied.emit(self.get_settings())

    def get_settings(self):
        """
        Zwraca słownik z ustawieniami osi.

        Returns:
            dict: Ustawienia osi.
        """
        return {
            'x_label': self.x_label_edit.text(),
            'y_label': self.y_label_edit.text(),
            'x_min': self.x_min_spin.value(),
            'x_max': self.x_max_spin.value(),
            'y_min': self.y_min_spin.value(),
            'y_max': self.y_max_spin.value(),
            'font': self.font
        }


class BaselineSettingsDialog(QtWidgets.QDialog):
    """
    Dialog umożliwiający numeryczną edycję ustawień linii bazowej dla utlenienia i redukcji.
    """
    baseline_applied = QtCore.pyqtSignal(dict)

    def __init__(self, current_settings, parent=None):
        """
        Inicjalizacja dialogu z aktualnymi ustawieniami linii bazowej.

        Parameters:
            current_settings (dict): Aktualne ustawienia bazowe.
        """
        super().__init__(parent)
        self.setWindowTitle("Ustawienia linii bazowej (numerycznie)")
        self.current_settings = current_settings
        # Zachowujemy oryginalne ustawienia do obliczeń
        self.initial_settings = {
            'oxidation': self.current_settings['oxidation'].copy(),
            'reduction': self.current_settings['reduction'].copy()
        }
        self.init_ui()

    def init_ui(self):
        """Tworzy interfejs dialogu z polami do ustawiania linii bazowej."""
        layout = QtWidgets.QFormLayout(self)
        # Utlenienie
        ox_x1 = QtWidgets.QDoubleSpinBox()
        ox_x1.setRange(-1e9, 1e9)
        ox_x1.setDecimals(3)
        ox_x1.setValue(self.current_settings['oxidation'].get('x1', 0))
        ox_y1 = QtWidgets.QDoubleSpinBox()
        ox_y1.setRange(-1e9, 1e9)
        ox_y1.setDecimals(3)
        ox_y1.setValue(self.current_settings['oxidation'].get('y1', 0))
        ox_x2 = QtWidgets.QDoubleSpinBox()
        ox_x2.setRange(-1e9, 1e9)
        ox_x2.setDecimals(3)
        ox_x2.setValue(self.current_settings['oxidation'].get('x2', 10))
        ox_y2 = QtWidgets.QDoubleSpinBox()
        ox_y2.setRange(-1e9, 1e9)
        ox_y2.setDecimals(3)
        ox_y2.setValue(self.current_settings['oxidation'].get('y2', 0))
        ox_layout = QtWidgets.QHBoxLayout()
        ox_layout.addWidget(QtWidgets.QLabel("x1:"))
        ox_layout.addWidget(ox_x1)
        ox_layout.addWidget(QtWidgets.QLabel("y1:"))
        ox_layout.addWidget(ox_y1)
        ox_layout.addWidget(QtWidgets.QLabel("x2:"))
        ox_layout.addWidget(ox_x2)
        ox_layout.addWidget(QtWidgets.QLabel("y2:"))
        ox_layout.addWidget(ox_y2)
        layout.addRow("Utlenienie:", ox_layout)
        self.ox_preview_label = QtWidgets.QLabel("Podgląd wartości: Punkty nie są jeszcze zainicjalizowane")
        layout.addRow(self.ox_preview_label)
        self.ox_x1 = ox_x1
        self.ox_y1 = ox_y1
        self.ox_x2 = ox_x2
        self.ox_y2 = ox_y2

        # Redukcja
        red_x1 = QtWidgets.QDoubleSpinBox()
        red_x1.setRange(-1e9, 1e9)
        red_x1.setDecimals(3)
        red_x1.setValue(self.current_settings['reduction'].get('x1', 0))
        red_y1 = QtWidgets.QDoubleSpinBox()
        red_y1.setRange(-1e9, 1e9)
        red_y1.setDecimals(3)
        red_y1.setValue(self.current_settings['reduction'].get('y1', 0))
        red_x2 = QtWidgets.QDoubleSpinBox()
        red_x2.setRange(-1e9, 1e9)
        red_x2.setDecimals(3)
        red_x2.setValue(self.current_settings['reduction'].get('x2', 10))
        red_y2 = QtWidgets.QDoubleSpinBox()
        red_y2.setRange(-1e9, 1e9)
        red_y2.setDecimals(3)
        red_y2.setValue(self.current_settings['reduction'].get('y2', 0))
        red_layout = QtWidgets.QHBoxLayout()
        red_layout.addWidget(QtWidgets.QLabel("x1:"))
        red_layout.addWidget(red_x1)
        red_layout.addWidget(QtWidgets.QLabel("y1:"))
        red_layout.addWidget(red_y1)
        red_layout.addWidget(QtWidgets.QLabel("x2:"))
        red_layout.addWidget(red_x2)
        red_layout.addWidget(QtWidgets.QLabel("y2:"))
        red_layout.addWidget(red_y2)
        layout.addRow("Redukcja:", red_layout)
        self.red_preview_label = QtWidgets.QLabel("Podgląd wartości: Punkty nie są jeszcze zainicjalizowane")
        layout.addRow(self.red_preview_label)
        self.red_x1 = red_x1
        self.red_y1 = red_y1
        self.red_x2 = red_x2
        self.red_y2 = red_y2

        # Połączenia sygnałów do aktualizacji wartości i podglądu
        self.ox_x1.valueChanged.connect(self.update_y_values)
        self.ox_x1.valueChanged.connect(self.update_preview_labels)
        self.ox_x2.valueChanged.connect(self.update_y_values)
        self.ox_x2.valueChanged.connect(self.update_preview_labels)
        self.red_x1.valueChanged.connect(self.update_y_values)
        self.red_x1.valueChanged.connect(self.update_preview_labels)
        self.red_x2.valueChanged.connect(self.update_y_values)
        self.red_x2.valueChanged.connect(self.update_preview_labels)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok |
            QtWidgets.QDialogButtonBox.StandardButton.Apply |
            QtWidgets.QDialogButtonBox.StandardButton.Cancel,
            parent=self
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Apply).clicked.connect(self.on_apply)
        layout.addRow(self.button_box)

    def update_y_values(self):
        """
        Aktualizuje wartości y dla obu linii bazowych na podstawie zmienionych wartości x
        przy zachowaniu oryginalnego nachylenia.
        """
        sender = self.sender()
        for key, x1_spin, y1_spin, x2_spin, y2_spin in [
            ("oxidation", self.ox_x1, self.ox_y1, self.ox_x2, self.ox_y2),
            ("reduction", self.red_x1, self.red_y1, self.red_x2, self.red_y2),
        ]:
            new_x1 = x1_spin.value()
            new_x2 = x2_spin.value()
            init = self.initial_settings[key]
            slope = (init['y2'] - init['y1']) / (init['x2'] - init['x1']) if init['x2'] != init['x1'] else 0
            if sender in (x1_spin, x2_spin):
                if sender == x1_spin:
                    y1_spin.setValue(init['y1'] + slope * (new_x1 - init['x1']))
                elif sender == x2_spin:
                    y2_spin.setValue(init['y2'] + slope * (new_x2 - init['x2']))
            else:
                y1_spin.setValue(init['y1'] + slope * (new_x1 - init['x1']))
                y2_spin.setValue(init['y2'] + slope * (new_x2 - init['x1']))

    def on_apply(self):
        """
        Zastosowanie zmian - przeliczenie ustawień i emisja sygnału.
        """
        for key, x1_spin, y1_spin, x2_spin, y2_spin in [
            ("oxidation", self.ox_x1, self.ox_y1, self.ox_x2, self.ox_y2),
            ("reduction", self.red_x1, self.red_y1, self.red_x2, self.red_y2),
        ]:
            init = self.initial_settings[key]
            new_x1 = x1_spin.value()
            new_x2 = x2_spin.value()
            slope = (init['y2'] - init['y1']) / (init['x2'] - init['x1']) if init['x2'] != init['x1'] else 0
            if new_x1 != init['x1']:
                y1_spin.setValue(init['y1'] + slope * (new_x1 - init['x1']))
            if new_x2 != init['x2']:
                y2_spin.setValue(init['y2'] + slope * (new_x2 - init['x2']))
        new_settings = self.get_settings()
        self.baseline_applied.emit(new_settings)
        self.initial_settings = {
            'oxidation': new_settings['oxidation'].copy(),
            'reduction': new_settings['reduction'].copy()
        }
        self.update_preview_labels()

    def accept(self):
        """Przy zatwierdzaniu zmian stosuje ustawienia oraz zamyka dialog."""
        self.on_apply()
        super().accept()

    def get_settings(self):
        """
        Zwraca aktualne ustawienia linii bazowej.

        Returns:
            dict: Ustawienia dla utlenienia i redukcji.
        """
        return {
            'oxidation': {
                'x1': self.ox_x1.value(),
                'y1': self.ox_y1.value(),
                'x2': self.ox_x2.value(),
                'y2': self.ox_y2.value(),
            },
            'reduction': {
                'x1': self.red_x1.value(),
                'y1': self.red_y1.value(),
                'x2': self.red_x2.value(),
                'y2': self.red_y2.value(),
            }
        }

    def update_preview_labels(self):
        """Aktualizuje etykiety podglądu dla obu ustawień linii bazowej."""
        settings = self.get_settings()
        self.ox_preview_label.setText(
            f"x1: {settings['oxidation']['x1']:.3f}, y1: {settings['oxidation']['y1']:.3f} | x2: {settings['oxidation']['x2']:.3f}, y2: {settings['oxidation']['y2']:.3f}"
        )
        self.red_preview_label.setText(
            f"x1: {settings['reduction']['x1']:.3f}, y1: {settings['reduction']['y1']:.3f} | x2: {settings['reduction']['x2']:.3f}, y2: {settings['reduction']['y2']:.3f}"
        )


class PeakDetectionDialog(QtWidgets.QDialog):
    """Dialog do konfiguracji automatycznego wykrywania pików."""

    detection_confirmed = QtCore.pyqtSignal(float, int, bool, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Automatyczne wykrywanie pików")
        self._init_ui()

    def _init_ui(self):
        layout = QtWidgets.QFormLayout(self)

        self.min_height_spin = QtWidgets.QDoubleSpinBox()
        self.min_height_spin.setRange(0.0, 10000.0)
        self.min_height_spin.setDecimals(3)
        self.min_height_spin.setValue(0.0)
        layout.addRow("Minimalna wysokość piku:", self.min_height_spin)

        self.min_distance_spin = QtWidgets.QSpinBox()
        self.min_distance_spin.setRange(1, 500)
        self.min_distance_spin.setValue(5)
        self.min_distance_spin.setSuffix(" punktów danych")
        layout.addRow("Minimalna odległość między pikami:", self.min_distance_spin)

        self.detect_ox_check = QtWidgets.QCheckBox("Zakres utlenienia")
        self.detect_ox_check.setChecked(True)
        layout.addRow(self.detect_ox_check)

        self.detect_red_check = QtWidgets.QCheckBox("Zakres redukcji")
        self.detect_red_check.setChecked(True)
        layout.addRow(self.detect_red_check)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok |
            QtWidgets.QDialogButtonBox.StandardButton.Cancel,
            parent=self
        )
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def _on_accept(self):
        self.detection_confirmed.emit(
            self.min_height_spin.value(),
            self.min_distance_spin.value(),
            self.detect_ox_check.isChecked(),
            self.detect_red_check.isChecked(),
        )
        self.accept()


class CalibrationDialog(QtWidgets.QDialog):
    """Dialog do kalibracji jednostek prądu względem powierzchni elektrody i stężenia analitu."""

    calibration_confirmed = QtCore.pyqtSignal(CalibrationSettings)

    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kalibracja jednostek")
        self._current = current_settings
        self._init_ui()
        self._update_unit_preview()

    def _init_ui(self):
        layout = QtWidgets.QFormLayout(self)

        self.area_spin = QtWidgets.QDoubleSpinBox()
        self.area_spin.setRange(0.001, 1000.0)
        self.area_spin.setDecimals(4)
        self.area_spin.setValue(self._current.electrode_area)
        layout.addRow("Powierzchnia elektrody [cm²]:", self.area_spin)

        self.normalize_area_check = QtWidgets.QCheckBox("Normalizuj względem powierzchni elektrody")
        self.normalize_area_check.setChecked(self._current.normalize_by_area)
        layout.addRow(self.normalize_area_check)

        self.concentration_spin = QtWidgets.QDoubleSpinBox()
        self.concentration_spin.setRange(0.0001, 10000.0)
        self.concentration_spin.setDecimals(4)
        self.concentration_spin.setValue(self._current.concentration)
        layout.addRow("Stężenie analitu [mM]:", self.concentration_spin)

        self.normalize_conc_check = QtWidgets.QCheckBox("Normalizuj względem stężenia")
        self.normalize_conc_check.setChecked(self._current.normalize_by_concentration)
        layout.addRow(self.normalize_conc_check)

        self.unit_preview_label = QtWidgets.QLabel()
        layout.addRow(self.unit_preview_label)

        self.normalize_area_check.toggled.connect(self._update_unit_preview)
        self.normalize_conc_check.toggled.connect(self._update_unit_preview)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok |
            QtWidgets.QDialogButtonBox.StandardButton.Cancel |
            QtWidgets.QDialogButtonBox.StandardButton.Reset,
            parent=self
        )
        buttons.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText("Anuluj")
        buttons.button(QtWidgets.QDialogButtonBox.StandardButton.Reset).setText("Resetuj")
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QtWidgets.QDialogButtonBox.StandardButton.Reset).clicked.connect(self._on_reset)
        layout.addRow(buttons)

    def _build_settings(self):
        return CalibrationSettings(
            electrode_area=self.area_spin.value(),
            concentration=self.concentration_spin.value(),
            normalize_by_area=self.normalize_area_check.isChecked(),
            normalize_by_concentration=self.normalize_conc_check.isChecked(),
        )

    def _update_unit_preview(self):
        import numpy as np
        _, unit = apply_calibration(np.array([0.0]), self._build_settings())
        self.unit_preview_label.setText(f"Jednostka wynikowa: {unit}")

    def _on_reset(self):
        defaults = CalibrationSettings()
        self.area_spin.setValue(defaults.electrode_area)
        self.concentration_spin.setValue(defaults.concentration)
        self.normalize_area_check.setChecked(defaults.normalize_by_area)
        self.normalize_conc_check.setChecked(defaults.normalize_by_concentration)
        self._update_unit_preview()

    def _on_accept(self):
        settings = self._build_settings()
        if settings.electrode_area == 0 or settings.concentration == 0:
            QtWidgets.QMessageBox.warning(
                self, "Nieprawidłowe wartości",
                "Powierzchnia elektrody oraz stężenie muszą być różne od zera."
            )
            self.reject()
            return
        self.calibration_confirmed.emit(settings)
        self.accept()


_MODEL_LABEL_TO_KEY = {
    "Gaussowski": "gaussian",
    "Lorentzowski": "lorentzian",
    "Asymetryczny Gaussowski": "asymmetric_gaussian",
}


class CurveFittingDialog(QtWidgets.QDialog):
    """Non-modal dialog for fitting Gaussian/Lorentzian/asymmetric-Gaussian to a peak."""

    fit_added_to_table = QtCore.pyqtSignal(str, float, float, float, float)

    def __init__(self, x, y1, y2, baseline_settings, x_label='E [mV]',
                 y_unit_label='μA', parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dopasowanie krzywej")
        self.setModal(False)
        self._x = np.asarray(x, dtype=float)
        self._y1 = np.asarray(y1, dtype=float)
        self._y2 = np.asarray(y2, dtype=float)
        self._baseline_settings = baseline_settings
        self._x_label = x_label
        self._y_unit_label = y_unit_label
        self._last_result = None
        self._init_ui()
        self._prefill_range_from_baseline()

    def _extract_x_unit(self):
        m = re.search(r'\[([^\]]+)\]', self._x_label)
        return m.group(1) if m else self._x_label

    def _init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        form = QtWidgets.QFormLayout()
        self.model_combo = QtWidgets.QComboBox()
        self.model_combo.addItems(list(_MODEL_LABEL_TO_KEY.keys()))
        form.addRow("Model:", self.model_combo)

        self.curve_combo = QtWidgets.QComboBox()
        self.curve_combo.addItems(["Utlenianie", "Redukcja"])
        self.curve_combo.currentIndexChanged.connect(self._prefill_range_from_baseline)
        form.addRow("Krzywa:", self.curve_combo)

        self.x_min_spin = QtWidgets.QDoubleSpinBox()
        self.x_min_spin.setRange(-1e9, 1e9)
        self.x_min_spin.setDecimals(3)
        form.addRow("Zakres X — od:", self.x_min_spin)

        self.x_max_spin = QtWidgets.QDoubleSpinBox()
        self.x_max_spin.setRange(-1e9, 1e9)
        self.x_max_spin.setDecimals(3)
        form.addRow("Zakres X — do:", self.x_max_spin)

        layout.addLayout(form)

        self.fit_button = QtWidgets.QPushButton("Dopasuj")
        self.fit_button.clicked.connect(self._run_fit)
        layout.addWidget(self.fit_button)

        self.results_group = QtWidgets.QGroupBox("Wyniki")
        res_layout = QtWidgets.QFormLayout(self.results_group)
        self.fwhm_label = QtWidgets.QLabel("—")
        self.center_label = QtWidgets.QLabel("—")
        self.amplitude_label = QtWidgets.QLabel("—")
        self.asymmetry_value_label = QtWidgets.QLabel("—")
        self.r2_label = QtWidgets.QLabel("—")
        self.fwhm_unit_label = QtWidgets.QLabel(self._extract_x_unit())
        res_layout.addRow("FWHM:", self.fwhm_label)
        res_layout.addRow("Centrum piku:", self.center_label)
        res_layout.addRow("Amplituda:", self.amplitude_label)
        self._asymmetry_key_label = QtWidgets.QLabel("Asymetria:")
        res_layout.addRow(self._asymmetry_key_label, self.asymmetry_value_label)
        res_layout.addRow("R²:", self.r2_label)
        res_layout.addRow("Jednostka FWHM:", self.fwhm_unit_label)
        self.results_group.setVisible(False)
        layout.addWidget(self.results_group)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('bottom', self._x_label)
        self.plot_widget.setLabel('left', f"Prąd [{self._y_unit_label}]")
        self.plot_widget.addLegend()
        self.plot_widget.setMinimumHeight(260)
        layout.addWidget(self.plot_widget)

        btn_row = QtWidgets.QHBoxLayout()
        self.add_button = QtWidgets.QPushButton("Dodaj do tabeli wyników")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self._on_add_to_table)
        btn_row.addWidget(self.add_button)
        close_btn = QtWidgets.QPushButton("Zamknij")
        close_btn.clicked.connect(self.close)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)

    def _prefill_range_from_baseline(self):
        key = 'oxidation' if self.curve_combo.currentIndex() == 0 else 'reduction'
        bs = self._baseline_settings.get(key, {})
        x1 = bs.get('x1', float(np.min(self._x)))
        x2 = bs.get('x2', float(np.max(self._x)))
        self.x_min_spin.setValue(min(x1, x2))
        self.x_max_spin.setValue(max(x1, x2))

    def _current_y(self):
        return self._y1 if self.curve_combo.currentIndex() == 0 else self._y2

    def _run_fit(self):
        x_min = self.x_min_spin.value()
        x_max = self.x_max_spin.value()
        if x_min >= x_max:
            QtWidgets.QMessageBox.warning(
                self, "Nieprawidłowy zakres",
                "Dolna granica zakresu X musi być mniejsza od górnej."
            )
            return

        y = self._current_y()
        mask = (self._x >= x_min) & (self._x <= x_max)
        n_points = int(np.sum(mask))
        if n_points < 5:
            QtWidgets.QMessageBox.warning(
                self, "Zbyt mało punktów",
                f"Wybrany zakres zawiera tylko {n_points} punktów danych. Wymagane minimum: 5."
            )
            return

        model_key = _MODEL_LABEL_TO_KEY[self.model_combo.currentText()]
        result = fit_peak(self._x, y, model=model_key, x_min=x_min, x_max=x_max)

        if result['error'] is not None:
            self.results_group.setVisible(False)
            self.add_button.setEnabled(False)
            self._last_result = None
            QtWidgets.QMessageBox.warning(
                self, "Dopasowanie nieudane",
                f"Nie udało się dopasować modelu: {result['error']}"
            )
            return

        self._last_result = result
        self._populate_results(result, model_key)
        self._plot_fit(result, x_min, x_max)
        self.add_button.setEnabled(True)

    def _populate_results(self, result, model_key):
        params = result['params']
        self.fwhm_label.setText(f"{result['fwhm']:.3f}")
        self.center_label.setText(f"{params['center']:.3f}")
        self.amplitude_label.setText(f"{params['amplitude']:.3f}")
        self.r2_label.setText(f"{result['r_squared']:.4f}")
        self.fwhm_unit_label.setText(self._extract_x_unit())
        is_asym = model_key == 'asymmetric_gaussian'
        self._asymmetry_key_label.setVisible(is_asym)
        self.asymmetry_value_label.setVisible(is_asym)
        if is_asym and result['asymmetry'] is not None:
            self.asymmetry_value_label.setText(f"{result['asymmetry']:.3f}")
        self.results_group.setVisible(True)

    def _plot_fit(self, result, x_min, x_max):
        self.plot_widget.clear()
        self.plot_widget.addLegend()
        mask = (self._x >= x_min) & (self._x <= x_max)
        x_crop = self._x[mask]
        y_crop = self._current_y()[mask]
        data_color = 'b' if self.curve_combo.currentIndex() == 0 else 'r'
        data_name = "Utlenianie" if self.curve_combo.currentIndex() == 0 else "Redukcja"
        self.plot_widget.plot(
            x_crop, y_crop, pen=pg.mkPen(color=data_color, width=2), name=data_name
        )
        self.plot_widget.plot(
            result['x_fit'], result['y_fit'],
            pen=pg.mkPen(color='g', width=2, style=QtCore.Qt.PenStyle.DashLine),
            name="Dopasowanie"
        )

    def _on_add_to_table(self):
        if self._last_result is None:
            return
        params = self._last_result['params']
        label = "Dopasowanie (utl)" if self.curve_combo.currentIndex() == 0 else "Dopasowanie (red)"
        self.fit_added_to_table.emit(
            label,
            float(params['center']),
            float(params['amplitude']),
            float(self._last_result['r_squared']),
            float(self._last_result['fwhm']),
        )
