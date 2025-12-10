from models.food import Food

class FoodDataService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_predefined_foods(self):
        foods = [
            # === PROTEINS ===
            Food(
                food_name="Chicken Breast, Grilled",
                calories=165,
                protein_g=31,
                carbs_g=0,
                fats_g=3.6,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Chicken Thigh, Grilled",
                calories=209,
                protein_g=26,
                carbs_g=0,
                fats_g=10.9,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Salmon, Baked",
                calories=206,
                protein_g=22,
                carbs_g=0,
                fats_g=12,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Tuna, Canned in Water",
                calories=116,
                protein_g=26,
                carbs_g=0,
                fats_g=0.8,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Egg, Boiled",
                calories=155,
                protein_g=13,
                carbs_g=1.1,
                fats_g=11,
                serving_size="1",
                serving_unit="large"
            ),
            Food(
                food_name="Egg White",
                calories=52,
                protein_g=11,
                carbs_g=0.7,
                fats_g=0.2,
                serving_size="3",
                serving_unit="large"
            ),
            Food(
                food_name="Ground Beef, 90% Lean",
                calories=176,
                protein_g=20,
                carbs_g=0,
                fats_g=10,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Pork Chop, Grilled",
                calories=231,
                protein_g=25,
                carbs_g=0,
                fats_g=14,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Tofu, Firm",
                calories=76,
                protein_g=8,
                carbs_g=1.9,
                fats_g=4.8,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Greek Yogurt, Plain",
                calories=59,
                protein_g=10,
                carbs_g=3.6,
                fats_g=0.4,
                serving_size="100",
                serving_unit="g"
            ),
            
            # === CARBOHYDRATES ===
            Food(
                food_name="White Rice, Cooked",
                calories=130,
                protein_g=2.7,
                carbs_g=28,
                fats_g=0.3,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Brown Rice, Cooked",
                calories=111,
                protein_g=2.6,
                carbs_g=23,
                fats_g=0.9,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Quinoa, Cooked",
                calories=120,
                protein_g=4.4,
                carbs_g=21,
                fats_g=1.9,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Pasta, Cooked",
                calories=131,
                protein_g=5,
                carbs_g=25,
                fats_g=1.1,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Whole Wheat Bread",
                calories=247,
                protein_g=13,
                carbs_g=41,
                fats_g=3.4,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="White Bread",
                calories=265,
                protein_g=9,
                carbs_g=49,
                fats_g=3.2,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Oatmeal, Cooked",
                calories=71,
                protein_g=2.5,
                carbs_g=12,
                fats_g=1.5,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Sweet Potato, Baked",
                calories=90,
                protein_g=2,
                carbs_g=21,
                fats_g=0.2,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Potato, Baked",
                calories=93,
                protein_g=2.5,
                carbs_g=21,
                fats_g=0.1,
                serving_size="100",
                serving_unit="g"
            ),
            
            # === FRUITS ===
            Food(
                food_name="Apple",
                calories=52,
                protein_g=0.3,
                carbs_g=14,
                fats_g=0.2,
                serving_size="1",
                serving_unit="medium"
            ),
            Food(
                food_name="Banana",
                calories=89,
                protein_g=1.1,
                carbs_g=23,
                fats_g=0.3,
                serving_size="1",
                serving_unit="medium"
            ),
            Food(
                food_name="Orange",
                calories=47,
                protein_g=0.9,
                carbs_g=12,
                fats_g=0.1,
                serving_size="1",
                serving_unit="medium"
            ),
            Food(
                food_name="Strawberries",
                calories=32,
                protein_g=0.7,
                carbs_g=7.7,
                fats_g=0.3,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Blueberries",
                calories=57,
                protein_g=0.7,
                carbs_g=14,
                fats_g=0.3,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Mango",
                calories=60,
                protein_g=0.8,
                carbs_g=15,
                fats_g=0.4,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Watermelon",
                calories=30,
                protein_g=0.6,
                carbs_g=7.6,
                fats_g=0.2,
                serving_size="100",
                serving_unit="g"
            ),
            
            # === VEGETABLES ===
            Food(
                food_name="Broccoli, Cooked",
                calories=55,
                protein_g=3.7,
                carbs_g=11,
                fats_g=0.6,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Spinach, Cooked",
                calories=23,
                protein_g=2.9,
                carbs_g=3.6,
                fats_g=0.3,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Carrot, Raw",
                calories=41,
                protein_g=0.9,
                carbs_g=10,
                fats_g=0.2,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Tomato",
                calories=18,
                protein_g=0.9,
                carbs_g=3.9,
                fats_g=0.2,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Bell Pepper",
                calories=20,
                protein_g=0.9,
                carbs_g=4.6,
                fats_g=0.2,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Cucumber",
                calories=16,
                protein_g=0.7,
                carbs_g=3.6,
                fats_g=0.1,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Lettuce",
                calories=15,
                protein_g=1.4,
                carbs_g=2.9,
                fats_g=0.2,
                serving_size="100",
                serving_unit="g"
            ),
            
            # === SNACKS & NUTS ===
            Food(
                food_name="Almonds",
                calories=579,
                protein_g=21,
                carbs_g=22,
                fats_g=50,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Peanuts",
                calories=567,
                protein_g=26,
                carbs_g=16,
                fats_g=49,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Peanut Butter",
                calories=588,
                protein_g=25,
                carbs_g=20,
                fats_g=50,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Walnuts",
                calories=654,
                protein_g=15,
                carbs_g=14,
                fats_g=65,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Cashews",
                calories=553,
                protein_g=18,
                carbs_g=30,
                fats_g=44,
                serving_size="100",
                serving_unit="g"
            ),
            
            # === DAIRY ===
            Food(
                food_name="Whole Milk",
                calories=61,
                protein_g=3.2,
                carbs_g=4.8,
                fats_g=3.3,
                serving_size="100",
                serving_unit="ml"
            ),
            Food(
                food_name="Skim Milk",
                calories=34,
                protein_g=3.4,
                carbs_g=5,
                fats_g=0.1,
                serving_size="100",
                serving_unit="ml"
            ),
            Food(
                food_name="Cheddar Cheese",
                calories=403,
                protein_g=25,
                carbs_g=1.3,
                fats_g=33,
                serving_size="100",
                serving_unit="g"
            ),
            Food(
                food_name="Mozzarella Cheese",
                calories=280,
                protein_g=28,
                carbs_g=3.1,
                fats_g=17,
                serving_size="100",
                serving_unit="g"
            ),
        ]
        
        return foods
    
    def populate_database(self, clear_existing = False):
        if clear_existing:
            self.db_manager.execute_query("DELETE FROM foods")
            print("Cleared existing foods.")

        foods = self.get_predefined_foods()
        count = 0

        print(f"Adding {len(foods)} predefined foods...")

        for food in foods:
            try:
                food.save(self.db_manager)
                count += 1
            except Exception as e:
                print(f"Error adding food {food.food_name}: {e}")

        print(f"Added {count} foods to the database.")
        return count
    
    def check_food_exists(self):
        query = "SELECT COUNT(*) as count FROM foods"
        result = self.db_manager.execute_query(query, fetch = True)
        count = result[0]['count']
        return count > 0