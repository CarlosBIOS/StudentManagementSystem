# Primeiro abri o terminal e digitei: pip install pyqt6
from PyQt6.QtWidgets import (QApplication, QMainWindow, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QLineEdit,
                             QComboBox, QPushButton, QToolBar, QStatusBar, QGridLayout, QLabel, QMessageBox)
from PyQt6.QtGui import QAction, QIcon
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
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu('&File')
        edit_menu_item = self.menuBar().addMenu('&Edit')
        help_menu_item = self.menuBar().addMenu('&Help')

        add_student_action = QAction(QIcon('icons/add.png'), 'Add Student', self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction('About', self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)

        search_action = QAction(QIcon('icons/search.png'), 'Search', self)
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
        toolbar.addAction(search_action)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        # Detect a cell click:
        self.table.cellClicked.connect(self.cell_clicked)

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

    @staticmethod
    def about(self):
        about = AboutDialog()
        about.exec()

    @staticmethod
    def search():
        dialog = SearchDialog()
        dialog.exec()

    def cell_clicked(self):
        edit_button = QPushButton('Edit Record')
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton('Delete Record')
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusBar().removeWidget(child)

        self.statusBar().addWidget(edit_button)
        self.statusBar().addWidget(delete_button)

    @staticmethod
    def edit():
        edit_dialog = EditDialog()
        edit_dialog.exec()

    @staticmethod
    def delete():
        delete_dialog = DeleteDialog()
        delete_dialog.exec()


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


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        index: int = main_Window.table.currentRow()

        self.student_id = main_Window.table.item(index, 0).text()

        student_name: str = main_Window.table.item(index, 1).text()
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText('Student Name')
        layout.addWidget(self.student_name)

        course_name = main_Window.table.item(index, 2).text()
        self.courses_name = QComboBox()
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']
        self.courses_name.addItems(courses)
        self.courses_name.setCurrentText(course_name)
        layout.addWidget(self.courses_name)

        turma_name = main_Window.table.item(index, 3).text()
        self.turma_name = QComboBox()
        courses = ['A', 'B', 'C', 'D']
        self.turma_name.addItems(courses)
        self.courses_name.setCurrentText(turma_name)
        layout.addWidget(self.turma_name)

        phone_number: str = main_Window.table.item(index, 4).text()
        self.phone_number = QLineEdit(phone_number)
        self.phone_number.setPlaceholderText('Mobile')
        layout.addWidget(self.phone_number)

        pai_mae: str = main_Window.table.item(index, 5).text()
        self.pai_mae = QLineEdit(pai_mae)
        self.pai_mae.setPlaceholderText('Pai/Mãe')
        layout.addWidget(self.pai_mae)

        button = QPushButton('Update')
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE students SET name = ?, course = ?, turma = ?, mobile= ?, paimae = ? WHERE id = ?',
                       (self.student_name.text(), self.courses_name.itemText(self.courses_name.currentIndex()),
                        self.turma_name.itemText(self.turma_name.currentIndex()), self.phone_number.text(),
                        self.pai_mae.text(), self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        main_Window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Delete Student Data')

        layout = QGridLayout()
        confirmation = QLabel('Are you sure do you want to delete?')

        yes = QPushButton('Yes')
        no = QPushButton('No')

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)

        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)

    def delete_student(self):
        index = main_Window.table.currentRow()
        student_id = main_Window.table.item(index, 0).text()

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id, ))
        connection.commit()
        cursor.close()
        connection.close()
        main_Window.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle('Sucess')
        confirmation_widget.setText('The record was deleted succesfully!')
        confirmation_widget.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('About')
        content: str = "This was an app that I created in the course. It's basically an app about Student Management"
        self.setText(content)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_Window = MainWindow()
    main_Window.show()
    main_Window.load_data()
    sys.exit(app.exec())
