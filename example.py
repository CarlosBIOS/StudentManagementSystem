# O PyQt6 é implementado como mais de 35 módulos de extensão e permite que o Python seja usado como uma linguagem de
# desenvolvimento de aplicativos alternativa ao C++ em todas as plataformas suportadas, incluindo iOS e Android.
# Em resumo, o PyQt6 permite que você crie interfaces gráficas (GUIs) ricas e multiplataforma com Python. Ele oferece
# uma ampla gama de recursos, incluindo:
# Widgets: Uma variedade de widgets prontos para usar, como botões, caixas de diálogo, menus e layouts.
# Sinais e slots: Um mecanismo poderoso para conectar eventos de GUI à lógica do seu aplicativo.
# Estilos: Personalização completa da aparência da sua GUI.
# Modelo-vista: Crie interfaces dinâmicas que representam dados.
# Gráficos: Crie gráficos e gráficos 2D e 3D.
# Implementação multiplataforma: Execute os seus aplicativos em Windows, macOS, Linux, iOS e Android.

# Primeiro abri o terminal e digitei: pip install pyqt6
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QLineEdit, QPushButton, QComboBox
from datetime import datetime
import sys


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Age Calculator')

        grid = QGridLayout()
        name_label = QLabel('Name:')
        self.name_line_edit = QLineEdit()
        date_label = QLabel('Date of Birth in DD/MM/YYYY:')
        self.date_line_edit = QLineEdit()

        self.unit_botton = QComboBox()
        self.unit_botton.addItems(['Option1', 'Option2'])

        calculate_button = QPushButton('Calculate Age')
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel('')

        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(date_label, 1, 0)
        grid.addWidget(self.date_line_edit, 1, 1)
        grid.addWidget(self.unit_botton, 2, 0)
        grid.addWidget(calculate_button, 3, 0, 1, 2)
        grid.addWidget(self.output_label, 4, 0, 1, 2)

        self.setLayout(grid)

    def calculate_age(self):
        day, month, year = datetime.now().day, datetime.now().month, datetime.now().year
        day_birth, month_birth, year_birth = [int(elem) for elem in self.date_line_edit.text().split('/')]

        if (day_birth > day and month_birth == month) or month < month_birth:
            year_birth += 1
        age = year - year_birth

        self.output_label.setText(f'{self.name_line_edit.text().title()} is {age} years old.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    age_calculador = AgeCalculator()
    age_calculador.show()
    sys.exit(app.exec())
