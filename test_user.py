# TEST TEST TEST TEST TEST

from models.user import User
from services.calorie_calculator import CalorieCalculator
from database.db_manager import DBManager

db = DBManager()
db.connect()

goal = CalorieCalculator.calculate_daily_goal(
    weight_kg = 75,
    height_cm = 175,
    age = 25,
    gender = 'male',
    activity_level = 'moderate',
    goal = 'lose_weight'
)
print(f"Calculated goal: {goal} calories")

user = User(
    user_name="Sir Kurt",
    age=25,
    gender="male",
    weight_kg=75,
    height_cm=175,
    activity_level="moderate",
    goal="lose_weight",
    daily_calorie_goal=goal
)

user_id = user.save(db)
print(f"Created user with ID: {user_id}")

loaded_user = User.get_by_id(user_id, db)
print(f"Loaded user: {loaded_user.user_name}")

db.close()