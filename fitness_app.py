import customtkinter as ctk
from tkinter import filedialog, messagebox
from logichandler import HabitHandler

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

    def create_components(self):
        sidebar_callbacks = {
            'new_file': self.handler.new_file,
            'load_file': self.handler.load_file,
            'save_file': self.handler.save_file,
            'refresh': self.handler.refresh
        }

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky='nsew')

        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.status_label = ctk.CTkLabel(self.main_frame, text="Please load a file to begin.")
        self.status_label.grid(row=0, column=0, pady=20)

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
    
    def refresh_habit_view(self):
        messagebox.showinfo("Loading", "Refreshing view with current habits...")

    def show_message(self, message, timeout=3000):
        toast = ctk.CTkToplevel(self)
        toast.title("Notification")
        toast.overrideredirect(True)

        x = self.winfo_x() + (self.winfo_width() // 2) - 150
        y = self.winfo_y() + (self.winfo_height // 2) - 50
        toast.geometry(f"300x100+{x}+{y}")

        label = ctk.CTkLabel(toast, text=message, font=ctk.CTkFont(size=14))
        label.pack(expand=True, padx=20, pady=20)

        toast.after(timeout, toast.destroy)
