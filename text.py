from taskid_input import TaskidInput

class TextInput(TaskidInput):
    def __init__(self, id, label, default=None, placeholder=None):
        super().__init__(id, label, "text", default, placeholder)
