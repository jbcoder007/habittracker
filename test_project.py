from habitlog import Habitlog
from habit import Habit
from db import get_db, log_habit, get_habit_description, list_habits, list_all_streaks, list_1habit_maxstreaks, add_habit, edit_description
from analyse import listallhabits


class Testapp:

    def setup_method(self):
        self.db = get_db("test_db")
        add_habit(self.db, "test_habitname1", "test_description1", "daily", 1, 5)
        log_habit(self.db, "test_habitname1", "2022-09-01 12:00:00")
        log_habit(self.db, "test_habitname1", "2022-09-02 12:00:00")
        log_habit(self.db, "test_habitname1", "2022-09-03 12:00:00")
        log_habit(self.db, "test_habitname1", "2022-09-04 12:00:00")
        log_habit(self.db, "test_habitname1", "2022-08-05 12:00:00")

    def test_add_habit(self):
        habit = Habit("test_habitname3", "test_description3", "daily", 1, 5)
        habit.store_habit(self.db)

    def test_habitlog(self):
        habitlog=Habitlog("test_habitname_3", "2022-09-01 12:00:00")
        habitlog.add_event(self.db)


    def test_get_habit_description(self):
        get_habit_description(self.db, "test_habitname3")

    def test_list_habits(self):
        list_habits(self.db)

    def test_edit_description(self):
        edit_description(self.db, "test_habitname1", "test_description_revised1")



    def test_list_all_streaks(self):
        data = list_all_streaks(self.db)
        assert len(data) == 2

    def test_list_1habit_maxstreaks(self):
        list_1habit_maxstreaks(self.db, "test_habitname1")



    def test_listallhabits(self):
        data = listallhabits(self.db)
        assert len(data) == 1




    def teardown_method(self):
        self.db.close()
        import os
        os.remove("test_db")


