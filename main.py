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


class NamedActor(vtkActor):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def get_name(self):
        return self.name


class MainWindow(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.deleted_actors = []
        self.deleted_test_actors = []
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
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.vtkWidget.resize(height, height)
        self.vtkWidget.move((width - height) // 2, 0)
        self.ren = vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        mapper1 = vtkPolyDataMapper()
        mapper1.SetInputConnection(ball.GetOutputPort())
        mapper2 = vtkPolyDataMapper()
        mapper2.SetInputConnection(cube.GetOutputPort())
        mapper3 = vtkPolyDataMapper()
        mapper3.SetInputConnection(cilinder.GetOutputPort())

        actor1 = NamedActor("ball")
        actor1.SetMapper(mapper1)
        actor2 = NamedActor("cube")
        actor2.SetMapper(mapper2)
        actor3 = NamedActor("cilinder")
        actor3.SetMapper(mapper3)

        self.ren.AddActor(actor1)
        self.ren.AddActor(actor2)
        self.ren.AddActor(actor3)

        self.ren.ResetCamera()
#        self.frame.move(0, 0)
        self.vtkWidget.hide()

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
        self.backbutton.resize((width - self.vtkWidget.width()) // 2, round(100 * self.kh))
#        self.backbutton.move()
        self.backbutton.hide()
        self.backbutton.clicked.connect(self.back)
        self.vtktext = QTextBrowser(self)
        self.vtktext.resize(self.backbutton.width(), height)
        self.vtktext.move(height + self.backbutton.width(), 0)
        self.vtktext.hide()
        self.c_test_button = QPushButton("Скрыть корпус", self)
        self.c_test_button.resize(self.backbutton.width(), self.backbutton.height())
        self.c_test_button.move(0, self.backbutton.height() + 1)
        self.c_test_button.hide()
        self.c_test_button.clicked.connect(self.c_test)

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
        self.vtkWidget.show()
        self.vtktext.show()
        self.vtktext.setText("Это тестовая модель")
        self.c_test_button.show()
        self.c_test_button.setText("Скрыть корпус")
        for actor in self.deleted_test_actors:
            self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor(actor)
            self.deleted_test_actors.remove(actor)

    def start(self):
        self.hidebuttons()

    def back(self):
        self.startbutton.show()
        self.endbutton.show()
        self.testbutton.show()
        self.guidebutton.show()
        self.backbutton.hide()
        self.guidetext.hide()
        self.vtkWidget.hide()
        self.vtktext.hide()
        self.c_test_button.hide()

    def c_test(self):
        if self.c_test_button.text() == "Скрыть корпус":
            for actor in self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors():
                if actor.get_name() == "cube":
                    del_actor = actor
                    self.deleted_test_actors.append(actor)
                    break
            self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor(del_actor)
            self.c_test_button.setText("Показать корпус")
        else:
            self.c_test_button.setText("Скрыть корпус")
            for actor in self.deleted_test_actors:
                self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor(actor)
                self.deleted_test_actors.remove(actor)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = QApplication.screens()[0].size()
    window = MainWindow(screen.width(), screen.height())
    window.show()
    window.showFullScreen()
    window.iren.Initialize()
    sys.exit(app.exec())
