#!/usr/bin/env python3

import json
from pathlib import Path
import os

from PySide2.QtCore import Qt, Signal, Slot
from PySide2.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class MainWidget(QWidget):
    start_exercise_file = Signal(str)
    open_exercise_file = Signal(str)

    file_select_list_base = None
    file_select_list = None

    def __init__(self):
        QWidget.__init__(self)

        self.setup_widget()
        self.load_exercise_files()

    def setup_widget(self):
        self.file_select_list_base = QWidget(self)
        self.file_select_list = QVBoxLayout()
        self.file_select_list.setAlignment(Qt.AlignTop)
        self.file_select_list.setMargin(2)

        self.file_select_list_base.setLayout(self.file_select_list)

    def load_exercise_files(self):
        path = str(Path.home()) + "/.local/share/epm"

        if not Path(path).is_dir():
            os.mkdir(path)

        directories = os.listdir(path)

        for dir in directories:
            file = path + "/" + dir
            widget = SelectPanel(file)
            widget.setMinimumHeight(25)
            widget.setMaximumHeight(25)
            self.file_select_list.addWidget(widget)

            widget.file_signal.connect(self.get_exercise_file)
            widget.file_open_signal.connect(self.get_open_exercise_file)

    def resizeEvent(self, event):
        self.file_select_list_base.move(self.width() / 2 + 5, 5)
        self.file_select_list_base.resize(self.width() / 2 - 10, self.height() - 10)

    @Slot(str)
    def get_exercise_file(self, file: str):
        self.start_exercise_file.emit(file)

    @Slot(str)
    def get_open_exercise_file(self, file: str):
        self.open_exercise_file.emit(file)


class SelectPanel(QWidget):
    name_label = None
    start_button = None
    edit_button = None

    file_signal = Signal(str)
    file_open_signal = Signal(str)

    def __init__(self, file: str):
        QWidget.__init__(self)

        self.file = file

        self.setup_widget()

    def setup_widget(self):
        with open(self.file, "r") as json_file:
            data = json.load(json_file)

        json_file.close()

        self.name_label = QLabel(data['name'], self)
        self.start_button = QPushButton("Start", self)
        self.edit_button = QPushButton("Edit", self)

        self.edit_button.clicked.connect(self.open_file)
        self.start_button.clicked.connect(self.send_file)

    def resizeEvent(self, event):
        self.name_label.resize(self.width() - 100, self.height())
        self.start_button.resize(50, self.height())
        self.edit_button.resize(50, self.height())

        self.start_button.move(self.width() - 100, 0)
        self.edit_button.move(self.width() - 50, 0)

    @Slot()
    def open_file(self):
        self.file_open_signal.emit(self.file)

    @Slot()
    def send_file(self):
        self.file_signal.emit(self.file)
