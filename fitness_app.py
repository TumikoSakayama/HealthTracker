import customtkinter as ctk
from tkinter import filedialog, messagebox
from logichandler import HabitHandler
from habits_form import HabitForm, HabitDisplay, HabitStats

class FitnessTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Fitness and Habit Tracker")
        self.geometry("1100x700")

        self.handler = HabitHandler()
        self.setup_layout()
        self.create_components()

    def setup_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def handle_new_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".json")

        if path:
            success, message = self.handler.new_collection(path)
            if success:
                self.refresh_habit_view()
            else:
                messagebox.showerror("Error", message)

    def handle_load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])

        if file_path:
            success, count, name = self.handler.load_habits(file_path)
            if success:
                self.refresh_habit_view()
                self.show_message(f"Successfully loaded {count} habits from {name}")
            else:
                messagebox.showerror("Load Error", count)

    def create_components(self):
        sidebar_callbacks = {
            'new_file': self.handle_new_file,
            'load_file': self.handle_load_file,
            'save_file': self.handler.save_to_file,
            'refresh': self.refresh_habit_view
        }

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky='nsew')

        buttons = [
            ("New File", sidebar_callbacks["new_file"]),
            ("Load File", sidebar_callbacks["load_file"]),
            ("Save File", sidebar_callbacks["save_file"]),
            ("Refresh View", sidebar_callbacks["refresh"])
        ]

        for i, (text, cmd) in enumerate(buttons):
            btn = ctk.CTkButton(self.sidebar, text=text, command=cmd)
            btn.grid(row=i, column=0, padx=20, pady=10)

        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        self.form = HabitForm(self.main_frame, self.add_habit)
        self.form.grid(row=0, column=0, sticky="ew", padx=20, pady=10)

        self.display = HabitDisplay(self.main_frame, self.toggle_completion, self.delete_habit)
        self.display.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        self.stats_widget = HabitStats(self.main_frame, self.handler)
        self.stats_widget.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

        self.status_label = ctk.CTkLabel(self.main_frame, text="Please load a file to begin.")
        self.status_label.grid(row=3, column=0, pady=10)

    def handle_save(self):
        success, message = self.handler.save_to_file()
        if success:
            self.show_message(message)
        else:
            messagebox.showerror("Save Failed", message)

    def add_habit(self, name, category, goal):
        success, message = self.handler.add_habit(name, category, goal)
        if success:
            self.refresh_habit_view()
            #self.form.clear_form()
        else:
            messagebox.showerror("Save Failed", message)

    def toggle_completion(self, habit_name):
        success, message = self.handler.toggle_completion(habit_name)
        if success:
           self.refresh_habit_view()
        else:
            messagebox.showerror("Save Failed", message)
    
    def delete_habit(self, habit_name):
        success, message = self.handler.delete_habit(habit_name)
        if success:
            self.refresh_habit_view()
            self.show_message(f"Habit '{habit_name}' deleted successfully")
        else:
            messagebox.showerror("Delete Failed", message)
    
    def refresh_habit_view(self):
        self.display.update_view(self.handler.habits)
        self.stats_widget.update_graph()

        file_name = self.handler.get_file_name() or "None"
        self.status_label.configure(text = f"File: {file_name}")

        if self.handler.current_file:
            self.form.set_enabled(True)


    def show_message(self, message, timeout=3000):
        toast = ctk.CTkToplevel(self)
        toast.title("Notification")
        toast.overrideredirect(True)

        x = self.winfo_x() + (self.winfo_width() // 2) - 150
        y = self.winfo_y() + (self.winfo_height() // 2) - 50
        toast.geometry(f"300x100+{x}+{y}")

        label = ctk.CTkLabel(toast, text=message, font=ctk.CTkFont(size=14))
        label.pack(expand=True, padx=20, pady=20)

        toast.after(timeout, toast.destroy)
