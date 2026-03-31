from datetime import date, timedelta
from enum import Enum
from itertools import combinations


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Task:
    FREQUENCY_DELTA = {
        "daily": timedelta(days=1),
        "weekly": timedelta(weeks=1),
    }

    def __init__(self, name: str, duration: int, priority: Priority, frequency: str,
                 due_date: date = None):
        """
        Args:
            name: short description of the task (e.g. "Morning walk")
            duration: time in minutes
            priority: Priority enum value
            frequency: how often the task recurs (e.g. "daily", "weekly")
            due_date: the date this task is due (defaults to today)
        """
        self.name = name
        self.duration = duration
        self.priority = priority
        self.frequency = frequency
        self.completed = False
        self.due_date = due_date if due_date is not None else date.today()

    def update_task(self, name=None, duration=None, priority=None, frequency=None):
        """Update any combination of task fields; omitted fields are unchanged."""
        if name is not None:
            self.name = name
        if duration is not None:
            self.duration = duration
        if priority is not None:
            self.priority = priority
        if frequency is not None:
            self.frequency = frequency

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self):
        """Reset this task to pending."""
        self.completed = False

    def next_occurrence(self) -> "Task":
        """Return a fresh pending copy of this task due on its next calculated date."""
        delta = Task.FREQUENCY_DELTA.get(self.frequency)
        next_due = self.due_date + delta if delta else self.due_date
        return Task(self.name, self.duration, self.priority, self.frequency, next_due)

    def __repr__(self):
        status = "done" if self.completed else "pending"
        return f"Task('{self.name}', {self.duration}min, {self.priority.name}, due {self.due_date}, {status})"


class Pet:
    def __init__(self, name: str, animal: str, image: str = ""):
        self.name = name
        self.animal = animal
        self.image = image
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        """Append a Task to this pet's task list."""
        self.tasks.append(task)

    def complete_task(self, task_name: str):
        """Mark a task complete and re-queue it if its frequency is daily or weekly."""
        for task in self.tasks:
            if task.name == task_name and not task.completed:
                task.mark_complete()
                if task.frequency in ("daily", "weekly"):
                    self.tasks.append(task.next_occurrence())
                break

    def remove_task(self, task_name: str):
        """Remove all tasks matching the given name."""
        self.tasks = [t for t in self.tasks if t.name != task_name]

    def get_pending_tasks(self) -> list[Task]:
        """Return only tasks that have not been marked complete."""
        return [t for t in self.tasks if not t.completed]

    def get_tasks_by_priority(self) -> list[Task]:
        """Return all tasks sorted from highest to lowest priority."""
        return sorted(self.tasks, key=lambda t: t.priority.value, reverse=True)

    def update_pet(self, name=None, animal=None, image=None):
        """Update any combination of pet fields; omitted fields are unchanged."""
        if name is not None:
            self.name = name
        if animal is not None:
            self.animal = animal
        if image is not None:
            self.image = image

    def __repr__(self):
        return f"Pet('{self.name}', {self.animal}, {len(self.tasks)} tasks)"


class Owner:
    def __init__(self, name: str, email: str, image: str = ""):
        self.name = name
        self.email = email
        self.image = image
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a Pet to this owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str):
        """Remove all pets matching the given name."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Returns all tasks across every pet as (pet, task) pairs."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]

    def get_pending_tasks(self) -> list[tuple[Pet, Task]]:
        """Returns only incomplete tasks across every pet as (pet, task) pairs."""
        return [(pet, task) for pet in self.pets for task in pet.get_pending_tasks()]

    def __repr__(self):
        return f"Owner('{self.name}', {len(self.pets)} pets)"


class Schedule:
    def __init__(self, time_budget: int = 120):
        """
        Args:
            time_budget: total minutes available for pet care today (default 120)
        """
        self.pets: list[Pet] = []
        self.schedule: list[dict] = []
        self.time_budget = time_budget

    def add_pet(self, pet: Pet):
        """Register a Pet with this scheduler."""
        self.pets.append(pet)

    def schedule_all_tasks(self) -> list[dict]:
        """
        Collects all pending tasks across pets, sorts by priority (high first),
        and fits as many as possible within the time budget.

        Returns a list of scheduled entries:
            {"pet": pet_name, "task": task_name, "duration": minutes, "priority": Priority}
        """
        candidates: list[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.get_pending_tasks():
                candidates.append((pet, task))

        # Sort by priority descending, then by duration ascending (shorter high-priority first)
        candidates.sort(key=lambda x: (-x[1].priority.value, x[1].duration))

        self.schedule = []
        time_used = 0
        for pet, task in candidates:
            if time_used + task.duration <= self.time_budget:
                self.schedule.append({
                    "pet": pet.name,
                    "task": task.name,
                    "duration": task.duration,
                    "priority": task.priority,
                    "completed": task.completed,
                    "start_time": time_used,
                })
                time_used += task.duration

        return self.schedule

    def detect_conflicts(self) -> list[tuple[dict, dict]]:
        """Return all (a, b) pairs from the schedule whose time windows overlap."""
        def overlaps(a, b) -> bool:
            return a["start_time"] < b["start_time"] + b["duration"] \
               and b["start_time"] < a["start_time"] + a["duration"]

        return [(a, b) for a, b in combinations(self.schedule, 2) if overlaps(a, b)]

    def filter_tasks(self, pet_name: str = None, completed: bool = None) -> list[dict]:
        """Filter scheduled tasks by pet name, completion status, or both."""
        results = self.schedule
        if pet_name is not None:
            results = [e for e in results if e["pet"] == pet_name]
        if completed is not None:
            results = [e for e in results if e["completed"] == completed]
        return results

    def sort_by_time(self, reverse: bool = False) -> list[dict]:
        """Sort the current schedule entries by task duration, shortest first by default."""
        self.schedule.sort(key=lambda e: e["duration"], reverse=reverse)
        return self.schedule

    def get_schedule_summary(self) -> str:
        """Return a formatted string of today's scheduled tasks."""
        if not self.schedule:
            return "No tasks scheduled. Run schedule_all_tasks() first."
        lines = [f"Daily Plan ({sum(e['duration'] for e in self.schedule)} min):"]
        for entry in self.schedule:
            lines.append(
                f"  [t={entry['start_time']:>3}min] [{entry['priority'].name}] {entry['pet']} — {entry['task']} ({entry['duration']} min)"
            )
        return "\n".join(lines)

    def __repr__(self):
        return f"Schedule({len(self.schedule)} tasks, budget={self.time_budget}min)"
