class Food:
    def __init__(self, food_id = None, food_name = None, calories = None, protein_g = 0, carbs_g = 0, fats_g = 0, serving_size = None, serving_unit = None, created_by = None):
        self.food_id = food_id
        self.food_name = food_name
        self.calories = calories
        self.protein_g = protein_g
        self.carbs_g = carbs_g
        self.fats_g = fats_g
        self.serving_size = serving_size
        self.serving_unit = serving_unit
        self.created_by = created_by

    def to_dict(self):
        return {
            'food_id': self.food_id,
            'food_name': self.food_name,
            'calories': self.calories,
            'protein_g': self.protein_g,
            'carbs_g': self.carbs_g,
            'fats_g': self.fats_g,
            'serving_size': self.serving_size,
            'serving_unit': self.serving_unit,
            'created_by': self.created_by
        }
    
    @staticmethod
    def from_dict(data):
        return Food(
            food_id=data.get('food_id'),
            food_name=data.get('food_name'),
            calories=data.get('calories'),
            protein_g=data.get('protein_g', 0),
            carbs_g=data.get('carbs_g', 0),
            fats_g=data.get('fats_g', 0),
            serving_size=data.get('serving_size'),
            serving_unit=data.get('serving_unit'),
            created_by=data.get('created_by')
        )
    
    def save(self, db_manager):
        query = """
            INSERT INTO foods (food_name, calories, protein_g, carbs_g, fats_g,
            serving_size, serving_unit, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (self.food_name, self.calories, self.protein_g, self.carbs_g, self.fats_g, self.serving_size, self.serving_unit, self.created_by)
        self.food_id = db_manager.execute_query(query, params)
        return self.food_id
    
    @staticmethod
    def search(keyword, db_manager, limit=20):
        query = """
            SELECT * FROM foods 
            WHERE food_name LIKE %s 
            ORDER BY food_name
            LIMIT %s
        """
        results = db_manager.execute_query(
            query, (f'%{keyword}%', limit), fetch=True
        )
        return [Food.from_dict(row) for row in results]
    
    @staticmethod
    def get_by_id(food_id, db_manager):
        query = "SELECT * FROM foods WHERE food_id = %s"
        result = db_manager.execute_query(query, (food_id,), fetch=True)
        if result:
            return Food.from_dict(result[0])
        return None
    
    @staticmethod
    def get_all(db_manager, limit=100):
        """Retrieve all foods from database."""
        query = """
            SELECT * FROM foods 
            ORDER BY food_name
            LIMIT %s
        """
        results = db_manager.execute_query(query, (limit,), fetch=True)
        return [Food.from_dict(row) for row in results]