from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QTextBrowser, QTextEdit
from PyQt6.QtGui import QFont
import sys
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
import vtkmodules.vtkInteractionStyle as vis
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderer
)


class NamedActor(vtkActor):
    def __init__(self, name=""):
        super().__init__()
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name


class MouseInteractorStyle(vis.vtkInteractorStyleRubberBandPick):
    def __init__(self, data, textwidget):
        self.AddObserver('LeftButtonPressEvent', self.left_button_press_event)
        self.AddObserver('MiddleButtonPressEvent', self.middle_button_press_event)
        self.AddObserver('MiddleButtonReleaseEvent', self.middle_button_release_event)
        self.data = data
        self.last_actor = None
        self.selected_mapper = vtkDataSetMapper()
        self.selected_actor = vtkActor()
        self.textwidget = textwidget

    def left_button_press_event(self, obj, event):
        colors = vtkNamedColors()

        # Get the location of the click (in window coordinates)
        pos = self.GetInteractor().GetEventPosition()

        picker = vtkCellPicker()
        picker.SetTolerance(0.0005)

        # Pick from this location.
        picker.Pick(pos[0], pos[1], 0, self.GetDefaultRenderer())

        world_position = picker.GetPickPosition()

        if picker.GetCellId() != -1:
            a = picker.GetActor()
            if self.last_actor:
                self.last_actor.GetProperty().SetColor(colors.GetColor3d("light_grey"))
            a.GetProperty().SetColor(colors.GetColor3d("orange"))
            self.last_actor = a
            self.textwidget.setText(open(f"descriptions/{a.get_name()}.txt", encoding="UTF-8").read())
        else:
            if self.last_actor:
                if self.last_actor.get_name() == "cube":
                    self.textwidget.setText(open("descriptions/test.txt", encoding="UTF-8").read())
                else:
                    self.textwidget.setText(open("descriptions/hide.txt", encoding="UTF-8").read())
                self.last_actor.GetProperty().SetColor(colors.GetColor3d("light_grey"))
                self.last_actor = None
        self.OnLeftButtonDown()

    def middle_button_press_event(self, obj, event):
        return

    def middle_button_release_event(self, obj, event):
        return


