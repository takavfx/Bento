# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
## Description
"""
Construct Cache Table with PySide.GtGui.
"""
#-------------------------------------------------------------------------------

import os, sys
sys.dont_write_bytecode = True

from PySide import QtCore, QtGui

from . import define as Define
reload(Define)


CURRENT_PATH = os.path.driname(__file__)


#-------------------------------------------------------------------------------
# QTreeWidget for displaying Cache List
#-------------------------------------------------------------------------------
class cacheTreeWidget(QtGui.QTreeWidget):
    """docstring for cacheTableView"""

    mouseReleased = QtCore.Signal(QtCore.QPoint)
    keyPressed = QtCore.Signal(QtGui.QKeyEvent)

    HEADER_SETTING = Define.HEADER_ITEMS

    def __init__(self, parent):
        super(cacheTableView, self).__init__(parent)
        self._parent = parent
        self.cache_nodes = self.getCacheList()
        self.initSettings()


    def _initUI(self):

        self.setColumnCount(len(self.HEADER_SETTING))
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        headerLabels = usefuls.makeListByDictKey("display", self.HEADER_SETTING, "")
        self.setHeaderLabels(headerLabels)
        self.setSortingEnabled(True)
        self._setHeaderWidth()
        self._setHeaderVisible()
        self.itemChanged.connect(self.checkItemEvent)
        self.customContextMenuRequested.connect(self.showCellMenu)


    def _setHeaderWidth(self):

        for i, setting in enumerate(self.HEADER_SETTING):
            width = setting.get("width")

            if width is not None:
                self.setColumnWidth(i, width)


    def _setHeaderVisible(self):

        for i, setting in enumerate(self.HEADER_SETTING):
            visible = setting.get("visible")

            if visible is False:
                self.hideColumn(i)


    def section(self, key):
        for i, setting in enumerate(self.HEADER_SETTING):

            if setting.get("key") == key:
                return i

        raise RuntimeError("No %s key found in table setting." % key)


    def showCellMenu(self, pos):
        pass


    def setData(self, nodes, category = None, uncheckAll = False):

        self.blockSignals(True)
        self.clear()
        self._categoryType = category

        for nodes, layerObjects in nodes.iteritems():

            if isinstance(nodes, tuple):
                itemName = "%s%s" % nodes

            elif isinstance(nodes, (str, unicode)):
                itemName = "%s" % nodes

            else:
                itemName = ""

#-------------------------------------------------------------------------------
# QTreeWidget for displaying Cache List
#-------------------------------------------------------------------------------
# class CacheTableDelegate(QtGui.QStyledItemDelegate):
#     """docstring for CacheTableModel"""
#
#     HEADER_SETTING = Define.
#
#     def __init__(self, parent=None):
#         super(CacheTableDelegate, self).__init__(parent)
#
#
#     def paint(self):
#         selected = False
#
#         if option.state & QtGui.QStyle.State_Selected:
#             selected = True
#
#         name = index.data(QtCore.Qt.BackgroundRole)
#         description = index.data(DESCRIPTION_ROLE)



#-------------------------------------------------------------------------------
# EOF
#-------------------------------------------------------------------------------
