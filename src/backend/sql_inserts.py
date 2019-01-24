import mysql.connector
from sql_data_queries import *
from mysql.connector import errorcode

"""
Add new item type, ignores the request if the type already exists.
"""
def add_item_type(cursor, type_name):
    try:
        q = ("INSERT INTO Item_Type(Type_Name) VALUES (%s)")
        cursor.execute(q, (type_name,))
        print("Successfully added to Item_Type Table type_name = ({})".format(type_name))
    except mysql.connector.IntegrityError as err:
        print(err ,"in **Item_Type** Table IGNORED.")

"""
Add an Item if the type_id is found 
Ignores the request otherwise
"""
def add_item(cursor, barcode, type_name):
    type_id = get_item_type_id(cursor, type_name)   
    if type_id:
        try:
            q = ("INSERT INTO Item(barcode, type_id) VALUES (%s, %s)")
            cursor.execute(q, (barcode, type_id)) 
            print("Successfully added to Item Table barcode = ({}) type_name = ({})".format(barcode, type_name))
        except mysql.connector.IntegrityError as err:
            print(err ,"in **Item** Table IGNORED.")
    else: 
        print('Cannot add Item barcode = ({}) because type_name = ({}) does not exist.'.format(barcode, type_name))

"""
Add new author, ignores the request if the author already exists.
""" 
def add_author(cursor, first_name, last_name):
    try:
        q = ("INSERT INTO Authors(first_name, last_name) VALUES (%s, %s)")
        cursor.execute(q, (first_name, last_name))
        print("Successfully added to Authors Table fist_name = ({}) last_name = ({})".format(first_name, last_name))
    except mysql.connector.IntegrityError as err:
        print(err ,"in **Authors** Table IGNORED.")

"""
Adds a book entry if the barcode is found and if the title does not exist, 
ignore the request otherwise.
"""
def add_book_entry(cursor, barcode, title, isbn, language, publication_year):
    q = ("SELECT COUNT(*) FROM Item WHERE barcode = %s")
    cursor.execute(q, (barcode,))
    result = cursor.fetchall()[0][0]
    if result == 1:
        try:
            q = ("INSERT INTO Books (title, isbn, language, publication_year) VALUES (%s, %s, %s, %s)")
            cursor.execute(q, (title, isbn, language, publication_year)) 
            print("Successfully added to Books title = ({})".format(title))
        except mysql.connector.IntegrityError as err:
            print(err ,"in **Books** Table IGNORED.")
    else: 
        print("Cannot add into Book title = ({}) because barcode = ({}) does not exist in the Item Table".format(title,barcode))



"""
Connects the author to the book only if both the author and book already exist, 
ignores the request otherwise.
"""
#TODO: rewrite the method to take in only the ids?
def add_authored_by(cursor, first_name, last_name, title): 
    author_id = get_author_id(cursor, first_name, last_name)
    book_id = get_book_id(cursor, title)
    if author_id and book_id:
        try: #TODO: add handling code for duplicate and non existant entries
            q = ("INSERT INTO Book_Authored_By (author_id, book_id) VALUES (%s, %s)")
            cursor.execute(q, (author_id, book_id))
            print("Successfully added to Book_Authored_By author_id = ({}) book_id = ({})".format(author_id, book_id))
        except mysql.connector.IntegrityError as err:
            print(err ,"in **Book_Authored_By** Table IGNORED.")
    else: 
        print("Cannot add to Authored by with author_id = ({}), book_id = ({})".format(author_id, book_id))    

"""
Connects a book to a barcode only if both already exist,
ignores the request otherwise.
"""
def add_book_to_barcode(cursor, title, barcode): 
    book_id = get_book_id(cursor, title)
    q = ("SELECT COUNT(*) FROM Item WHERE barcode = %s")
    cursor.execute(q, (barcode,))
    result = cursor.fetchall()[0][0]
    if result == 1 and book_id:   
        try:
            q = ("INSERT INTO Book_To_Barcode (Book_Id, Barcode) VALUES (%s, %s)")
            cursor.execute(q, (book_id, barcode))
            print("Successfully added to Book_To_Barcode title = ({}) barcode = ({})".format(title, barcode))
        except mysql.connector.IntegrityError as err:
            print(err ,"in **Book_To_Barcode** Table IGNORED.")
    else: 
        print("Cannot add to Book_To_Barcode with " + 
        "barcode = ({}) title = ({}) book_id = ({}) quantity = ({})".format(barcode, title, book_id, result))

"""
Adds a book into the database.
"""
def add_book(cursor, type_name, barcode, title, first_name, last_name, isbn, language, publication_year):
    if type_name == 'book': 
        add_item_type(cursor, type_name)
        add_item(cursor, barcode, type_name)
        add_book_entry(cursor, barcode, title, isbn, language, publication_year)
        add_author(cursor, first_name, last_name)
        add_authored_by(cursor, first_name, last_name, title)
        add_book_to_barcode(cursor, title, barcode)
    else: 
        print('Cannot add into Book of type = ({})'.format(type_name))