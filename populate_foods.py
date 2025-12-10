from database.db_manager import DBManager
from services.food_data_service import FoodDataService

db = DBManager()
db.connect()
db.initialize_database()

food_service = FoodDataService(db)

if food_service.check_food_exists():
    print("Foods already exist in database.")
    response = input("Do you want to clear and repopulate? (yes/no): ")
    if response.lower() == 'yes':
        food_service.populate_database(clear_existing=True)
else:
    food_service.populate_database()

db.close()
print("\nDone! You can now run the application.")