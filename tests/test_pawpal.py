from pawpal_system import Pet, Task, Priority


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
