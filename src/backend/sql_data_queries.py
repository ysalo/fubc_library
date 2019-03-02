def get_author_id(cursor, first_name, last_name, middle_name=None):
    #TODO: Check the <=> 'null safe' operator.
    q = ("""
        SELECT 
            author_id 
        FROM 
            Author 
        WHERE 
            first_name = %s And last_name = %s And middle_name <=> %s 
        """)
    cursor.execute(q, (first_name, last_name, middle_name))
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]

def get_item_type_id(cursor, type_name):
    q = ("""
        SELECT 
            type_id 
        FROM 
            Item_Type 
        WHERE 
            type_name = %s
        """)
    cursor.execute(q, (type_name,))
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]

"""
Returns the book_id if found. 
Otherwise returns None used for checking. 
"""
def get_book_id(cursor, title): #TODO: NEEDS TO BE FIXED BECAUSE BOOKS CAN HAVE DUPLICATE TITLES.
                                #NOT LIKELY SO I'LL DO IT LATER. CAN BE DONE BY AUTHOR.
    q =("""
        SELECT 
            book_id 
        FROM 
            Book
        WHERE 
            title = %s
        """)
    cursor.execute(q, (title, ))
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]

def get_book_quantity(cursor, title):
    book_id = get_book_id(cursor, title)
    if not book_id:
        return 0
    q = ("""
        SELECT 
            COUNT(*)
        FROM 
            (SELECT 
                Book_To_Barcode.book_Id, Barcode 
            FROM 
                Book LEFT JOIN Book_To_Barcode 
            ON 
                Book.book_id = Book_To_Barcode.book_Id
            ) AS BB  
        WHERE 
            BB.book_id = %s
        """)
    cursor.execute(q, (book_id,))
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]

def get_books_by_author(cursor, first_name, last_name, middle_name=None):
    author_id = get_author_id(cursor, first_name, last_name, middle_name)
    if not author_id:
        return []
    #TODO: don't think it will work with NULL names
    q = ("""
        SELECT
            B.title
        FROM 
            Book as B
        JOIN 
            Book_Authored_By as BAB ON B.book_id = BAB.book_id
        JOIN 
            Author AS A ON A.author_id = BAB.author_id
        WHERE 
            A.first_name = %s and A.last_name = %s and A.middle_name <=> %s
        """)
    cursor.execute(q, (first_name, last_name))
    result = cursor.fetchall()
    if not result:
        return None
    return result

def db_get_book_info_by_barcode(cursor, barcode):
    q = ("""
    SELECT 
        B.title, B.isbn, B.language, B.publication_year, A.first_name, A.last_name, A.middle_name
    FROM 
        Item AS I
    LEFT JOIN
        Book_To_Barcode AS BTB ON I.barcode = BTB.barcode
    LEFT JOIN
        Book AS B on BTB.book_id = B.book_id
    LEFT JOIN
        Book_Authored_By AS BAB ON BAB.book_id = B.book_id
    LEFT JOIN 
        Authors AS A ON A.author_id = BAB.author_id
    WHERE 
        I.barcode = %s
    """)
    cursor.execute(q, (barcode,))
    result = cursor.fetchall()
    if not result:
        return None
    return result

# def split_author_name(author): 
#     name = author.split(' ')
#     if len(name) == 2:
#         return name[0], name[1]
#     return name[0], name[2]

#def get_bible_id(cursor, language, translation, size, condition):
#     q = ("""
#         Select 
#             Bible_Id
#         From 
#             Bible 
#         WHERE 
#             language = %s AND translation = %s AND size = %s AND condition = %s
#         """)
#     cursor.execute(q, (language, translation, size, condition))
#     result = cursor.fetchall()
#     if not result:
#         return None 
#     return result[0][0]

# def get_bible_quantity(cursor, bible_id):
#     q = """
#         SELECT quantity 
#         FROM Bible 
#         WHERE Bible_Id = %s
#         """
#     cursor.execute(q, (bible_id))
#     result = cursor.fetchall()
#     if not result:
#         return None
#     return result[0][0]
#