#!/usr/bin/env python3

import json
from pathlib import Path

from PySide2.QtCore import Qt, Signal, Slot
from PySide2.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QVBoxLayout, QWidget


class ViewWidget(QWidget):
    exercise_name_label = None
    exercise_name_line = None

    scroll_area = None
    base_widget = None
    exercises_widget = None

    return_button = None

    add_button = None
    save_button = None

    def __init__(self):
        QWidget.__init__(self)

        self.file = ""
        self.setup_widget()

    def setup_widget(self):
        self.exercise_name_label = QLabel("Exercise name:", self)
        self.exercise_name_label.move(5, 5)
        self.exercise_name_label.resize(125, 25)

        self.add_button = QPushButton("Add", self)
        self.add_button.resize(75, 25)
        self.add_button.clicked.connect(self.add_line)

        self.save_button = QPushButton("Save", self)
        self.save_button.resize(150, 40)
        self.save_button.clicked.connect(self.save)

        self.exercise_name_line = QLineEdit(self)
        self.exercise_name_line.move(135, 5)
        self.exercise_name_line.resize(125, 25)

        self.scroll_area = QScrollArea(self)
        self.base_widget = QWidget(self)
        self.scroll_area.setWidget(self.base_widget)

        self.exercises_widget = QVBoxLayout()
        self.exercises_widget.setAlignment(Qt.AlignTop)
        self.exercises_widget.setMargin(0)

        self.base_widget.setLayout(self.exercises_widget)

        self.return_button = QPushButton("Return wo save", self)
        self.return_button.resize(150, 40)

    def resizeEvent(self, event):
        self.scroll_area.move(5, 35)
        self.scroll_area.resize(self.width() - 165, self.height() - 40)
        self.add_button.move(self.width() - 160 - 75, 5)
        self.save_button.move(self.width() - 155, 5)
        self.return_button.move(self.width() - 155, 50)

        self.base_widget.resize(self.scroll_area.width() - 25, self.exercises_widget.count() * 25)

    def clear_widget(self):
        while self.exercises_widget.count() > 0:
            self.exercises_widget.itemAt(0).widget().remove_panel()

        self.exercise_name_line.setText("")
        self.file = ""

    def open_exercise_file(self, file: str):
        self.file = file

        with open(self.file, "r") as json_file:
            json_data = json.load(json_file)

            name = json_data['name']

            for data in json_data['exercise']:
                movement = data['name']
                description = data['description']
                time = data['time']

                widget = PanelWidget()
                widget.set_data(movement, description, time)
                widget.remove_signal.connect(self.remove_panel_item)
                widget.move_down_signal.connect(self.move_widget_down)
                widget.move_up_signal.connect(self.move_widget_up)

                self.exercises_widget.addWidget(widget)

            json_file.close()

        self.base_widget.resize(self.scroll_area.width() - 25, self.exercises_widget.count() * 25)

        self.exercise_name_line.setText(name)

    @Slot()
    def add_line(self):
        widget = PanelWidget()
        self.exercises_widget.addWidget(widget)
        self.base_widget.resize(self.scroll_area.width() - 25, self.exercises_widget.count() * 25)

    @Slot(QWidget)
    def move_widget_down(self, widget: QWidget):
        ind = self.exercises_widget.indexOf(widget) + 1
        self.exercises_widget.removeWidget(widget)
        self.exercises_widget.insertWidget(ind, widget)

    @Slot(QWidget)
    def move_widget_up(self, widget: QWidget):
        ind = self.exercises_widget.indexOf(widget) - 1
        self.exercises_widget.removeWidget(widget)
        self.exercises_widget.insertWidget(ind, widget)

    @Slot(QWidget)
    def remove_panel_item(self, widget: QWidget):
        self.exercises_widget.removeWidget(widget)
        self.base_widget.resize(self.scroll_area.width() - 25, self.exercises_widget.count() * 25)

    @Slot()
    def save(self):
        name = self.exercise_name_line.text()

        json_data = {}
        json_data['name'] = name
        json_data['change-time'] = 5
        json_data['exercise'] = []

        for i in range(self.exercises_widget.count()):
            widget = self.exercises_widget.itemAt(i).widget()
            print(widget)
            json_data['exercise'].append({
                'name': widget.get_name(),
                'description': widget.get_description(),
                'time': widget.get_time(),
                'type': 'seconds'
            })

        json.dumps(json_data, indent=4)

        if self.file == "":
            name = self.exercise_name_line.text().replace(" ", "_") + ".json"
            path = str(Path.home()) + "/.local/share/epm/"

            self.file = path + name

        with open(self.file, 'w') as outfile:
            json.dump(json_data, outfile, indent=4)


class PanelWidget(QWidget):
    name_line = None
    description_line = None
    time_line = None
    remove_button = None
    move_up = None
    move_down = None

    layout = None

    remove_signal = Signal(QWidget)
    move_down_signal = Signal(QWidget)
    move_up_signal = Signal(QWidget)

    def __init__(self):
        QWidget.__init__(self)
        self.setup_widget()

    def setup_widget(self):
        self.layout = QHBoxLayout()
        self.layout.setMargin(0)
        self.layout.setSpacing(0)

        self.name_line = QLineEdit()
        self.description_line = QLineEdit()
        self.time_line = QLineEdit()
        self.time_line.setInputMask("999")
        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.remove_widget)
        self.move_up = QPushButton("\u25B2")
        self.move_down = QPushButton("\u25BC")
        self.move_up.clicked.connect(self.move_widget_up)
        self.move_down.clicked.connect(self.move_widget_down)

        self.layout.addWidget(self.name_line)
        self.layout.addWidget(self.description_line)
        self.layout.addWidget(self.time_line)
        self.layout.addWidget(self.remove_button)
        self.layout.addWidget(self.move_up)
        self.layout.addWidget(self.move_down)

        self.setLayout(self.layout)

        self.name_line.setMinimumWidth(200)
        self.name_line.setMaximumWidth(200)

        self.time_line.setMinimumWidth(40)
        self.time_line.setMaximumWidth(40)

        self.remove_button.setMinimumWidth(75)
        self.remove_button.setMaximumWidth(75)

        self.setMinimumHeight(25)
        self.setMaximumHeight(25)

        self.move_up.setMinimumWidth(25)
        self.move_up.setMaximumWidth(25)

        self.move_down.setMinimumWidth(25)
        self.move_down.setMaximumWidth(25)

    def get_description(self):
        return self.description_line.text()

    def get_name(self):
        return self.name_line.text()

    def get_time(self):
        return int(self.time_line.text())

    def set_data(self, name: str, description: str, time: int):
        self.name_line.setText(name)
        self.description_line.setText(description)
        self.time_line.setText(str(time))

    def remove_panel(self):
        self.remove_signal.emit(self)

    @Slot()
    def move_widget_down(self):
        self.move_down_signal.emit(self)

    @Slot()
    def move_widget_up(self):
        self.move_up_signal.emit(self)

    @Slot()
    def remove_widget(self):
        self.remove_signal.emit(self)
