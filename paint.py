import sys
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
        self.brushSize = 2
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

        threepxAction = QAction("3px", self)
        threepxAction.setShortcut("Ctrl+T")
        brushMenu.addAction(threepxAction)

        fivepxAction = QAction("5px", self)
        fivepxAction.setShortcut("Ctrl+F")
        brushMenu.addAction(fivepxAction)

        sevenpxAction = QAction("7px", self)
        sevenpxAction.setShortcut("Ctrl+S")
        brushMenu.addAction(sevenpxAction)

        ninepxAction = QAction("9px", self)
        ninepxAction.setShortcut("Ctrl+N")
        brushMenu.addAction(ninepxAction)

        blackAction = QAction("Black", self)
        blackAction.setShortcut("Ctrl+B")
        brushColor.addAction(blackAction)

        whiteAction = QAction("White", self)
        whiteAction.setShortcut("Ctrl+W")
        brushColor.addAction(whiteAction)

        redAction = QAction("Red", self)
        redAction.setShortcut("Ctrl+R")
        brushColor.addAction(redAction)

        greenAction = QAction("Green", self)
        greenAction.setShortcut("Ctrl+G")
        brushColor.addAction(greenAction)

        yellowAction = QAction("Yellow", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColor.addAction(yellowAction)

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

    def save(file):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpeg *.jpeg);; ALL Files(*.*)")
        if filePath == "":
            return
        self.image.save(filePath)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
