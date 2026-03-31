class Owner:
    def __init__(self, name, email, image):
        self.name = name
        self.email = email
        self.image = image


class Task:
    def __init__(self, name, duration, priority, frequency):
        self.name = name
        self.duration = duration
        self.priority = priority
        self.frequency = frequency

    def update_task(self, name=None, duration=None, priority=None, frequency=None):
        if name is not None:
            self.name = name
        if duration is not None:
            self.duration = duration
        if priority is not None:
            self.priority = priority
        if frequency is not None:
            self.frequency = frequency


class Pet:
    def __init__(self, name, animal, image):
        self.name = name
        self.animal = animal
        self.image = image
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def update_pet(self, name=None, animal=None, image=None):
        if name is not None:
            self.name = name
        if animal is not None:
            self.animal = animal
        if image is not None:
            self.image = image


class Schedule:
    def __init__(self):
        self.pets = []
        self.schedule = []

    def schedule_all_tasks(self):
        pass
