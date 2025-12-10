import customtkinter as ctk
from datetime import date
from models.food_log import FoodLog
from services.daily_reset_service import DailyResetService
from gui.food_search import FoodSearchDialog
from gui.add_food import AddFoodDialog
from gui.daily_log import DailyLogView

class MainWindow(ctk.CTkFrame):
    def __init__(self, parent, db_manager, current_user):
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.user = current_user
        self.reset_service = DailyResetService(db_manager)
        
        self.reset_service.check_today_log_exists(self.user.user_id)
        
        self.create_widgets()
        self.refresh_summary()
    
    def create_widgets(self):
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        header = ctk.CTkFrame(self, height=100)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header.grid_columnconfigure(1, weight=1)
        
        greeting = ctk.CTkLabel(
            header,
            text=f"Welcome, {self.user.user_name}!",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        greeting.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        today_label = ctk.CTkLabel(
            header,
            text=date.today().strftime("%A, %B %d, %Y"),
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        today_label.grid(row=1, column=0, padx=20, sticky="w")
        
        summary_frame = ctk.CTkFrame(self)
        summary_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        summary_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.goal_card = self.create_stat_card(
            summary_frame, "Daily Goal", "0", "calories", 0
        )

        self.consumed_card = self.create_stat_card(
            summary_frame, "Consumed", "0", "calories", 1
        )

        self.remaining_card = self.create_stat_card(
            summary_frame, "Remaining", "0", "calories", 2
        )

        progress_frame = ctk.CTkFrame(self)
        progress_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            progress_frame,
            text="Today's Progress",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 5))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=400, height=20)
        self.progress_bar.pack(pady=(5, 10))
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="0%",
            font=ctk.CTkFont(size=14)
        )
        self.progress_label.pack(pady=(0, 15))

        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        ctk.CTkButton(
            button_frame,
            text="🔍 Search Food",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50,
            command=self.open_food_search
        ).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ctk.CTkButton(
            button_frame,
            text="➕ Add Custom Food",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50,
            command=self.open_add_food
        ).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkButton(
            button_frame,
            text="📊 View Today's Log",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50,
            command=self.open_daily_log
        ).grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    def create_stat_card(self, parent, title, value, unit, column):
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.grid(row=0, column=column, padx=10, pady=20, sticky="nsew")

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(pady=(20, 5))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=36, weight="bold")
        )
        value_label.pack(pady=5)

        unit_label = ctk.CTkLabel(
            card,
            text=unit,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        unit_label.pack(pady=(0, 20))

        return {"value": value_label, "unit": unit_label}
    
    def refresh_summary(self):
        summary = self.reset_service.update_daily_logs(
            self.user.user_id, date.today()
        )

        goal = summary['calorie_goal']
        consumed = summary['total_calories']
        remaining = summary['remaining_calories']

        self.goal_card["value"].configure(text=str(goal))
        self.consumed_card["value"].configure(text=str(int(consumed)))

        if remaining < 0:
            self.remaining_card["value"].configure(
                text=str(int(remaining)),
                text_color="red"
            )
        else:
            self.remaining_card["value"].configure(
                text=str(int(remaining)),
                text_color="green"
            )

        progress = min(consumed / goal, 1.0)  
        self.progress_bar.set(progress)
        self.progress_label.configure(text=f"{int(progress * 100)}%")

    def open_food_search(self):
        dialog = FoodSearchDialog(
            self,
            self.db_manager,
            self.user,
            on_food_logged=self.refresh_summary
        )
        dialog.grab_set()

    def open_add_food(self):
        dialog = AddFoodDialog(
            self,
            self.db_manager,
            self.user
        )
        dialog.grab_set()

    def open_daily_log(self):
        dialog = DailyLogView(
            self,
            self.db_manager,
            self.user,
            on_delete=self.refresh_summary
        )
        dialog.grab_set()

