import customtkinter as ctk

class HabitForm():
  def __init__(self, add_callback):
    super().__init__(master)
    self.add_callback = add_callback

    self.grid_columnconfigure((0, 1, 2, 3), weight=1)
    self.create_widgets()

  def create_widgets(self):
      self.title = ctk.CTKLabel(
        self, text="New Habit"
        font=ctk.CTKFont(size=16, weight="bold)
        )
    
        self.title.grid(row=0, column=0, columnspan=4, padx=(10, 20))

        ctk.CTKLabel(self, text="Habit Name: ").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = ctk.CTKEntry(self, placeholder_text="e.g., Gym, Reading...")
        self.name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    
        ctk.CTKLabel(self, text="Category: ").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.cat_entry = ctk.CTKEntry(self, placeholder_text="e.g., Health, Mind...")
        self.cat_entry.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
        
        ctk.CTKLabel(self, text="Goal (Days/Week): ").grid(row=2, column=0, padx=10, pady=20, sticky="e")
        self.goal_var = ctk.StringVar(value=7)
        self.open_menu = ctk.CTKOptionMenu(
            self,
            values = ["1", "2", "3", "4", "5", "6", "7"],
            variable = self.goal_var
        )
        self.open_menu.grid(row=2, column=1, padx=10, pady=20, sticky="w")
        
        self.add_btn = ctk.CTKButton(
            self,
            text="Add Habit",
            command= self.handle_submit,
            state="disabled"
        )
        self.add_btn.grid(row=2, column=2, columnspan=2, pady=20, pady=10, sticky="ew")
    
    def handle_submit(self):
        self.name_entry.get()
        self.cat_entry.get()
        self.goal_var.get()
        
    def clear_form(self):
        self.name_entry.delete(0, "end")
        self.cat_entry.delete(0, "end")
        self.goal_var.set("7")
        
    def set_enabled(self enabled=True):
        state = "normal" if enabled else "disabled"
        self.add_btn.configure(state=state)
    
