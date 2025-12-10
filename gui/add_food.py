import customtkinter as ctk
from models.food import Food
from tkinter import messagebox


class AddFoodDialog(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, current_user):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.user = current_user
        
        self.title("Add Custom Food")
        self.geometry("400x520")
        self.resizable(True, True)
        self.minsize(350, 420)
        
        # responsive layout
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title = ctk.CTkLabel(
            self,
            text = "Add Custom Food",
            font = ctk.CTkFont(size = 18, weight = "bold")
        )
        title.grid(row = 0, column = 0, pady = (10, 5))
        
        form_frame = ctk.CTkScrollableFrame(self)
        form_frame.grid(row = 1, column = 0, sticky = "nsew", padx = 15, pady = 5)
        form_frame.grid_columnconfigure(1, weight = 1)

        self.create_form_field(form_frame, "Food Name *", "name_entry", "e.g., Spanish Latte", 0)
        self.create_form_field(form_frame, "Serving Size *", "serving_size_entry", "e.g., 100", 1)
        self.create_form_field(form_frame, "Serving Unit *", "serving_unit_entry", "e.g., g, ml", 2)
        self.create_form_field(form_frame, "Calories *", "calories_entry", "e.g., 320", 3)
        
        # Separator
        separator_label = ctk.CTkLabel(
            form_frame,
            text = "── Optional ──",
            font = ctk.CTkFont(size = 11),
            text_color = "gray"
        )
        separator_label.grid(row = 4, column = 0, columnspan = 2, pady = 10)
        
        self.create_form_field(form_frame, "Protein (g)", "protein_entry", "e.g., 25", 5)
        self.create_form_field(form_frame, "Carbs (g)", "carbs_entry", "e.g., 15", 6)
        self.create_form_field(form_frame, "Fat (g)", "fat_entry", "e.g., 18", 7)
        
        # Add button
        add_btn = ctk.CTkButton(
            self,
            text = "Add Food",
            font = ctk.CTkFont(size = 14, weight = "bold"),
            height = 38,
            command = self.add_food
        )
        add_btn.grid(row = 2, column = 0, pady = 10)
    
    def create_form_field(self, parent, label_text, entry_name, placeholder, row):
        ctk.CTkLabel(
            parent,
            text = label_text,
            font = ctk.CTkFont(size = 12, weight = "bold")
        ).grid(row = row, column = 0, padx = 8, pady = 8, sticky = "w")
        
        entry = ctk.CTkEntry(
            parent,
            placeholder_text = placeholder
        )
        entry.grid(row = row, column = 1, padx = 8, pady = 8, sticky = "ew")
        
        setattr(self, entry_name, entry)
    
    def validate_inputs(self):
        name = self.name_entry.get().strip()
        serving_size_str = self.serving_size_entry.get().strip()
        serving_unit = self.serving_unit_entry.get().strip()
        calories_str = self.calories_entry.get().strip()
        
        if not name:
            return False, "Please enter a food name"
        
        if not serving_size_str:
            return False, "Please enter a serving size"
        
        try:
            serving_size = float(serving_size_str)
            if serving_size <= 0:
                return False, "Serving size must be positive"
        except ValueError:
            return False, "Please enter a valid serving size"
        
        if not serving_unit:
            return False, "Please enter a serving unit"
        
        if not calories_str:
            return False, "Please enter calories"
        
        try:
            calories = float(calories_str)
            if calories < 0:
                return False, "Calories cannot be negative"
        except ValueError:
            return False, "Please enter valid calories"
        
        protein_str = self.protein_entry.get().strip()
        carbs_str = self.carbs_entry.get().strip()
        fat_str = self.fat_entry.get().strip()
        
        if protein_str:
            try:
                if float(protein_str) < 0:
                    return False, "Protein cannot be negative"
            except ValueError:
                return False, "Please enter valid protein"
        
        if carbs_str:
            try:
                if float(carbs_str) < 0:
                    return False, "Carbs cannot be negative"
            except ValueError:
                return False, "Please enter valid carbs"
        
        if fat_str:
            try:
                if float(fat_str) < 0:
                    return False, "Fat cannot be negative"
            except ValueError:
                return False, "Please enter valid fat"
        
        return True, ""
    
    def add_food(self):
        is_valid, error_msg = self.validate_inputs()
        if not is_valid:
            messagebox.showerror("Validation Error", error_msg)
            return
        
        try:
            name = self.name_entry.get().strip()
            serving_size = float(self.serving_size_entry.get().strip())
            serving_unit = self.serving_unit_entry.get().strip()
            calories = float(self.calories_entry.get().strip())
            
            protein_str = self.protein_entry.get().strip()
            carbs_str = self.carbs_entry.get().strip()
            fat_str = self.fat_entry.get().strip()
            
            protein = float(protein_str) if protein_str else 0
            carbs = float(carbs_str) if carbs_str else 0
            fat = float(fat_str) if fat_str else 0
            
            food = Food(
                food_name = name,
                calories = calories,
                protein_g = protein,
                carbs_g = carbs,
                fats_g = fat,
                serving_size = serving_size,
                serving_unit = serving_unit,
                created_by = self.user.user_id
            )
            
            food.save(self.db_manager)
            
            messagebox.showinfo(
                "Food Added",
                f"Successfully added '{name}'!\n"
                f"Calories: {int(calories)} per {serving_size} {serving_unit}"
            )
            
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add food: {str(e)}")
