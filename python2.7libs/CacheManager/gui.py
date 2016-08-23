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

import core
reload(core)
import define as Define
reload(Define)
import cacheWidget
reload(cacheWidget)

try:
    import hqt.hqt as hqt
    reload(hqt)
except:
    pass


class CacheManager(QtGui.QWidget):
    """docstring for CacheManager"""


    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    UIPATH = CURRENT_DIR + "/ui/gui.ui"


    def __init__(self, parent=None):
        super(CacheManager, self).__init__()

        self.UI = None
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(self.UIPATH)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.UI = loader.load(ui_file)

        self.initSettings()


    def initSettings(self):
        self.initGUI()


    def initGUI(self):

        toolbarLayout = self.UI.toolbarLayout
        self._createMenuBar()
        self._createEditMenu()
        toolbarLayout.addWidget(self.menuBar)

        self.cacheTreeWidget = self._createCacheTree()
        treeWidgetLayout = self.UI.treeWidgetLayout
        treeWidgetLayout.addWidget(self.cacheTreeWidget)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.UI)
        self.setLayout(layout)


    def _createMenuBar(self):
        """Helper method for the constructor.

        Create the menu bar.
        """
        self.menuBar = QtGui.QMenuBar()
        self.menuBar.setFixedHeight(25)

        help_button = QtGui.QToolButton()
        help_button.setFixedWidth(25)
        help_button.setFixedHeight(25)
        # help_button.clicked.connect(self.showHelp)
        try:
            help_button.setIcon(hou.ui.createQtIcon("BUTTONS_help", 32, 32))
        except:
            help_button.setText("H")
        help_button.setProperty("transparent", True);
        #
        self.menuBar.setCornerWidget(help_button)
        self.menuBar.cornerWidget(QtCore.Qt.TopRightCorner)


    def _createEditMenu(self):
        """Helper method for the constructor.

        Create the Pose menu.
        """
        edit_menu = QtGui.QMenu(self)

        reloadAction = edit_menu.addAction("Reload")
        reloadAction.setShortcut("Ctrl+R")
        self.addAction(reloadAction)
        reloadAction.triggered.connect(self._reload)

        edit_action = self.menuBar.addAction("Edit")
        edit_action.setMenu(edit_menu)


    def _createCacheTree(self):
        return cacheWidget.cacheTreeWidget()


    def _reload(self):
        cacheWidget.cacheTreeWidget().resetItems()


def main(launch_type=""):
    try:
        return hqt.showUi(CacheManager())
    except:
        return CacheManager()

#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
