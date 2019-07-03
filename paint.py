import sys
from functools import partial
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QMenuBar, QFileDialog


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        top = 400
        left = 400
        width = 800
        height = 600

        self.setWindowTitle('Paint')
        self.setGeometry(top, left, width, height)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.black

        self.lastPoint = QPoint()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        brushMenu = mainMenu.addMenu("Brush Size")
        brushColor = mainMenu.addMenu("Brush Color")

        saveAction = QAction("Save", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction("Clear", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        threepxAction = QAction("3px", self)
        threepxAction.setShortcut("Ctrl+T")
        brushMenu.addAction(threepxAction)
        threepxAction.triggered.connect(partial(self.brush_size, 3))

        fivepxAction = QAction("5px", self)
        fivepxAction.setShortcut("Ctrl+F")
        brushMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(partial(self.brush_size, 5))

        sevenpxAction = QAction("7px", self)
        sevenpxAction.setShortcut("Ctrl+S")
        brushMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(partial(self.brush_size, 7))

        ninepxAction = QAction("9px", self)
        ninepxAction.setShortcut("Ctrl+N")
        brushMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(partial(self.brush_size, 9))

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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

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

    def brush_size(self, size):
        self.brushSize = size

    def brush_color(self, color):
        self.brushColor = color

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
