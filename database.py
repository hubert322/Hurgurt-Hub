import sqlite3
from client import User, Mission, Post

def initTable (conn):
    c = conn.cursor ()
    sql = """
    CREATE TABLE IF NOT EXISTS users
    (
        username TEXT PRIMARY KEY NOT NULL,
        displayName TEXT NOT NULL,
        password TEXT NOT NULL,
        rank INTEGER NOT NULL
    )
    """
    c.execute (sql)

    sql = """
    CREATE TABLE IF NOT EXISTS missions
    (
        _id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        rank TEXT NOT NULL,
        reward TEXT NOT NULL
    )
    """
    c.execute (sql)

    sql = """
    CREATE TABLE IF NOT EXISTS posts
    (
        _id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        text TEXT NOT NULL,
        file TEXT NOT NULL,
        author TEXT NOT NULL,
        time TEXT NOT NULL
    )
    """

def login (conn, username, password):
    c = conn.cursor ()
    sql = "SELECT username, displayName, password, rank FROM users WHERE username = ?"
    c.execute (sql, (username,))

    arr = c.fetchall ()

    if len (arr) == 0:
        return -1
    elif password != arr [0][2]:
            return -2
    else:
        return arr

def addUser (conn, user):
    c = conn.cursor ()
    sql = "INSERT INTO users (username, displayName, password, rank) VALUES (?, ?, ?, ?)"
    c.execute (sql, (user.username, user.displayName, user.password, user.rank))

def unique (conn, field, val):
    c = conn.cursor ()
    sql = "SELECT " + field + " FROM users WHERE " + field + " = ?"
    c.execute (sql, (val,))
    arr = c.fetchall ()

    if len (arr) == 0:
        return True
    else:
        return False

def deleteUser (conn, username):
    c = conn.cursor ()
    sql = "DELETE FROM users WHERE username = ?"
    c.execute (sql, (username,))

def updateUser (conn, username, displayName, password, rank):
    c = conn.cursor ()
    sql = "UPDATE users SET displayName = ?, password = ?, rank = ? WHERE username = ?"
    c.execute (sql, (displayName, password, rank, username))

def getUser (conn, username):
    c = conn.cursor ()
    sql = "SELECT username, displayName, password, rank FROM users WHERE username = ?"
    c.execute (sql, (username,))
    arr = c.fetchall ()
    return User (arr [0][0], arr [0][1], arr [0][2], arr [0][3])

def getAllUsers (conn, order):
    c = conn.cursor ()
    sql = "SELECT username, displayName, password, rank FROM users ORDER BY " + order
    if order == "rank":
        sql += " DESC"
    c.execute (sql)
    arr = c.fetchall ()
    return [User (i [0], i [1], i [2], i [3]) for i in arr]

def addMission (conn, mission):
    c = conn.cursor ()
    sql = "INSERT INTO missions (name, description, rank, reward) VALUES (?, ?, ?, ?)"
    c.execute (sql, (mission.name, mission.description, mission.rank, mission.reward))

def deleteMission (conn, name):
    c = conn.cursor ()
    sql = "DELETE FROM missions WHERE name = ?"
    c.execute (sql, (name,))

def getAllMissions (conn, rank, order):
    c = conn.cursor ()
    sql = "SELECT _id, name, description, rank, reward FROM missions"
    if rank != "All":
        sql += " WHERE rank = ? OR rank = 'All'"
    sql += " ORDER BY " + order
    if rank != "All":
        c.execute (sql, (rank,))
    else:
        c.execute (sql)
    arr = c.fetchall ()
    return [Mission (i [0], i [1], i [2], i [3], i [4]) for i in arr]

def addPost (conn, post):
    c = conn.cursor ()
    sql = "INSERT INTO posts (title, text, file, author, time) VALUES (?, ?, ?, ?, ?)"
    c.execute (sql, (post.title, post.text, post.file, post.author, post.time))

def deletePost (conn, _id):
    c = conn.cursor ()
    sql = "DELETE FROM posts WHERE _id = ?"
    c.execute (sql, (_id,))

def getAllPosts (conn):
    c = conn.cursor ()
    sql = "SELECT _id, title, text, file, author, time FROM posts"
    c.execute (sql)
    arr = c.fetchall ()
    return [Post (i [0], i [1], i [2], i [3], i [4], i [5]) for i in arr]

def connect ():
    return sqlite3.connect ("database.db")