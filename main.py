from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, \
    QMessageBox
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')
        self.setMinimumSize(800, 600)

        # Adding the main menu bar
        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu('&Edit')

        # Adding the submenu items of the main menu bar items
        add_student_action = QAction(QIcon('icons/add.png'), 'Add Student', self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction('About', self)
        help_menu_item.addAction(about_action)

        search_action = QAction(QIcon('icons/search.png'), 'Search', self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # Adding table and setting the columncount and columnlabels
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile'))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create toolbar and add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

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

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Student')
        # set Window title and size
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # vertical box layout
        layout = QVBoxLayout()

        # Add Search option
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # Add a Search button
        button = QPushButton('Search')
        button.clicked.connect(self.student_search)
        layout.addWidget(button)

        self.setLayout(layout)

    def student_search(self):
        name = self.student_name.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        results = cursor.execute('SELECT * FROM students WHERE name = ?', (name,))
        rows = list(results)
        print(rows)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            # item.row() gives the row value and 1 represents name column
            main_window.table.item(item.row(), 1).setSelected(True)

        # Handle no matching records found with pop-up dialog.
        if not rows:
            msg = QMessageBox()
            msg.setWindowTitle("No Records")
            msg.setText("No matching records found")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()

        cursor.close()
        connection.close()



class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ['Biology', 'Math', 'Astronomy', 'Physics']
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add Mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText('Mobile')
        layout.addWidget(self.mobile)

        # Add a Submit button
        button = QPushButton('Register')
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)


    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO students (name, course, mobile) VALUES (?,?,?)',
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())