#!/usr/bin/env python3

import sys

from PySide2.QtCore import Slot
from PySide2.QtWidgets import QApplication, QStackedWidget, QWidget

from exercise import ExerciseWidget
from mainwidget import MainWidget
from viewwidget import ViewWidget


class MainWindow(QWidget):
    widget_stack = None
    main_widget = None
    exercise_widget = None
    exercise_view_widget = None

    def __init__(self):
        QWidget.__init__(self)

        self.setup_window()

        self.widget_stack.setCurrentWidget(self.main_widget)

    def setup_window(self):
        self.widget_stack = QStackedWidget(self)
        self.main_widget = MainWidget()
        self.exercise_widget = ExerciseWidget()
        self.exercise_view_widget = ViewWidget()

        self.widget_stack.addWidget(self.main_widget)
        self.widget_stack.addWidget(self.exercise_widget)
        self.widget_stack.addWidget(self.exercise_view_widget)

        self.main_widget.add_exercise_file.connect(self.show_new_exercise_view_widget_with)
        self.main_widget.start_exercise_file.connect(self.show_exercise_window)
        self.main_widget.open_exercise_file.connect(self.show_exercise_view_widget)
        self.exercise_view_widget.return_button.clicked.connect(self.show_main_widget)
        self.exercise_widget.finished_signal.connect(self.show_main_widget)

    def resizeEvent(self, event):
        self.widget_stack.resize(self.size())

    @Slot()
    def show_main_widget(self):
        if self.widget_stack.currentWidget() == self.exercise_view_widget:
            self.exercise_view_widget.clear_widget()

            self.main_widget.load_exercise_files()

        self.widget_stack.setCurrentWidget(self.main_widget)

    @Slot(str)
    def show_exercise_view_widget(self, file: str):
        self.widget_stack.setCurrentWidget(self.exercise_view_widget)
        self.exercise_view_widget.open_exercise_file(file)

    @Slot(str)
    def show_exercise_window(self, file: str):
        self.exercise_widget.set_file(file)
        self.exercise_widget.setup_exercise()
        self.exercise_widget.start()
        self.widget_stack.setCurrentWidget(self.exercise_widget)

    @Slot()
    def show_new_exercise_view_widget_with(self):
        self.widget_stack.setCurrentWidget(self.exercise_view_widget)
        self.exercise_view_widget.clear_widget()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec_())
