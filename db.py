import sqlite3
from datetime import datetime


def get_db(name="main.db"):
    """
    Get a database connection
    :param name: database name=main.db

    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """
    Create the tables in the database if they don't exist yet
    :param db: initialise sqlite3 databsse conenction

    """
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habit (
        Name TEXT PRIMARY KEY, 
        Description TEXT,
        Periodocity TEXT,
        Mineventsperperiod INT,
        Maxeventsperperiod INT,
        CreatedDateTime TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS habitlog (
        habitname TEXT,
        event_datetime TEXT,
        logstatus BOOLEAN,
        FOREIGN KEY (habitname) REFERENCES habit(Name))""")



    db.commit()



def add_habit(db, name, description, periodocity, mineventsperperiod, maxeventsperperiod):
    """
    Add a habit to the database
    :param db: initialise sqlite3 databsse conenction
    :param name: habit name
    :param description: habit description
    :param periodocity: periodocity of the habit
    :param mineventsperperiod: minimum number of events per period
    :param maxeventsperperiod: maximum number of events per period
    :return: None
    """

    cur = db.cursor()
    CreatedDateTime = str(datetime.today())
    cur.execute("INSERT INTO habit VALUES(?, ?, ?, ?, ?, ?)", (name, description,  periodocity, mineventsperperiod,
                                                                   maxeventsperperiod, CreatedDateTime))
    db.commit()


def edit_name(db, name, newname):
    """
    Edit the name of a habit
    :param db: ini
    :param name: Current habit name
    :param newname: New habit name
    :return: None
    """
    cur = db.cursor()
    cur.execute("UPDATE habit SET Name=(?) WHERE Name=(?)", (newname, name))
    cur.execute("UPDATE habitlog SET habitname=? WHERE habitname=?", (newname, name))
    db.commit()

def edit_description(db, name, newdescription):
    """
    Edit the description of a habit
    :param db: initialise sqlite3 databsse connection
    :param name: habit name
    :param newdescription: New Description
    :return: None
    """
    cur = db.cursor()
    cur.execute("UPDATE habit SET Description=? WHERE Name=?", (newdescription, name))
    db.commit()

def edit_periodocity(db, name, newperiodocity):
    """
    Edit the periodocity of a habit
    :param db: initialise sqlite3 database connection
    :param name: habit name
    :param newperiodocity: New habit periodocity
    :return: None
    """
    cur = db.cursor()
    cur.execute("UPDATE habit SET Periodocity=? WHERE Name=?", (newperiodocity, name))
    db.commit()


def edit_minmaxeventsperperiod(db, name, newmin, newmax):
    """
    Edit the minimum and maximum number of  events per period of a habit
    :param db: initialise sqlite3 database connection
    :param name: hab
    :param newmin: New minimum number of events per period
    :param newmax: New maximum number of events per period
    :return: None
    """
    cur = db.cursor()
    cur.execute("UPDATE habit SET Mineventsperperiod=(?), Maxeventsperperiod=(?) WHERE Name=?", (newmin, newmax, name))
    db.commit()

def delete_habit(db, name):
    """
    Delete a habit from both the habit and habitlog tables
    :param db: initialise sqlite3 database connection
    :param name: habit name
    :return: None
    """
    cur = db.cursor()
    cur.execute("DELETE FROM habit WHERE Name=?", (name,))
    cur.execute("DELETE FROM habitlog WHERE habitname=?", (name,))
    db.commit()

def get_habit_name(db, name):
    """
    Get the name of a habit
    :param db: initialise sqlite3 database connection
    :param name: habit name
    :return: habit name
    """
    cur = db.cursor()
    cur.execute("SELECT Name FROM habit where Name=(?)", (name,))
    return cur.fetchall()

def get_habit_description(db, name):
    """
    Get the description of a habit
    :param db: initialise sqlite3 database conection
    :param name: habit
    :return: THe habit description
    """
    cur = db.cursor()
    cur.execute("SELECT Description FROM habit where Name=(?)", (name,))
    return cur.fetchall()


