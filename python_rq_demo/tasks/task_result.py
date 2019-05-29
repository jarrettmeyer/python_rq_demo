class TaskResult:

    duration: float = 0
    message: str = ''
    title: str = ''

    def get(self, key: str):
        return self.toDict().get(key)

    def toDict(self) -> dict:
        return {
            'duration': self.duration,
            'message': self.message,
            'title': self.title,
        }

    def __init__(self, **kwargs):
        self.duration = kwargs.get('duration', 0)
        self.message = kwargs.get('message', '')
        self.title = kwargs.get('title', '')
