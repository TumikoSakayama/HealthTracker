import json
import os
from datetime import datetime
from habits import Habit

class HabitHandler:
    def __init__(self):
        self.habits = []
        self.current_file = None

    def new_collection(self, file_path):
        try:
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            if directory and not os.access(directory, os.W_OK):
                return False, "Permission Denied: Cannot write to this folder."

            with open(file_path, 'w') as f:
                json.dump([], f)

            self.current_file = file_path
            self.habits = []
            return True, os.path.basename(file_path)
        except PermissionError:
            return False, "Permission Denied: You don't have rights to save here."
        except Exception as e:
            return False, f"Location Error: {str(e)}"

    def load_habits(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.habits = [Habit.from_dict(item) for item in data]
            
            self.current_file = file_path
            return True, len(self.habits), self.get_file_name()
        except Exception as e:
            return False, str(e), None

    def add_habit(self, name, category, goal):
        if not name or category:
            return False, "Name nor category cannot be empty."
        
        if any(h.name.lower() == name.strip().lower() for h in self.habits):
            return False, f"A habit named {name} already exists."

        try:
            g_val = int(goal)
            if not (1 <= g_val <=7):
                return False, "Goal must be between 1 to 7 days per week." 
        except ValueError:
            return False, "Goal must be a whole (integer) number."

        new_h = Habit(name, category, g_val)
        self.habits.append(new_h)
        return self.save_to_file()

    def toggle_completion(self, habit_name, date_str=None):
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        for h in self.habits:
            if h.name == habit_name:
                if date_str in h.completion_date:
                    h.completion_date.remove(date_str)
                    msg = "Entry removed."
                else:
                    h.completion_date.append(date_str)
                    msg = "Entry added."
                return self.save_to_file(msg)
        
        return False, "Habit not found."

    def save_to_file(self, success_msg="Changes saved!"):
        if not self.current_file:
            return False, "No file loaded, please load a file."
        
        if not os.path.exists(os.path.dirname(self.current_file)):
            return False, "Error: The folder containing your file has been moved or deleted"

        try:
            if not os.path.exists(self.current_file) and not os.access(self.current_file, os.W_OK):
                return False, "Error: The file is now read-only. Please check file permissions."
            
            data_to_save = [h.to_dict() for h in self.habits]
            with open(self.current_file, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            return True, success_msg
        except PermissionError:
            return False, "Permission Denied: Cannot overwrite the file."
        except Exception as e:
            return False, f"Disk Error: {str(e)}"