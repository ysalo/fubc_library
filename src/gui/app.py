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
import isbn_fetch
class MainWindow(QStackedWidget, Ui_StackedWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.cnx = None 
        self.cursor = None

        self.connect_buttons()
        self.hide_msgs()    
        self.add_mem_hide_msgs()
        self.hide_genre_msgs()
        self.series_check_box.stateChanged.connect(self.on_in_series_checkbox)
        self.setWindowIcon(QIcon('D:\\church_lib\\python_code\\img\\fubc_logo.jpg'))
        self.on_login()
        self.series_check_box.installEventFilter(self)
        self.showMaximized()

    def on_change_author_btn(self):
        author_id = self.author_list.selectedItems()[0].text().split(' ')[0]
        f_name = self.new_first_name_line.text()
        m_name = self.new_middle_name_line.text()
        l_name = self.new_last_name_line.text()
        print('changing name')
        si.change_author(self.cursor, author_id, f_name, m_name, l_name)
        self.cnx.commit()

    def show_books(self): 
        books = sdq.get_book_titles(self.cursor)
        for book in books: 
            self.books_list.addItem(book)

    def show_loans(self):
        self.loan_list.clear()
        loans = sdq.get_outstanding_loans(self.cursor)
        print(loans)
        for loan in loans: 
            temp = loan[0]  + ' ' + loan[1] + " " + loan[2] + " " + " " + str(loan[4])
            self.loan_list.addItem(temp)

    def show_authors(self):
        self.author_list.clear()
        authors = sdq.get_authors(self.cursor)
        for author in authors: 
            self.author_list.addItem(author)

    def show_genre_names(self):
        genre_list = sdq.get_genre_names(self.cursor)
        self.genre_box.addItems(genre_list)

    def connect_buttons(self):
        #login on 'Enter' press in password line
        self.user_line.returnPressed.connect(self.on_enter_user_line)
        self.pass_line.returnPressed.connect(self.on_enter_pass_line)

        self.loans_back_btn.clicked.connect(self.on_loans_back_btn)
        self.show_loans_btn.clicked.connect(self.on_menu_loan_btn)
        self.login_btn.clicked.connect(self.on_login)
        self.add_book_menu_btn.clicked.connect(self.on_add_book_menu_btn)
        self.add_author_menu_btn.clicked.connect(self.on_add_menu_author_btn)
        self.add_mem_menu_btn.clicked.connect(self.on_add_mem_menu_btn)
        self.add_book_btn.clicked.connect(self.on_add_book)
        self.add_book_cancel_btn.clicked.connect(self.on_add_book_cancel)
        self.clear_book_btn.clicked.connect(self.on_clear_book)
        self.clear_series_btn.clicked.connect(self.on_clear_series)
        self.clear_author_btn.clicked.connect(self.on_clear_author)
        self.add_mem_back_btn.clicked.connect(self.on_add_mem_back_btn)
        self.add_book_back_btn.clicked.connect(self.on_add_book_back_btn)
        self.add_mem_add_btn.clicked.connect(self.on_add_mem)
        self.add_mem_clear_btn.clicked.connect(self.on_add_mem_clear)
        self.add_genre_menu_btn.clicked.connect(self.on_add_genre_menu_btn)
        self.add_genre_back_btn.clicked.connect(self.on_add_genre_back_btn)
        self.clear_genre_btn.clicked.connect(self.on_clear_genre_btn)
        self.add_genre_btn.clicked.connect(self.on_add_genre_btn)
        self.checkout_menu_btn.clicked.connect(self.on_checkout_menu_btn)
        self.checkout_back_btn.clicked.connect(self.on_checkout_back_btn)
        self.checkout_clear_btn.clicked.connect(self.on_checkout_clear_btn)
        self.checkout_btn.clicked.connect(self.on_checkout_btn)
        self.display_genre_btn.clicked.connect(self.on_display_genre_btn)
        self.checkout_br_line.returnPressed.connect(self.on_enter_br_line)
        self.checkout_email_line.returnPressed.connect(self.on_enter_checkout_email_line)
        self.search_gernre_btn.clicked.connect(self.on_search_gernre_btn)
        self.display_genre_back_btn.clicked.connect(self.on_display_genre_back_btn)
        self.clear_display_genre_btn.clicked.connect(self.on_clear_display_genre_btn)
        self.info_from_isbn_btn.clicked.connect(self.on_info_from_isbn_btn)
        self.add_author_btn.clicked.connect(self.on_add_author_btn)
        self.change_author_menu_btn.clicked.connect(self.on_change_author_menu_btn)
        self.change_author_back_btn.clicked.connect(self.on_change_author_back_btn)
        self.change_author_btn.clicked.connect(self.on_change_author_btn)
        self.add_author_back_btn.clicked.connect(self.on_add_author_back_btn)

    def on_info_from_isbn_btn(self):
        isbn = self.isbn_info_line.text()
        try: 
            can_isbn, book_info = isbn_fetch.get_isbn_info(isbn)
            print(book_info)
            title = book_info.get('Title')
            pub_year = book_info.get('Year')
            author = book_info.get('Authors')[0].split(' ')
            if len(author) == 3: 
                self.first_name_line.setText(author[0])
                self.middle_name_line.setText(author[1]) 
                self.last_name_line.setText(author[2])
            else: 
                self.first_name_line.setText(author[0])
                self.last_name_line.setText(author[1])
                
                
                
            self.book_title_line.setText(title)
            self.isbn_line.setText(can_isbn)
            self.language_box.setCurrentIndex(2)
            self.pub_year_line.setText(pub_year)
            #self.genre_box.setCurrentIndex(2)``
            self.barcode_line.setFocus()
        except: 
            self.isbn_line.setText(self.isbn_info_line.text())
            e = sys.exc_info()[0]
            print(e)
            
     
    def on_login(self):
        user_name = 'root'
        pass_word = ''
        self.connect(user_name, pass_word)
        if self.cnx is None or not self.cnx.is_connected():
            self.user_line.clear()
            self.pass_line.clear()
            self.user_line.setFocus()
            self.login_err_msg.show()
        else:
            print("connected")
            self.show_genre_names()
            self.genre_box.setCurrentIndex(5)
            self.setCurrentIndex(1)

    def on_add_author_back_btn(self):
        self.setCurrentIndex(1)

    def on_loans_back_btn(self):
        self.setCurrentIndex(1)

    def on_menu_loan_btn(self):
        self.show_loans()
        self.setCurrentIndex(9)

    def on_add_author_btn(self):
        for item in self.books_list.selectedItems():
            print(item.text())

    def on_add_menu_author_btn(self):
        self.show_books()
        self.setCurrentIndex(7)

    def on_change_author_menu_btn(self):
        self.show_authors()
        self.setCurrentIndex(8)

    def on_change_author_back_btn(self):
        self.setCurrentIndex(1)

    def on_checkout_menu_btn(self):
        self.setCurrentIndex(5)

    def on_display_genre_btn(self):
        self.setCurrentIndex(6)

    def on_checkout_back_btn(self):
        self.setCurrentIndex(1)

    def on_add_book_menu_btn(self):
        self.setCurrentIndex(2)

    def on_add_mem_menu_btn(self):
        self.setCurrentIndex(3)

    def on_add_mem_back_btn(self):
        self.setCurrentIndex(1)

    def on_add_book_back_btn(self):
        self.setCurrentIndex(1)

    def on_add_genre_menu_btn(self):
        self.setCurrentIndex(4)

    def on_add_genre_back_btn(self):
        self.setCurrentIndex(1)

    def on_display_genre_back_btn(self):
        self.setCurrentIndex(1)
    
    def on_search_gernre_btn(self):
        self.display_genre_list.clear()
        barcode = self.barcode_search_line.text()
        genre_name = sdq.get_genre_name(self.cursor, barcode)
        self.display_genre_list.addItem(genre_name)
        print(genre_name)

    def on_clear_display_genre_btn(self):
        self.display_genre_list.clear()
        self.barcode_search_line.clear()
        self.barcode_search_line.setFocus() 

    def on_checkout_clear_btn(self):
        self.checkout_br_line.clear()
        self.checkout_email_line.clear()
        self.checkout_br_line.setFocus()

    def on_clear_genre_btn(self):
        self.add_genre_fail_err_msg.hide()
        self.genre_name_line.clear()
        self.genre_name_line.setFocus()

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
        self.isbn_info_line.clear()
        self.hide_msgs()
        self.isbn_info_line.setFocus()

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

    def on_enter_br_line(self):
        self.checkout_email_line.setFocus()
    
    def on_enter_checkout_email_line(self):
        self.checkout_btn.click()
        

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

    def on_add_genre_btn(self):
        self.hide_genre_msgs()
        genre_name = self.genre_name_line.text()
        if self.check_genre_form():
            si.add_genre(self.cursor, genre_name)
            self.cnx.commit()
            self.genre_box.addItem(genre_name)
            self.add_genre_suc_msg.show()
        else:
            self.add_genre_fail_err_msg.show()

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

    def on_checkout_btn(self):
        barcode = self.checkout_br_line.text()
        email = self.checkout_email_line.text()
        si.add_loan(self.cursor, barcode, email)
        self.cnx.commit()
    
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

    def check_genre_form(self):
        return not len(self.genre_name_line.text()) == 0


    def hide_genre_msgs(self):
        self.add_genre_fail_err_msg.hide()
        self.add_genre_suc_msg.hide()

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

    # def closeEvent(self, event):
    #     if self.cnx: 
    #         self.cnx.close()
    #         self.cursor.close() 
    #         print('MySql Connection Closed')
    #     print('Application Closing')
    #     event.accept()

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
    myscreen = QApplication.desktop()
    width = myscreen.width()
    height = myscreen.height()
    main_window = MainWindow()
    # main_window.setFixedSize(width, height)
    main_window.showMaximized()
    #main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()