import sqlite3
from datetime import date

def start():
    '''
    creates the database tables if they dont exist yet
    :return:
    '''
    conn = sqlite3.connect('mdmd.db')
    cursorObj = conn.cursor()
    cursorObj.execute('''CREATE TABLE IF NOT EXISTS 'users' (
                            'username' TEXT PRIMARY KEY,
                            'password' TEXT,
                            'money' INTEGER)''')

    cursorObj.execute('''CREATE TABLE IF NOT EXISTS 'history' (
                            'username' TEXT,
                            'money' INTEGER,
                            'date' DATE,
                            FOREIGN KEY('username') REFERENCES userss('username'))''')
    conn.commit()
    conn.close()

def add_user(username, password):
    '''
    Adds a newly registered user to the database
    :param username: Username
    :param password: Password
    :return:
    '''
    conn = sqlite3.connect('mdmd.db')
    cursorObj = conn.cursor()

    cursorObj.execute("INSERT INTO users VALUES(:n, :p, 0)", {'n': username, 'p': password})

    conn.commit()
    conn.close()

def get_user(username):
    '''
    searches for the user with the given username
    :param username: username
    :return:
    '''
    conn = sqlite3.connect('mdmd.db')
    cursorObj = conn.cursor()

    cursorObj.execute('SELECT * FROM users WHERE username = :n', {'n': username})
    user = cursorObj.fetchall()
    conn.close()
    return user

def update(username, money):
    '''
    updates the total amount of money the user has and inserts the data of the match into the history table
    :param username: Username
    :param money: Money won in last game
    :return:
    '''
    user = get_user(username)
    new_money = user[0][2] + money

    conn = sqlite3.connect('mdmd.db')
    cursorObj = conn.cursor()

    cursorObj.execute('''UPDATE users
                            SET money = :m
                            WHERE username = :n''', {'m': new_money, 'n': username})

    today = date.today()
    cursorObj.execute("INSERT INTO history VALUES(:n, :m, :d)", {'n': username, 'm': money, 'd': today})

    conn.commit()
    conn.close

def get_history(username):
    '''
    returns the data (username, Amount of Money won, date) of the games the user has played
    :param username: username
    :return:
    '''
    conn = sqlite3.connect('mdmd.db')
    cursorObj = conn.cursor()

    cursorObj.execute('SELECT * FROM history WHERE username = :n', {'n': username})
    hist = cursorObj.fetchall()
    conn.close()

    return hist