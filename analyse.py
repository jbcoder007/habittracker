from db import get_habit_data, list_habits, list_all_habits




def listallhabits(db):
    """
    list all the habits in the db
    :param db: initialise sqlite3 databsse conenction
    :return: list of all the habits in the db
    """
    return list_all_habits(db)



