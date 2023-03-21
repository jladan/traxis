# Copyright (C) 2014 Syed Haider Abidi, Nooruddin Ahmed and Christopher Dydula
#
# This file is part of traxis.
#
# traxis is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# traxis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with traxis.  If not, see <http://www.gnu.org/licenses/>.

""" GuiSkeleton provides the layout for the traxis gui.
"""

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from traxis.graphics import markers, angleref, fittedarc


class GuiSkeleton(QtWidgets.QWidget):

    """The topmost widget which places all the GUI's widgets onto itself upon
    initialization.
    """

    def __init__(self):
        """Setup the base user interface - create layouts and place widgets
        and labels.
        """

        super().__init__()

        # main layout of the skeleton
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        # layout for the top portion of the user interface
        self.topWidget = QtWidgets.QWidget()
        self.mainLayout.addWidget(self.topWidget)
        # the top portion should have a fixed height, just big enough to fit
        # all of its contents
        self.topWidget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.topUiLayout = QtWidgets.QHBoxLayout(self.topWidget)
        # don't add any extra padding around the edges of this layout's widgets
        self.topUiLayout.setContentsMargins(0, 0, 0, 0)

        # track marker list GUI segment
        markerListLayout = self._create_marker_list()
        # "technical buttons" panel (reset, zoom, calculations)
        techButtonLayout = self._create_technical_buttons()
        # "user selection" GUI segment
        userSelectionLayout = self._create_user_selection()
        # console GUI segment
        consoleLayout = self._create_console()

        # Bottom portion of UI with the actual image and graphics
        bottomUiLayout = self._create_bottom_ui()

        # layout for the bottom portion of the user interface
        self._add_items(self.topUiLayout,
                        [markerListLayout, 
                         self._make_vline(), 
                         techButtonLayout, 
                         self._make_vline(), 
                         userSelectionLayout, 
                         self._make_vline(),
                         consoleLayout,
                         ])
        self.mainLayout.addWidget(self._make_hline()) # horizontal line
        self.mainLayout.addLayout(bottomUiLayout)


    def _make_vline(self):
        vline = QtWidgets.QFrame(self)  # vertical divider widget
        vline.setFrameShape(QtWidgets.QFrame.VLine)
        vline.setFrameShadow(QtWidgets.QFrame.Sunken)
        return vline

    def _make_hline(self):
        hline = QtWidgets.QFrame(self)  # vertical divider widget
        hline.setFrameShape(QtWidgets.QFrame.HLine)
        hline.setFrameShadow(QtWidgets.QFrame.Sunken)
        return hline

    def _add_items(self, layout, items):
        """ Add each widget or layout in items to the layout
        """
        for w in items:
            if isinstance(w, QtWidgets.QWidget):
                layout.addWidget(w)
            elif isinstance(w, QtWidgets.QLayout):
                layout.addLayout(w)
            else:
                raise TypeError("Expected QWidget or QLayout to add to interface")

    def _create_marker_list(self):
        """ Create the Marker List layout
        """
        markerListLayout = QtWidgets.QVBoxLayout()  # marker list layout

        markerListLabel = QtWidgets.QLabel(self)  # marker list label
        markerListLabel.setText("Track Markers")

        self.markerList = markers.MarkerList(self)  # marker list widget
        self.markerList.setFixedWidth(markerListLabel.width()*2)
        # don't focus on this widget when clicked
        self.markerList.setFocusPolicy(QtCore.Qt.NoFocus)

        # clear markers button widget
        self.clearMarkerButton = QtWidgets.QPushButton(self)
        # don't focus on this widget when clicked
        self.clearMarkerButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clearMarkerButton.setText("Clear Markers")
        self.clearMarkerButton.setToolTip(
            "Clear all the selected points and calculated values")
        # self.clearMarkerButton.setShortcut(QtGui.QKeySequence("C"))

        self._add_items(markerListLayout, 
                          [markerListLabel, self.markerList, self.clearMarkerButton])
        return markerListLayout


    def _create_technical_buttons(self):
        """ Create the "technical buttons" layout.

        This includes the reset, zoom, and calculation buttons.
        """
        techButtonLayout = QtWidgets.QVBoxLayout()

        resetButtonLabel = QtWidgets.QLabel(self)  # reset button label
        resetButtonLabel.setText("Reset Analysis")

        self.resetButton = QtWidgets.QPushButton(self)  # reset button widget
        # don't focus on this widget when clicked
        self.resetButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.resetButton.setText("Reset")
        self.resetButton.setToolTip(
            "Reset all the selected points and calculated variables")
        self.resetButton.setShortcut(QtGui.QKeySequence("R"))

        zoomLabel = QtWidgets.QLabel(self)  # zoom label
        zoomLabel.setText("Zoom")

        # horizontal layout for zoom buttons
        zoomLayout = QtWidgets.QHBoxLayout()

        # zoom in button widget
        self.zoomInButton = QtWidgets.QPushButton(self)
        # don't focus on this widget when clicked
        self.zoomInButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zoomInButton.setText("Zoom In")
        self.zoomInButton.setToolTip("Zoom into the picture")
        self.zoomInButton.setShortcut(QtGui.QKeySequence("Z"))

        # zoom out button widget
        self.zoomOutButton = QtWidgets.QPushButton(self)
        self.zoomOutButton.setFocusPolicy(QtCore.Qt.NoFocus)
        # don't focus on this widget when clicked
        self.zoomOutButton.setText("Zoom Out")
        self.zoomOutButton.setToolTip("Zoom out from the picture")
        self.zoomOutButton.setShortcut(QtGui.QKeySequence("X"))

        zoomLayout.addWidget(self.zoomInButton)
        zoomLayout.addWidget(self.zoomOutButton)

        calcLabel = QtWidgets.QLabel(self)  # calculate label
        calcLabel.setText("Calculate")

        # calculate momentum button widget
        self.calcMomentumButton = QtWidgets.QPushButton(self)
        # don't focus on this widget when clicked
        self.calcMomentumButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.calcMomentumButton.setText("Calculate Track Momentum")
        self.calcMomentumButton.setToolTip("Calculate Track momentum")
        self.calcMomentumButton.setShortcut(QtGui.QKeySequence("M"))

        # calculate optical density button widget
        self.calcDensityButton = QtWidgets.QPushButton(self)
        # don't focus on this widget when clicked
        self.calcDensityButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.calcDensityButton.setText("Calculate Optical Density")
        self.calcDensityButton.setToolTip("Calculate Optical Density")
        self.calcDensityButton.setShortcut(QtGui.QKeySequence("N"))

        # calculate angle button widget
        self.calcAngleButton = QtWidgets.QPushButton(self)
        # don't focus on this widget when clicked
        self.calcAngleButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.calcAngleButton.setText("Calculate Angle")
        self.calcAngleButton.setToolTip("Calculate Opening Angle")
        self.calcAngleButton.setShortcut(QtGui.QKeySequence("B"))

        self._add_items(techButtonLayout,
                          [resetButtonLabel, 
                           self.resetButton, 
                           zoomLabel,
                           zoomLayout,
                           calcLabel,
                           self.calcMomentumButton, 
                           self.calcDensityButton, 
                           self.calcAngleButton,
                           ])
        # add stretch to segment to keep widgets together
        techButtonLayout.addStretch(0)
        return techButtonLayout

    def _create_user_selection(self):
        # user seletion segment layout
        userSelectionLayout = QtWidgets.QVBoxLayout()

        openSaveLabel = QtWidgets.QLabel(self)  # open/save label
        openSaveLabel.setText("Open/Save")

        self.openImageButton = QtWidgets.QPushButton(
            self)  # open image button widget
        # don't focus on this widget when clicked
        self.openImageButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.openImageButton.setText("Open Image")
        self.openImageButton.setToolTip("Open image for analysis")
        self.openImageButton.setShortcut(QtGui.QKeySequence("O"))

        # horizontal layout for save and load buttons
        saveLayout = QtWidgets.QHBoxLayout()

        # save session button widget
        self.saveSessionButton = QtWidgets.QPushButton(self)
        # don't focus on this widget when clicked
        self.saveSessionButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.saveSessionButton.setText("Save")
        self.saveSessionButton.setToolTip("Save current analysis session")
        
        # load session button widget
        self.loadSessionButton = QtWidgets.QPushButton(self)
        # don't focus on this widget when clicked
        self.loadSessionButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.loadSessionButton.setText("Load")
        self.loadSessionButton.setToolTip(
            "Load a previously saved analysis session")

        # screenshot button widget
        self.screenshotButton = QtWidgets.QPushButton(self)
        # don't focus on this widget when clicked
        self.screenshotButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.screenshotButton.setText("Save Screenshot")
        self.screenshotButton.setToolTip(
            "Take a screenshot of the scroll area contents and save to image")

        modeLabel = QtWidgets.QLabel(self) # mode label
        modeLabel.setText("Mode")

        # place marker mode button widget
        self.placeMarkerButton = QtWidgets.QPushButton(self)
        # make the button checkable (i.e. stays depressed when clicked)
        self.placeMarkerButton.setCheckable(True)
        # don't focus on this widget when clicked
        self.placeMarkerButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.placeMarkerButton.setText("[Mode] Place Track Markers")
        self.placeMarkerButton.setToolTip(
            "Enter mode for placing markers on loaded image.")
        self.placeMarkerButton.setShortcut("P")

        # draw angle reference mode button widget
        self.drawRefButton = QtWidgets.QPushButton(self)
        # make the button checkable (i.e. stays depressed when clicked)
        self.drawRefButton.setCheckable(True)
        # don't focus on this widget when clicked
        self.drawRefButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.drawRefButton.setText("[Mode] Draw Angle Reference")
        self.drawRefButton.setToolTip(
            "Enter mode for drawing angle reference on loaded image.")
        self.drawRefButton.setShortcut("L")

        # dl form layout
        dlFormLayout = QtWidgets.QFormLayout()

        # dl label
        dlLabel = QtWidgets.QLabel(self)
        dlFormLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, dlLabel)
        dlLabel.setText("Set dL")

        # dl text box (line edit) widget
        self.dlLineEdit = QtWidgets.QLineEdit(self)
        # fix the size of the text box
        self.dlLineEdit.setSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        dlFormLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.dlLineEdit)
        # set the dL value to 0 by default
        self.dlLineEdit.setText("0")
        # validate the contents of the text box so that only floats can
        # be entered
        self.dlLineEdit.setValidator(
            QtGui.QRegExpValidator(QtCore.QRegExp('[0-9]+\.?[0-9]*')))

        # Add all the widgets and layout
        saveLayout.addWidget(self.saveSessionButton)
        saveLayout.addWidget(self.loadSessionButton)
        self._add_items(userSelectionLayout,
                        [openSaveLabel, self.openImageButton, saveLayout,
                         self.screenshotButton, 
                         modeLabel, 
                         self.placeMarkerButton, 
                         self.drawRefButton, 
                         dlFormLayout, ])
        # add stretch to segment to keep widgets together
        userSelectionLayout.addStretch(0)
        return userSelectionLayout

    def _create_console(self):
        # console GUI segment
        consoleLayout = QtWidgets.QVBoxLayout()  # console segment layout

        consoleLabel = QtWidgets.QLabel(self)  # console label
        consoleLabel.setText("Console")

        # console text browser widget
        self.consoleTextBrowser = QtWidgets.QTextBrowser(self)
        self.consoleTextBrowser.setMinimumWidth(100)

        # Add widgets to layout
        consoleLayout.addWidget(self.consoleTextBrowser)
        consoleLayout.addWidget(consoleLabel)
        return consoleLayout

    def _create_bottom_ui(self):
        bottomUiLayout = QtWidgets.QHBoxLayout()

        # create a graphics scene on which images and all graphics will be
        # displayed
        self.scene = QtWidgets.QGraphicsScene()
        # the graphics view is the widget that actually displays the contents
        # of the graphics scene
        self.sceneView = QtWidgets.QGraphicsView(self.scene, self)
        # set a minimum size for the scene view
        self.sceneView.setMinimumWidth(900)
        self.sceneView.setMinimumHeight(400)

        # instantiate QImage and PixmapItem
        self.sceneImage = QtGui.QImage()
        self.scenePixmap = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.scenePixmap)

        # instantiate reference line and momentum arc objects
        self.angleRefLine = angleref.ReferenceLine()
        self.momentumArc = fittedarc.MomentumArc()
 
        # set the tangentLine attribute to None initially so that there is
        # something to check for when a tangent has not been drawn yet
        self.tangentLine = None

        bottomUiLayout.addWidget(self.sceneView)
        return bottomUiLayout
