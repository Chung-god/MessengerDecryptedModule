from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Button(QToolButton):
    def __init__(self, img, size, callback=None):
        super().__init__()
        self.img = img
        self.size = size
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        if callback != None:
            self.clicked.connect(callback)
        
    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(self.size)
        size.setWidth(max(size.width(), size.height()))
        return size

    def paintEvent(self, event):
        QToolButton.paintEvent(self, event)
        qp = QPainter(self)
        qp.drawPixmap(self.rect(), self.img)