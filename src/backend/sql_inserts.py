import mysql.connector
from sql_data_queries import *
from mysql.connector import errorcode

"""
Add new item type, ignores the request if the type already exists.
"""
def add_item_type(cursor, type_name):
    try:
        q = ("""
        INSERT INTO Item_Type(Type_Name) VALUES (%s)
        """)
        cursor.execute(q, (type_name, ))
        print("Successfully added to Item_Type Table type_name = ({})".format(type_name))
    except mysql.connector.IntegrityError as err:
        print(err ,"in **Item_Type** Table, IGNORED.")

"""
Add an Item if the type_id is found 
Ignores the request otherwise.
DB Trigger sets the status of an item to 1 (available).
"""
def add_item(cursor, barcode, type_name):
    type_id = get_item_type_id(cursor, type_name)   
    if type_id:
        try:
            q = ("""
            INSERT INTO Item(barcode, type_id) VALUES (%s, %s)
            """)
            cursor.execute(q, (barcode, type_id)) 
            print("Successfully added to Item Table barcode = ({}) type_name = ({})".format(barcode, type_name))
        except mysql.connector.IntegrityError as err:
            print(err ,"in **Item** Table IGNORED.")
    else: 
        print('Cannot add Item barcode = ({}) because type_name = ({}) does not exist.'.format(barcode, type_name))

"""
Add new author, ignores the request if the author already exists.
""" 
def add_author(cursor, first_name, last_name, middle_name=None):
    try:
        q = ("""
        INSERT INTO Author(first_name, last_name, middle_name) VALUES (%s, %s, %s)
        """)
        cursor.execute(q, (first_name, last_name, middle_name))
        print("""Successfully added to Authors Table fist_name = ({}) last_name = ({}) middle_name = ({})"""
            .format(first_name, last_name, middle_name))
    except mysql.connector.IntegrityError as err:
        print(err ,"in **Authors** Table IGNORED.")

"""
Adds a book entry if the barcode is found and if the title does not exist, 
ignore the request otherwise.
"""
def add_book_entry(cursor, barcode, title, language, publication_year, genre_name, isbn=None, series_title=None, in_series_number=None):
    q = ("""
        SELECT 
            COUNT(*) 
        FROM 
            Item 
        WHERE 
            barcode = %s
        """)
    cursor.execute(q, (barcode,))
    result = cursor.fetchall()[0][0]
    genre_id = get_genre_id(cursor, genre_name)
    series_id = get_series_id(cursor, series_title)
    if result == 1:
        try:
            q = ("""
                INSERT INTO Book (genre_id, series_id, title, isbn, language, publication_year, in_series_number) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """)
            cursor.execute(q, (genre_id, series_id, title, isbn, language, publication_year, in_series_number)) 
            print("Successfully added to Books title = ({})".format(title))
        except mysql.connector.IntegrityError as err:
            print(err ,"in **Books** Table IGNORED.")
    elif result > 1:
        print("Duplicate barcode in Item Table. This is not a thing that should happen!") 
    else:    
        print("Cannot add into Book title = ({}) because barcode = ({}) does not exist in the Item Table".format(title,barcode))

"""
Connects the author to the book only if both the author and book already exist, 
ignores the request otherwise.
"""
def add_authored_by(cursor, first_name, last_name, title, middle_name=None): 
    author_id = get_author_id(cursor, first_name, last_name, middle_name)
    book_id = get_book_id(cursor, title)
    if author_id and book_id:
        try: #TODO: add handling code for duplicate and non existant entries
            q = ("""
                INSERT INTO Book_Authored_By (author_id, book_id) VALUES (%s, %s)
                """)
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
def add_book_to_barcode(cursor, title, barcode): #TODO: THIS SHOULD BE DONE WITH THE book_id
    book_id = get_book_id(cursor, title)
    q = ("""
            SELECT 
                COUNT(*) 
            FROM 
                Item 
            WHERE 
                barcode = %s
        """)
    cursor.execute(q, (barcode,))
    result = cursor.fetchall()[0][0]
    if result == 1 and book_id:   
        try:
            q = ("INSERT INTO Book_To_Barcode (Book_Id, Barcode) VALUES (%s, %s)")
            cursor.execute(q, (book_id, barcode))
            print("Successfully added to Book_To_Barcode title = ({}) barcode = ({})".format(title, barcode))
        except mysql.connector.IntegrityError as err:
            print(err ,"in **Book_To_Barcode** Table IGNORED.")
    elif result > 1:
        print("Duplicate barcode found. This is not a thing that should happen!") 
    else: 
        print("Cannot add to Book_To_Barcode with " + 
        "barcode = ({}) title = ({}) book_id = ({}) quantity = ({})".format(barcode, title, book_id, result))

