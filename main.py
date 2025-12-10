import customtkinter as ctk
from database.db_manager import DBManager
from gui.profile_setup import ProfileSetupScreen
from gui.main_window import MainWindow
from models.user import User

class CalorieTrackerApp:
    def __init__(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.db_manager = DBManager()
        if not self.db_manager.connect():
            print("Failed to connect to the database.")
            return
        
        self.db_manager.initialize_database()

        self.root = ctk.CTk()
        self.root.title("Calorie Tracker")
        self.root.geometry("900x700")

        self.center_window()

        self.current_user = None

        self.current_screen = None

        users = User.get_all(self.db_manager)

        if not users:
            self.show_profile_setup()

        else:
            self.current_user = users[0]
            self.show_main_window()


        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def center_window(self):
        # center ts
        self.root.update_idletasks()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"+{x}+{y}")

    def show_profile_setup(self):
        if self.current_screen:
            self.current_screen.destroy()
        
        self.current_screen = ProfileSetupScreen(
            self.root,
            self.db_manager,
            on_complete = self.on_profile_created
        )
        self.current_screen.pack(fill = "both", expand = True)
    
    def on_profile_created(self, user):
        self.current_user = user
        self.show_main_window()

    def show_main_window(self):
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = MainWindow(
            self.root,
            self.db_manager,
            self.current_user
        )
        self.current_screen.pack(fill = "both", expand = True)

    def on_closing(self):
        self.db_manager.close()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CalorieTrackerApp()
    app.run()

