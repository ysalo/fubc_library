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

        self.connect_buttons()
        self.hide_msgs()
        self.add_mem_hide_msgs()
        self.series_check_box.stateChanged.connect(self.on_in_series_checkbox)
        self.setWindowIcon(QIcon('D:\\church_lib\\python_code\\img\\fubc_logo.jpg'))
        self.series_check_box.installEventFilter(self)
        self.showMaximized()



 
    # '''
    # align widgets that could not be aligned in Designer
    # '''
    # def set_alignment(self):
    #     self.formLayout.setAlignment(QtCore.Qt.AlignHCenter)
    #     self.formLayout_2.setAlignment(QtCore.Qt.AlignHCenter)


    def connect_buttons(self):
        self.user_line.returnPressed.connect(self.on_enter_user_line)
        self.pass_line.returnPressed.connect(self.on_enter_pass_line)
        self.login_btn.clicked.connect(self.on_login)
        self.add_book_menu_btn.clicked.connect(self.on_add_book_menu_btn)
        self.add_mem_menu_btn.clicked.connect(self.on_add_mem_menu_btn)
        self.add_book_btn.clicked.connect(self.on_add_book)
        self.add_book_cancel_btn.clicked.connect(self.on_add_book_clear)
        self.clear_book_btn.clicked.connect(self.on_clear_book)
        self.clear_series_btn.clicked.connect(self.on_clear_series)
        self.clear_author_btn.clicked.connect(self.on_clear_author)
        self.add_mem_back_btn.clicked.connect(self.on_add_mem_back_btn)
        self.add_book_back_btn.clicked.connect(self.on_add_book_back_btn)
        self.add_mem_add_btn.clicked.connect(self.on_add_mem)
        self.add_mem_clear_btn.clicked.connect(self.on_add_mem_clear)

    def on_login(self):
        user_name = self.user_line.text()
        pass_word = self.pass_line.text()
        self.connect(user_name, pass_word)
        if self.cnx is None or not self.cnx.is_connected():
            self.user_line.clear()
            self.pass_line.clear()
            self.user_line.setFocus()
            self.login_err_msg.show()
        else:
            self.setCurrentIndex(1)


    def on_add_book_menu_btn(self):
        self.setCurrentIndex(2)

    def on_add_mem_menu_btn(self):
        self.setCurrentIndex(3)

    def on_add_mem_back_btn(self):
        self.setCurrentIndex(1)

    def on_add_book_back_btn(self):
        self.setCurrentIndex(1)

    def on_clear_book(self):
        self.book_title_line.clear()
        self.isbn_line.clear()
        self.pub_year_line.clear()
        self.language_box.setCurrentIndex(0)
        self.genre_box.setCurrentIndex(0)
        self.book_title_line.setFocus()
        
    def on_clear_author(self):
        self.last_name_line.clear()
        self.first_name_line.clear()
        self.middle_name_line.clear()
        self.last_name_line.setFocus()
    
    def on_clear_series(self):
        self.series_title_line.clear()
        self.in_series_line.clear()
        self.series_title_line.setFocus()

    def on_add_book_clear(self):
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
        self.hide_msgs()

    def on_add_mem_clear(self):
        self.add_mem_last_line.clear()
        self.add_mem_mid_line.clear()
        self.add_mem_first_line.clear()
        self.add_mem_email_line.clear()
        self.add_mem_phone_line.clear()
        self.add_mem_hide_msgs()
        self.add_mem_last_line.setFocus()

    def on_enter_user_line(self):
        self.pass_line.setFocus()

    def on_enter_pass_line(self):
        self.login_btn.click()

    def on_in_series_checkbox(self):
        state = not self.series_label.isEnabled()
        self.series_label.setEnabled(state)
        self.in_series_label.setEnabled(state)
        self.series_title_label.setEnabled(state)
        self.series_title_line.setEnabled(state)
        self.in_series_line.setEnabled(state)
        self.clear_series_btn.setEnabled(state)
        self.series_title_err_msg.hide()
        self.in_series_err_msg.hide()

    def on_add_mem(self):
        self.add_mem_hide_msgs()
        last_name = self.add_mem_last_line.text()
        mid_name = self.add_mem_mid_line.text() if self.add_mem_mid_line.isEnabled() else None 
        first_name = self.add_mem_first_line.text()
        email = self.add_mem_email_line.text()
        phone = self.add_mem_phone_line.text() if self.add_mem_phone_line.isEnabled() else None 

        if self.check_mem_form():
            si.add_member(self.cursor, first_name, last_name, email, mid_name, phone)
            self.cnx.commit()
            self.add_mem_suc_msg.show()
        else: 
            self.add_mem_fail_err_msg.show()

    def on_add_book(self):
        self.hide_msgs()
        title = self.book_title_line.text()
        isbn = self.isbn_line.text()
        language = self.language_box.currentText()
        publication_year = self.pub_year_line.text()
        genre_name = self.genre_box.currentText()
        last_name = self.last_name_line.text()
        first_name = self.first_name_line.text()
        middle_name = self.middle_name_line.text()
        series_title = self.series_title_line.text() if self.series_title_line.isEnabled() else None 
        in_series_number = self.in_series_line.text() if self.series_title_line.isEnabled() else None 
        barcode = self.barcode_line.text()

        if self.check_add_book_form():
            si.add_book(self.cursor, 'book', barcode, title, first_name, last_name, language, publication_year, genre_name,
            middle_name, isbn, series_title, in_series_number)
            self.cnx.commit()
            self.add_book_sucs_msg.show()
            self.barcode_line.setFocus()
            self.barcode_line.selectAll()
        else: 
            self.add_book_err_msg.show()
            
        # print("""Title: {} ISBN: {} Language: {} Publication Year: {} \nGenre: {} Last Name: {} First Name: {} Middle Name: {} 
        #     Series Title: {} In Series Number: {} Barcode: {}""".format(title, isbn, language, publication_year, genre_name
        # ,last_name,first_name,middle_name,series_title,in_series_number,barcode))

    #TODO: find a way to do this cleaner, eventually.
    def check_add_book_form(self):
        flag = True
        if len(self.book_title_line.text()) == 0:
            self.book_title_err_msg.show()
            flag = False 

        if len(self.pub_year_line.text()) == 0:
            self.pub_year_err_msg.show()
            flag = False

        if len(self.last_name_line.text()) == 0:
            self.last_name_err_msg.show()
            flag = False
            
        if len(self.first_name_line.text()) == 0:
            self.first_name_err_msg.show()
            flag = False

        if len(self.first_name_line.text()) == 0:
            self.first_name_err_msg.show()
            flag = False
        
        if len(self.barcode_line.text()) == 0:
            self.barcode_err_msg.show()
            flag = False
    
        if self.series_check_box.checkState():
            if len(self.series_title_line.text()) == 0:
                self.series_title_err_msg.show()
                flag = False
        
        if self.series_check_box.checkState():
            if len(self.in_series_line.text()) == 0:
                self.in_series_err_msg.show()
                flag = False
        return flag

    def check_mem_form(self):
        flag = True
        if len(self.add_mem_last_line.text()) == 0:
            self.add_mem_last_err_msg.show()
            flag = False 

        if len(self.add_mem_first_line.text()) == 0:
            self.add_mem_first_err_msg.show()
            flag = False

        if len(self.add_mem_email_line.text()) == 0:
            self.add_mem_email_err_msg.show()
            flag = False
 
        return flag

    def hide_msgs(self):
        self.login_err_msg.hide()
        self.book_title_err_msg.hide()
        self.pub_year_err_msg.hide()
        self.series_title_err_msg.hide()
        self.in_series_err_msg.hide()
        self.last_name_err_msg.hide()
        self.first_name_err_msg.hide()
        self.barcode_err_msg.hide()
        self.add_book_err_msg.hide()
        self.add_book_sucs_msg.hide()
        self.add_mem_last_err_msg.hide()
        self.add_mem_first_err_msg.hide()
        self.add_mem_email_err_msg.hide()

    def add_mem_hide_msgs(self):
        self.add_mem_last_err_msg.hide()
        self.add_mem_first_err_msg.hide()
        self.add_mem_email_err_msg.hide()
        self.add_mem_fail_err_msg.hide()
        self.add_mem_suc_msg.hide()

    def closeEvent(self, event):
        if self.cnx: 
            self.cnx.close()
            self.cursor.close() 
            print('MySql Connection Closed')
        print('Application Closing')
        event.accept()

    def eventFilter(self, o, e):
        if e.type() == QtCore.QEvent.KeyPress and e.key() ==  QtCore.Qt.Key_Return:
            self.series_check_box.nextCheckState()
            return True 
        return False

    def connect(self, user_name, pass_word):
        try:
            self.cnx = mysql.connector.connect(user=user_name, password=pass_word,
                                        host='127.0.0.1',
                                        database='fubc_library')
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error:
            pass

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_window = MainWindow()
    main_window.show()
    main_window.setFixedSize(main_window.size())
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()