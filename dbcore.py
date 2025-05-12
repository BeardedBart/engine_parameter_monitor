#NOTE additional file to help flask 
# working with subprograms
import sqlite3


def make_db(cursor):
    #func for checking if db called engparamdb exists
    temp = "engpdb" #Engine Parameters Database
    table_check = cursor.execute(f"""
                                 SELECT name FROM sqlite_master 
                                 WHERE type='table' AND name='{temp}';
                                 """).fetchall()
    if table_check == []:
        cursor.execute(f"""
                       CREATE TABLE {temp} (
                           eng_name char(32),
                           typ char(32),
                           TOil REAL,
                           egt REAL,
                           cht REAL);
                       """)
    else:
        return 0
    
    
if __name__ == '__main__':
    try: 
        connection = sqlite3.connect('engparamdb.db')
        cursor = connection.cursor()
        # make_db(cursor)
        # cursor.execute(f"""
        #                INSERT INTO engpdb VALUES
        #                ('rotax912','petrol', '110', '240', '900')
        #                """)
        # cursor.execute(f"""
        #                INSERT INTO engpdb VALUES
        #                ('izh62','petrol', '130', '250', '1000')
        #                """)
        # cursor.execute(f"""
        #                INSERT INTO engpdb VALUES
        #                ('IO540','petrol', '120', '260', '950')
        #                """)
        # print("DB Crated, data added")
        # connection.commit()
        data = cursor.execute("""SELECT * FROM engpdb""").fetchall()
        print(data)
        
        
    except sqlite3.Error as error:
        print('Error occurred - ', error)


    finally:
        if connection:
            connection.close()
            print(" ")
            print('SQLite Connection closed')
