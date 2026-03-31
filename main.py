from pawpal_system import Owner, Pet, Task, Schedule, Priority

# --- Owner ---
owner = Owner(name="Alex", email="alex@email.com")

# --- Pets ---
dog = Pet(name="Biscuit", animal="Dog")
cat = Pet(name="Mochi", animal="Cat")

# --- Tasks for Biscuit (dog) ---
dog.add_task(Task(name="Morning walk",    duration=30, priority=Priority.HIGH,   frequency="daily"))
dog.add_task(Task(name="Evening walk",    duration=20, priority=Priority.HIGH,   frequency="daily"))
dog.add_task(Task(name="Flea treatment",  duration=10, priority=Priority.MEDIUM, frequency="weekly"))

# --- Tasks for Mochi (cat) ---
cat.add_task(Task(name="Feeding",         duration=5,  priority=Priority.HIGH,   frequency="daily"))
cat.add_task(Task(name="Litter box",      duration=10, priority=Priority.MEDIUM, frequency="daily"))
cat.add_task(Task(name="Brush coat",      duration=15, priority=Priority.LOW,    frequency="weekly"))

# --- Owner manages both pets ---
owner.add_pet(dog)
owner.add_pet(cat)

# --- Scheduler ---
scheduler = Schedule(time_budget=90)
for pet in owner.pets:
    scheduler.add_pet(pet)

scheduler.schedule_all_tasks()

# --- Print Today's Schedule ---
print(f"Owner: {owner.name} ({owner.email})")
print(f"Pets:  {', '.join(p.name for p in owner.pets)}")
print()
print(scheduler.get_schedule_summary())
