#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

from phantasy_ui.templates import BaseAppForm
from phantasy_ui.widgets.latticewidget import LatticeWidget

from .ui.ui_app import Ui_MainWindow

from collections import OrderedDict
from phantasy.apps.trajectory_viewer.app_elem_selection import ElementSelectionWidget
from .utils import ElementListModelDV as ElementListModel

DTYPE_LIST = ("BCM", )


class DiagViewerWindow(BaseAppForm, Ui_MainWindow):

    # update
    data_updated = pyqtSignal(QVariant, QVariant, QVariant)
    # init
    data_initialized = pyqtSignal(QVariant, QVariant, QVariant)
    ## selected devices and fields, k: ename, v: list of fields
    #devicesChanged = pyqtSignal(dict)

    def __init__(self, version):
        super(DiagViewerWindow, self).__init__()

        # app version
        self._version = version

        # window title
        self.setWindowTitle("Diagnostics Viewer")

        # set app properties
        self.setAppTitle("Diagnostics Viewer")
        self.setAppVersion(self._version)

        # about info
        self.app_about_info = """
            <html>
            <h4>About Diagnostics Viewer</h4>
            <p>This app is created to visualize the beam diagnostics
            readings of FRIB accelerator, current version is {}.
            </p>
            <p>Copyright (C) 2019 Facility for Rare Isotope Beams and other contributors.</p>
            </html>
        """.format(self._version)

        # UI
        self.setupUi(self)

        #
        self._post_init()

    def _post_init(self,):
        # lattice load window
        self._lattice_load_window = None
        # elem selection widget
        self._elem_sel_widget = None
        #
        # list of field names of selected elements
        self.__mp = None
        self._field_list = []
        # list of selected elems
        self._elems_list = []

        # DAQ
        self.daq_timer = QTimer()
        self.daq_timer.timeout.connect(self.on_daq_update)
        #
        self.data_updated.connect(self.matplotlibbarWidget.update_curve)
        self.data_initialized.connect(self.matplotlibbarWidget.reset_data)
        self.__enable_widgets("WAIT")

        # DAQ freq
        self._daqfreq = 1.0
        self.freq_dSpinbox.valueChanged[float].connect(self.update_daqfreq)

        # xdata opt
        self.id_as_x_rbtn.setChecked(False)
        self.pos_as_x_rbtn.setChecked(True)
        self._xdata_gauge = 'pos'

        # annote
        self._show_annote = False

        # device selection
        self.choose_elems_btn.clicked.connect(self.on_list_devices)
        self.select_all_elems_btn.clicked.connect(self.on_select_all_elems)
        self.inverse_selection_btn.clicked.connect(self.on_inverse_current_elem_selection)

        # field cbb
        self.field_cbb.currentTextChanged.connect(self.on_elem_field_changed)

    @pyqtSlot()
    def on_select_all_elems(self):
        try:
            model = self.devices_treeView.model()
            model.select_all_items()
        except AttributeError:
            QMessageBox.warning(self, "Element Selection",
                    "Selection error, Choose elements first.",
                    QMessageBox.Ok)

    @pyqtSlot()
    def on_inverse_current_elem_selection(self):
        try:
            model = self.devices_treeView.model()
            model.inverse_current_selection()
        except AttributeError:
            QMessageBox.warning(self, "Element Selection",
                    "Selection error, Choose elements first.",
                    QMessageBox.Ok)

    @pyqtSlot(float)
    def update_daqfreq(self, f):
        self._daqfreq = f

    @pyqtSlot()
    def on_daq_start(self):
        """Start DAQ.
        """
        if self._elems_list == [] :
            QMessageBox.warning(self, "DAQ Warning",
                    "Cannot find loaded devices.", QMessageBox.Ok)
            return

        self.daq_timer.start(1000.0 / self._daqfreq)
        self.__enable_widgets("START")

    @pyqtSlot()
    def on_daq_stop(self):
        """Stop DAQ.
        """
        self.daq_timer.stop()
        self.__enable_widgets("STOP")

    @pyqtSlot()
    def on_daq_update(self):
        s, h, herr = self.__refresh_data()
        self.data_updated.emit(s, h, herr)
        #
        self.matplotlibbarWidget.clear_annote()
        self.annote_height_chkbox.toggled.emit(self._show_annote)

    def __refresh_data(self):
        h = [getattr(e, f) for e, f in zip(self._elems_list, self._field_list)]

        if self._xdata_gauge == 'pos':
            s = [e.sb for e in self._elems_list]
        else: # ID as x
            s = list(range(len(h)))
        herr = [0] * len(h)
        return s, h, herr

    @pyqtSlot()
    def on_init_dataviz(self):
        # initial plot (reset figure btn)
        s, h, herr = self.__refresh_data()
        self.data_initialized.emit(s, h, herr)

    @pyqtSlot(bool)
    def on_apply_id_as_xdata(self, f):
        if f:
            print("Apply ID as xdata")
            self._xdata_gauge = 'id'

    @pyqtSlot(bool)
    def on_apply_pos_as_xdata(self, f):
        if f:
            print("Apply Pos as xdata")
            self._xdata_gauge = 'pos'

    def __enable_widgets(self, status):
        if status != "START":
            self.reset_figure_btn.setEnabled(True)
            self.start_btn.setEnabled(True)
            self.id_as_x_rbtn.setEnabled(True)
            self.pos_as_x_rbtn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.devices_treeView.setEnabled(True)
        else:
            self.reset_figure_btn.setEnabled(False)
            self.start_btn.setEnabled(False)
            self.id_as_x_rbtn.setEnabled(False)
            self.pos_as_x_rbtn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.devices_treeView.setEnabled(False)

    @pyqtSlot(bool)
    def on_annote_height(self, f):
        o = self.matplotlibbarWidget
        self._show_annote = f
        if f:
            # annote height on top/bottom of bar
            o.annotate_bar()
        else:
            if o._all_annotes is None:
                return
            # hide annotes
            [i.set_visible(False) for i in o._all_annotes]
        o.update_figure()

    @pyqtSlot()
    def onLoadLatticeAction(self):
        """Load lattice.
        """
        if self._lattice_load_window is None:
            self._lattice_load_window = LatticeWidget()
        self._lattice_load_window.show()
        self._lattice_load_window.latticeChanged.connect(self.update_lattice)
        # reset element selection widgets
        self._elem_sel_widget = None

    @pyqtSlot(QVariant)
    def update_lattice(self, o):
        self.__mp = o

    @pyqtSlot()
    def on_list_devices(self):
        if self.__mp is None:
            QMessageBox.warning(self, "Device Selection",
                    "Cannot find loaded lattice, try to load first, either by clicking Tools > Load Lattice or Ctrl+Shift+L.",
                    QMessageBox.Ok)
            return
        w = self._elem_sel_widget = ElementSelectionWidget(self,
                self.__mp, dtypes=DTYPE_LIST)
        w.elementsSelected.connect(self.on_update_elems)
        w.show()

    @pyqtSlot(list)
    def on_update_elems(self, enames):
        """Selected element names list updated.
        """
        tv = self.devices_treeView
        model = ElementListModel(tv, self.__mp, enames)
        # list of fields of selected element type
        model.fieldsSelected.connect(self.on_selected_fields_updated)
        model.set_model()

        m = tv.model()
        m.elementSelected.connect(self.on_elem_selection_updated)
        model.select_all_items()

    @pyqtSlot(OrderedDict)
    def on_elem_selection_updated(self, d):
        print("selected elems:", d)
        self._field_list = [f[0] for _, f in d.items()]
        self._elems_list = self.devices_treeView.model().get_elements("selected")
        #model = self.devices_treeView.model()
        #self.devicesChanged.emit(model._selected_elements)

    @pyqtSlot(list)
    def on_selected_fields_updated(self, fields):
        o = self.field_cbb
        o.clear()
        o.addItems(fields)
        if 'X' in fields:
            # BPM
            o.setCurrentText('X')
        elif 'TYP' in fields:
            # BCM
            o.setCurrentText('TYP')

    @pyqtSlot('QString')
    def on_elem_field_changed(self, s):
        try:
            model = self.devices_treeView.model()
            model.change_field(s)
        except AttributeError:
            QMessageBox.warning(self, "Change Field",
                    "Failed to change field.", QMessageBox.Ok)

