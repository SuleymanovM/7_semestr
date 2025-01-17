from lab1 import Solution
from lab2 import RSA, BBS, LinearCongruent

import datetime
import os

from typing import List, Tuple
from PyQt5.QtWidgets import (QWidget, QLabel, QDateEdit,
                             QHBoxLayout, QVBoxLayout, QPushButton, QComboBox,
                             QTextEdit, QFileDialog, QSpinBox)
from PyQt5.QtCore import QDate, Qt, QThreadPool

import re

GENERATORS = {
    "Генератор RSA": RSA,
    "Генератор BBS": BBS,
    "Линейный конгруэнтный генератор": LinearCongruent,
}
TESTS = {
    "Тест частотности": "frequency_test",
    "Тест на повторяемость": "identical_bits_test",
    "Расширенный тест": "extended_test",
    "Все тесты": "check",
}

VALUES_DIVIDERS = "[,;\n\s]"

class MainWindow(QWidget):
    io_field: QTextEdit
    generator_selector: QComboBox
    test_selector: QComboBox
    save_path: QFileDialog
    sequence: List[str]
    status: QLabel
    user_length: int
    user_size: int
    size_box: QSpinBox
    length_box: QSpinBox

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа 2")
        self.resize(350, 200)
        self.setStyleSheet("padding: 5px; margin: 3px")

        self.labels = {
            "intents_label": QLabel('Поле ввода/вывода'),
            "generator_label": QLabel('Генератор'),
            "test_label": QLabel('Тест'),
            "start_button_text": 'Начать',
            "upload_button_text": 'Загрузить',
            "save_button_text": 'Сохранить',
        }

        self.start_button = QPushButton(self.labels['start_button_text'], self)
        self.upload_button = QPushButton(self.labels['upload_button_text'], self)
        self.save_button = QPushButton(self.labels['save_button_text'], self)

        self.test_status_label = QLabel()

        self.layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()

        self.left_layout.addLayout(self.io_field_layout())
        self.left_layout.addLayout(self.length_size_layout())
        self.left_layout.addLayout(self.generator_selector_layout())
        self.left_layout.addLayout(self.test_selector_layout())
        self.left_layout.addWidget(self.start_button)
        self.left_layout.addWidget(self.upload_button)
        self.left_layout.addWidget(self.save_button)

        self.status = QLabel()
        self.left_layout.addWidget(self.status)

        self.layout.addLayout(self.left_layout)
        self.setLayout(self.layout)

        self.start_button.clicked.connect(self.start)
        self.upload_button.clicked.connect(self.upload)
        self.save_button.clicked.connect(self.save)

    def start(self):
        if not self.io_field.toPlainText():
            self.test_status_label.setText("")
            sequence = str(GENERATORS[self.generator_selector.currentText()](
                length=self.length_box.value(),size=self.size_box.value()).generate())[1:-1]
            self.io_field.setText(sequence)
        else:
            sequence = list(map(int, filter(None, re.split(VALUES_DIVIDERS, self.io_field.toPlainText().strip()))))
            res = getattr(Solution(sequence=sequence), TESTS[self.test_selector.currentText()])()
            if res:
                self.test_status_label.setText("Тест пройден")
                self.test_status_label.setStyleSheet("color: green")
            else:
                self.test_status_label.setText("Тест провален")
                self.test_status_label.setStyleSheet("color: red")

    def upload(self):
        open_path, _ = QFileDialog.getOpenFileName(self, filter="Text documents (*.txt)")
        with open(open_path, "r") as f:
            self.io_field.setText(f.read())

    def save(self):
        save_path, _ = QFileDialog.getSaveFileName(self, filter="Text documents (*.txt)")
        with open(save_path, "w") as f:
            f.write(self.io_field.toPlainText())

    def io_field_layout(self) -> QVBoxLayout:
        io_field_layout = QVBoxLayout()
        io_field_layout.addWidget(self.labels['intents_label'])
        self.io_field = QTextEdit()
        io_field_layout.addWidget(self.io_field)
        return io_field_layout

    def length_size_layout(self) -> QVBoxLayout:
        self.size_box, self.length_box = QSpinBox(), QSpinBox()
        self.size_box.setMaximum(2048)
        self.size_box.setValue(160)
        self.length_box.setMaximum(1000000)
        self.length_box.setValue(1000)
        length_size_layout = QVBoxLayout()
        top = QHBoxLayout()
        bottom = QHBoxLayout()
        top.addWidget(QLabel("Размер простых чисел в битах"))
        top.addWidget(QLabel("Длина последовательности"))
        bottom.addWidget(self.size_box)
        bottom.addWidget(self.length_box)
        length_size_layout.addLayout(top)
        length_size_layout.addLayout(bottom)
        return length_size_layout

    def generator_selector_layout(self) -> QHBoxLayout:
        generator_selector_layout = QHBoxLayout()
        generator_selector_layout.addWidget(self.labels['generator_label'])
        self.generator_selector = QComboBox()
        self.generator_selector.addItems(list(map(str, GENERATORS.keys())))
        generator_selector_layout.addWidget(self.generator_selector)
        generator_selector_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        return generator_selector_layout

    def test_selector_layout(self) -> QHBoxLayout:
        test_selector_layout = QHBoxLayout()
        test_selector_layout.addWidget(self.labels['test_label'])
        self.test_selector = QComboBox()
        self.test_selector.addItems(list(map(str, TESTS.keys())))
        test_selector_layout.addWidget(self.test_selector)
        test_selector_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        test_selector_layout.addWidget(self.test_status_label)
        return test_selector_layout

