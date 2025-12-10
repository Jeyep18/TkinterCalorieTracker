from datetime import datetime, date, timedelta
from models.food_log import FoodLog

class DailyResetService:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def get_or_create_daily_log(self, user_id, target_date = None):
        if target_date is None:
            target_date = date.today()
        
        query = """
            SELECT * FROM daily_logs
            WHERE user_id = %s AND log_date = %s
        """
        result = self.db_manager.execute_query(query, (user_id, target_date), fetch = True)

        if result:
            return result[0]
        
        user_query = "SELECT daily_calorie_goal FROM users WHERE user_id = %s"
        user_result = self.db.execute_query(user_query, (user_id,), fetch=True)

        if not user_result:
            raise Exception(f"USER {user_id} NOT FOUND")
        
        calorie_goal = user_result[0]['daily_calorie_goal']

        insert_query = """
            INSERT INTO daily_logs 
            (user_id, log_date, total_calories, calorie_goal, remaining_calories)
            VALUES (%s, %s, 0, %s, %s)
        """

        self.db_manager.execute_query(insert_query, (user_id, target_date, calorie_goal, calorie_goal))

        result = self.db_manager.execute_query(query, (user_id, target_date), fetch = True)

        return result[0]
    
    def update_daily_logs(self, user_id, target_date = None):
        # call after adding or deleting food logs fsagjkansga
        if target_date is None:
            target_date = date.today()

            logs = self.get_or_create_daily_log(user_id, target_date)

            total_calories = FoodLog.get_daily_total(user_id, target_date, self.db_manager)

            remaining = logs['calorie_goal'] - total_calories

            update_query = """
                UPDATE daily_logs
                SET total_calories = %s, remaining_calories = %s
                WHERE user_id = %s AND log_date = %s
            """
            self.db.execute_query(
                update_query,
                (total_calories, remaining, user_id, target_date)
            )

            query = """
                SELECT * FROM daily_logs
                WHERE user_id = %s AND log_date = %s
            """
            result = self.db.execute_query(
                query, (user_id, target_date), fetch=True
            )
            return result[0]
        
    def check_today_log_exists(self, user_id):
        today = date.today()

        query = """
            SELECT summary_id FROM daily_logs
            WHERE user_id = %s AND log_date = %s
        """
        result = self.db.execute_query(query, (user_id, today), fetch=True)

        if not result:
            self.get_or_create_daily_log(user_id, today)
            return True
        
        return False
    
    def get_log_stats(self, user_id, days = 7):
        start_date = date.today() - timedelta(days=days-1)
        
        query = """
            SELECT * FROM daily_logs
            WHERE user_id = %s AND log_date >= %s
            ORDER BY log_date DESC
        """
        results = self.db.execute_query(query, (user_id, start_date), fetch=True)
        return results


