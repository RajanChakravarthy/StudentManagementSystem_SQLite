from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QAction
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')

        # Adding the main menu bar
        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')

        # Adding the submenu items of the main menu bar items
        add_student_action = QAction('Add Student', self)
        file_menu_item.addAction(add_student_action)

        about_action = QAction('About', self)
        help_menu_item.addAction(about_action)

        # Adding table and setting the columncount and columnlabels
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        # Loading the sql database
        connection = sqlite3.connect('database.db')
        result = connection.execute('SELECT * FROM students')
        # Reloads the tables with data on the db and not reloads over the existing data
        self.table.setRowCount(0)
        # Each row in enumerated
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            # data in each row is enumerated
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()


app = QApplication(sys.argv)
Student_management_system = MainWindow()
Student_management_system.show()
Student_management_system.load_data()
sys.exit(app.exec())