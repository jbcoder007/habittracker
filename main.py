import click
import questionary
import datetime
import tabulate


from analyse import listallhabits
from db import get_db
from habit import Habit
from habitlog import Habitlog
from datetime import datetime
from db import list_habits, get_habit_name, get_habit_description, get_habit_periodocity, \
    get_habit_maxeventsperperiod, get_habit_mineventsperperiod, edit_minmaxeventsperperiod, \
     edit_name, edit_description, edit_periodocity, delete_habit, list_all_streaks,  \
    list_habits_by_periodocity, list_all_maxstreaks, list_1habit_streaks, list_1habit_maxstreaks, list_habitlogs, \
    get_habit_createddatetime
from tabulate import tabulate








def switch(action):
    db = get_db()



    if action == 'Create habit':
        print("Let's get started! \n")
        print("Please Note: For habits you want to stop completly e.g. smoking, eneter the minimum and maximum events per period as 0 \n")

        name = click.prompt('Please enter the new habit name', type=str)
        description = click.prompt('Please enter the habit description', type=str)
        periodocity = questionary.select('Please select  the habit periodocity', choices=(['daily', 'weekly', 'monthly',
                                                                                                    'yearly'])).ask()
        mineventsperperiod = click.prompt('Please enter the minimum number of events per period this habit may have (None = 0)', type=click.IntRange(0, None))
        maxeventsperperiod = click.prompt('Please enter the maximum number of events per period this habit may have  (None = 0)', type=click.IntRange(mineventsperperiod, None))
        habit = Habit(name, description, periodocity, mineventsperperiod, maxeventsperperiod)
        habit.store_habit(db)
        print(" \n Habit created \n")

    elif action == 'Log habit':
        class CustomError(Exception):
            "Base class exception for all exceptions of this module"
            pass

        class Nohabitscreated(CustomError):
            """Raised when User trys to log habit without creating any habits"""
        class Logdatebeforecreateddate(CustomError):
            """Raised when User trys to log habit to a date and time before the habit was created"""
        class Logdateaftercurrentdate(CustomError):
            """Raised when User trys to log habit to a date and time after the current date and time"""
            pass
        try:
            listofhabits = list_habits(db)
            listofhabits2 = str(listofhabits)[1:-1]
            listofhabits3 = listofhabits2.replace(" '", "")
            listofhabits4 = listofhabits3.replace("'", "")
            if(len(listofhabits4) == 0):
                raise Nohabitscreated
            else:
                listofhabits = list_habits(db)
                listofhabits2 = str(listofhabits)[1:-1]
                listofhabits3 = listofhabits2.replace(" '", "")
                listofhabits4 = listofhabits3.replace("'", "")
                options = listofhabits4.split(',')

                habitname = questionary.select('Please select the habit you wish to log', choices=(options)).ask()
                event_datetime = questionary.select('Please select when this event happened',
                                                    choices=(['Now', 'Specify'])).ask()
                if event_datetime == "Now":
                    dtnow = datetime.now()
                    habitlog = Habitlog(habitname, dtnow)
                    habitlog.add_event(db)
                elif event_datetime == "Specify":
                    dtentry = click.prompt('Please enter the date and time in the formats YYYY-MM-DD HH:MM:SS'
                                           'or YYYY-MM-DD e.g. 2020-01-01 12:00:00 or just 2020-01-01',
                                           type=click.DateTime(formats=None))
                    try:
                        habitcreateddatetime = get_habit_createddatetime(db, habitname)
                        habitcreateddatetime2 = str(habitcreateddatetime)[2:-3]
                        habitcreateddatetime3 = datetime.strptime(habitcreateddatetime2, '%Y-%m-%d %H:%M:%S')
                        dtentry2 = str(dtentry)
                        dtentry3 = datetime.strptime(dtentry2, '%Y-%m-%d %H:%M:%S')

                        if dtentry3 < habitcreateddatetime3:
                            raise Logdatebeforecreateddate
                        elif dtentry3 > datetime.now():
                            raise Logdateaftercurrentdate
                        else:
                            habitlog = Habitlog(habitname, dtentry)
                            habitlog.add_event(db)


                        print("Habit logged")

                    except Logdatebeforecreateddate:
                        print("You cannot log a habit to a date and time before the habit was created")
                    except Logdateaftercurrentdate:
                        print("You cannot log a habit to a date and time after the current date and time")

        except Nohabitscreated:
            print(" \n No habits created yet. Please create a habit first \n")



    elif action == 'Edit habit':
        class CustomError(Exception):
            "Base class exception for all exceptions of this module"
            pass

        class Nohabitscreated(CustomError):
            """Raised when User trys to log habit without creating any habits"""
            pass
        try:
            listofhabits = list_habits(db)
            listofhabits2 = str(listofhabits)[1:-1]
            listofhabits3 = listofhabits2.replace(" '", "")
            listofhabits4 = listofhabits3.replace("'", "")
            if(len(listofhabits4) == 0):
                raise Nohabitscreated
            else:
                listofhabits = list_habits(db)
                listofhabits2 = str(listofhabits)[1:-1]
                listofhabits3 = listofhabits2.replace(" '", "")
                listofhabits4 = listofhabits3.replace("'", "")
                options = listofhabits4.split(',')

                name = questionary.select('Please select the habit you wish to edit', choices=(options)).ask()
                editaction = questionary.select('Please select a field to edit', choices=(
                    ['Edit name', 'Edit description', 'Edit periodocity',
                     'Edit the minimum and maximum events per period'])).ask()

                if editaction == 'Edit name':
                    currentname = get_habit_name(db, name)
                    currentname2 = str(currentname)[2:-3]
                    print("The Current habit name is: ", currentname2)
                    newname = click.prompt('Please enter the new habit name', type=str)
                    edit_name(db, name, newname)
                elif editaction == 'Edit description':
                    currentdescription = get_habit_description(db, name)
                    currentdescription2 = str(currentdescription)[2:-3]
                    print("The Current description is: ", currentdescription2)
                    newdescription = click.prompt('Please enter the new habit description', type=str)
                    edit_description(db, name, newdescription)
                elif editaction == 'Edit periodocity':
                    currentperiodocity = get_habit_periodocity(db, name)
                    currentperiodocity2 = str(currentperiodocity)[2:-3]
                    print("The Current habit periodocity is: ", currentperiodocity2)
                    newperiodocity = questionary.select('Please type  the new habit periodocity',
                                                        choices=(['daily', 'weekly',
                                                                  'monthly', 'yearly'])).ask()
                    edit_periodocity(db, name, newperiodocity)
                elif editaction == 'Edit the minimum and maximum events per period':
                    currentminevents = get_habit_mineventsperperiod(db, name)
                    currentminevents2 = str(currentminevents)[2:-3]
                    currentmaxevents = get_habit_maxeventsperperiod(db, name)
                    currentmaxevents2 = str(currentmaxevents)[2:-3]
                    print("The Current minimum number of events per period for this habit is: ", currentminevents2)
                    print("The Current maximum number of events per period for this habit is: ", currentmaxevents2)
                    newmin = click.prompt(
                        'Please enter the new minimum number of events per period this habit may have (for none = 0)', type=click.IntRange(0, None))
                    newmax = click.prompt(
                        'Please enter the new maximum number of events per period this habit may have (for none = 0)', type=click.IntRange(newmin, None))
                    edit_minmaxeventsperperiod(db, name, newmin, newmax)

                print("\n Habit edited \n")

        except Nohabitscreated:
            print("\n No habits created yet. Please create a habit first \n")




    elif action == 'Delete habit':
        class CustomError(Exception):
            "Base class exception for all exceptions of this module"
            pass

        class Nohabitscreated(CustomError):
            """Raised when User trys to log habit without creating any habits"""
            pass
        try:
            listofhabits = list_habits(db)
            listofhabits2 = str(listofhabits)[1:-1]
            listofhabits3 = listofhabits2.replace(" '", "")
            listofhabits4 = listofhabits3.replace("'", "")
            if(len(listofhabits4) == 0):
                raise Nohabitscreated
            else:
                listofhabits = list_habits(db)
                listofhabits2 = str(listofhabits)[1:-1]
                listofhabits3 = listofhabits2.replace(" '", "")
                listofhabits4 = listofhabits3.replace("'", "")
                options = listofhabits4.split(',')

                name = questionary.select('Please select the habit you wish to delete', choices=(options)).ask()
                check = questionary.confirm('Are you sure you want to delete this habit?').ask()
                if check == True:
                    delete_habit(db, name)
                    print("\n Habit deleted \n")
                else:
                    print("\n Habit not deleted \n")


        except Nohabitscreated:
            print("\n You have not created any habits yet \n")






    elif action == 'Analyse habit':

        report_choice = questionary.select('Please select the report you wish to run:', choices=(
            ['List All Habits', 'List all Habits with the same periodocity', 'List all streaks for each habit',
             'List all streaks for a specific habit', 'List the longest streak for each habit',
             'List the longest streak for a specific habit'])).ask()

        if report_choice == 'List All Habits':
            class CustomError(Exception):
                "Base class exception for all exceptions of this module"
                pass

            class Nohabitscreated(CustomError):
                """Raised when User trys to log habit without creating any habits"""
                pass

            try:
                listofhabits = list_habits(db)
                listofhabits2 = str(listofhabits)[1:-1]
                listofhabits3 = listofhabits2.replace(" '", "")
                listofhabits4 = listofhabits3.replace("'", "")
                if (len(listofhabits4) == 0):
                    raise Nohabitscreated
                else:
                    result_allhabits = listallhabits(db)
                    print(tabulate(result_allhabits,
                                   headers=['Habit name', 'Description', 'Periodocity', 'Minvents/period',
                                            'MaxEvents/period', 'Created Date'], tablefmt='psql'))

            except Nohabitscreated:
                print("\n No habits created yet. Please create a habit first \n")



        elif report_choice == 'List all Habits with the same periodocity':
            class CustomError(Exception):
                "Base class exception for all exceptions of this module"
                pass

            class Nohabitscreated(CustomError):
                """Raised when User trys to log habit without creating any habits"""
                pass

            try:
                listofhabits = list_habits(db)
                listofhabits2 = str(listofhabits)[1:-1]
                listofhabits3 = listofhabits2.replace(" '", "")
                listofhabits4 = listofhabits3.replace("'", "")
                if (len(listofhabits4) == 0):
                    raise Nohabitscreated
                else:
                    periodchoices = questionary.select('Please select the periodocity you wish to run the report for:',
                                                       choices=(['daily', 'weekly', 'monthly', 'yearly'])).ask()
                    results_habitsbyperiodocity = list_habits_by_periodocity(db, periodchoices)
                    print(tabulate(results_habitsbyperiodocity,
                                   headers=['Habit name', 'Description', 'Periodocity', 'MaxEvents/period',
                                            'MinEvents/period', 'Created Date'], tablefmt='psql'))

            except Nohabitscreated:
                print("\n No habits created yet. Please create a habit first \n")



        elif report_choice == 'List all streaks for each habit':
            class CustomError(Exception):
                "Base class exception for all exceptions of this module"
                pass

            class Nohabitslogged(CustomError):
                """Raised when User trys to log habit without logging any habits"""
                pass

            class Nostreak(CustomError):
                """Raised when User trys to report on streaks without logging any habits"""
                pass

            try:
                listofhabitlog = list_habitlogs(db)
                listofhabitlog2 = str(listofhabitlog)[1:-1]
                listofhabitlog3 = listofhabitlog2.replace(" '", "")
                listofhabitlog4 = listofhabitlog3.replace("'", "")
                if (len(listofhabitlog4) == 0):
                    raise Nohabitslogged
                else:
                    result_allstreaks = list_all_streaks(db)
                    try:
                        if(len(str(result_allstreaks)) < 3):
                            raise Nostreak
                        else:
                            print(tabulate(result_allstreaks,
                                       headers=['Habit name', 'Streak Start Date', 'Streak End Date', 'Streak Length'],
                                       tablefmt='psql'))
                    except Nostreak:
                        print("\n No streaks logged yet. \n")


            except Nohabitslogged:
                print(" \n No habits Logged yet. Please Log a habit first \n")





        elif report_choice == 'List all streaks for a specific habit':
            class CustomError(Exception):
                "Base class exception for all exceptions of this module"
                pass

            class Nohabitslogged(CustomError):
                """Raised when User trys to log habit without logging any habits"""
                pass

            class Nostreaks(CustomError):
                """Raised when User trys to report on streaks without logging any streaks"""
                pass

            try:
                listofhabitlog = list_habitlogs(db)
                listofhabitlog2 = str(listofhabitlog)[1:-1]
                listofhabitlog3 = listofhabitlog2.replace(" '", "")
                listofhabitlog4 = listofhabitlog3.replace("'", "")
                if (len(listofhabitlog4) == 0):
                    raise Nohabitslogged
                else:
                    listofhabits = list_habits(db)
                    listofhabits2 = str(listofhabits)[1:-1]
                    listofhabits3 = listofhabits2.replace(" '", "")
                    listofhabits4 = listofhabits3.replace("'", "")
                    options = listofhabits4.split(',')

                    habitname = questionary.select('Please select the specific habit you wish to Analyse',
                                                   choices=(options)).ask()
                    result_1habitstreaks = list_1habit_streaks(db, habitname)
                    try:
                        if (len(str(result_1habitstreaks)) < 3):
                            raise Nostreaks
                        else:
                            print(tabulate(result_1habitstreaks,
                                           headers=['Habit name', 'Streak Count', 'First Date', 'Last Date'],
                                           tablefmt='psql'))
                    except Nostreaks:
                        print("\n No streaks logged for this habit yet \n")


            except Nohabitslogged:
                print("\n No habits Logged yet. Please Log a habit first \n")




        elif report_choice == 'List the longest streak for each habit':
            class CustomError(Exception):
                "Base class exception for all exceptions of this module"
                pass

            class Nohabitslogged(CustomError):
                """Raised when User trys to report on streaks without logging any habits"""
                pass

            class Nostreaks(CustomError):
                """Raised when User trys to log habit without logging any streaks"""
                pass

            try:
                listofhabitlog = list_habitlogs(db)
                listofhabitlog2 = str(listofhabitlog)[1:-1]
                listofhabitlog3 = listofhabitlog2.replace(" '", "")
                listofhabitlog4 = listofhabitlog3.replace("'", "")
                if (len(listofhabitlog4) == 0):
                    raise Nohabitslogged
                else:
                    result_longeststreaks = list_all_maxstreaks(db)
                    try:
                        if (len(str(result_longeststreaks)) < 3):
                            raise Nostreaks
                        else:
                            print(tabulate(result_longeststreaks,
                                           headers=['Habit name', 'Streak Count', 'First Date', 'Last Date'],
                                           tablefmt='psql'))
                    except Nostreaks:
                        print("\n No streaks logged yet. \n")


            except Nohabitslogged:
                print("\n No habits Logged yet. Please Log a habit first \n")




        elif report_choice == 'List the longest streak for a specific habit':
            class CustomError(Exception):
                "Base class exception for all exceptions of this module"
                pass

            class Nohabitslogged(CustomError):
                """Raised when User trys to log habit without logging any habits"""
                pass

            class Nostreaks(CustomError):
                """Raised when User trys to log habit without logging any habits"""
                pass

            try:
                listofhabitlog = list_habitlogs(db)
                listofhabitlog2 = str(listofhabitlog)[1:-1]
                listofhabitlog3 = listofhabitlog2.replace(" '", "")
                listofhabitlog4 = listofhabitlog3.replace("'", "")
                if (len(listofhabitlog4) == 0):
                    raise Nohabitslogged
                else:
                    listofhabits = list_habits(db)
                    listofhabits2 = str(listofhabits)[1:-1]
                    listofhabits3 = listofhabits2.replace(" '", "")
                    listofhabits4 = listofhabits3.replace("'", "")
                    options = listofhabits4.split(',')

                    habitname = questionary.select('Please select the specific habit you wish to Analyse',
                                                   choices=(options)).ask()
                    result_1habitmaxstreaks = list_1habit_maxstreaks(db, habitname)

                    try:
                        if (len(str(result_1habitmaxstreaks)) < 3):
                            raise Nostreaks
                        else:
                            print(tabulate(result_1habitmaxstreaks,
                                           headers=['Habit name', 'Streak Count', 'First Date', 'Last Date'],
                                           tablefmt='psql'))
                    except Nostreaks:
                        print("\nYou have no Streaks for this habit yet.\n")



            except Nohabitslogged:
                print("\n No habits Logged yet. Please Log a habit first \n")




    elif action=='Quit':
        Exit = click.confirm('Are you sure you want to quit?', abort=False)
        if Exit == True:
            print(" \n Goodbye for now \n")
            exit()
        else:
            print(" \n Returning to main menu \n")









if click.confirm("Welcome to habitracker. THe app that helps you make and break your habits. \n"
                 "Are you ready to start?", default=True):
    stop = False
    while not stop:
        action = questionary.select('Please select an action', choices=(['Create habit', 'Log habit', 'Edit habit',
                                                                            'Delete habit', 'Analyse habit', 'Quit'])).ask()
        switch(action)

else:
    print(" \n Goodbye for now \n")
    exit()





if __name__ == '__main__':
    switch(action)