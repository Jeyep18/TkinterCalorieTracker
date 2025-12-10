import customtkinter as ctk
from datetime import date
from models.food_log import FoodLog
from tkinter import messagebox


class DailyLogView(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, current_user, on_delete = None):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.user = current_user
        self.on_delete = on_delete
        
        self.title("Today's Food Log")
        self.geometry("480x560")
        self.resizable(True, True)
        self.minsize(380, 400)
        
        self.meal_emojis = {
            "breakfast": "Breakfast",
            "lunch": "Lunch",
            "dinner": "Dinner",
            "snack": "Snacks"
        }
        
        self.meal_order = ["breakfast", "lunch", "dinner", "snack"]
        
        # responsive layout
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        
        self.create_widgets()
        self.load_logs()
    
    def create_widgets(self):
        # Header
        header = ctk.CTkFrame(self, fg_color = "transparent")
        header.grid(row = 0, column = 0, sticky = "ew", padx = 15, pady = (10, 5))
        
        title = ctk.CTkLabel(
            header,
            text = "Today's Food Log",
            font = ctk.CTkFont(size = 18, weight = "bold")
        )
        title.pack()

        date_label = ctk.CTkLabel(
            header,
            text = date.today().strftime("%A, %B %d, %Y"),
            font = ctk.CTkFont(size = 12),
            text_color = "gray"
        )
        date_label.pack()
       
        self.content_frame = ctk.CTkScrollableFrame(self)
        self.content_frame.grid(row = 1, column = 0, sticky = "nsew", padx = 15, pady = 5)
        
        # Close button
        close_btn = ctk.CTkButton(
            self,
            text = "Close",
            font = ctk.CTkFont(size = 13),
            width = 100,
            height = 32,
            command = self.destroy
        )
        close_btn.grid(row = 2, column = 0, pady = 10)
    
    def load_logs(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        logs = FoodLog.get_by_user_and_date(
            self.user.user_id,
            date.today(),
            self.db_manager
        )
        
        if not logs:
            self.show_empty_state()
            return
        
        meals = {}
        for log in logs:
            meal_type = log.meal_type
            if meal_type not in meals:
                meals[meal_type] = []
            meals[meal_type].append(log)
        
        for meal_type in self.meal_order:
            if meal_type in meals:
                self.create_meal_section(meal_type, meals[meal_type])
    
    def show_empty_state(self):
        empty_frame = ctk.CTkFrame(self.content_frame, fg_color = "transparent")
        empty_frame.pack(fill = "both", expand = True, pady = 30)
        
        message_label = ctk.CTkLabel(
            empty_frame,
            text = "No foods logged today",
            font = ctk.CTkFont(size = 16, weight = "bold"),
            text_color = "gray"
        )
        message_label.pack(pady = 10)
        
        hint_label = ctk.CTkLabel(
            empty_frame,
            text = "Use 'Search Food' to get started!",
            font = ctk.CTkFont(size = 12),
            text_color = "gray"
        )
        hint_label.pack()
    
    def create_meal_section(self, meal_type, logs):
        meal_total = sum(float(log.total_calories) for log in logs)
        
        # Meal header
        header_frame = ctk.CTkFrame(self.content_frame, fg_color = "transparent")
        header_frame.pack(fill = "x", pady = (10, 3))
        
        meal_title = ctk.CTkLabel(
            header_frame,
            text = self.meal_emojis.get(meal_type, meal_type.capitalize()),
            font = ctk.CTkFont(size = 14, weight = "bold")
        )
        meal_title.pack(side = "left")
        
        meal_calories = ctk.CTkLabel(
            header_frame,
            text = f"{int(meal_total)} cal",
            font = ctk.CTkFont(size = 13),
            text_color = "gray"
        )
        meal_calories.pack(side = "right")
        
        for log in logs:
            self.create_food_entry(log)
    
    def create_food_entry(self, log):
        card = ctk.CTkFrame(self.content_frame, corner_radius = 6)
        card.pack(fill = "x", pady = 3, padx = 5)
        
        content_frame = ctk.CTkFrame(card, fg_color = "transparent")
        content_frame.pack(fill = "x", padx = 10, pady = 6)
        content_frame.grid_columnconfigure(0, weight = 1)
        
        # Top row
        top_row = ctk.CTkFrame(content_frame, fg_color = "transparent")
        top_row.pack(fill = "x")
        top_row.grid_columnconfigure(0, weight = 1)
        
        food_name = ctk.CTkLabel(
            top_row,
            text = log.food_name,
            font = ctk.CTkFont(size = 12, weight = "bold"),
            anchor = "w"
        )
        food_name.pack(side = "left")
        
        delete_btn = ctk.CTkButton(
            top_row,
            text = "X",
            font = ctk.CTkFont(size = 11),
            width = 28,
            height = 22,
            fg_color = "transparent",
            border_width = 1,
            text_color = ("red", "red"),
            hover_color = ("gray90", "gray20"),
            command = lambda l = log: self.delete_log(l)
        )
        delete_btn.pack(side = "right")
        
        time_str = log.log_time
        if hasattr(log.log_time, 'strftime'):
            time_str = log.log_time.strftime("%I:%M %p")
        
        details_text = f"{float(log.servings):.1f} × {log.serving_size}{log.serving_unit} | {int(float(log.total_calories))} cal | {time_str}"
        details_label = ctk.CTkLabel(
            content_frame,
            text = details_text,
            font = ctk.CTkFont(size = 11),
            text_color = "gray",
            anchor = "w"
        )
        details_label.pack(anchor = "w")
    
    def delete_log(self, log):
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete '{log.food_name}'?"
        )
        
        if confirm:
            try:
                FoodLog.delete(log.log_id, self.db_manager)
                messagebox.showinfo("Deleted", f"'{log.food_name}' removed.")
                self.load_logs()
                
                if self.on_delete:
                    self.on_delete()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {str(e)}")
