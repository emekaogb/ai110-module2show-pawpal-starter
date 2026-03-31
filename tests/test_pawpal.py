from datetime import date, timedelta
from pawpal_system import Pet, Task, Priority, Schedule


def test_mark_complete_changes_status():
    task = Task(name="Morning walk", duration=30, priority=Priority.HIGH, frequency="daily")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", animal="Dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task(name="Feeding", duration=5, priority=Priority.MEDIUM, frequency="daily"))
    assert len(pet.tasks) == 1


def test_sort_by_time_returns_ascending_order():
    pet = Pet(name="Biscuit", animal="Dog")
    pet.add_task(Task(name="Bath",         duration=40, priority=Priority.LOW,    frequency="weekly"))
    pet.add_task(Task(name="Morning walk", duration=30, priority=Priority.HIGH,   frequency="daily"))
    pet.add_task(Task(name="Feeding",      duration=5,  priority=Priority.MEDIUM, frequency="daily"))

    scheduler = Schedule(time_budget=120)
    scheduler.add_pet(pet)
    scheduler.schedule_all_tasks()
    sorted_entries = scheduler.sort_by_time()

    durations = [e["duration"] for e in sorted_entries]
    assert durations == sorted(durations)


def test_complete_daily_task_creates_next_day_occurrence():
    today = date.today()
    pet = Pet(name="Mochi", animal="Cat")
    pet.add_task(Task(name="Feeding", duration=5, priority=Priority.HIGH, frequency="daily", due_date=today))

    pet.complete_task("Feeding")

    assert pet.tasks[0].completed is True
    assert len(pet.tasks) == 2
    assert pet.tasks[1].due_date == today + timedelta(days=1)
    assert pet.tasks[1].completed is False


def test_detect_conflicts_flags_overlapping_tasks():
    pet = Pet(name="Biscuit", animal="Dog")
    pet.add_task(Task(name="Morning walk", duration=30, priority=Priority.HIGH,   frequency="daily"))
    pet.add_task(Task(name="Feeding",      duration=10, priority=Priority.MEDIUM, frequency="daily"))

    scheduler = Schedule(time_budget=120)
    scheduler.add_pet(pet)
    scheduler.schedule_all_tasks()

    # Force both tasks to start at the same time to create a conflict
    scheduler.schedule[0]["start_time"] = 0
    scheduler.schedule[1]["start_time"] = 0

    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    names = {conflicts[0][0]["task"], conflicts[0][1]["task"]}
    assert names == {"Morning walk", "Feeding"}
