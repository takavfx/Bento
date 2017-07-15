# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Managing cache tool.
"""
#-------------------------------------------------------------------------------

import sys
sys.dont_write_bytecode = True
import os
import webbrowser

import imp
try:
    imp.find_module('PySide2')
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *
except ImportError:
    from PySide.QtGui import *
    from PySide.QtCore import *

import hou

import core
reload(core)
import define as Define
reload(Define)
import cacheWidget
reload(cacheWidget)

try:
    import hqt
except:
    pass


class CacheManager(QWidget):
    """docstring for CacheManager"""


    def __init__(self, parent=None):
        super(CacheManager, self).__init__()

        self.initSettings()


    def initSettings(self):
        self.initGUI()


    def initGUI(self):
        self.setProperty("houdiniStyle", True)

        layout = QVBoxLayout()

        ## Create Menu Bar
        self._createMenuBar()

        ## Add Edit Menu
        self._createEditMenu()

        ## Add View Menu
        self._createViewMenu()

        ## Add About Menu
        self._createAboutMenu()
        layout.addWidget(self.menuBar)

        self.cacheTreeWidget = self._createCacheTree()
        layout.addWidget(self.cacheTreeWidget)
        layout.setContentsMargins(0,0,0,0)

        self.setLayout(layout)

        try:
            self.setStyleSheet(hqt.get_h14_style())
        except:
            pass

    def _createMenuBar(self):
        """Helper method for the constructor.

        Create the menu bar.
        """
        self.menuBar = QMenuBar()
        self.menuBar.setFixedHeight(25)

        # help_button = QToolButton()
        # help_button.setFixedWidth(25)
        # help_button.setFixedHeight(25)
        # help_button.clicked.connect(self.showHelp)
        # try:
        #     help_button.setIcon(hou.ui.createQtIcon("BUTTONS_help", 32, 32))
        # except:
        #     help_button.setText("H")
        # help_button.setProperty("transparent", True);
        #
        # self.menuBar.setCornerWidget(help_button)
        # self.menuBar.cornerWidget(Qt.TopRightCorner)


    def _createEditMenu(self):

        edit_menu = QMenu(self)

        reloadAction = edit_menu.addAction("Reload")
        reloadAction.setShortcuts(("Ctrl+R", "F5"))
        self.addAction(reloadAction)
        reloadAction.triggered.connect(self._reloadButtonTriggered)

        edit_action = self.menuBar.addAction("Edit")
        edit_action.setMenu(edit_menu)


    def _createViewMenu(self):

        view_menu = QMenu(self)

        self.viewActionGroup = QActionGroup(self)

        showRWaction = view_menu.addAction("Toggle R/W")
        showRWaction.setShortcut("Ctrl+E")
        self.addAction(showRWaction)
        showRWaction.triggered.connect(self._showRwButtonTriggered)

        view_menu.addSeparator()

        self.bothNodesAction = view_menu.addAction("Both Nodes")
        self.bothNodesAction.setCheckable(True)
        self.bothNodesAction.setChecked(True)
        self.bothNodesAction.triggered.connect(self._showBothNodes)
        self.viewActionGroup.addAction(self.bothNodesAction)

        self.readNodesOnlyAction = view_menu.addAction("Read Nodes Only")
        self.readNodesOnlyAction.setCheckable(True)
        self.readNodesOnlyAction.triggered.connect(self._showReadNodesOnly)
        self.viewActionGroup.addAction(self.readNodesOnlyAction)

        self.writeNodesOnlyAction = view_menu.addAction("Write Nodes Only")
        self.writeNodesOnlyAction.setCheckable(True)
        self.writeNodesOnlyAction.triggered.connect(self._showWriteNodesOnly)
        self.viewActionGroup.addAction(self.writeNodesOnlyAction)

        view_action = self.menuBar.addAction("View")
        view_action.setMenu(view_menu)


    def _createAboutMenu(self):

        about_menu = QMenu(self)

        openGitHubAction = QAction("Bento on GitHub", self)
        openGitHubAction.triggered.connect(self._gitHubButtonTriggered)

        about_menu.addAction(openGitHubAction)
        about_action = self.menuBar.addAction("About")
        about_action.setMenu(about_menu)


    def _createCacheTree(self):
        return cacheWidget.cacheTreeWidget()


    def _reloadButtonTriggered(self):
        self.cacheTreeWidget.reload()
        checked_action = self.viewActionGroup.checkedAction()

        if checked_action.text() == "Read Nodes Only":
            self.cacheTreeWidget.showNodesToggle("read")

        elif checked_action.text() == "Write Nodes Only":
            self.cacheTreeWidget.showNodesToggle("write")


    def _showRwButtonTriggered(self):
        self.cacheTreeWidget.switchRwVisible()


    def _showBothNodes(self):
        self.cacheTreeWidget.showNodesToggle("both")


    def _showReadNodesOnly(self):
        self.cacheTreeWidget.showNodesToggle("read")


    def _showWriteNodesOnly(self):
        self.cacheTreeWidget.showNodesToggle("write")


    def _gitHubButtonTriggered(self):
        webbrowser.open('http://github.com/takavfx/Bento')
