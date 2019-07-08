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

from PyQt5 import QtWidgets, QtGui, QtCore
from traxis import constants


class MarkerList(QtWidgets.QListWidget):
    """Track Marker list class.

    This class is intended to contain TrackMarker objects, and implements a
    number of methods to work with the extra features that TrackMarker adds to
    QListWidgetItem.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def addMarker(self, x, y, size, width, scene):
        """Create a new TrackMarker and add it to the list.

        The marker is created with this list as its parent, and is drawn to the
        designated QGraphicsScene.

        Parameters
        ----------
        x, y  : (floats) marker coordinates
        size  : size of ellipse to draw
        width : pen width
        scene : the QGraphicsScene to draw the marker on.

        Returns
        -------
        the TrackMarker object.
        """
        # use the last item in the list to determine the new marker's id
        lastItem = self.item(self.count()-1)
        if lastItem:
            newMarkerId = lastItem.id + 1
        else:
            newMarkerId = 1

        newMarker = TrackMarker(newMarkerId, x, y, size, width, self)
        self.setCurrentItem(newMarker)
        scene.addItem(newMarker.ellipse)

        return newMarker

    def deleteMarker(self, marker):
        """Remove the TrackMarker object marker from this marker list."""
        # remove the marker's ellipse from its graphics scene
        marker.ellipse.scene().removeItem(marker.ellipse)

        markerRow = self.row(marker)
        self.takeItem(markerRow)

    def empty(self):
        """Remove all TrackMarker objects from this marker list."""
        # First remove the markers from the scene
        for row in range(self.count()):
            marker = self.item(row)
            marker.ellipse.scene().removeItem(marker.ellipse)
        # now it's safe to clear the list
        self.clear()

    def rescale(self, size, width):
        """Set the size of each marker's circle.

        Parameters
        size  : the circle's diameter
        width : the pen width
        """
        for row in range(self.count()):
            marker = self.item(row)
            marker.rescale(size, width)

    def setStartPoint(self, marker):
        """Designate marker as the start point."""
        # Clear the old startpoint's designation
        oldStartPoint = self.getStartPoint()
        if oldStartPoint:
            oldStartPoint.setDesignation()
            oldStartPoint.recolor()

        # designate marker as the new start point
        marker.setDesignation('start')

    def setEndPoint(self, marker):
        """Designate marker as the end point for this list of markers."""
        # Clear the old startpoint's designation
        oldEndPoint = self.getEndPoint()
        if oldEndPoint:
            oldEndPoint.setDesignation()
            oldEndPoint.recolor()

        # designate marker as the new start point
        marker.setDesignation('end')

    def getStartPoint(self):
        """Return the TrackMarker object designated as the start point

        If no TrackMarker is designated as the start, return None.
        """
        for row in range(self.count()):
            marker = self.item(row)
            if marker.designation == 'start':
                return marker
        return None

    def getEndPoint(self):
        """Return the TrackMarker object designated as the end point

        If no TrackMarker is designated as the end, return None.
        """
        for row in range(self.count()):
            marker = self.item(row)
            if marker.designation == 'end':
                return marker
        return None

    def highlightCurrent(self):
        """Change all markers to their correct colour."""
        for row in range(self.count()):
            marker = self.item(row)
            marker.recolor()

    def selectNext(self):
        """Set the currently selected marker to the next marker in the list."""
        # if there are no markers selected (currentRow() == -1) or if the
        # currently selected marker is the last one in the list, return
        if self.currentRow() == -1 or self.currentRow() == self.count() - 1:
            return
        else:
            self.setCurrentRow(self.currentRow() + 1)

    def selectPrevious(self):
        """Set the currently selected marker to the previous marker in the list."""
        # if there are no markers selected (currentRow() == -1) or if the
        # currently selected marker is the first one in the list, return
        if self.currentRow() == -1 or self.currentRow() == 0:
            return
        else:
            self.setCurrentRow(self.currentRow() - 1)

class TrackMarker(QtWidgets.QListWidgetItem):
    """Track marker class.

    This class subclasses QListWidgetItem, adding attributes for markers:
       - id (unique),
       - displayed name
       - designation (start, end, selected, or none),
       - coordinates
       - QGraphicsEllipseItem
    """

    def __init__(self, markerId, x, y, size, width, parent=None):
        """ Create a new marker.

        It is up to the caller to ensure the markerId is unique. This is
        primarily used to create a displayed name.

        Parameters:
        markerId    : identifier for the marker,
        x, y        : (float) x and y coordinates,
        size        : (float) the size of the marker,
        width       : (float) the width of the pen used to draw the marker,
        parent      : (optional) MarkerList to which the marker will be added.
        """
        self.id = markerId
        self._x = x
        self._y = y

        self.designation = None
        markerName = "Point {}".format(self.id)

        super().__init__(markerName, parent)

        # set a minimum rect size
        if size < 2:
            size = 2

        # set a minimum pen width
        if width < 1:
            width = 1

        # create the ellipse to be drawn as the marker
        ellipsePen = QtGui.QPen(constants.DEFAULTMARKERCOLOR)
        ellipsePen.setWidth(width)
        ellipseRect = QtCore.QRectF(x, y, size, size)
        ellipseRect.moveCenter(QtCore.QPointF(x, y))

        self.ellipse = QtWidgets.QGraphicsEllipseItem(ellipseRect)
        self.ellipse.setPen(ellipsePen)

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value

    def setDesignation(self, designation=None):
        """Indicate the marker as a Start Point, an End Point or neither, as
        specified by designation (a string).
        """
        if designation not in [None, 'start', 'end']:
            return

        self.designation = designation

        # indicate the designation in the displayed name
        if designation == 'start':
            self.setText("s - Point {}".format(self.id))
        elif designation == 'end':
            self.setText("e - Point {}".format(self.id))
        else:
            self.setText("Point {}".format(self.id))

    def recolor(self):
        """Update the colour of the marker based on its designation or whether
        it is currently selected.
        """
        newPen = self.ellipse.pen()

        # Set the pen's colour based on the designation
        if self.isSelected():
            newPen.setColor(constants.HIGHLIGHTMARKERCOLOR)
        elif self.designation == 'start':
            newPen.setColor(constants.STARTMARKERCOLOR)
        elif self.designation == 'end':
            newPen.setColor(constants.ENDMARKERCOLOR)
        else:
            newPen.setColor(constants.DEFAULTMARKERCOLOR)

        self.ellipse.setPen(newPen)

    def move(self, dx, dy):
        """Move the marker from its current position (x, y) to (x+dx, y+dy).
        dx and dy are floats.
        """
        # create a new rect, starting from the existing rect of the marker's
        # ellipse
        newRect = self.ellipse.rect()
        # translate the rect by (dx, dy)
        newRect.translate(dx, dy)
        # set the translated rect as the marker's ellipse's rect
        self.ellipse.setRect(newRect)

    def getAngle(self, origin, referenceMarker=None):
        """Return the marker's angular coordinate.

        Parameters:
        origin          : a tuple of x, and y values for the origin.
        referenceMarker : another marker to use as an angle reference with the origin

        Returns:
        angle : The marker's angle in polar coordinates using the origin, or
                relative to the line connecting the origin to tyhe reference marker.
        """
        markerVector = QtCore.QLineF(origin[0], origin[1], self.x, self.y)

        # define the the vector to measure the angle from
        if referenceMarker:
            referenceX = referenceMarker.x
            referenceY = referenceMarker.y
        else:
            referenceX = origin[0] + 1
            referenceY = origin[1]
        referenceVector = QtCore.QLineF(origin[0], origin[1], referenceX, referenceY)

        # compute the angular coordinate of the marker
        angle = referenceVector.angleTo(markerVector)

        return angle

    def rescale(self, size, width):
        """Set the radius and penwidth of the marker's circle."""
        if size < 2:
            size = 2
        if width < 1:
            width = 1

        # Make the new circle by updating ellipse's rectangle
        newRect = self.ellipse.rect()
        newRect.setWidth(size)
        newRect.setHeight(size)
        # move the rect's center to match that of the original rect's (the
        # center gets shifted when resizing)
        newRect.moveCenter(self.ellipse.rect().center())
        self.ellipse.setRect(newRect)

        # Set the circle's penwidth
        newPen = self.ellipse.pen()
        newPen.setWidth(width)
        self.ellipse.setPen(newPen)
