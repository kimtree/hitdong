import datetime

import dateutil.tz


def get_yesterday():
    now = datetime.datetime.now(dateutil.tz.tzlocal())
    yesterday = now - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)

    return yesterday
