from json import JSONEncoder
from text import TextInput

class TaskidJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TextInput):
            return obj.__dict__

        return JSONEncoder.default(self, obj)
