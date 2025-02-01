from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication,QLabel,QGridLayout,QLineEdit,QPushButton,QWidget,QComboBox,QMainWindow,QTableWidget,QTableWidgetItem,QDialog,QVBoxLayout,QToolBar,QStatusBar,QMessageBox

import sys

from PyQt6.QtGui import QAction,QIcon

import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #sets the title
        self.setWindowTitle("Student Management Program")
        self.setWindowIcon(QIcon('icons/learning.png'))
        
        #minimum window opening size
        self.setMinimumSize(800,600)
        
        #creates a file menu in header
        file_menu_item=self.menuBar().addMenu("&File")
        
        #creates a help menu in header
        help_menu_item=self.menuBar().addMenu('&Help')
        
        #creates edit menu in header
        edit_menu_item=self.menuBar().addMenu('&Edit')
        
        """
        self is passed to make this action a child of MainWindow
        This ensures proper memory management and event handling
        """
        
        #creates add option in the file menu
        add_action=QAction(QIcon('icons/add.png'),"Add Student",self)
        add_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_action)
        
        #creates about section in help menu
        about_action=QAction(QIcon('icons/person.png'),"About",self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)
        
        
        #creates search section in help menu
        search_action=QAction(QIcon('icons/search.png'),"Search",self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)
        
        #creating columns for the database data
        self.table=QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id","Name","Course","Mobile"))
        
        #avoid index 
        self.table.verticalHeader().setVisible(False)
        #self here is refering to MainWindow instance
        self.setCentralWidget(self.table)

        #create toolbar and add icons
        toolbar=QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_action)
        toolbar.addAction(search_action)
      
        #creating statusbar and add its elements
        self.status_bar=QStatusBar()
        self.setStatusBar(self.status_bar)
        
        
        # Detect cell click
        self.table.cellClicked.connect(self.cell_clicked)
        
        
    #when a cell is clicked two button appear on the status bar
    def cell_clicked(self):
        edit_button=QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)
        
        delete_button=QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)
        
        #remove duplicates button
        children=self.findChildren(QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)

        #adds the buttons to the status bar
        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)


    #Load the data from the Database file into the pyqt window    
    def load_data(self):
        connection=sqlite3.connect("database.db")
        result=connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        
        #load all the data on pyqt6 window
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.table.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        connection.close()
        
    #Insert data function    
    def insert(self):
        dialog=InsertDialog()
        dialog.exec()

    def search(self):
        dialog=SearchDialog()
        dialog.exec()

    def delete(self):
        dialog=DeleteDialog()
        dialog.exec()

    def edit(self):
        dialog=EditDialog()
        dialog.exec()
        
    def about(self):
        dialog=AboutDialog()
        dialog.exec()
        

#Edit Dialog
class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Edit Dialog")
        self.setWindowIcon(QIcon('icons/pencil'))
        self.setFixedHeight(300)
        self.setFixedWidth(300)        

        layout=QVBoxLayout()
        
        #Get student name after row is selected
        index=window.table.currentRow()
        student_name=window.table.item(index,1).text()
         
        self.student_id=window.table.item(index,0).text()
        
        self.student_name=QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        
        #retreive the course name
        course_name=window.table.item(index,2).text()
        
        self.courses_menu=QComboBox()
        courses=['Biology','Astronomy','Maths',"Physics"]
        self.courses_menu.addItems(courses)
        self.courses_menu.setCurrentText(course_name)
        
        #retreive the mobile number
        mobile_number=window.table.item(index,3).text()
        
        self.mobile=QLineEdit(mobile_number)
        self.mobile.setPlaceholderText('Mobile')
        
        edit_button=QPushButton("Edit")
        edit_button.clicked.connect(self.edit)
        
        
        layout.addWidget(self.student_name)
        layout.addWidget(self.courses_menu)
        layout.addWidget(self.mobile)
        layout.addWidget(edit_button)

        
        self.setLayout(layout)
        
    def edit(self):
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        
        cursor.execute('UPDATE students SET name=?, course =?, mobile=? WHERE id=?',(self.student_name.text(),self.courses_menu.current(),self.mobile.text(),self.student_id))
        
        connection.commit()
        cursor.close()
        
        #refresh table
        window.load_data()


