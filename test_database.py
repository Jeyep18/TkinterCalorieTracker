# TEST TEST TEST TEST TEST
from database.db_manager import DBManager

db = DBManager()
if db.connect():
    print("Test database connection successful.")

    if db.initialize_database():
        print("may database kana boss.")
    
    result = db.execute_query("SHOW TABLES;", fetch = True)
    print("Tables: ", result)

    db.close()