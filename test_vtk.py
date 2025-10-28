from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QTextBrowser, QFrame
from PyQt6.QtGui import QFont
import sys
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer
)


class MainWindow(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.InintUI(width, height)

    def InintUI(self, width, height):
        self.kw = 1500 / width
        self.kh = 750 / height
        self.setGeometry(0, 0, width, height)
        self.setFixedSize(width, height)
        font = QFont()
        font.setFamily("Comic Sans MS")

        ball = vtk.vtkSTLReader()
        ball.SetFileName("models/ball.stl")
        cilinder = vtk.vtkSTLReader()
        cilinder.SetFileName("models/cilinder.stl")
        cube = vtk.vtkSTLReader()
        cube.SetFileName("models/cube.stl")
        self.frame = QFrame()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vtkWidget.resize(width, height)
        self.ren = vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        mapper1 = vtkPolyDataMapper()
        mapper1.SetInputConnection(ball.GetOutputPort())
        mapper2 = vtkPolyDataMapper()
        mapper2.SetInputConnection(cube.GetOutputPort())
        mapper3 = vtkPolyDataMapper()
        mapper3.SetInputConnection(cilinder.GetOutputPort())

        actor1 = vtkActor()
        actor1.SetMapper(mapper1)
#        actor2 = vtkActor()
#        actor2.SetMapper(mapper2)
        actor3 = vtkActor()
        actor3.SetMapper(mapper3)

        self.ren.AddActor(actor1)
#        self.ren.AddActor(actor2)
        self.ren.AddActor(actor3)

        self.ren.ResetCamera()

        self.setCentralWidget(self.frame)
        self.frame.resize(1500, 1500)
#        self.frame.move(0, 0)
        self.frame.hide()

        self.startbutton = QPushButton("Начать просмотр", self)
        self.startbutton.resize(round(500 * self.kw), round(100 * self.kh))
        self.startbutton.move(width // 2 - self.startbutton.width() // 2,
                              round(height * 0.26) - self.startbutton.height() // 2)
        self.startbutton.clicked.connect(self.start)
        self.endbutton = QPushButton("Выйти из программы", self)
        self.endbutton.resize(round(500 * self.kw), round(100 * self.kh))
        self.endbutton.move(width // 2 - self.endbutton.width() // 2,
                            round(height * 0.74) - self.endbutton.height() // 2)
        self.guidebutton = QPushButton("Дополнительная информация", self)
        self.guidebutton.resize(round(500 * self.kw), round(100 * self.kh))
        self.guidebutton.move(width // 2 - self.guidebutton.width() // 2,
                              round(height * 0.58) - self.guidebutton.height() // 2)
        self.guidebutton.clicked.connect(self.guide)
        self.testbutton = QPushButton("Обучение по работе с программой", self)
        self.testbutton.resize(round(500 * self.kw), round(100 * self.kh))
        self.testbutton.move(width // 2 - self.testbutton.width() // 2,
                             round(height * 0.42) - self.testbutton.height() // 2)
        self.testbutton.clicked.connect(self.test)
        self.endbutton.clicked.connect(self.end)
        self.guidetext = QTextBrowser(self)
        self.guidetext.resize(round(500 * self.kw), (round(height * 0.48)))
        self.guidetext.move(width // 2 - self.guidetext.width() // 2,
                            round(height * 0.26) - round(100 * self.kh) // 2)
        self.guidetext.setText("Разрабы Дауны")
        self.guidetext.hide()
        self.backbutton = QPushButton("Назад", self)
        self.backbutton.resize(round(500 * self.kw), round(100 * self.kh))
#        self.backbutton.move()
        self.backbutton.hide()
        self.backbutton.clicked.connect(self.back)

    def end(self):
        sys.exit()

    def hidebuttons(self):
        self.startbutton.hide()
        self.endbutton.hide()
        self.testbutton.hide()
        self.guidebutton.hide()
        self.backbutton.show()

    def guide(self):
        self.hidebuttons()
        self.guidetext.show()

    def test(self):
        self.hidebuttons()
        self.frame.show()

    def start(self):
        self.hidebuttons()

    def back(self):
        self.startbutton.show()
        self.endbutton.show()
        self.testbutton.show()
        self.guidebutton.show()
        self.backbutton.hide()
        self.guidetext.hide()
        self.frame.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = QApplication.screens()[0].size()
    window = MainWindow(screen.width(), screen.height())
    window.show()
    window.showFullScreen()
    window.iren.Initialize()
    sys.exit(app.exec())
