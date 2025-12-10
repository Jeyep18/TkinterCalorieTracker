import customtkinter as ctk
from datetime import date, datetime
from models.food import Food
from models.food_log import FoodLog
from tkinter import messagebox


class FoodSearchDialog(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, current_user, on_food_logged = None):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.user = current_user
        self.on_food_logged = on_food_logged
        self.selected_food = None
        
        self.title("Search Food")
        self.geometry("480x560")
        self.resizable(True, True)
        self.minsize(400, 450)
        
        # responsive layout
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(2, weight = 1)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title = ctk.CTkLabel(
            self,
            text = "Search Food",
            font = ctk.CTkFont(size = 20, weight = "bold")
        )
        title.grid(row = 0, column = 0, pady = (10, 5), sticky = "ew")
        
        search_frame = ctk.CTkFrame(self, fg_color = "transparent")
        search_frame.grid(row = 1, column = 0, sticky = "ew", padx = 15, pady = 5)
        search_frame.grid_columnconfigure(0, weight = 1)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text = "Type food name and press Enter...",
            height = 35,
            font = ctk.CTkFont(size = 13)
        )
        self.search_entry.grid(row = 0, column = 0, sticky = "ew", padx = (0, 8))
        self.search_entry.bind("<Return>", lambda e: self.search_foods())
        
        search_btn = ctk.CTkButton(
            search_frame,
            text = "Search",
            width = 80,
            height = 35,
            command = self.search_foods
        )
        search_btn.grid(row = 0, column = 1)
        
        self.results_frame = ctk.CTkScrollableFrame(self)
        self.results_frame.grid(row = 2, column = 0, sticky = "nsew", padx = 15, pady = 5)
        
       
        self.selected_frame = ctk.CTkFrame(self)
        self.selected_frame.grid(row = 3, column = 0, sticky = "ew", padx = 15, pady = 5)
        
        self.selected_label = ctk.CTkLabel(
            self.selected_frame,
            text = "No food selected",
            font = ctk.CTkFont(size = 12),
            text_color = "gray"
        )
        self.selected_label.pack(pady = 8)
        
        options_frame = ctk.CTkFrame(self)
        options_frame.grid(row = 4, column = 0, sticky = "ew", padx = 15, pady = 5)
        options_frame.grid_columnconfigure((0, 1, 2, 3), weight = 1)
        
        ctk.CTkLabel(
            options_frame,
            text = "Servings:",
            font = ctk.CTkFont(size = 12, weight = "bold")
        ).grid(row = 0, column = 0, padx = 8, pady = 8, sticky = "e")
        
        self.servings_entry = ctk.CTkEntry(options_frame, width = 70, placeholder_text = "1.0")
        self.servings_entry.grid(row = 0, column = 1, padx = 8, pady = 8, sticky = "w")
        self.servings_entry.insert(0, "1")
        
        ctk.CTkLabel(
            options_frame,
            text = "Meal:",
            font = ctk.CTkFont(size = 12, weight = "bold")
        ).grid(row = 0, column = 2, padx = 8, pady = 8, sticky = "e")
        
        self.meal_var = ctk.StringVar(value = "snack")
        meal_menu = ctk.CTkOptionMenu(
            options_frame,
            variable = self.meal_var,
            values = ["breakfast", "lunch", "dinner", "snack"],
            width = 100
        )
        meal_menu.grid(row = 0, column = 3, padx = 8, pady = 8, sticky = "w")
        
        # Log button
        self.log_btn = ctk.CTkButton(
            self,
            text = "Log Food",
            font = ctk.CTkFont(size = 14, weight = "bold"),
            height = 38,
            state = "disabled",
            command = self.log_food
        )
        self.log_btn.grid(row = 5, column = 0, pady = 10)
    
    def search_foods(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            return
        
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        foods = Food.search(keyword, self.db_manager)
        
        if not foods:
            no_results = ctk.CTkLabel(
                self.results_frame,
                text = "No foods found.",
                text_color = "gray"
            )
            no_results.pack(pady = 15)
            return
        
        for food in foods:
            self.create_food_card(food)
    
    def create_food_card(self, food):
        card = ctk.CTkFrame(self.results_frame, corner_radius = 6)
        card.pack(fill = "x", pady = 3, padx = 3)
        card.bind("<Button-1>", lambda e, f = food: self.select_food(f))
        
        inner_frame = ctk.CTkFrame(card, fg_color = "transparent")
        inner_frame.pack(fill = "x", padx = 10, pady = 6)
        inner_frame.bind("<Button-1>", lambda e, f = food: self.select_food(f))
      
        name_label = ctk.CTkLabel(
            inner_frame,
            text = food.food_name,
            font = ctk.CTkFont(size = 13, weight = "bold"),
            anchor = "w"
        )
        name_label.pack(anchor = "w")
        name_label.bind("<Button-1>", lambda e, f = food: self.select_food(f))
       
        info_text = f"{food.calories} cal | P:{food.protein_g}g C:{food.carbs_g}g F:{food.fats_g}g"
        info_label = ctk.CTkLabel(
            inner_frame,
            text = info_text,
            font = ctk.CTkFont(size = 11),
            text_color = "gray",
            anchor = "w"
        )
        info_label.pack(anchor = "w")
        info_label.bind("<Button-1>", lambda e, f = food: self.select_food(f))
    
    def select_food(self, food):
        self.selected_food = food

        selected_text = f"Selected: {food.food_name} ({food.calories} cal/serving)"
        self.selected_label.configure(
            text = selected_text,
            text_color = "green"
        )
       
        self.log_btn.configure(state = "normal")
    
    def log_food(self):
        if not self.selected_food:
            messagebox.showerror("Error", "Please select a food first")
            return
        
        try:
            servings = float(self.servings_entry.get().strip())
            if servings <= 0:
                raise ValueError("Servings must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for servings")
            return
        
        try:
            total_calories = float(self.selected_food.calories) * servings
            meal_type = self.meal_var.get()
            
            food_log = FoodLog(
                user_id = self.user.user_id,
                food_id = self.selected_food.food_id,
                servings = servings,
                total_calories = total_calories,
                meal_type = meal_type,
                log_date = date.today(),
                log_time = datetime.now().time()
            )
            
            food_log.save(self.db_manager)
            
            messagebox.showinfo(
                "Success",
                f"Logged {servings} serving(s) of {self.selected_food.food_name}\n"
                f"Total: {int(total_calories)} calories"
            )
           
            if self.on_food_logged:
                self.on_food_logged()
            
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to log food: {str(e)}")
