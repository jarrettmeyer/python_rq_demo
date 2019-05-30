class TaskResult:

    body: dict = {}
    duration: float = None
    message: str = None
    title: str = None


    def get(self, key: str):
        return self.__dict__.get(key)

    def __init__(self, title=None, message=None, duration=None, **kwargs):
        self.title = title
        self.message = message
        self.duration = duration
        for key in kwargs:
            self.body[key] = kwargs.get(key, None)

    def __repr__(self):
        return '<TaskResult title: {0}>'.format(self.title)
