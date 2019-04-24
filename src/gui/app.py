import mysql.connector
from mysql.connector import errorcode
from PyQt5.QtWidgets import QApplication, QStackedWidget, QStyleFactory
from fubc_lib import Ui_StackedWidget

import sys 
sys.path.insert(0, 'D:\\church_lib\\python_code\\src\\backend')
import sql_data_queries as sdq
 
class MainWindow(QStackedWidget, Ui_StackedWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.cnx = None 
        self.cursor = None
        self.loginBtn.clicked.connect(self.on_login)
    
    def on_login(self):
        user_name = self.user_line.text()
        pass_word = self.pass_line.text()
        self.connect(user_name, pass_word)
        if self.cnx is None or not self.cnx.is_connected():
            print('Login error')
        else:
            print('Sucessful login') 
            self.setCurrentIndex(1)


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