from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QTextBrowser, QTextEdit
from PyQt6.QtGui import QFont
import sys
import vtkmodules.vtkInteractionStyle as vis
import vtkmodules.vtkRenderingOpenGL2
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
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
        self.cans = [x.strip() for x in open("tasks/ans.txt").read().split("\n")]

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
#        self.iren.SetInteractorStyle(vis.vtkInteractorStyleTrackballCamera())
        self.iren.SetInteractorStyle(vis.vtkInteractorStyleRubberBandPick())
        self.iren.AddObserver('LeftButtonPressEvent', self.process_pick)

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
                             round(height * 0.35) - self.startbutton.height() // 2)
        self.startbutton.clicked.connect(self.start)
        self.endbutton = QPushButton("Выйти из программы", self)
        self.endbutton.resize(round(500 * self.kw), round(100 * self.kh))
        self.endbutton.move(width // 2 - self.endbutton.width() // 2,
                            round(height * 0.8) - self.endbutton.height() // 2)
        self.guidebutton = QPushButton("Дополнительная информация", self)
        self.guidebutton.resize(round(500 * self.kw), round(100 * self.kh))
        self.guidebutton.move(width // 2 - self.guidebutton.width() // 2,
                              round(height * 0.5) - self.guidebutton.height() // 2)
        self.guidebutton.clicked.connect(self.guide)
        self.testbutton = QPushButton("Обучение по работе с программой", self)
        self.testbutton.resize(round(500 * self.kw), round(100 * self.kh))
        self.testbutton.move(width // 2 - self.startbutton.width() // 2,
                              round(height * 0.2) - self.startbutton.height() // 2)
        self.testbutton.clicked.connect(self.test)
        self.endbutton.clicked.connect(self.end)
        self.guidetext = QTextBrowser(self)
        self.guidetext.resize(round(500 * self.kw), (round(height * 0.48)))
        self.guidetext.move(width // 2 - self.guidetext.width() // 2,
                            round(height * 0.26) - round(100 * self.kh) // 2)
        self.guidetext.setText("Здесь могла бы быть наша документация")
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

        self.lesson_button = QPushButton("Задачи", self)
        self.lesson_button.resize(round(500 * self.kw), round(100 * self.kh))
        self.lesson_button.move(width // 2 - self.lesson_button.width() // 2,
                              round(height * 0.65) - self.lesson_button.height() // 2)

        self.firsttask = QTextBrowser(self)
        self.firsttask.resize(width // 2, round(height * 0.1))
        self.firsttask.move(width // 4, round(height * 0.05))
        self.firsttask.setText(open("tasks/first.txt", encoding="UTF-8").read())

        self.secondtask = QTextBrowser(self)
        self.secondtask.resize(width // 2, round(height * 0.1))
        self.secondtask.move(width // 4, round(height * 0.25))
        self.secondtask.setText(open("tasks/second.txt", encoding="UTF-8").read())

        self.thirdtask = QTextBrowser(self)
        self.thirdtask.resize(width // 2, round(height * 0.1))
        self.thirdtask.move(width // 4, round(height * 0.45))
        self.thirdtask.setText(open("tasks/third.txt", encoding="UTF-8").read())

        self.fourthtask = QTextBrowser(self)
        self.fourthtask.resize(width // 2, round(height * 0.1))
        self.fourthtask.move(width // 4, round(height * 0.65))
        self.fourthtask.setText(open("tasks/fourth.txt", encoding="UTF-8").read())

        self.fifthtask = QTextBrowser(self)
        self.fifthtask.resize(width // 2, round(height * 0.1))
        self.fifthtask.move(width // 4, round(height * 0.85))
        self.fifthtask.setText(open("tasks/fifth.txt", encoding="UTF-8").read())

        self.firsttask.hide()
        self.secondtask.hide()
        self.thirdtask.hide()
        self.fourthtask.hide()
        self.fifthtask.hide()

        self.lesson_button.clicked.connect(self.lesson)

        self.firstans = QTextEdit(self)
        self.firstans.resize(self.firsttask.width() // 2, self.firsttask.height() // 2)
        self.firstans.move(width // 4, round(height * 0.15))
        self.firstans.setPlaceholderText("Введите ответ")

        self.secondans = QTextEdit(self)
        self.secondans.resize(self.firsttask.width() // 2, self.firsttask.height() // 2)
        self.secondans.move(width // 4, round(height * 0.35))
        self.secondans.setPlaceholderText("Введите ответ")

        self.thirdans = QTextEdit(self)
        self.thirdans.resize(self.firsttask.width() // 2, self.firsttask.height() // 2)
        self.thirdans.move(width // 4, round(height * 0.55))
        self.thirdans.setPlaceholderText("Введите ответ")

        self.fourthans = QTextEdit(self)
        self.fourthans.resize(self.firsttask.width() // 2, self.firsttask.height() // 2)
        self.fourthans.move(width // 4, round(height * 0.75))
        self.fourthans.setPlaceholderText("Введите ответ")

        self.fifthans = QTextEdit(self)
        self.fifthans.resize(self.firsttask.width() // 2, self.firsttask.height() // 2)
        self.fifthans.move(width // 4, round(height * 0.95))
        self.fifthans.setPlaceholderText("Введите ответ")

        self.subbutton = QPushButton("проверить ответы", self)
        self.subbutton.resize(self.backbutton.width(), self.backbutton.height())
        self.subbutton.move(self.c_test_button.x(), self.c_test_button.y())

        self.clearButton = QPushButton("сбросить", self)
        self.clearButton.resize(self.backbutton.width(), self.backbutton.height())
        self.clearButton.move(0, self.c_test_button.y() + self.backbutton.height() + 1)

        self.clearButton.hide()
        self.firstans.hide()
        self.subbutton.hide()
        self.secondans.hide()
        self.thirdans.hide()
        self.fourthans.hide()
        self.fifthans.hide()

        self.clearButton.clicked.connect(self.clear)
        self.subbutton.clicked.connect(self.check_ans)


    def end(self):
        sys.exit()

    def process_pick(self, object, event):
        pass
#        print(event)
#        print(object)
#        point_id = object.GetPointId()
#        if point_id >= 0:
#            vector_magnitude = self.vtkWidget.GetOutput().GetPointData().GetScalars().GetTuple(point_id)
#            print(vector_magnitude)
#            print(vector_magnitude[0])
#        else:
#            print(True)
#        print("You clicked at", self.iren.GetEventPosition())

    def hidebuttons(self):
        self.startbutton.hide()
        self.endbutton.hide()
        self.testbutton.hide()
        self.guidebutton.hide()
        self.backbutton.show()
        self.lesson_button.hide()

    def guide(self):
        self.hidebuttons()
        self.guidetext.show()

    def clear(self):
        self.firstans.setText("")
        self.secondans.setText("")
        self.thirdans.setText("")
        self.fourthans.setText("")
        self.fifthans.setText("")
        self.firstans.setStyleSheet("")
        self.secondans.setStyleSheet("")
        self.thirdans.setStyleSheet("")
        self.fourthans.setStyleSheet("")
        self.fifthans.setStyleSheet("")
        self.firsttask.setStyleSheet("")
        self.secondtask.setStyleSheet("")
        self.thirdtask.setStyleSheet("")
        self.fourthtask.setStyleSheet("")
        self.fifthtask.setStyleSheet("")


    def lesson(self):
        self.hidebuttons()
        self.firsttask.show()
        self.secondtask.show()
        self.thirdtask.show()
        self.fourthtask.show()
        self.fifthtask.show()
        self.clearButton.show()
        self.firstans.show()
        self.subbutton.show()
        self.secondans.show()
        self.thirdans.show()
        self.fourthans.show()
        self.fifthans.show()


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


    def check_ans(self):
        if self.firstans.toPlainText() == self.cans[0]:
            self.firstans.setStyleSheet("border: 1px solid green;")
            self.firsttask.setStyleSheet("border: 1px solid green;")
        else:
            self.firstans.setStyleSheet("border: 1px solid red;")
            self.firsttask.setStyleSheet("border: 1px solid red;")
        if self.secondans.toPlainText() == self.cans[1]:
            self.secondans.setStyleSheet("border: 1px solid green;")
            self.secondtask.setStyleSheet("border: 1px solid green;")
        else:
            self.secondans.setStyleSheet("border: 1px solid red;")
            self.secondtask.setStyleSheet("border: 1px solid red;")
        if self.thirdans.toPlainText() == self.cans[2]:
            self.thirdans.setStyleSheet("border: 1px solid green;")
            self.thirdtask.setStyleSheet("border: 1px solid green;")
        else:
            self.thirdans.setStyleSheet("border: 1px solid red;")
            self.thirdtask.setStyleSheet("border: 1px solid red;")
        if self.fourthans.toPlainText() == self.cans[3]:
            self.fourthans.setStyleSheet("border: 1px solid green;")
            self.fourthtask.setStyleSheet("border: 1px solid green;")
        else:
            self.fourthans.setStyleSheet("border: 1px solid red;")
            self.fourthtask.setStyleSheet("border: 1px solid red;")
        if self.fifthans.toPlainText() == self.cans[4]:
            self.fifthans.setStyleSheet("border: 1px solid green;")
            self.fifthtask.setStyleSheet("border: 1px solid green;")
        else:
            self.fifthans.setStyleSheet("border: 1px solid red;")
            self.fifthtask.setStyleSheet("border: 1px solid red;")

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
        self.lesson_button.show()
        self.firsttask.hide()
        self.secondtask.hide()
        self.thirdtask.hide()
        self.fourthtask.hide()
        self.fifthtask.hide()
        self.clearButton.hide()
        self.firstans.hide()
        self.subbutton.hide()
        self.secondans.hide()
        self.thirdans.hide()
        self.fourthans.hide()
        self.fifthans.hide()
        self.clear()

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
        self.vtkWidget.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = QApplication.screens()[0].size()
    window = MainWindow(screen.width(), screen.height())
#    window.show()
    window.showFullScreen()
    window.iren.Initialize()
    sys.exit(app.exec())
