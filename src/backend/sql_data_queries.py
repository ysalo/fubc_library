def get_author_id(cursor, first_name, last_name, middle_name=''):
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
                                #NOT LIKELY SO I'LL DO IT LATER. CAN BE CHECKED DONE BY AUTHOR.
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

def get_books_by_author(cursor, first_name, last_name, middle_name=''):
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
    cursor.execute(q, (first_name, last_name, middle_name))
    result = cursor.fetchall()
    if not result:
        return None
    return result

def get_series_title(cursor, book_title):
    q = ("""
        SELECT 
            S.title
        FROM 
            Book as B 
        LEFT JOIN 
            Series as S 
        ON 
            B.series_id = S.series_id
        WHERE 
            B.title = %s
        """)
    cursor.execute(q, (book_title,))
    return cursor.fetchall()[0][0]

#     select s.title
# from series as s
# left join book as b on s.series_id = b.series_id 
# where b.title = 'Рози Для Мами';


"""
Return a list of tuples containing the book titles from a given genre.
"""
def get_books_by_genre(cursor, genre_title):
    #split the query into two parts
    genre_id = get_genre_id(cursor, genre_title) 
    q = ("""
        SELECT
            B.title
        FROM 
            Book as B
        LEFT JOIN  
            Genre as G ON B.genre_id = G.genre_id
        WHERE 
            G.genre_id = %s
        """)
    cursor.execute(q, (genre_id,))
    result = cursor.fetchall()
    if not result:
        return None
    return result

"""
Returns ('Book Title, ISBN, Language, Publication Year, Author First Name, Author Last Name, Author Middle Name') 
given a barcode, if the barcode exists otherwise returns None.
"""
#TODO: rework so that the authors are returned as a list and not a separate instance multiple times for different authors of the 
#      same book.
def book_from_barcode(cursor, barcode):
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
            Author AS A ON A.author_id = BAB.author_id
        WHERE 
            I.barcode = %s
    """)
    cursor.execute(q, (barcode,))
    result = cursor.fetchall()
    if not result:
        return None
    return result


#TODO: rework so that the list of authors gets printed.
def print_book(t):
    if not t: 
        print("Book does not exit!")
        return 

    l = t[0]
    print(l)
    print("""BOOK INFO\nTitle = {}\nISBN = {}\nLanguage = {}\nPublication Year = {}\nFirst Name = {}\nLast Name = {}\nMiddle Name = {}
            """.format(l[0], l[1], l[2], l[3], l[4], l[5], l[6]))

def get_member_id(cursor, email):
    q = ("""
        SELECT 
            member_id 
        FROM 
            Member
        WHERE 
            email = %s
        """)
    cursor.execute(q, (email, ))
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]

def get_item_status(cursor, barcode):
    q = ("""
        SELECT 
            status 
        FROM 
            Item
        WHERE 
            barcode = %s
        """)
    cursor.execute(q, (barcode, ))
    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]

def get_series_id(cursor, title):
    q = ("""
    SELECT 
        series_id 
    FROM 
        Series
    WHERE 
        title = %s
    """)
    cursor.execute(q, (title, ))
    result = cursor.fetchall()
    if result:
        return result[0][0]
    return None


def get_genre_id(cursor, name):
    q = ("""
    SELECT 
        genre_id 
    FROM 
        Genre
    WHERE 
        name = %s
    """)
    cursor.execute(q, (name, ))
    result = cursor.fetchall()
    if result: 
        return result[0][0]
    return None
    
def get_books_in_series(cursor, series_title):
    series_id = get_series_id(cursor, series_title)
    q = ("""
    SELECT 
        title, in_series_number 
    FROM 
        Book
    WHERE 
        series_id = %s
    """)
    cursor.execute(q, (series_id, ))
    result = cursor.fetchall()
    if result: 
        return result
    return None
    

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

# """
# Returns if a specific book is in a series.
# """
# def is_in_series(cursor, book_title):
#     q =("""
#         SELECT 
#             series_id 
#         FROM 
#             Book
#         WHERE 
#             title = %s
#         """)
#     cursor.execute(q, (book_title, ))
#     result = cursor.fetchall()[0][0]
#     return False if result is None else True  
