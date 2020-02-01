#!/usr/bin/env python3

import sys

from PySide2.QtCore import Slot
from PySide2.QtWidgets import QApplication, QStackedWidget, QWidget

from exercise import ExerciseWidget


class MainWindow(QWidget):
    widget_stack = None
    exercise_widget = None

    def __init__(self):
        QWidget.__init__(self)

        self.setup_window()

        self.widget_stack.setCurrentWidget(self.exercise_widget)

    def setup_window(self):
        self.widget_stack = QStackedWidget(self)
        self.exercise_widget = ExerciseWidget()

        self.widget_stack.addWidget(self.exercise_widget)

    def resizeEvent(self, event):
        self.widget_stack.resize(self.size())

    @Slot(str)
    def show_exercise_window(self, file: str):
        self.exercise_widget.set_file(file)
        self.exercise_widget.setup_exercise()
        self.widget_stack.setCurrentWidget(self.exercise_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec_())
