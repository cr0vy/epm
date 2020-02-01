#!/usr/bin/env python3

import json
import subprocess

from PySide2.QtCore import Qt, QTimer, Slot
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QLabel, QWidget


class ExerciseWidget(QWidget):
    total_time_label = None
    exercise_time_label = None

    exercise_name_label = None
    exercise_description_label = None

    def __init__(self):
        QWidget.__init__(self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.set_time)

        self.total_time = 0
        self.time = 0
        self.file = None

        self.is_exercise = False
        self.exercise_list = []
        self.exercise_description_list = []
        self.exercise_duration = []
        self.exercise_num = 0

        self.setup_widget()

    def setup_exercise(self):
        with open(self.file) as json_file:
            json_data = json.load(json_file)

            for exercise in json_data['exercise']:
                self.exercise_list.append(exercise['name'])
                self.exercise_description_list.append(exercise['description'])
                self.exercise_duration.append(int(exercise['time']))

        self.exercise_name_label.setText(self.exercise_list[self.exercise_num])
        self.exercise_description_label.setText(self.exercise_description_list[self.exercise_num])

    def setup_widget(self):
        self.total_time_label = QLabel("00:00:00", self)
        self.exercise_time_label = QLabel("00:00:00", self)

        font = QFont(self.total_time_label.font())
        font.setPixelSize(48)
        self.total_time_label.setFont(font)
        self.exercise_time_label.setFont(font)

        self.exercise_name_label = QLabel(self)
        self.exercise_name_label.setAlignment(Qt.AlignCenter)
        self.exercise_description_label = QLabel(self)
        self.exercise_description_label.setAlignment(Qt.AlignCenter)

        font = QFont(self.exercise_name_label.font())
        font.setPixelSize(18)
        self.exercise_name_label.setFont(font)
        self.exercise_description_label.setFont(font)
        self.exercise_description_label.setWordWrap(True)

    def get_str_time(self, time: int):
        hour = int(time / 3600)
        minute = int((time - hour * 3600) / 60)
        second = int(time - hour * 3600 - minute * 60)

        hour = self.get_double_str_num_format(hour)
        minute = self.get_double_str_num_format(minute)
        second = self.get_double_str_num_format(second)

        return hour + ":" + minute + ":" + second

    def resizeEvent(self, event):
        self.total_time_label.move(self.width() / 2, 0)
        self.total_time_label.resize(self.width() / 2, self.height() / 2)

        self.exercise_time_label.move(self.width() / 2, self.height() / 2)
        self.exercise_time_label.resize(self.width() / 2, self.height() / 2)

        self.exercise_name_label.move(0, 0)
        self.exercise_name_label.resize(self.width() / 2, self.height() / 3)

        self.exercise_description_label.move(0, self.height() / 3)
        self.exercise_description_label.resize(self.width() / 2, self.height() / 3)

    def set_file(self, file: str):
        self.file = file

    def start(self):
        self.time = 0
        self.total_time = 0

        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()
        print("Stop")

    @staticmethod
    def get_double_str_num_format(time: int):
        if time < 10:
            return "0" + str(time)
        else:
            return str(time)

    @Slot()
    def set_time(self):
        self.total_time += 1
        self.time += 1

        if self.time > self.exercise_duration[self.exercise_num] and self.is_exercise:
            self.time = 0
            self.is_exercise = False
            self.exercise_num += 1

            subprocess.call(['speech-dispatcher'])
            subprocess.call(['spd-say', '"Change"'])

            if self.exercise_num == len(self.exercise_list):
                self.stop_timer()
            else:
                self.exercise_name_label.setText(self.exercise_list[self.exercise_num])
                self.exercise_description_label.setText(self.exercise_description_list[self.exercise_num])

        elif self.time > 5 and not self.is_exercise:
            self.time = 0
            self.is_exercise = True

            subprocess.call(['speech-dispatcher'])
            subprocess.call(['spd-say', '"Start"'])

        self.total_time_label.setText(self.get_str_time(self.total_time))
        self.exercise_time_label.setText(self.get_str_time(self.time))