from db import  log_habit


class Habitlog:

    def __init__(self,  habitname: str, event_datetime: str):
        """
       class to log events

       :param name: name of the habit
       :param description: description of the habit
       """
        self.habitname = habitname
        self.event_datetime = event_datetime

    def add_event(self, db):
        log_habit(db, self.habitname, self.event_datetime)