def get_habit_periodocity(db, name):
    """
    Get the periodocity of a habit
    :param db: initialise sqlite3 database connection
    :param name: habit name
    :return: The periodocity of the habit
    """
    cur = db.cursor()
    cur.execute("SELECT Periodocity FROM habit where Name=(?)", (name,))
    return cur.fetchall()

def get_habit_maxeventsperperiod(db, name):
    """
    Get the maximum number of events per period of a habit
    :param db: initialise sqlite3 database connection
    :param name: habit name
    :return: The current maximum number of events per period of a habit
    """
    cur = db.cursor()
    cur.execute("SELECT Maxeventsperperiod FROM habit where Name=(?)", (name,))
    return cur.fetchall()

def get_habit_mineventsperperiod(db, name):
    """
    Get the minimum number of events per period of a habit
    :param db: initialise sqlite3 database connection
    :param name: habit name
    :return: The current minimum number of events per period of a habit
    """
    cur = db.cursor()
    cur.execute("SELECT MinEventsperperiod FROM habit where Name=(?)", (name,))
    return cur.fetchall()

def get_habit_createddatetime(db, name):
    """
    Get the date and time a habit was created
    :param db: initialise sqlite3 database connection
    :param name: habit name
    :return: THe date and time the habit was created
    """
    cur = db.cursor()
    cur.execute("SELECT datetime(CreatedDateTime) FROM habit where Name=(?)", (name,))
    return cur.fetchone()


def log_habit(db, habitname, event_datetime):
    """
    Log a habit event
    :param db: initialise sqlite3 database connection
    :param habitname: habit name
    :param event_datetime: THe date and time of the event being logged
    :return: None
    """
    cur = db.cursor()
    logstatus = 1
    cur.execute("INSERT INTO habitlog VALUES (?, ?, ?)", (habitname, event_datetime, logstatus))
    db.commit()





def list_habits(db):
    """
    List all habits Names
    :param db: intialise sqlite3 database connection
    :return: List of all habit names
    """
    cur = db.cursor()
    query=("SELECT Name FROM habit")
    r_set = cur.execute(query)
    my_list = [r for r, in r_set]
    return (my_list)

def list_habitlogs(db):
    """
    List the each logged event's habit name
    :param db: initialise sqlite3 database connection
    :return: List of each event's habit name
    """
    cur = db.cursor()
    query=("SELECT habitname FROM habitlog")
    r_set = cur.execute(query)
    my_habitloglist = [r for r, in r_set]
    return (my_habitloglist)

def list_all_habits(db):
    """
    List all the details of habits currently stored in the database
    :param db: initialise sqlite3 database connection
    :return: List of all the details of habits currently stored in the database
    """
    cur = db.cursor()
    cur.execute("SELECT Name, Description, Periodocity, Mineventsperperiod, Maxeventsperperiod, date(CreatedDatetime)  FROM habit")
    return cur.fetchall()

def list_habits_by_periodocity(db, periodocity):
    """
    List all the details of habits currently stored in the database with a selected periodicity
    :param db: initialise sqlite3 database connection
    :param periodocity:
    :return:
    """
    cur = db.cursor()
    cur.execute("SELECT Name, Description, Periodocity, Maxeventsperperiod, Mineventsperperiod, date(CreatedDatetime)  FROM habit where Periodocity = (?)", (periodocity,))
    return cur.fetchall()






