# main.py - AI Student Support Assistant

import json
from datetime import datetime

class StudentAssistant:
    def __init__(self):
        self.tasks = []
        self.notes = []

    def add_task(self, title, due_date):
        task = {"id": len(self.tasks) + 1, "title": title, "due_date": due_date, "status": "Pending"}
        self.tasks.append(task)
        print(f"Task '{title}' added successfully!")

    def view_tasks(self):
        if not self.tasks:
            print("\nNo pending tasks.")
            return
        print("\n--- Your Tasks ---")
        for t in self.tasks:
            print(f"[{t['id']}] {t['title']} | Due: {t['due_date']} | Status: {t['status']}")

    def calculate_gpa(self, grades):
        # grades format: [("Math", "A", 3), ("CS", "B", 4)]
        grade_points = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}
        total_points = sum(grade_points.get(g.upper(), 0) * credits for _, g, credits in grades)
        total_credits = sum(credits for _, _, credits in grades)
        
        if total_credits == 0:
            return 0.0
        return round(total_points / total_credits, 2)

if __name__ == "__main__":
    assistant = StudentAssistant()
    print("Welcome to AI Student Support Assistant")
    
    # Quick demo execution
    assistant.add_task("Complete Python Assignment", "2026-09-15")
    assistant.add_task("Submit Literature Essay", "2026-09-20")
    assistant.view_tasks()
    
    sample_grades = [("Computer Science", "A", 4), ("Mathematics", "B", 3)]
    gpa = assistant.calculate_gpa(sample_grades)
    print(f"\nCalculated GPA: {gpa}")
