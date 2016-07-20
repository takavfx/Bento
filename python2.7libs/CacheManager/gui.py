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

        self.initSettings()


    def initSettings(self):
        self.initGUI()
        self.setSignals()


    def initGUI(self):

        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(self.UIPATH)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.UI = loader.load(ui_file)

        self.cacheTreeWidget = self._createCacheTree()
        treeWidgetLayout = self.UI.treeWidgetLayout
        treeWidgetLayout.addWidget(self.cacheTreeWidget)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.UI)
        self.setLayout(layout)


    def setSignals(self):

        self.UI.applyChangesButton.clicked.connect(self._applyChnagesButtonClicked)
        self.UI.reloadButton.clicked.connect(self._reloadButtonClicked)
        self.UI.testButton.clicked.connect(self._testButtonClicked)


    def _createCacheTree(self):
        return cacheWidget.cacheTreeWidget()

        # treeWidget = QtGui.QTreeWidget()
        # treeWidget.setColumnCount(3)
        # treeWidget.setColumnWidth(1, 200)
        # treeWidget.setHeaderLabels(['Node', 'Cache Path', 'Status']);
        #
        # item0 = QtGui.QTreeWidgetItem(treeWidget, ['Node 0', '', ''])
        # item00 = QtGui.QTreeWidgetItem(item0, ['Node 00', u'F:/', ''] )
        # item01 = QtGui.QTreeWidgetItem(item0, ['Node 01', u'F:/', 'None'])
        #
        # return treeWidget


    def _applyChnagesButtonClicked(self):
        pass


    def _reloadButtonClicked(self):
        pass


    def _testButtonClicked(self):
        print core.houManager().getCacheList()



def main(launch_type=""):
    try:
        return hqt.showUi(CacheManager())
    except:
        return CacheManager()

#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
