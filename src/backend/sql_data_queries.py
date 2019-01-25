def get_author_id(cursor, first_name, last_name):
    q = ("SELECT author_id FROM Authors WHERE first_name = %s And last_name = %s")
    cursor.execute(q, (first_name, last_name))
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]

def get_item_type_id(cursor, type_name):
    q = ("SELECT type_id FROM Item_Type WHERE type_name = %s")
    cursor.execute(q, (type_name,))
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]
"""
Returns the book_id if found. 
Otherwise returns None used for checking. 
"""
def get_book_id(cursor, title):
    q =("SELECT book_id FROM Books WHERE title= %s")
    cursor.execute(q, (title, ))
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]

def get_book_quantity(cursor, title):
    book_id = get_book_id(cursor, title)
    if not book_id:
        return 0
    q =     """
            SELECT 
                COUNT(*)
            FROM 
                (SELECT book_to_barcode.Book_Id, Barcode 
                FROM Books LEFT JOIN Book_To_Barcode 
                ON Books.book_id = book_to_barcode.Book_Id) as TJ 
            WHERE 
                TJ.book_id = %s
            """
    cursor.execute(q, (book_id,))
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]

def get_books_by_author(cursor, first_name, last_name):
    author_id = get_author_id(cursor, first_name, last_name)
    if not author_id:
        return []
    q =     """
            SELECT
                b.title
            FROM 
                books as b
            JOIN 
                book_authored_by as bab ON b.book_id = bab.book_id
            JOIN 
                authors as a ON a.author_id = bab.author_id
            WHERE 
                a.first_name = %s and a.last_name = %s
            """
    cursor.execute(q, (first_name, last_name))
    result = cursor.fetchall()
    if not result:
        return None
    return result

def db_get_book_info_by_barcode(cursor, barcode):
    q =     """
            SELECT 
                b.title, b.isbn, b.language, b.publication_year, a.first_name, a.last_name
            FROM 
                item AS i
            LEFT JOIN
                book_to_barcode AS btb ON i.barcode = btb.barcode
            LEFT JOIN
                books AS b on btb.book_id = b.book_id
            LEFT JOIN
                book_authored_by AS bab ON bab.title = b.title
            LEFT JOIN 
                authors AS a ON a.author_id = bab.author_id
            WHERE 
                i.barcode = %s
            """
    cursor.execute(q, (barcode,))
    result = cursor.fetchall()
    if not result:
        return None
    return result
    
def get_bible_quantity(cursor, language, translation):
    q = """
        SELECT quantity 
        FROM Bible 
        WHERE language = %s AND translation = %s
        """
    cursor.execute(q, (language, translation))
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]

def split_author_name(author): #TODO: find a better way to do this
    name = author.split(' ')
    if len(name) == 2:
        return name[0], name[1]
    return name[0], name[2]