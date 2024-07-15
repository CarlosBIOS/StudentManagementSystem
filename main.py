# Primeiro abri o terminal e digitei: pip install pyqt6
from PyQt6.QtWidgets import (QApplication, QMainWindow, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QLineEdit,
                             QComboBox, QPushButton, QToolBar)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import sqlite3
import sys
import os


# Atenção, eu usei o QMainWindow instead of QWidget, como no example.py, pois no QMainWindow é mais abrangente e tem
# mais ferramentas onde no outro não têm. Como, por exemplo, o Menu Bar.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')

        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu('&Edit')

        add_student_action = QAction('Add Student', self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction('About', self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)

        search_action = QAction('Search', self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        if os.name == 'darwin':  # é do mac, e pode ser preciso se não, não aparece as actions!!
            add_student_action.setMenuRole(QAction.MenuRole.NoRole)
            about_action.setMenuRole(QAction.MenuRole.NoRole)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Turma', 'Mobile', 'Pai/Mãe'))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)

    def load_data(self):
        connection = sqlite3.connect('database.db')
        result: list = list(connection.execute('SELECT * FROM students'))
        self.table.setRowCount(0)  # Vai garantir que a data não será adicionada em cima de outras datas, ou seja,
        # refresh the table
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        connection.close()

    @staticmethod
    def insert():
        dialog = InsertDialog()
        dialog.exec()

    def about(self):
        pass

    @staticmethod
    def search():
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        self.courses_name = QComboBox()
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']
        self.courses_name.addItems(courses)
        layout.addWidget(self.courses_name)

        self.turma_name = QComboBox()
        courses = ['A', 'B', 'C', 'D']
        self.turma_name.addItems(courses)
        layout.addWidget(self.turma_name)

        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText('Mobile')
        layout.addWidget(self.phone_number)

        self.pai_mae = QLineEdit()
        self.pai_mae.setPlaceholderText('Pai/Mãe')
        layout.addWidget(self.pai_mae)

        button = QPushButton('Register')
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        """Vai adicionar diretamente ao ficheiro da database"""
        name: str = self.student_name.text()
        course: str = self.courses_name.itemText(self.courses_name.currentIndex())
        turma: str = self.turma_name.itemText(self.turma_name.currentIndex())
        mobile: str = self.phone_number.text()
        pais: str = self.pai_mae.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO students (name, course, turma, mobile, paimae) VALUES (?, ?, ?, ?, ?)',
                       (name, course, turma, mobile, pais))

        connection.commit()  # Sem este método, não iria colocar a nova row na tabela
        cursor.close()
        connection.close()
        main_Window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Student Name')
        layout.addWidget(self.student_name)

        button = QPushButton('Search')
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):
        name: str = self.student_name.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        # result = cursor.execute('SELECT * FROM students WHERE name = ?', (name,))
        # rows = list(result)
        items = main_Window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_Window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_Window = MainWindow()
    main_Window.show()
    main_Window.load_data()
    sys.exit(app.exec())
