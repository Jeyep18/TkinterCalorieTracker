from datetime import datetime, date, time as dt_time

class FoodLog:
    def __init__(self, log_id = None, user_id = None, food_id = None, servings = 1.0, total_calories = 0, meal_type = 'snack', log_date = None, log_time = None): 
        self.log_id = log_id
        self.user_id = user_id
        self.food_id = food_id
        self.servings = servings
        self.total_calories = total_calories
        self.meal_type = meal_type
        self.log_date = log_date or date.today()
        self.log_time = log_time or datetime.now().time()

    def to_dict(self):
        return {
            'log_id': self.log_id,
            'user_id': self.user_id,
            'food_id': self.food_id,
            'servings': self.servings,
            'total_calories': self.total_calories,
            'meal_type': self.meal_type,
            'log_date': self.log_date,
            'log_time': self.log_time
        }
    
    @staticmethod
    def from_dict(data):
        return FoodLog(
            log_id=data.get('log_id'),
            user_id=data.get('user_id'),
            food_id=data.get('food_id'),
            servings=data.get('servings', 1.0),
            total_calories=data.get('total_calories', 0),
            meal_type=data.get('meal_type', 'snack'),
            log_date=data.get('log_date'),
            log_time=data.get('log_time')
        )
    
    def save(self, db_manager):
        query = """
            INSERT INTO food_logs 
            (user_id, food_id, servings, total_calories, 
             meal_type, log_date, log_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            self.user_id, self.food_id, self.servings,
            self.total_calories, self.meal_type,
            self.log_date, self.log_time
        )
        self.log_id = db_manager.execute_query(query, params)
        
        self._update_daily_logs(db_manager)
        
        return self.log_id
    
    def _update_daily_logs(self, db_manager):
        #auto call after save()

        from models.user import User
        user = User.get_by_id(self.user_id, db_manager)

        if not user:
            return
        
        total_query = """
            SELECT SUM(total_calories) as daily_total
            FROM food_logs
            WHERE user_id = %s AND log_date = %s
        """

        result = db_manager.execute_query(total_query, (self.user_id, self.log_date), fetch = True)

        daily_total = result[0]['daily_total'] or 0
        remaining = user.daily_calorie_goal - daily_total

        check_query = """
            SELECT log_id FROM daily_logs
            WHERE user_id = %s AND log_date = %s
        """

        existing = db_manager.execute_query(check_query, (self.user_id, self.log_date), fetch = True)

        if existing:
            update_query = """
                UPDATE daily_logs
                SET total_calories = %s,
                    remaining_calories = %s
                WHERE user_id = %s AND log_date = %s
            """
            db_manager.execute_query(update_query, (daily_total, remaining, self.user_id, self.log_date))

        else:
            insert_query = """
                INSERT INTO daily_logs
                (user_id, log_date, total_calories, 
                 calorie_goal, remaining_calories)
                VALUES (%s, %s, %s, %s, %s)
            """
            db_manager.execute_query(insert_query, (self.user_id, self.log_date, daily_total, user.daily_calorie_goal, remaining))

    @staticmethod
    def get_by_user_and_date(user_id, log_date, db_manager):
        query = """
            SELECT 
                fl.*,
                f.food_name,
                f.calories as food_calories,
                f.serving_size,
                f.serving_unit
            FROM food_logs fl
            JOIN foods f ON fl.food_id = f.food_id
            WHERE fl.user_id = %s AND fl.log_date = %s
            ORDER BY fl.log_time DESC
        """
        results = db_manager.execute_query(query, (user_id, log_date), fetch = True)

        logs = []
        for row in results:
            log = FoodLog.from_dict(row)
            log.food_name = row['food_name']
            log.food_calories = row['food_calories']
            log.serving_size = row['serving_size']
            log.serving_unit = row['serving_unit']
            logs.append(log)

        return logs
    
    @staticmethod
    def delete(log_id, db_manager):
        log_query = "SELECT * FROM food_logs WHERE log_id = %s"
        result = db_manager.execute_query(log_query, (log_id,), fetch=True)

        if not result:
            return False
        
        log_data = result[0]

        delete_query = "DELETE FROM food_logs WHERE log_id = %s"
        db_manager.execute_query(delete_query, (log_id,))

        log = FoodLog.from_dict(log_data)
        log._update_daily_logs(db_manager)

        return True
    
    @staticmethod
    def get_daily_logs(user_id, log_date, db_manager):
        query = """
            SELECT * FROM daily_logs
            WHERE user_id = %s AND log_date = %s
        """
        result = db_manager.execute_query(query, (user_id, log_date), fetch = True)

        if result:
            return result[0]
        
        from models.user import User
        user = User.get_by_id(user_id, db_manager)

        return {
            'total_calories': 0,
            'calorie_goal': user.daily_calorie_goal if user else 0,
            'remaining_calories': user.daily_calorie_goal if user else 0
        }
    
    @staticmethod
    def get_daily_total(user_id, log_date, db_manager):
        query = """
            SELECT COALESCE(SUM(total_calories), 0) as total
            FROM food_logs
            WHERE user_id = %s AND log_date = %s
        """
        result = db_manager.execute_query(
            query, (user_id, log_date), fetch=True
        )
        return float(result[0]['total'])