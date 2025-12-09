class CalorieCalculator:
    ACTIVITY_MULTIPLIERS = {
        'sedentary' : 1.2,
        'light' : 1.375,
        'moderate' : 1.55,
        'active' : 1.725,
        'very_active' : 1.9
    }

    GOAL_ADJUSTMENTS = {
        'lose_weight' : -500,
        'maintain_weight' : 0,
        'gain_weight' : 500,
    }

    @staticmethod
    def calculate_bmr(weight_kg, height_cm, age, gender):
        # Men:   BMR = (10 × weight) + (6.25 × height) - (5 × age) + 5
        # Women: BMR = (10 × weight) + (6.25 × height) - (5 × age) - 161
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)

        if gender.lower() == 'male':
            bmr += 5
        else:
            bmr -= 161
        return round(bmr,2)
    
    @staticmethod
    def calculate_tdee(bmr, activity_level):
        multiplier = CalorieCalculator.ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)
        tdee = bmr * multiplier
        return round(tdee,2)
    
    @staticmethod
    def calculate_daily_goal(weight_kg, height_cm, age, gender, activity_level, goal):
        bmr = CalorieCalculator.calculate_bmr(weight_kg, height_cm, age, gender)
        tdee = CalorieCalculator.calculate_tdee(bmr, activity_level)

        adjustment =  CalorieCalculator.GOAL_ADJUSTMENTS.get(goal, 0)
        daily_goal = tdee + adjustment

        min_calories = 1200 if gender.lower() == 'female' else 1500
        daily_goal = max(daily_goal, min_calories)

        return int(daily_goal)
    
    @staticmethod
    def get_activity_description(activity_level):
        descriptions = {
            'sedentary': 'Little or no exercise',
            'light': 'Light exercise/sports 1-3 days/week',
            'moderate': 'Moderate exercise/sports 3-5 days/week',
            'active': 'Hard exercise/sports 6-7 days a week',
            'very_active': 'Very hard exercise/sports & physical job or 2x training'
        }
        return descriptions.get(activity_level, 'Unknown')
    
    @staticmethod
    def get_goal_description(goal):
        descriptions = {
            'lose_weight': 'Lose Weight (0.5 kg/week)',
            'maintain_weight': 'Maintain Weight',
            'gain_weight': 'Gain Weight (0.5 kg/week)'
        }
        return descriptions.get(goal, 'Unknown')