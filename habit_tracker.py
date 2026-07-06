import csv
import os
import uuid
from datetime import datetime, date, timedelta


class HabitTracker:

    def __init__(self, habits_file="habits.csv", logs_file="logs.csv"):
        self.habits_file = habits_file
        self.logs_file = logs_file

        self.habit_fields = [
            "habit_id",
            "name",
            "frequency",
            "target_goal",
            "category",
            "start_date",
            "reminder_time",
            "active",
        ]

        self.log_fields = [
            "log_id",
            "habit_id",
            "completed_at",
            "amount",
            "note",
        ]

        self._create_file_if_missing(self.habits_file, self.habit_fields)
        self._create_file_if_missing(self.logs_file, self.log_fields)

    def _create_file_if_missing(self, file_path, fieldnames):
        """Create a CSV file with headers if it does not already exist."""
        if not os.path.exists(file_path):
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

    def _read_csv(self, file_path):
        """Read CSV rows and return them as a list of dictionaries."""
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def _write_csv(self, file_path, fieldnames, rows):
        """Write a list of dictionaries into a CSV file."""
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def add_habit(self, name, frequency, target_goal, category, start_date, reminder_time="09:00"):
        """Add a new habit and save it to the habits CSV file."""
        habit = {
            "habit_id": str(uuid.uuid4())[:8],
            "name": name.strip(),
            "frequency": frequency,
            "target_goal": str(target_goal),
            "category": category.strip(),
            "start_date": str(start_date),
            #"reminder_time": reminder_time,
            "active": "Yes",
        }

        habits = self._read_csv(self.habits_file)
        habits.append(habit)
        self._write_csv(self.habits_file, self.habit_fields, habits)
        return habit

    def get_all_habits(self, active_only=False):
        """Return all habits. If active_only is True, return only active habits."""
        habits = self._read_csv(self.habits_file)
        if active_only:
            habits = [habit for habit in habits if habit.get("active") == "Yes"]
        return habits

    def find_habit(self, habit_id):
        """Find one habit by its habit_id."""
        for habit in self.get_all_habits():
            if habit["habit_id"] == habit_id:
                return habit
        return None

    def update_habit(self, habit_id, name=None, frequency=None, target_goal=None, category=None, start_date=None, reminder_time=None):
        """Update an existing habit. Only values provided by the user are changed."""
        habits = self._read_csv(self.habits_file)
        updated_habit = None

        for habit in habits:
            if habit["habit_id"] == habit_id:
                if name is not None:
                    habit["name"] = name.strip()
                if frequency is not None:
                    habit["frequency"] = frequency
                if target_goal is not None:
                    habit["target_goal"] = str(target_goal)
                if category is not None:
                    habit["category"] = category.strip()
                if start_date is not None:
                    habit["start_date"] = str(start_date)
                if reminder_time is not None:
                    habit["reminder_time"] = reminder_time
                updated_habit = habit

        self._write_csv(self.habits_file, self.habit_fields, habits)
        return updated_habit

    def remove_habit(self, habit_id):
        """Remove a habit and its completion logs."""
        habits = self._read_csv(self.habits_file)
        logs = self._read_csv(self.logs_file)

        new_habits = [habit for habit in habits if habit["habit_id"] != habit_id]
        new_logs = [log for log in logs if log["habit_id"] != habit_id]

        self._write_csv(self.habits_file, self.habit_fields, new_habits)
        self._write_csv(self.logs_file, self.log_fields, new_logs)
        return len(new_habits) < len(habits)

    def log_completion(self, habit_id, completed_at=None, amount=1, note=""):
        """Record a completion for a habit with a timestamp."""
        if completed_at is None:
            completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log = {
            "log_id": str(uuid.uuid4())[:8],
            "habit_id": habit_id,
            "completed_at": str(completed_at),
            "amount": str(amount),
            "note": note.strip(),
        }

        logs = self._read_csv(self.logs_file)
        logs.append(log)
        self._write_csv(self.logs_file, self.log_fields, logs)
        return log

    def get_logs(self, habit_id=None):
        """Return completion logs. If habit_id is given, return logs for one habit."""
        logs = self._read_csv(self.logs_file)
        if habit_id is not None:
            logs = [log for log in logs if log["habit_id"] == habit_id]
        return logs

    def get_active_habits_for_today(self):
        """Return active habits that the user can log today."""
        return self.get_all_habits(active_only=True)

    def _date_from_log(self, log):
        """Convert a log timestamp into a date object."""
        return datetime.strptime(log["completed_at"][:10], "%Y-%m-%d").date()

    def _period_number(self, some_date, frequency):
        """Convert a date into a simple number for daily, weekly, or monthly streaks."""
        if frequency == "Daily":
            return some_date.toordinal()
        if frequency == "Weekly":
            year, week, _ = some_date.isocalendar()
            return year * 53 + week
        if frequency == "Monthly":
            return some_date.year * 12 + some_date.month
        return some_date.toordinal()

    def _current_period_number(self, frequency):
        """Get the current period number based on today's date."""
        return self._period_number(date.today(), frequency)

    def calculate_current_streak(self, habit_id):
        """Calculate the current streak for one habit."""
        habit = self.find_habit(habit_id)
        if habit is None:
            return 0

        frequency = habit["frequency"]
        logs = self.get_logs(habit_id)
        completed_periods = set()

        for log in logs:
            log_date = self._date_from_log(log)
            completed_periods.add(self._period_number(log_date, frequency))

        current_period = self._current_period_number(frequency)
        streak = 0

        while current_period in completed_periods:
            streak += 1
            current_period -= 1

        return streak

    def calculate_best_streak(self, habit_id):
        """Calculate the best streak ever for one habit."""
        habit = self.find_habit(habit_id)
        if habit is None:
            return 0

        frequency = habit["frequency"]
        logs = self.get_logs(habit_id)
        completed_periods = sorted(set(self._period_number(self._date_from_log(log), frequency) for log in logs))

        if len(completed_periods) == 0:
            return 0

        best_streak = 1
        current_streak = 1

        for index in range(1, len(completed_periods)):
            if completed_periods[index] == completed_periods[index - 1] + 1:
                current_streak += 1
            else:
                current_streak = 1
            best_streak = max(best_streak, current_streak)

        return best_streak

    def calculate_completion_rate(self, habit_id):
        """Calculate completion rate from the habit start date until today."""
        habit = self.find_habit(habit_id)
        if habit is None:
            return 0

        start_date = datetime.strptime(habit["start_date"], "%Y-%m-%d").date()
        today = date.today()
        frequency = habit["frequency"]

        start_period = self._period_number(start_date, frequency)
        current_period = self._period_number(today, frequency)
        expected_periods = max(1, current_period - start_period + 1)

        logs = self.get_logs(habit_id)
        completed_periods = set(self._period_number(self._date_from_log(log), frequency) for log in logs)

        rate = (len(completed_periods) / expected_periods) * 100
        return round(min(rate, 100), 1)

    def get_reward(self, current_streak):
         """Give a simple reward badge based on the current streak."""
         if current_streak >= 30:
             return "Gold Badge"
         if current_streak >= 14:
             return "Silver Badge"
         if current_streak >= 7:
             return "Bronze Badge"
         if current_streak >= 1:
             return "Starter Badge"
         return "No Badge Yet"

    def get_statistics(self):
        """Return streaks, completion rates, and total completions for all habits."""
        statistics = []
        for habit in self.get_all_habits(active_only=True):
            current_streak = self.calculate_current_streak(habit["habit_id"])
            best_streak = self.calculate_best_streak(habit["habit_id"])
            completion_rate = self.calculate_completion_rate(habit["habit_id"])
            total_completions = len(self.get_logs(habit["habit_id"]))

            statistics.append({
                "Habit": habit["name"],
                "Frequency": habit["frequency"],
                "Current Streak": current_streak,
                "Best Streak": best_streak,
                "Completion Rate %": completion_rate,
                "Total Completions": total_completions,
            })

        return statistics

    def get_calendar_view(self, habit_id, days=30):
         """Return a simple calendar-style list showing completed and missed days."""
         logs = self.get_logs(habit_id)
         completed_dates = set(self._date_from_log(log) for log in logs)
    
         calendar_rows = []
         today = date.today()
    
         for number in range(days - 1, -1, -1):
             current_date = today - timedelta(days=number)
             completed = current_date in completed_dates
             calendar_rows.append({
                 "Date": current_date.strftime("%Y-%m-%d"),
                 "Status": "Done" if completed else "Not Done",
                 "Symbol": "✅" if completed else "⬜",
             })
    
         return calendar_rows

