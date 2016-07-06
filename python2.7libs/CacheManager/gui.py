# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Managing cache tool.
"""
#-------------------------------------------------------------------------------

import os, sys
sys.dont_write_bytecode = True
import hou

from PySide import QtCore, QtGui
from PySide import QtUiTools

import define as Define
reload(Define)
import cacheWidget as CacheWidget
reload(CacheWidget)
# import hqt.hqt as hqt
# reload(hqt)


class CacheManager(QtGui.QWidget):
    """docstring for CacheManager"""

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    UIPATH = CURRENT_DIR + "/ui/gui.ui"

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)

        self.UI = None

        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(self.UIPATH)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.UI = loader.load(ui_file)

        cacheTreeWidget = self._createCacheTree()
        treeWidgetLayout = self.UI.verticalLayout_3
        treeWidgetLayout.addWidget(cacheTreeWidget)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.UI)
        self.setLayout(layout)


    def initSettings(self):
        self.initGUI()
        self.setSignals()

    def initGUI(self):
        pass

    def setSignals(self):
        pass

    def _createCacheTree(self):
        return CacheWidget.cacheTreeWidget()

    # def _createCacheTable(self):
    #     CacheTable()


def main(launch_type=""):
    if launch_type == "python_panel":
        return CacheManager()

#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
