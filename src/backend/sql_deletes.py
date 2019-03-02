from sql_data_queries import * 
def delete_item_type(cursor, type_name):
    q = "DELETE FROM Item_Type WHERE type_name = %s"
    cursor.execute(q, (type_name,))

def delete_item(cursor , barcode):
    q = "DELETE FROM Item WHERE barcode = %s"
    cursor.execute(q, (barcode,))

def delete_author(cursor, first_name, last_name, middle_name=None):
    a_id = get_author_id(cursor, first_name, last_name, middle_name)
    q = "DELETE FROM Authors WHERE author_id = %s"
    cursor.execute(q, (a_id,))

# def delete_bible(cursor, language, translation): 
#     q = ("DELETE FROM Bible WHERE language = %s AND translation = %s") 
#     cursor.execute(q, (language, translation))