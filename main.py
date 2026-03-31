from pawpal_system import Owner, Pet, Task, Schedule, Priority

# --- Owner ---
owner = Owner(name="Alex", email="alex@email.com")

# --- Pets ---
dog = Pet(name="Biscuit", animal="Dog")
cat = Pet(name="Mochi", animal="Cat")

# --- Tasks added intentionally out of order (by duration) ---
dog.add_task(Task(name="Flea treatment",  duration=10, priority=Priority.MEDIUM, frequency="weekly"))
dog.add_task(Task(name="Evening walk",    duration=20, priority=Priority.HIGH,   frequency="daily"))
dog.add_task(Task(name="Morning walk",    duration=30, priority=Priority.HIGH,   frequency="daily"))

cat.add_task(Task(name="Brush coat",      duration=15, priority=Priority.LOW,    frequency="weekly"))
cat.add_task(Task(name="Feeding",         duration=5,  priority=Priority.HIGH,   frequency="daily"))
cat.add_task(Task(name="Litter box",      duration=10, priority=Priority.MEDIUM, frequency="daily"))

# Mark one task complete to demonstrate filtering
dog.tasks[0].mark_complete()  # Flea treatment -> done

# --- Owner + Scheduler ---
owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Schedule(time_budget=90)
for pet in owner.pets:
    scheduler.add_pet(pet)

scheduler.schedule_all_tasks()

# --- 1. Default schedule (priority order) ---
print("=== Today's Schedule (priority order) ===")
print(scheduler.get_schedule_summary())

# --- 2. Sorted by duration, shortest first ---
print("\n=== Sorted by Duration (shortest first) ===")
for e in scheduler.sort_by_time():
    print(f"  {e['pet']:8} | {e['task']:20} | {e['duration']:>3} min")

# --- 3. Sorted by duration, longest first ---
print("\n=== Sorted by Duration (longest first) ===")
for e in scheduler.sort_by_time(reverse=True):
    print(f"  {e['pet']:8} | {e['task']:20} | {e['duration']:>3} min")

# --- 4. Filter: only Biscuit's tasks ---
print("\n=== Biscuit's Tasks Only ===")
for e in scheduler.filter_tasks(pet_name="Biscuit"):
    print(f"  {e['task']:20} | {e['duration']:>3} min | completed: {e['completed']}")

# --- 5. Filter: only pending tasks ---
print("\n=== Pending Tasks Only ===")
for e in scheduler.filter_tasks(completed=False):
    print(f"  {e['pet']:8} | {e['task']:20} | {e['duration']:>3} min")