"""
Adds a book into the database.
"""
def add_book(cursor, type_name, barcode, title, first_name, last_name, language, publication_year,
 genre_name, middle_name=None, isbn=None, series_title=None, in_series_number=None):
    if type_name == 'book': 
        add_item_type(cursor, type_name)
        add_item(cursor, barcode, type_name)
        add_genre(cursor, genre_name)
        if series_title is not None: 
            add_series(cursor, series_title)
        #TODO: FIX THIS MESS 
        #Done to ensure that (author + book_title) is unique.
        if not get_author_id(cursor, first_name, last_name, middle_name) or not get_book_id(cursor, title):
            add_book_entry(cursor, barcode, title, language, publication_year, genre_name, isbn, series_title, in_series_number)
        else: 
            print("Duplicate add for title = ({}) and author = {} {} {}".format(title, first_name, last_name, middle_name ))
        add_author(cursor, first_name, last_name, middle_name)
        add_authored_by(cursor, first_name, last_name, title, middle_name)
        add_book_to_barcode(cursor, title, barcode)
    else: 
        print('Cannot add into Book of type = ({})'.format(type_name))

def add_member(cursor, first_name, last_name, email, middle_name=None , phone_number=None):
    try:
        q = ("""
        INSERT INTO Member(first_name, last_name, email, middle_name, phone_number) VALUES (%s, %s, %s, %s, %s)
        """)
        cursor.execute(q, (first_name, last_name, email, middle_name, phone_number))
        print("Successfully added to Member Table email = ({}) phone = ({}) first_name = ({}) last_name = ({}) middle_name = ({})"
        .format(email, phone_number, first_name, last_name, middle_name))
    except mysql.connector.IntegrityError as err:
        print(err ,"in **Member** Table, IGNORED.")


def add_loan(cursor, barcode, email):
    member_id = get_member_id(cursor, email)
    item_status = get_item_status(cursor, barcode)
    if member_id and item_status:
        try:
            q = ("""
            INSERT INTO Loan(barcode, member_id) VALUES (%s, %s)
            """)
            cursor.execute(q, (barcode, member_id))
            print("Successfully added to Loan Table barcode = ({}) email = ({})"
            .format(barcode, email  ))
        except mysql.connector.IntegrityError as err:
            print(err ,"in **Loan** Table, IGNORED.") 
    else: 
        print("Cannot add loan for email =({}) barcode = ({})".format(email, barcode)) 

"""
Add new genre, ignores the request if the genre already exists.
""" 
def add_genre(cursor, genre_name):
    try:
        q = ("""
        INSERT INTO Genre(name) VALUES (%s)
        """)
        cursor.execute(q, (genre_name,))
        print("""Successfully added to Genre Table genre_name = ({})"""
            .format(genre_name))
    except mysql.connector.IntegrityError as err:
        print(err ,"in **Genre** Table IGNORED.")

"""
Add new series, ignores the request if the series already exists.
""" 
def add_series(cursor, title):
    try:
        q = ("""
        INSERT INTO Series(title) VALUES (%s)
        """)
        cursor.execute(q, (title,))
        print("""Successfully added to Series Table title = ({})"""
            .format(title))
    except mysql.connector.IntegrityError as err:
        print(err ,"in **Series** Table IGNORED.")

# """
# Creates a new data entry if the bible does not exist, 
# Otherwise modifies the existing quantity by the quatity passed in.
# """
# def add_bible(cursor, language, translation, size, condition, quantity):
#     bible_id = get_bible_id(cursor, language, translation, size, condition)
#     if bible_id == None:
#         q = ("INSERT INTO Bible" 
#         "(language, translation, size, condition, quantity) VALUES (%s, %s, %s, %s, %s)")
#     old_qun = get_bible_quantity(cursor, bible_id) #accessing the same thing twice here
#     test_qun = old_qun + quantity
#     if test_qun < 0: 
#         print('Update Rejected! Update will result in negative bible quantity for ' 
#         '(language = {}, translation = {}, quantity = {}). '.format(language, translation, test_qun)) 
#         return
#     q = ("UPDATE Bible SET quantity = quantity + %s WHERE bible_id = %s")
#     cursor.execute(q, (bible_id,))