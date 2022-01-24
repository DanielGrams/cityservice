import datetime
from json import JSONEncoder

from project.dateutils import berlin_tz


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return (obj.astimezone(berlin_tz)).isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
