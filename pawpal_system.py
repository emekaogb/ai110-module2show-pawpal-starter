from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Task:
    def __init__(self, name: str, duration: int, priority: Priority, frequency: str):
        """
        Args:
            name: short description of the task (e.g. "Morning walk")
            duration: time in minutes
            priority: Priority enum value
            frequency: how often the task recurs (e.g. "daily", "weekly")
        """
        self.name = name
        self.duration = duration
        self.priority = priority
        self.frequency = frequency
        self.completed = False

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

    def __repr__(self):
        status = "done" if self.completed else "pending"
        return f"Task('{self.name}', {self.duration}min, {self.priority.name}, {status})"


class Pet:
    def __init__(self, name: str, animal: str, image: str = ""):
        self.name = name
        self.animal = animal
        self.image = image
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        """Append a Task to this pet's task list."""
        self.tasks.append(task)

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
                })
                time_used += task.duration

        return self.schedule

    def get_schedule_summary(self) -> str:
        """Return a formatted string of today's scheduled tasks."""
        if not self.schedule:
            return "No tasks scheduled. Run schedule_all_tasks() first."
        lines = [f"Daily Plan ({sum(e['duration'] for e in self.schedule)} min):"]
        for entry in self.schedule:
            lines.append(
                f"  [{entry['priority'].name}] {entry['pet']} — {entry['task']} ({entry['duration']} min)"
            )
        return "\n".join(lines)

    def __repr__(self):
        return f"Schedule({len(self.schedule)} tasks, budget={self.time_budget}min)"
