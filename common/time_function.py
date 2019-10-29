import datetime


class GetTime:
    @staticmethod
    def get_yesterday():
        today = datetime.date.today()
        yesterday = today + datetime.timedelta(days=-1)
        yesterday.isoformat()
        return yesterday

    @staticmethod
    def get_today():
        today = datetime.date.today()
        today = str(today)
        return today

    @staticmethod
    def get_tomorrow():
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        tomorrow = str(tomorrow)
        return tomorrow

    @staticmethod
    def get_this_monday():
        today = datetime.date.today()
        this_monday = today - datetime.timedelta(days=today.weekday())
        this_monday.isoformat()
        this_monday = str(this_monday)
        return this_monday

    @staticmethod
    def get_this_sunday():
        today = datetime.date.today()
        this_sunday = today + datetime.timedelta(days=6 - today.weekday())
        this_sunday.isoformat()
        this_sunday = str(this_sunday)
        return this_sunday

    @staticmethod
    def get_next_monday():
        today = datetime.date.today()
        next_monday = today - datetime.timedelta(days=today.weekday() - 7)
        next_monday.isoformat()
        next_monday = str(next_monday)
        return next_monday

    @staticmethod
    def get_next_sunday():
        today = datetime.date.today()
        next_sunday = today + datetime.timedelta(days=6 - today.weekday() + 7)
        next_sunday.isoformat()
        next_sunday = str(next_sunday)
        return next_sunday

    @staticmethod
    def get_next_next_monday():
        today = datetime.date.today()
        next_next_monday = today - datetime.timedelta(days=today.weekday() - 14)
        next_next_monday.isoformat()
        next_next_monday = str(next_next_monday)
        return next_next_monday

    @staticmethod
    def get_next_next_sunday():
        today = datetime.date.today()
        next_next_sunday = today + datetime.timedelta(days=6 - today.weekday() + 14)
        next_next_sunday.isoformat()
        next_next_sunday = str(next_next_sunday)
        return next_next_sunday