class MainWindow(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.deleted_actors = []
        self.deleted_test_actors = []
        self.InintUI(width, height)
        self.cans = [x.strip() for x in open("tasks/ans.txt", encoding="UTF-8").read().split("\n")]
        self.curstage = 0
        self.testactors = []
        self.mainactors = []

    def InintUI(self, width, height):
        self.kw = 1500 / width
        self.kh = 750 / height
        self.setGeometry(0, 0, width, height)
        self.setFixedSize(width, height)
        font = QFont()
        font.setFamily("Comic Sans MS")

        outputports = [vtk.vtkSTLReader() for _ in range(10)]

        outputports[0].SetFileName("models/ball.stl")
        outputports[1].SetFileName("models/cilinder.stl")
        outputports[2].SetFileName("models/cube.stl")
        outputports[3].SetFileName("models/Anchore_Core.stl")
        outputports[4].SetFileName("models/Brushes.stl")
        outputports[5].SetFileName("models/Collector.stl")
        outputports[6].SetFileName("models/Excitation_coil.stl")
        outputports[7].SetFileName("models/Shaft.stl")
        outputports[8].SetFileName("models/Shell.stl")
        outputports[9].SetFileName("models/Fan.stl")

        triangle_filter = vtkTriangleFilter()

        for i in range(10):
            triangle_filter.SetInputConnection(outputports[i].GetOutputPort())
        triangle_filter.Update()

        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.vtkWidget.resize(height, height)
        self.vtkWidget.move((width - height) // 2, 0)
        self.ren = vtkRenderer()
        colors = vtkNamedColors()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        #        self.iren.SetInteractorStyle(vis.vtkInteractorStyleTrackballCamera())

        self.backbutton = QPushButton("Назад", self)
        self.backbutton.resize((width - self.vtkWidget.width()) // 2, round(100 * self.kh))
        #        self.backbutton.move()
        self.backbutton.hide()
        self.backbutton.clicked.connect(self.back)

        self.vtktext = QTextBrowser(self)
        self.vtktext.resize(self.backbutton.width(), height)
        self.vtktext.move(height + self.backbutton.width(), 0)
        self.vtktext.hide()

        style = MouseInteractorStyle(triangle_filter.GetOutput(), self.vtktext)
        style.SetDefaultRenderer(self.ren)
        self.iren.SetInteractorStyle(style)
        #        self.iren.SetInteractorStyle(vis.vtkInteractorStyleRubberBandPick())
        #        self.iren.AddObserver("Select3DEvent", self.process_pick)

        mappers = [vtkPolyDataMapper() for _ in range(10)]
        for x in range(10):
            mappers[x].SetInputConnection(outputports[x].GetOutputPort())

        actors = [NamedActor() for _ in range(10)]
        for x in actors:
            x.GetProperty().SetColor(colors.GetColor3d("light_grey"))
        actors[0].set_name("ball")
        actors[1].set_name("cilinder")
        actors[2].set_name("cube")
        actors[3].set_name("Anchor_Core")
        actors[4].set_name("Brushes")
        actors[5].set_name("Collector")
        actors[6].set_name("Excitation_coil")
        actors[7].set_name("Shaft")
        actors[8].set_name("Shell")
        actors[9].set_name("Fan")

        for x in range(10):
            actors[x].SetMapper(mappers[x])

        self.deleted_test_actors.append(actors[0])
        self.deleted_test_actors.append(actors[1])
        self.deleted_test_actors.append(actors[2])
        self.deleted_actors.append(actors[3])
        self.deleted_actors.append(actors[4])
        self.deleted_actors.append(actors[5])
        self.deleted_actors.append(actors[6])
        self.deleted_actors.append(actors[7])
        self.deleted_actors.append(actors[8])
        self.deleted_actors.append(actors[9])

        self.ren.SetBackground(colors.GetColor3d('Black'))

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
        colors = vtkNamedColors()
        for act in self.ren.GetActors():
            act.GetProperty().SetColor(colors.GetColor3d("light_grey"))

    def test(self):
        self.hidebuttons()
        self.vtkWidget.show()
        self.vtktext.show()
        self.vtktext.setText(open("descriptions/test.txt", encoding="UTF-8").read())
        self.c_test_button.show()
        self.c_test_button.setText("Скрыть корпус")
        print(len(self.deleted_test_actors))
        for _ in range(len(self.deleted_test_actors)):
            self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor(self.deleted_test_actors[0])
            self.deleted_test_actors.remove(self.deleted_test_actors[0])

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
        self.curstage = 1
        self.hidebuttons()
        self.vtkWidget.show()
        self.vtktext.show()
        self.vtktext.setText(open("descriptions/main.txt", encoding="UTF-8").read())
        self.c_test_button.show()
        self.c_test_button.setText("Скрыть корпус")
        print(len(self.deleted_actors))
        for _ in range(len(self.deleted_actors)):
            self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor(self.deleted_actors[0])
            self.deleted_actors.remove(self.deleted_actors[0])

    def back(self):
        self.curstage = 0
        if self.vtkWidget.isVisible():
            if list(self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors())[0].get_name() in ["ball",
                                                                                                     "cilinder",
                                                                                                     "cube"]:
                for actor in self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors():
                    del_actor = actor
                    self.deleted_test_actors.append(actor)
                    self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor(del_actor)
            else:
                for actor in self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors():
                    del_actor = actor
                    self.deleted_actors.append(actor)
                    self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor(del_actor)
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
        if list(self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors())[0].get_name() in ["ball",
                                                                                                            "cilinder",
                                                                                                            "cube"]:
            if self.c_test_button.text() == "Скрыть корпус":
                for actor in self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors():
                    print(actor.get_name())
                    if actor.get_name() == "cube":
                        del_actor = actor
                        self.deleted_test_actors.append(actor)
                        print(actor.get_name())
                        break
                self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor(del_actor)
                self.c_test_button.setText("Показать корпус")
            else:
                self.c_test_button.setText("Скрыть корпус")
                for actor in self.deleted_test_actors:
                    self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor(actor)
                    self.deleted_test_actors.remove(actor)
        else:
            if self.c_test_button.text() == "Скрыть корпус":
                for actor in self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().GetActors():
                    if actor.get_name() == "Shell":
                        del_actor = actor
                        self.deleted_actors.append(actor)
                        break
                self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().RemoveActor(del_actor)
                self.c_test_button.setText("Показать корпус")
            else:
                self.c_test_button.setText("Скрыть корпус")
                for actor in self.deleted_actors:
                    self.vtkWidget.GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor(actor)
                    self.deleted_actors.remove(actor)
        self.vtkWidget.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = QApplication.screens()[0].size()
    window = MainWindow(screen.width(), screen.height())
    # window.show()
    window.showFullScreen()
    window.iren.Initialize()
    sys.exit(app.exec())
