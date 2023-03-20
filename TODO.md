TODO List for the traxis code review
====================================

Overall
-------
- clean up comments (many just state the next line of code)
- Fix docstrings to a more common standard format
  - state function
  - summary of algorithm
  - then arguments/inputs
  - then the result
  - finally the algorithm details if appropriate
- Add module docstrings where appropriate
- Format docstrings

traxis/constants.py
------------------
- Highlight which "constants" can be modified
- Possibly add in-program controls for changing settings
- Remove useless comments like "tangent line colours"

traxis/gui/maingui.py
---------------------
- move calcTrackMomentum() to the calc submodule
  - also make separate functions for handling the conversions (px to cm, etc)
- Separate the drawing code from the calculation code
- look into template strings for the messages (to reduce calls to .displayMessage())
- rename .displayMessage() to something shorter, like `log()`
- restructure the key-handler - make it more of a decision-tree
  - make a function to move a point, and call that from the wasd events
  - otherwise, it's fine.

traxis/calc/anglecalc.py
------------------------
- make marker.getAngle() a function in calc instead of a marker method
- circleParams makes more sense as a named tuple than a dict
+ The change in radius would affect the slope, because it changes tangentPoint
- I think points could also be named tuples.
- Double check error calculation for the angle
- check where angleTo() is defined to see if it's appropriate

traxis/calc/circlefit.py
------------------------
- see if QListWidget has an __iter__() method for all the for loops
- I am uncomfortable with the markers having their drawn centers used as points, rather than storing their actual values
- The doc punctuation is bad.
- look into whether the algorithm using means is the best way to fit the circle

traxis/gui/mainwindow.py
------------------------
- Doesn't really need its own file
- probably move into maingui.py

traxis/gui/skeleton.py
----------------------
- Go over comments and make sure they're useful
- Look into QT XML for window layout

traxis/graphics/angleref.py
---------------------------
- docs and comments

traxis/graphics/fittedarc.py
---------------------------
- This should handle odd dl values rather than MainGui
- Use setters and getters to handle properties and update, rather than args to draw
  - including, dl, center, radius, start/end
- start angle and span should be handled by this object too (instead of MainGui)
- Add accessor function to span_angle

traxis/graphics/markers.py
---------------------------
- There must be a way to grab all objects from a scene to redraw them, so that MarkerList and such aren't stuck tracking them for all rescales
- Change 'start_point' and 'end_point' to properties (@property) of the MarkerList, rather than the markers themselves
  - except that markers handle their own colour by their designation
  - so just set the designation in that setup
- Look up the QListWidget methods for something better than self.item() and self.count()
- Why does TrackMarker() take sie and width arguments?
- @properties for TrackMarker.designation too
- make enum-style constants for designation types
- could probably do something better than an if, elif statement to set pen colour
- not sure why `getAngle()` is a marker method
- also don't know why rescaling is partially handled by the objects the way it is.
- Do new rects and pens have to be created for each change, or can their properties be changed?

traxis/graphics/tangent.py
--------------------------
- similar questions to width and rescale as in markers.py

