# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Managing cache tool.
"""
#-------------------------------------------------------------------------------

__version__ = 'v1.1.1'

#-------------------------------------------------------------------------------

import os, sys

from hutil.Qt import QtWidgets
from hutil.Qt import QtGui
from hutil.Qt import QtCore

import hou


class CamSwitcherGUI(QtWidgets.QWidget):
    """docstring for GUI"""


    _windowName   = 'camSwticher'
    _windowTitle  = 'Cam Switcher'
    _windowWidth  = 260
    _windowHeight = 400

    def __init__(self, parent=None):
        super(CamSwitcherGUI, self).__init__(parent)

        self.initUI()


    def closeEvent(self, event):
        self.setParent(None)


    def initUI(self):
        self.setProperty("houdiniStyle", True)
        self.setWindowTitle(self._windowTitle)

        # Create Camera List Layout > self.createCamListLayout
        self._createRefreshButton()
        self._createCamListLayout()

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(self.buttonLayout)
        layout.addLayout(self.camListLayout)
        layout.setContentsMargins(0,0,0,0)

        self.setLayout(layout)

        self.setSignals()

        self.resize(self._windowWidth, self._windowHeight)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def setSignals(self):
        self.refreshButton.clicked.connect(self.refreshCamList)


    def _createRefreshButton(self):
        self.refreshButton = QtWidgets.QPushButton()
        self.refreshButton.setText('Refresh')
        self.refreshButton.setFixedHeight(30)

        self.buttonLayout = QtWidgets.QVBoxLayout()
        self.buttonLayout.addWidget(self.refreshButton)


    def _createCamListLayout(self):

        self.cam_listView = QtWidgets.QListView()
        self.cam_listView.setAlternatingRowColors(True)

        model = camListModel(data = self.getCamList())
        self.cam_listView.setModel(model)

        self.cam_listView.clicked.connect(self.selectCam)

        self.camListLayout = QtWidgets.QVBoxLayout()
        self.camListLayout.addWidget(self.cam_listView)


    def refreshCamList(self):
        model = camListModel(data = self.getCamList())
        self.cam_listView.setModel(model)


    def getCamList(self):
        camList = []
        nodes = hou.pwd().allSubChildren()

        for node in nodes:
            node_type = node.type().name().lower()

            if node_type == "cam":
                camList.append(self.createNodeInfo(node, node_type))

        return camList


    def createNodeInfo(self, node, node_type):
        node_info = {}

        node_info["path"]  = node.path()
        node_info["name"]  = node.name()
        node_info["color"] = node.color().rgb()

        return node_info


    def selectCam(self):
        listview = self.sender()
        currentItem = listview.selectedIndexes()

        tabs = hou.ui.currentPaneTabs()

        for tab in tabs:
            if tab.isCurrentTab():
                if tab.type() == hou.paneTabType.SceneViewer:
                    try:
                        tab.viewports()[-1].setCamera(hou.node(currentItem[0].data()))
                    except:
                        pass
                        


class camListModel(QtCore.QAbstractListModel):
    """docstring for camListModel"""
    def __init__(self, parent=None, data=None):
        super(camListModel, self).__init__(parent)
        self.__items = data


    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__items)


    def data(self, index, role = QtCore.Qt.DisplayRole):

        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self.__items):
            return None

        if role == QtCore.Qt.DisplayRole:
            return self.__items[index.row()].get("path")

        else:
            return None


    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled


def main(launch_type=''):
    if launch_type == 'pypanel':
        return CamSwitcherGUI()

    elif launch_type == 'floating':
        ui = CamSwitcherGUI()
        ui.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        ui.show()
