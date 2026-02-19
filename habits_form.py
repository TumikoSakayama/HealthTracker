import customtkinter as ctk
from datetime import datetime

class HabitForm(ctk.CTkFrame):
    def __init__(self, master, add_callback):
        super().__init__(master)
        self.add_callback = add_callback
        self.create_widgets()
        #self.grid_columnconfigure((0, 1, 2, 3), weight=1)

    def handle_submit(self):
        name = self.name_entry.get()
        category = self.cat_entry.get()
        goal = self.goal_var.get()
        
        if name and category:
            self.add_callback(name, category, goal)
            self.clear_form()
        
    def clear_form(self):
        self.name_entry.delete(0, "end")
        self.cat_entry.delete(0, "end")
        self.goal_var.set("7")

        
    def create_widgets(self):
        self.title = ctk.CTkLabel(
            self, text="New Habit",
            font=ctk.CTkFont(size=16, weight="bold")
        )
    
        self.title.grid(row=0, column=0, columnspan=4, padx=(10, 20))

        ctk.CTkLabel(self, text="Habit Name: ").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = ctk.CTkEntry(self, placeholder_text="e.g., Gym, Reading...")
        self.name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(self, text="Category: ").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.cat_entry = ctk.CTkEntry(self, placeholder_text="e.g., Health, Mind...")
        self.cat_entry.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
            
        ctk.CTkLabel(self, text="Goal (Days/Week): ").grid(row=2, column=0, padx=10, pady=20, sticky="e")
        self.goal_var = ctk.StringVar(value=7)
        self.open_menu = ctk.CTkOptionMenu(
                self,
                values = ["1", "2", "3", "4", "5", "6", "7"],
                variable = self.goal_var
            )
        self.open_menu.grid(row=2, column=1, padx=10, pady=20, sticky="w")
            
        self.add_btn = ctk.CTkButton(
                self,
                text="Add Habit",
                command= self.handle_submit,
                state="disabled"
            )
        self.add_btn.grid(row=2, column=2, columnspan=2, padx=20, pady=10, sticky="ew")
        
    def set_enabled(self, enabled=True):
        state = "normal" if enabled else "disabled"
        self.add_btn.configure(state=state)
    
class HabitCard(ctk.CTkFrame):
    def __init__(self, master, habit, toggle_callback, delete_callback):
        super().__init__(master)
        self.habit = habit
        self.toggle_callback = toggle_callback
        self.delete_callback = delete_callback
        
        self.grid_columnconfigure(1, weight=1)
        self.create_widgets()
    
    def create_widgets(self):
        self.name_label = ctk.CTkLabel(
            self, text=self.habit_name,
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=140, justify="left"
        )
        self.name_label.grid(row=0, column=0, padx=15, pady=5, stick="w")
        
        stats_text = self.calculate_stats_display()
        self.stats_label = ctk.CTkLabel(
            self, text=self.stats_text,
            font=ctk.CTkFont(size=12),
            text_color="gray70"
        )
        self.stats_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")
        
        today = datetime.now().strftime("%Y-%m-%d")
        is_done = today in self.habit.completion_date
        
        self.check_var = ctk.BooleanVar(value=is_done)
        self.check_btn = ctk.CTkCheckBox(
            self, text="Done Today",
            variable = self.check_var,
            command = self.handle_toogle,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.check_btn.grid(row=2, column=0, rowspan=2, padx=20)
        
    def calculate_stats_display(self):
        count = len(self.habit.completion_date)
        goal = self.habit.weekly_goal
        
        return f"Total: {count} | Weekly: {goal}"
        
    def handle_toogle(self):
        self.check_btn.configure(state="disabled")
        self.toggle_callback(self.habit.name)
        
class HabitDisplay(ctk.CTkScrollableFrame):
    def __init__(self, master, toggle_callback):
        super().__init__(master)
        self.toggle_callback = toggle_callback
        self.grid_columnconfigure(0, weight=1)
        
    def update_view(self, habits):
        for widget in self.winfo_children():
            widget.destroy()
            
        for i, habit in enumerate(habits):
            card = HabitCard(self, habit, self.toggle_callback)
            card.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