def list_all_streaks(db):
    """
    List all the streaks of all habits
    :param db: initialise sqlite3 database connection
    :return: List of all the streaks of all habits
    """

    cur = db.cursor()
    cur.execute("""with groups(habitname, Period,  grp, mindate, maxdate) AS (select habitname,
                                              Period,
                                              (Period + 1) - dense_rank() over (partition by habitname order by  Period) as  grp, mindate, maxdate
                                       from (select C.habitname, C.Periodocity, C.Period, C.count, C.mindate, C.maxdate
                                             from (select B.habitname,
                                                          B.Periodocity,
                                                          B.Period,
                                                          sum(B.logstatus) AS 'count',
                                                        min(B.Date) as mindate,
                                                        max(B.Date) as maxdate

                                                   from (SELECT A.habitname,
                                                                A.Periodocity,
                                                                date(A.event_datetime) AS 'Date',
                                                                floor(A.Interval / A.Intduration) AS Period,
                                                                A.logstatus
                                                         from (select habitname,
                                                                      event_datetime,
                                                                      CreatedDateTime,
                                                                      Periodocity,
                                                                      CASE
                                                                          when periodocity = 'daily' then 1
                                                                          when periodocity = 'weekly' then 7
                                                                          when periodocity = 'monthly' then 30
                                                                          when periodocity = 'yearly' then 365
                                                                          else 0
                                                                          end                                                           AS Intduration,
                                                                      (JULIANDAY(habitlog.event_datetime) - JULIANDAY(CreatedDateTime)) AS Interval,
                                                                      logstatus
                                                               FROM (select * from habitlog
                                                                                   Union all
                                                                                   select Name as 'habitname', Z.event_datetime, 0 as 'logstatus' from habit,   (
                                                                    WITH RECURSIVE
                                                                      cnt(x) AS (
                                                                         SELECT 0
                                                                         UNION ALL
                                                                         SELECT x+1 FROM cnt, habit
                                                                          LIMIT (SELECT floor((((JulianDAY('now', 'localtime')) - (julianday(min(CreatedDateTime)))))) from habit) +1  )
                                                                    
                                                                    SELECT DISTINCT date(julianday((habit.CreatedDateTime)), '+' || x || ' days') as event_datetime FROM cnt, habit) Z
                                                                    where date(Z.event_datetime) <= date('now', 'localtime') and date(Z.event_datetime) >= date(createddatetime)) habitlog,
                                                                    habit
                                                               where habitlog.habitname = habit.Name) A) B
                                                   Group By B.habitname, B.Periodocity, B.Period) C,
                                                  habit
                                             where C.habitname = habit.Name
                                               and count >= habit.MinEventsperperiod
                                               and count <= habit.MaxEventsperperiod))
select
        groups.habitname,
        count (groups.habitname) as streak_count,
        min(groups.mindate) as min_date,
        max(groups.maxdate) as max_date

        from groups

Group By grp, groups.habitname
Order By 1 desc, 2 desc;""")
    return cur.fetchall()

