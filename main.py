# Primeiro abri o terminal e digitei: pip install pyqt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QLineEdit
from PyQt6.QtGui import QAction
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

        add_student_action = QAction('Add Student', self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction('About', self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)

        if os.name == 'darwin':  # é do mac, e pode ser preciso se não, não aparece as actions!!
            add_student_action.setMenuRole(QAction.MenuRole.NoRole)
            about_action.setMenuRole(QAction.MenuRole.NoRole)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Turma', 'Mobile', 'Pai/Mãe'))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

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

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def about(self):
        pass


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        student_name = QLineEdit()
        student_name.setPlaceholderText('Name')
        layout.addWidget(student_name)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    age_calculador = MainWindow()
    age_calculador.show()
    age_calculador.load_data()
    sys.exit(app.exec())
