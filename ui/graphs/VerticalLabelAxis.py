import math
from PyQt5.QtGui import QColor
import pyqtgraph as pg

class VerticalLabelAxis(pg.AxisItem):
    def __init__(self, orientation, **kwargs):
        super().__init__(orientation, **kwargs)
        self._angle = -45  # Set the desired angle for the labels
        self._height_updated = False

    def drawPicture(self, p, axisSpec, tickSpecs, textSpecs):
        max_width = 80
        self._angle = self._angle % 90
        p.setPen(QColor(200, 200, 200))  # Set the text color to light grey

        for rect, flags, text in textSpecs:
            p.save()  # Save the painter state
            p.translate(rect.center())  # Move coordinate system to center of text rect
            p.rotate(self._angle)  # Rotate text
            p.translate(-rect.center())  # Revert coordinate system
            x_offset = math.ceil(math.fabs(math.sin(math.radians(self._angle)) * rect.width()))
            if self._angle < 0:
                x_offset = -x_offset
            p.translate(x_offset / 1.5, 0)  # Move the coordinate system (relatively) downwards
            p.drawText(rect, flags, text)
            p.restore()  # Restore the painter state
            offset = math.fabs(x_offset)
            max_width = offset if max_width < offset else max_width

        # Adjust the height
        if not self._height_updated:
            self.setHeight(self.height() + max_width)
            self._height_updated = True
