from db import add_habit



class Habit:

    def __init__( self, Name: str, Description: str, Periodocity: str, Maxeventsperperiod: int, Mineventsperperiod: int):
        self.name = Name
        self.description = Description
        self.periodocity = Periodocity
        self.maxeventsperperiod = Maxeventsperperiod
        self.mineventsperperiod =Mineventsperperiod







    """ 
    Class to add habits to the database

    :param name: the name of the habit
    :param description:  the description of the habit
    :param periodocity: the periodocity of the habit i.e. daily, weekly, monthly, yearly
    :param maxeventsperperiod: the maximum number of events per period
    :param mineventsperperiod: the minimum number of events per period
   
   """



    def store_habit(self, db):
        add_habit(db, self.name, self.description, self.periodocity, self.maxeventsperperiod, self.mineventsperperiod)

    ''''''












