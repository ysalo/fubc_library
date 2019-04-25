import mysql.connector
from mysql.connector import errorcode
from PyQt5.QtWidgets import QApplication, QStackedWidget, QStyleFactory
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets
from fubc_lib import Ui_StackedWidget

import sys 
sys.path.insert(0, 'D:\\church_lib\\python_code\\src\\backend')
import sql_data_queries as sdq
import sql_inserts as si
 
class MainWindow(QStackedWidget, Ui_StackedWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.cnx = None 
        self.cursor = None
        self.loginBtn.clicked.connect(self.on_login)
        self.add_book_btn.clicked.connect(self.on_add_book)
        self.add_book_cancel_btn.clicked.connect(self.on_add_book_cancel)
        self.login_error_label.hide()
        self.user_line.returnPressed.connect(self.on_enter_user_line)
        self.pass_line.returnPressed.connect(self.on_enter_pass_line)
        self.series_check_box.stateChanged.connect(self.on_in_series_checkbox)
        self.setWindowIcon(QIcon('D:\\church_lib\\python_code\\img\\fubc_logo.jpg'))
        self.series_check_box.installEventFilter(self)
        
        self.setFixedSize(self.size())

    def eventFilter(self, o, e):
        # if (o.objectName() == "series_check_box"):
        if e.type() == QtCore.QEvent.KeyPress and e.key() ==  QtCore.Qt.Key_Return:
            self.series_check_box.nextCheckState()
            return True 
        return False
    # def eventFilter(self, o, e):
    #     if e.type() == QEvent.DragEnter: #remember to accept the enter event
    #         e.acceptProposedAction()
    #         return True
    #     if e.type() == QEvent.Drop:
    #         # handle the event
    #         # ...
    #         return True
    #     return False #remember to return false for other event types

    def on_in_series_checkbox(self):
        state = not self.series_label.isEnabled()
        self.series_label.setEnabled(state)
        self.in_series_label.setEnabled(state)
        self.series_title_label.setEnabled(state)
        self.series_title_line.setEnabled(state)
        self.in_series_line.setEnabled(state)

    def on_enter_user_line(self):
        self.pass_line.setFocus()

    def on_enter_pass_line(self):
        self.loginBtn.click()

    def on_login(self):
        user_name = self.user_line.text()
        pass_word = self.pass_line.text()
        self.connect(user_name, pass_word)
        if self.cnx is None or not self.cnx.is_connected():
            print('Login error')
            self.user_line.clear()
            self.pass_line.clear()
            self.user_line.setFocus()
            self.login_error_label.show()
        else:
            print('Sucessful login') 
            self.setCurrentIndex(1)

    def on_add_book(self):
        title = self.book_title_line.text()
        isbn = self.isbn_line.text()
        language = self.language_box.currentText()
        publication_year = self.pub_year_line.text()
        genre_name = self.genre_box.currentText()
        last_name = self.last_name_line.text()
        first_name = self.first_name_line.text()
        middle_name = self.middle_name_line.text()
        series_title = self.series_title_line.text()
        in_series_number = self.in_series_line.text()
        barcode = self.barcode_line.text()

        print("""Title: {} ISBN: {} Language: {} Publication Year: {} \nGenre: {} Last Name: {} First Name: {} Middle Name: {} 
            Series Title: {} In Series Number: {} Barcode: {}""".format(title, isbn, language, publication_year, genre_name
        ,last_name,first_name,middle_name,series_title,in_series_number,barcode))

    def on_add_book_cancel(self):
        self.book_title_line.clear()
        self.isbn_line.clear()
        self.pub_year_line.clear()
        self.last_name_line.clear()
        self.first_name_line.clear()
        self.middle_name_line.clear()
        self.series_title_line.clear()
        self.in_series_line.clear()
        self.barcode_line.clear()
        self.book_title_line.setFocus()

    def connect(self, user_name, pass_word):
        try:
            self.cnx = mysql.connector.connect(user=user_name, password=pass_word,
                                        host='127.0.0.1',
                                        database='fubc_library')

            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Incorrect Username or Password!")

            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist!")
    
            else:
                print(err)    
        # else:
        #     print('Closing Database Connection.')
        #     self.cnx.close()
        
    def closeEvent(self, event):
        if self.cnx: 
            self.cnx.close()
            self.cursor.close() 
            print('MySql Connection Closed')
        print('Application Closing')
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()