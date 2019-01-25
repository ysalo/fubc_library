from sql_data_queries import * 
def delete_item_type(cursor, type_name):
    query = "DELETE FROM Item_Type WHERE type_name = %s"
    cursor.execute(query, [type_name])

def delete_item(cursor , barcode):
    query = "DELETE FROM Item WHERE barcode = %s"
    cursor.execute(query, [barcode])

def delete_author(cursor, first_name, last_name):
    a_id = get_author_id(cursor, first_name, last_name)
    query = "DELETE FROM Authors WHERE author_id = %s"
    cursor.execute(query, (a_id,))

def delete_bible(cursor, language, translation): 
    q = ("DELETE FROM Bible WHERE language = %s AND translation = %s") 
    cursor.execute(q, (language, translation))