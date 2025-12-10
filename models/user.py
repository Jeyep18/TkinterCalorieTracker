class User:
    def __init__(self, user_id = None, user_name = None, age = None, gender = None, weight_kg = None, height_cm = None, activity_level = None, goal = None, daily_calorie_goal = None):
        self.user_id = user_id
        self.user_name = user_name
        self.age = age
        self.gender = gender
        self.weight_kg = weight_kg
        self.height_cm = height_cm
        self.activity_level = activity_level
        self.goal = goal
        self.daily_calorie_goal = daily_calorie_goal
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'age': self.age,
            'gender': self.gender,
            'weight_kg': self.weight_kg,
            'height_cm': self.height_cm,
            'activity_level': self.activity_level,
            'goal': self.goal,
            'daily_calorie_goal': self.daily_calorie_goal
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            user_id = data.get('user_id'),
            user_name = data.get('user_name'),
            age=data.get('age'),
            gender=data.get('gender'),
            weight_kg=data.get('weight_kg'),
            height_cm=data.get('height_cm'),
            activity_level=data.get('activity_level'),
            goal=data.get('goal'),
            daily_calorie_goal=data.get('daily_calorie_goal')
        )
    
    def save(self, db_manager):
        if self.user_id:
            # update ts
            query = """
                UPDATE users 
                SET user_name=%s, age=%s, gender=%s, weight_kg=%s, 
                    height_cm=%s, activity_level=%s, goal=%s, 
                    daily_calorie_goal=%s
                WHERE user_id=%s
            """
            params = (
                self.user_name, self.age, self.gender, self.weight_kg,
                self.height_cm, self.activity_level, self.goal,
                self.daily_calorie_goal, self.user_id
            )
            db_manager.execute_query(query, params)
            return self.user_id
        else:
            #bago ni
            query = """
                INSERT INTO users 
                (user_name, age, gender, weight_kg, height_cm, 
                 activity_level, goal, daily_calorie_goal)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                self.user_name, self.age, self.gender, self.weight_kg,
                self.height_cm, self.activity_level, self.goal,
                self.daily_calorie_goal
            )
            # execute_query returns last inserted ID
            self.user_id = db_manager.execute_query(query, params)
            return self.user_id
        
    @staticmethod
    def get_by_id(user_id, db_manager):
        query = "SELECT * FROM users WHERE user_id=%s"
        result = db_manager.execute_query(query, (user_id,), fetch = True)

        if result:
            return User.from_dict(result[0])
        return None
    
    @staticmethod
    def get_all(db_manager):
        query = "SELECT * FROM users"
        results = db_manager.execute_query(query, fetch = True)
        return [User.from_dict(row) for row in results]
    
    def __str__(self):
        return f"User: {self.user_name} ({self.age} years old)"