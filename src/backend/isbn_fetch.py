from isbnlib import notisbn, get_canonical_isbn, is_isbn10, to_isbn13, meta
import requests

def get_isbn_info(user_input):

    if notisbn(user_input):
        print('Invalid ISBN')
    can_isbn = get_canonical_isbn(user_input)
    if(is_isbn10(can_isbn)):
        print('IS ISBN 10')
        can_isbn = to_isbn13(can_isbn)
        print('This is the isbn 13 version: ', can_isbn)
    book_info = meta(user_input)
    if book_info is None:
        print('Unknown ISBN')
    return (can_isbn, book_info)
    
#     title = book_info.get('Title')
#     authors = book_info.get('Authors')
#     publisher = book_info.get('Publisher')
#     year = book_info.get('Year')
#     language = book_info.get('Language')

#     print('\nTitle: {}\nAuthors: {}\nPublisher: {}\nYear: {}\nLanguage: {}\n'
#     .format(title, authors, publisher, year, language)) 