from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QTextBrowser
from PyQt6.QtGui import QFont
import sys


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
        self.startbutton = QPushButton("Начать просмотр", self)
        self.startbutton.resize(round(500 * self.kw), round(100 * self.kh))
        self.startbutton.move(width // 2 - self.startbutton.width() // 2,
                              round(height * 0.26) - self.startbutton.height() // 2)
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
        self.endbutton.clicked.connect(self.end)
        self.guidetext = QTextBrowser(self)
        self.guidetext.resize(round(500 * self.kw), (round(height * 0.48)))
        self.guidetext.move(width // 2 - self.guidetext.width() // 2,
                            round(height * 0.26) - round(100 * self.kh) // 2)
        self.guidetext.setText("Разрабы Дауны")
        self.guidetext.hide()
        self.backbutton = QPushButton("Назад", self)
        self.backbutton.resize(round(500 * self.kw), round(100 * self.kh))
        self.backbutton.move()

    def end(self):
        sys.exit()

    def hidebuttons(self):
        self.startbutton.hide()
        self.endbutton.hide()
        self.testbutton.hide()
        self.guidebutton.hide()

    def guide(self):
        self.hidebuttons()
        self.guidetext.show()

    def test(self):
        self.hidebuttons()

    def start(self):
        self.hidebuttons()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = QApplication.screens()[0].size()
    window = MainWindow(screen.width(), screen.height())
    window.showFullScreen()
    sys.exit(app.exec())
