import sys
from functools import partial
from pynput.mouse import Button, Controller
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QImage, QPainter, QPen, QTabletEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QMenuBar, QFileDialog


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        top = 400
        left = 400
        width = 800
        height = 600

        self.cursor = Controller()

        self.setWindowTitle('Paint')
        self.setGeometry(top, left, width, height)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.brushColor = Qt.black
        self.pen_down = False
        self.lastPoint = QPoint()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        brushColor = mainMenu.addMenu("Brush Color")

        saveAction = QAction("Save", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction("Clear", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        blackAction = QAction("Black", self)
        blackAction.setShortcut("Ctrl+B")
        brushColor.addAction(blackAction)
        blackAction.triggered.connect(partial(self.brush_color, Qt.black))

        whiteAction = QAction("White", self)
        whiteAction.setShortcut("Ctrl+W")
        brushColor.addAction(whiteAction)
        whiteAction.triggered.connect(partial(self.brush_color, Qt.white))

        redAction = QAction("Red", self)
        redAction.setShortcut("Ctrl+R")
        brushColor.addAction(redAction)
        redAction.triggered.connect(partial(self.brush_color, Qt.red))

        greenAction = QAction("Green", self)
        greenAction.setShortcut("Ctrl+G")
        brushColor.addAction(greenAction)
        greenAction.triggered.connect(partial(self.brush_color, Qt.green))

        blueAction = QAction("Blue", self)
        blueAction.setShortcut("Ctrl+B")
        brushColor.addAction(blueAction)
        blueAction.triggered.connect(partial(self.brush_color, Qt.blue))

    def tabletEvent(self, event):
        if event.type() == QTabletEvent.TabletPress:
            self.pen_down = True
            self.lastPoint = event.pos()
            self.brushSize = int(event.pressure() * 20)
        elif event.type() == QTabletEvent.TabletMove and event.pressure() > 0:
            self.pen_down = True
            self.brushSize = int(event.pressure() * 20)
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
        else:
            self.pen_down = False
        if self.pen_down:
            self.cursor.click(Button.left, 1)
        event.accept()
        self.update()

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "untitled.png", "PNG(*.png);;JPEG(*.jpg *.jpeg);; ALL Files(*.*)")
        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def brush_color(self, color):
        self.brushColor = color

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
