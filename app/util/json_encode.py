from json import JSONEncoder
from bson import ObjectId


# GENERATE UNIQUE OBJECTID
class Encode(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)