def list_1habit_streaks(db, habitname):

    """
    List all the streaks of a selected habit
    :param db: initialise sqlite3 database connection
    :param habitname: habit name
    :return: list of all the streaks of a selected habit
    """

    cur = db.cursor()
    cur.execute("""with groups(habitname, Period,  grp, mindate, maxdate) AS (select habitname,
                                              Period,
                                              (Period + 1) - dense_rank() over (partition by habitname order by  Period) as  grp, mindate, maxdate
                                       from (select C.habitname, C.Periodocity, C.Period, C.count, C.mindate, C.maxdate
                                             from (select B.habitname,
                                                          B.Periodocity,
                                                          B.Period,
                                                          sum(B.logstatus) AS 'count',
                                                        min(B.Date) as mindate,
                                                        max(B.Date) as maxdate

                                                   from (SELECT A.habitname,
                                                                A.Periodocity,
                                                                date(A.event_datetime) AS 'Date',
                                                                floor(A.Interval / A.Intduration) AS Period,
                                                                A.logstatus
                                                         from (select habitname,
                                                                      event_datetime,
                                                                      CreatedDateTime,
                                                                      Periodocity,
                                                                      CASE
                                                                          when periodocity = 'daily' then 1
                                                                          when periodocity = 'weekly' then 7
                                                                          when periodocity = 'monthly' then 30
                                                                          when periodocity = 'yearly' then 365
                                                                          else 0
                                                                          end                                                           AS Intduration,
                                                                      (JULIANDAY(habitlog.event_datetime) - JULIANDAY(CreatedDateTime)) AS Interval,
                                                                      logstatus
                                                               FROM (select * from habitlog
                                                                                   Union all
                                                                                   select Name as 'habitname', Z.event_datetime, 0 as 'logstatus' from habit,   (
                                                                    WITH RECURSIVE
                                                                      cnt(x) AS (
                                                                         SELECT 0
                                                                         UNION ALL
                                                                         SELECT x+1 FROM cnt, habit
                                                                          LIMIT (SELECT floor((((JulianDAY('now', 'localtime')) - (julianday(min(CreatedDateTime)))))) from habit) +1  )

                                                                    SELECT DISTINCT date(julianday((habit.CreatedDateTime)), '+' || x || ' days') as event_datetime FROM cnt, habit) Z
                                                                    where date(Z.event_datetime) <= date('now', 'localtime') and date(Z.event_datetime) >= date(createddatetime)) habitlog,
                                                                    habit
                                                               where habitlog.habitname = habit.Name) A) B
                                                   Group By B.habitname, B.Periodocity, B.Period) C,
                                                  habit
                                             where C.habitname = habit.Name
                                               and count >= habit.MinEventsperperiod
                                               and count <= habit.MaxEventsperperiod))
select
        groups.habitname,
        count (groups.habitname) as streak_count,
        min(groups.mindate) as min_date,
        max(groups.maxdate) as max_date

        from groups
        
where groups.habitname = (?)
Group By grp, groups.habitname
Order By 1 desc, 2 desc;""", (habitname,))
    return cur.fetchall()

def list_all_maxstreaks(db):
    """
    List  the longest streaks of each habit
    :param db: initialise sqlite3 database connection
    :return: lists the longest streaks of each habit
    """
    cur = db.cursor()
    cur.execute("""Select E.habitname, Max(E.streak_count), E.min_date, E.max_date from (with groups(habitname, Period,  grp, mindate, maxdate) AS (select habitname,
                                              Period,
                                              (Period + 1) - dense_rank() over (partition by habitname order by  Period) as  grp, mindate, maxdate
                                       from (select C.habitname, C.Periodocity, C.Period, C.count, C.mindate, C.maxdate
                                             from (select B.habitname,
                                                          B.Periodocity,
                                                          B.Period,
                                                          sum(B.logstatus) AS 'count',
                                                        min(B.Date) as mindate,
                                                        max(B.Date) as maxdate

                                                   from (SELECT A.habitname,
                                                                A.Periodocity,
                                                                date(A.event_datetime) AS 'Date',
                                                                floor(A.Interval / A.Intduration) AS Period,
                                                                A.logstatus
                                                         from (select habitname,
                                                                      event_datetime,
                                                                      CreatedDateTime,
                                                                      Periodocity,
                                                                      CASE
                                                                          when periodocity = 'daily' then 1
                                                                          when periodocity = 'weekly' then 7
                                                                          when periodocity = 'monthly' then 30
                                                                          when periodocity = 'yearly' then 365
                                                                          else 0
                                                                          end                                                           AS Intduration,
                                                                      (JULIANDAY(habitlog.event_datetime) - JULIANDAY(CreatedDateTime)) AS Interval,
                                                                      logstatus
                                                               FROM (select * from habitlog
                                                                                   Union all
                                                                                   select Name as 'habitname', Z.event_datetime, 0 as 'logstatus' from habit,   (
                                                                    WITH RECURSIVE
                                                                      cnt(x) AS (
                                                                         SELECT 0
                                                                         UNION ALL
                                                                         SELECT x+1 FROM cnt, habit
                                                                          LIMIT (SELECT floor((((JulianDAY('now', 'localtime')) - (julianday(min(CreatedDateTime)))))) from habit) +1  )

                                                                    SELECT DISTINCT date(julianday((habit.CreatedDateTime)), '+' || x || ' days') as event_datetime FROM cnt, habit) Z
                                                                    where date(Z.event_datetime) <= date('now', 'localtime') and date(Z.event_datetime) >= date(createddatetime)) habitlog,
                                                                    habit
                                                               where habitlog.habitname = habit.Name) A) B
                                                   Group By B.habitname, B.Periodocity, B.Period) C,
                                                  habit
                                             where C.habitname = habit.Name
                                               and count >= habit.MinEventsperperiod
                                               and count <= habit.MaxEventsperperiod))
select
        groups.habitname,
        count (groups.habitname) as streak_count,
        min(groups.mindate) as min_date,
        max(groups.maxdate) as max_date

        from groups
        
Group By grp, groups.habitname
Order By 1 desc, 2 desc) E
Group By habitname
Order By habitname;""")
    return cur.fetchall()