#Search Dialog
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        #setting window dimensions
        self.setWindowTitle("Search Data")
        self.setWindowIcon(QIcon('icons/search.png'))
        self.setFixedHeight(300)
        self.setFixedWidth(300)
        
        layout=QVBoxLayout()
        
        #search input by user
        self.search_line=QLineEdit()
        self.search_line.setPlaceholderText("Search name")
        
        #search button
        self.search_button=QPushButton("Search")
        self.search_button.clicked.connect(self.search)
        
        #adding these widgets to the layout
        layout.addWidget(self.search_line)
        layout.addWidget(self.search_button)
        
        self.setLayout(layout)

    def search(self):
        name=self.search_line.text()
        connection=sqlite3.connect('database.db')
        cursor=connection.cursor()
        result=cursor.execute('SELECT * FROM students WHERE name=?',(name, ))
        
        items = window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
    
    # Clear previous selections
        window.table.clearSelection()
    
        if items:
        # Select the found items
            for item in items:
                item.setSelected(True)
            # Optionally scroll to the item
                window.table.scrollToItem(item)
        else:
        # Show a message box if no results are found
            QMessageBox.information(self, "No Results", "No records found for the given name.")

        
        
        cursor.close()
        connection.close()
            
        

#create insert dialog 
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        #set the dimensions of window 
        self.setWindowTitle('Insert Student Data')
        self.setWindowIcon(QIcon('icons/add.png'))
        self.setFixedHeight(300)
        self.setFixedWidth
        (300)
        
        layout=QVBoxLayout()
        
        #Student Name widget
        self.student_name=QLineEdit()
        self.student_name.setPlaceholderText("Name")
        
        #Course Dropdown list
        self.course_name=QComboBox()
        courses=['Biology',"Math","Physics","Astronomy"]
        self.course_name.addItems(courses)
        
        #Mobile Widget
        self.mobile=QLineEdit()
        self.mobile.setPlaceholderText("Phone number")
        
        #submit button
        submit_button=QPushButton("Submit button")
        submit_button.clicked.connect(self.add_student)
        
        #adding these widgets to the layout
        layout.addWidget(self.student_name)        
        layout.addWidget(self.course_name)
        layout.addWidget(self.mobile)        
        layout.addWidget(submit_button)
        
        self.setLayout(layout)
        
    #Add student functionality code  
    def add_student(self):
        name=self.student_name.text()
        mobile=self.mobile.text()
        course=self.course_name.itemText(self.course_name.currentIndex())
        
        connection=sqlite3.connect("database.db")
        cursor=connection.cursor()
        cursor.execute('INSERT INTO students (name,course,mobile) VALUES (?,?,?)',(name,course,mobile))
        connection.commit()
        cursor.close()
        connection.close()
        
        #refreshes the data
        window.load_data()
        
        
#Delete Dialog
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        
        grid=QGridLayout()
        
        self.setWindowTitle("Delete Confirmation")
        self.setWindowIcon(QIcon('icons/delete.png'))
        
        confirmation_label=QLabel("Are you sure that you want to delete this data?")

        yes_button=QPushButton("Yes")
        
        no_button=QPushButton("No")
                
        
        grid.addWidget(confirmation_label,0,0,1,2)
        grid.addWidget(yes_button,1,0)
        grid.addWidget(no_button,1,1)
        
        self.setLayout(grid)
        
        yes_button.clicked.connect(self.delete)
        
        
        
    def delete(self):
        index=window.table.currentRow()
        student_id=window.table.item(index,0).text()
        connection=sqlite3.connect('database.db')
        cursor=connection.cursor()
        
        cursor.execute("DELETE from students WHERE id=?", (student_id, ))
        
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()

        self.close()
        
        sucess_widget=QMessageBox()
        sucess_widget.setWindowTitle("Success")
        sucess_widget.setText("The record was deleted sucessfully!")
        sucess_widget.exec()
        

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon('icons/person.png'))

        message='''A streamlined student management system developed by Arpit Jain. Built with PyQt6 in Python, this application offers essential database operations including adding, deleting, searching, and editing student records. The system features a clean, minimalist interface designed for ease of use.
        
        Enjoy using this app
        '''
        
        self.setText(message)
        
    
app=QApplication(sys.argv)
window=MainWindow()
window.show()
window.load_data()
sys.exit(app.exec())
        