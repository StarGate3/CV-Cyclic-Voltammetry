"""
Moduł derivative_windows.py
----------------------------
Zawiera bazową klasę okna analizy pochodnych (BaseDerivativeWindow) oraz dwie
podklasy: DerivativeWindow (pierwsza pochodna) i SecondDerivativeWindow (druga pochodna).
Wspólna logika jest zdefiniowana raz w klasie bazowej.
"""

import numpy as np
from PyQt6 import QtWidgets
import pyqtgraph as pg
from scipy.signal import savgol_filter
from utils import compute_zero_crossings


class BaseDerivativeWindow(QtWidgets.QDialog):
    """
    Bazowe okno do wyświetlania wykresu pochodnych oraz wyszukiwania miejsc zerowych.
    Klasy pochodne przekazują tytuły okna/wykresu, nazwy legend i dane przez __init__.
    """

    def __init__(self, window_title, plot_title, legend_name1, legend_name2,
                 x, y1, y2, parent=None):
        """
        Parameters:
            window_title  (str):     Tytuł okna dialogowego.
            plot_title    (str):     Tytuł wykresu pyqtgraph.
            legend_name1  (str):     Nazwa pierwszej krzywej w legendzie.
            legend_name2  (str):     Nazwa drugiej krzywej w legendzie.
            x  (ndarray):            Wartości osi x.
            y1 (ndarray):            Pochodna dla utlenienia.
            y2 (ndarray):            Pochodna dla redukcji.
        """
        super().__init__(parent)
        self.setWindowTitle(window_title)
        self.resize(800, 600)
        self.x = x
        self.orig_y1 = y1
        self.orig_y2 = y2
        self._plot_title = plot_title
        self._legend_name1 = legend_name1
        self._legend_name2 = legend_name2
        self.current_curve1 = None
        self.current_curve2 = None
        self.intersectionPlot = None
        self.intersections = []
        self.init_ui()

    def init_ui(self):
        """Buduje interfejs okna: kontrolki wygładzania, zakres zerowania, wykres."""
        main_layout = QtWidgets.QVBoxLayout(self)

        # Kontrolki wygładzania
        controls_layout = QtWidgets.QHBoxLayout()
        self.smoothingCheckBox = QtWidgets.QCheckBox("Wygładzanie (Savitzky-Golay)")
        self.smoothingCheckBox.setChecked(True)
        self.smoothingCheckBox.stateChanged.connect(self.update_plot)
        controls_layout.addWidget(self.smoothingCheckBox)
        controls_layout.addWidget(QtWidgets.QLabel("Okno:"))
        self.windowSpinBox = QtWidgets.QSpinBox()
        self.windowSpinBox.setRange(3, 101)
        self.windowSpinBox.setSingleStep(2)
        self.windowSpinBox.setValue(15)
        self.windowSpinBox.valueChanged.connect(self.update_plot)
        controls_layout.addWidget(self.windowSpinBox)
        controls_layout.addWidget(QtWidgets.QLabel("Stopień:"))
        self.polySpinBox = QtWidgets.QSpinBox()
        self.polySpinBox.setRange(1, 5)
        self.polySpinBox.setValue(3)
        self.polySpinBox.valueChanged.connect(self.update_plot)
        controls_layout.addWidget(self.polySpinBox)
        main_layout.addLayout(controls_layout)

        # Kontrolki zakresu zerowania
        intersection_layout = QtWidgets.QHBoxLayout()
        intersection_layout.addWidget(QtWidgets.QLabel("Zakres miejsc zerowych od:"))
        self.intMinSpin = QtWidgets.QDoubleSpinBox()
        self.intMinSpin.setRange(-1e9, 1e9)
        self.intMinSpin.setDecimals(3)
        self.intMinSpin.setValue(np.min(self.x))
        intersection_layout.addWidget(self.intMinSpin)
        intersection_layout.addWidget(QtWidgets.QLabel("do:"))
        self.intMaxSpin = QtWidgets.QDoubleSpinBox()
        self.intMaxSpin.setRange(-1e9, 1e9)
        self.intMaxSpin.setDecimals(3)
        self.intMaxSpin.setValue(np.max(self.x))
        intersection_layout.addWidget(self.intMaxSpin)
        self.findIntButton = QtWidgets.QPushButton("Znajdź miejsca zerowe")
        self.findIntButton.clicked.connect(self.find_intersections)
        intersection_layout.addWidget(self.findIntButton)
        main_layout.addLayout(intersection_layout)

        self.cursorLabel = QtWidgets.QLabel("x = ?, y = ?")
        main_layout.addWidget(self.cursorLabel)
        self.plot_widget = pg.PlotWidget(title=self._plot_title)
        self.plot_widget.addLegend()
        main_layout.addWidget(self.plot_widget)
        self.plot_widget.scene().sigMouseMoved.connect(self.mouseMoved)
        self.update_plot()

    def update_plot(self):
        """Aktualizuje wykres pochodnych, stosując opcjonalne wygładzanie."""
        if self.smoothingCheckBox.isChecked():
            window_length = self.windowSpinBox.value()
            polyorder = self.polySpinBox.value()
            if window_length % 2 == 0:
                window_length += 1
            if window_length > len(self.orig_y1):
                window_length = len(self.orig_y1) if len(self.orig_y1) % 2 == 1 else len(self.orig_y1) - 1
            if window_length <= polyorder:
                # savgol_filter requires window_length > polyorder; bump up to satisfy it.
                window_length = polyorder + 1
                if window_length % 2 == 0:
                    window_length += 1
            try:
                smooth_y1 = savgol_filter(self.orig_y1, window_length, polyorder)
                smooth_y2 = savgol_filter(self.orig_y2, window_length, polyorder)
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Błąd", f"Nie udało się wygładzić danych: {str(e)}")
                smooth_y1 = self.orig_y1
                smooth_y2 = self.orig_y2
        else:
            smooth_y1 = self.orig_y1
            smooth_y2 = self.orig_y2

        self.current_curve1 = smooth_y1
        self.current_curve2 = smooth_y2
        self.plot_widget.clear()
        self.plot_widget.addLegend()
        self.plot_widget.plot(self.x, smooth_y1, pen=pg.mkPen(color='b', width=2), name=self._legend_name1)
        self.plot_widget.plot(self.x, smooth_y2, pen=pg.mkPen(color='r', width=2), name=self._legend_name2)
        if self.intersectionPlot is not None:
            self.plot_widget.removeItem(self.intersectionPlot)
            self.intersectionPlot = None

    def find_intersections(self):
        """
        Wyszukuje miejsca zerowe obu krzywych w zadanym zakresie i wyświetla je na wykresie.
        """
        range_min = self.intMinSpin.value()
        range_max = self.intMaxSpin.value()
        zeros1 = compute_zero_crossings(self.x, self.current_curve1, range_min, range_max)
        zeros2 = compute_zero_crossings(self.x, self.current_curve2, range_min, range_max)

        intersections = zeros1 + zeros2
        self.intersections = intersections
        if intersections:
            xs = [pt[0] for pt in intersections]
            ys = [pt[1] for pt in intersections]
            self.intersectionPlot = pg.ScatterPlotItem(xs, ys, symbol='o', size=8, brush='y')
            self.plot_widget.addItem(self.intersectionPlot)
            lines = []
            for x, y in zeros1:
                lines.append(f"[Utlenianie] x = {x:.3f}, y = {y:.3f}")
            for x, y in zeros2:
                lines.append(f"[Redukcja]  x = {x:.3f}, y = {y:.3f}")
            msg = "Znalezione miejsca zerowe:\n" + "\n".join(lines)
            QtWidgets.QMessageBox.information(self, "Miejsca zerowe", msg)
        else:
            QtWidgets.QMessageBox.information(self, "Miejsca zerowe", "Brak miejsc zerowych w zadanym zakresie.")

    def mouseMoved(self, evt):
        """Aktualizuje etykietę z pozycją kursora podczas poruszania myszką."""
        pos = evt[0] if isinstance(evt, (list, tuple)) else evt
        if self.plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self.plot_widget.getViewBox().mapSceneToView(pos)
            self.cursorLabel.setText(f"x = {mouse_point.x():.3f}, y = {mouse_point.y():.3f}")


class DerivativeWindow(BaseDerivativeWindow):
    """Okno analizy pierwszej pochodnej."""

    def __init__(self, x, deriv_y1, deriv_y2, parent=None):
        super().__init__(
            window_title="Pochodne utlenienia i redukcji",
            plot_title="Wykres pochodnych",
            legend_name1="Pochodna utleniania",
            legend_name2="Pochodna redukcji",
            x=x, y1=deriv_y1, y2=deriv_y2,
            parent=parent,
        )


class SecondDerivativeWindow(BaseDerivativeWindow):
    """Okno analizy drugiej pochodnej."""

    def __init__(self, x, second_deriv_y1, second_deriv_y2, parent=None):
        super().__init__(
            window_title="Druga pochodna utlenienia i redukcji",
            plot_title="Wykres drugiej pochodnej",
            legend_name1="Druga pochodna utleniania",
            legend_name2="Druga pochodna redukcji",
            x=x, y1=second_deriv_y1, y2=second_deriv_y2,
            parent=parent,
        )
