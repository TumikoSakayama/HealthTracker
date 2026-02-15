from datetime import datetime

class Habit:
    def __init__(self, name, category, weekly_goal=7, created_at=None, completion_date=None):
        self.name = name.strip()
        self.category = category.strip()
        self.weekly_goal = int(weekly_goal)
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d")
        self.completion_date = completion_date if completion_date else []

    def to_dict(self):
        return{
            "name": self.name,
            "category": self.category,
            "weekly_goal": self.weekly_goal,
            "created_at": self.created_at,
            "completion_date": self.completion_date
        }

    @staticmethod
    def from_dict(self):
        return Habit(
            data['name'],
            data['category'],
            data['weekly_goal', 7],
            data['created_at'],
            data['completion_date']
        )

    

        
