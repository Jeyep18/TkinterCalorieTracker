import customtkinter as ctk
from models.user import User
from services.calorie_calculator import CalorieCalculator
from tkinter import messagebox

class ProfileSetupScreen(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_complete = None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.on_complete = on_complete

        self.grid_columnconfigure(0, weight = 1)
        self.create_widgets()

    def create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text = "Set Up Your Profile",
            font = ctk.CTkFont(size = 28, weight = "bold")
        )
        title.pack(pady = (40, 30))

        subtitle = ctk.CTkLabel(
            self,
            text = "Tell us about yourself to calculate your daily calorie goal",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 40))

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(padx=100, pady=20, fill="both", expand=True)

        self.create_form_field(form_frame, "Full Name:", "name_entry", row=0)

        self.create_form_field(form_frame, "Age (years):", "age_entry", row=1)

        ctk.CTkLabel(
            form_frame,
            text="Gender:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=2, column=0, padx=20, pady=15, sticky="w")

        self.gender_var = ctk.StringVar(value="male")
        gender_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        gender_frame.grid(row=2, column=1, padx=20, pady=15, sticky="w")
        
        ctk.CTkRadioButton(
            gender_frame,
            text="Male",
            variable=self.gender_var,
            value="male"
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            gender_frame,
            text="Female",
            variable=self.gender_var,
            value="female"
        ).pack(side="left", padx=10)

        self.create_form_field(form_frame, "Weight (kg):", "weight_entry", row=3)

        self.create_form_field(form_frame, "Height (cm):", "height_entry", row=4)

        ctk.CTkLabel(
            form_frame,
            text="Activity Level:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=5, column=0, padx=20, pady=15, sticky="w")
        
        self.activity_var = ctk.StringVar(value="moderate")
        activity_options = [
            ("Sedentary (little or no exercise)", "sedentary"),
            ("Lightly Active (1-3 days/week)", "light"),
            ("Moderately Active (3-5 days/week)", "moderate"),
            ("Very Active (6-7 days/week)", "active"),
            ("Extra Active (athlete/physical job)", "very_active")
        ]
        
        activity_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=self.activity_var,
            values=[opt[1] for opt in activity_options],
            width=300
        )
        activity_menu.grid(row=5, column=1, padx=20, pady=15, sticky="w")

        ctk.CTkLabel(
            form_frame,
            text="Goal:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=6, column=0, padx=20, pady=15, sticky="w")
        
        self.goal_var = ctk.StringVar(value="maintain")
        goal_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        goal_frame.grid(row=6, column=1, padx=20, pady=15, sticky="w")
        
        ctk.CTkRadioButton(
            goal_frame,
            text="Lose Weight",
            variable=self.goal_var,
            value="lose"
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            goal_frame,
            text="Maintain",
            variable=self.goal_var,
            value="maintain"
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            goal_frame,
            text="Gain Weight",
            variable=self.goal_var,
            value="gain"
        ).pack(side="left", padx=10)

        create_btn = ctk.CTkButton(
            self,
            text="Create Profile",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            command=self.create_profile
        )
        create_btn.pack(pady=30)

    def create_form_field(self, parent, label_text, entry_name, row):
        ctk.CTkLabel(
            parent,
            text=label_text,
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=row, column=0, padx=20, pady=15, sticky="w")
        
        entry = ctk.CTkEntry(parent, width=300)
        entry.grid(row=row, column=1, padx=20, pady=15, sticky="w")

        setattr(self, entry_name, entry)
    
    def validate_inputs(self):
        name = self.name_entry.get().strip()
        age_str = self.age_entry.get().strip()
        weight_str = self.weight_entry.get().strip()
        height_str = self.height_entry.get().strip()

        if not name:
            return False, "Please enter your name"
        
        try:
            age = int(age_str)
            if age < 10 or age > 120:
                return False, "Age must be between 10 and 120"
        except ValueError:
            return False, "Please enter a valid age"
        
        try:
            weight = float(weight_str)
            if weight < 20 or weight > 300:
                return False, "Weight must be between 20 and 300 kg"
        except ValueError:
            return False, "Please enter a valid weight"
        
        try:
            height = float(height_str)
            if height < 100 or height > 250:
                return False, "Height must be between 100 and 250 cm"
        except ValueError:
            return False, "Please enter a valid height"
        
        return True, ""
    
    def create_profile(self):
        is_valid, error_msg = self.validate_inputs()
        if not is_valid:
            messagebox.showerror("Validation Error", error_msg)
            return
        
        try:
            name = self.name_entry.get().strip()
            age = int(self.age_entry.get().strip())
            gender = self.gender_var.get()
            weight = float(self.weight_entry.get().strip())
            height = float(self.height_entry.get().strip())
            activity_level = self.activity_var.get()
            goal = self.goal_var.get()

            #calc daily goal
            daily_goal = CalorieCalculator.calculate_daily_goal(
                weight_kg=weight,
                height_cm=height,
                age=age,
                gender=gender,
                activity_level=activity_level,
                goal=goal
            )

            user = User(
                user_name=name,
                age=age,
                gender=gender,
                weight_kg=weight,
                height_cm=height,
                activity_level=activity_level,
                goal=goal,
                daily_calorie_goal=daily_goal
            )

            user_id = user.save(self.db_manager)

            messagebox.showinfo(
                "Profile Created",
                f"Profile created successfully!\n\n"
                f"Your daily calorie goal: {daily_goal} calories"
            )

            if self.on_complete:
                self.on_complete(user)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create profile: {str(e)}")