def list_1habit_maxstreaks(db, habitname):
    """
    List  the longest streaks of a specific habit
    :param db: initialise sqlite3 database connection
    :param habitname: habit name
    :return: lists the longest streaks of a specific habit
    """
    cur = db.cursor()
    cur.execute("""Select E.habitname, Max(E.streak_count), E.min_date, E.max_date from (with groups(habitname, Period,  grp, mindate, maxdate) AS (select habitname,
                                              Period,
                                              (Period + 1) - dense_rank() over (partition by habitname order by  Period) as  grp, mindate, maxdate
                                       from (select C.habitname, C.Periodocity, C.Period, C.count, C.mindate, C.maxdate
                                             from (select B.habitname,
                                                          B.Periodocity,
                                                          B.Period,
                                                          sum(B.logstatus) AS 'count',
                                                        min(B.Date) as mindate,
                                                        max(B.Date) as maxdate

                                                   from (SELECT A.habitname,
                                                                A.Periodocity,
                                                                date(A.event_datetime) AS 'Date',
                                                                floor(A.Interval / A.Intduration) AS Period,
                                                                A.logstatus
                                                         from (select habitname,
                                                                      event_datetime,
                                                                      CreatedDateTime,
                                                                      Periodocity,
                                                                      CASE
                                                                          when periodocity = 'daily' then 1
                                                                          when periodocity = 'weekly' then 7
                                                                          when periodocity = 'monthly' then 30
                                                                          when periodocity = 'yearly' then 365
                                                                          else 0
                                                                          end                                                           AS Intduration,
                                                                      (JULIANDAY(habitlog.event_datetime) - JULIANDAY(CreatedDateTime)) AS Interval,
                                                                      logstatus
                                                               FROM (select * from habitlog
                                                                                   Union all
                                                                                   select Name as 'habitname', Z.event_datetime, 0 as 'logstatus' from habit,   (
                                                                    WITH RECURSIVE
                                                                      cnt(x) AS (
                                                                         SELECT 0
                                                                         UNION ALL
                                                                         SELECT x+1 FROM cnt, habit
                                                                          LIMIT (SELECT floor((((JulianDAY('now', 'localtime')) - (julianday(min(CreatedDateTime)))))) from habit) +1  )

                                                                    SELECT DISTINCT date(julianday((habit.CreatedDateTime)), '+' || x || ' days') as event_datetime FROM cnt, habit) Z
                                                                    where date(Z.event_datetime) <= date('now', 'localtime') and date(Z.event_datetime) >= date(createddatetime)) habitlog,
                                                                    habit
                                                               where habitlog.habitname = habit.Name) A) B
                                                   Group By B.habitname, B.Periodocity, B.Period) C,
                                                  habit
                                             where C.habitname = habit.Name
                                               and count >= habit.MinEventsperperiod
                                               and count <= habit.MaxEventsperperiod))
select
        groups.habitname,
        count (groups.habitname) as streak_count,
        min(groups.mindate) as min_date,
        max(groups.maxdate) as max_date

        from groups
        
Group By grp, groups.habitname
Order By 1 desc, 2 desc) E
where habitname = (?)
Group By habitname
Order By habitname;""", (habitname,))
    return cur.fetchall()






