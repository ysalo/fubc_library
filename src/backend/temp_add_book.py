import sql_inserts, sql_data_queries, isbn_fetch
import mysql.connector
from mysql.connector import errorcode

try:
    user_name = 'root'
    password = 'Boryslav1948'
    cnx = mysql.connector.connect(user=user_name, password=password,
                                host='127.0.0.1',
                                database='fubc_library')
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Incorrect Username or Password!")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist!")
    else:
        print(err)

while True:
    user_input = input('Scan ISBN: ')
    isbn, book_info = isbn_fetch.get_isbn_info(user_input)
    title = book_info.get('Title')
    authors = book_info.get('Authors')
    first_name, last_name = sql_data_queries.split_author_name(authors[0])
    year = book_info.get('Year')
    language = book_info.get('Language')
    barcode = input('Scan Barcode: ')

    sql_inserts.add_book(cursor, barcode, title, first_name, last_name, isbn, language, year)
    cnx.commit()