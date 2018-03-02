"""Provides link to interact safely with the database"""

import sqlite3

class DataLink:
    """A class to access fields from database and functions to get and set fields"""

    def __init__(self):
        """Initializes the database connection and cursor for executing queries"""
        self._db = sqlite3.connect("accounts.db")
        self._cur = self._db.cursor()

    def rowCount(self):
        """Returns the row count from the database"""
        self._cur.execute("select count(*) from accounts")
        return int(self._cur.fetchone()[0])

    def getRow(self, id):
        """Gets the row from the db and returns a tuple"""
        self._cur.execute("select * from accounts where id=?", str(id))
        rowTuple = self._cur.fetchall()[0]
        return dict(id=rowTuple[0], email=rowTuple[1], password=rowTuple[2], points=int(rowTuple[3]), timesRedeemed=int(rowTuple[4]))

    def getLogin(self, id):
        """Gets login email and password from the db and returns a tuple"""
        self._cur.execute("select email,password from accounts where id=?", str(id))
        loginTuple = self._cur.fetchall()[0]
        return dict(email=loginTuple[0], password=loginTuple[1])

    def getPoints(self, id):
        """Gets point amount from db and returns the int amount"""
        self._cur.execute("select points from accounts where id=?", str(id))
        return int(self._cur.fetchall()[0][0])

    def setPoints(self, id, points):
        """Takes a new point amount in and updates the field"""
        try:
            val = int(points)
            dbIn = (str(val), str(id))
            self._cur.execute("update accounts set 'points'=? where id=?",dbIn)
            self._db.commit()
        except Exception:
            print("FAILED!!!!! Points was not a valid input value")

    def getTimes(self, id):
        """Gets the Times Redeemed from the db and returns the int amount"""
        self._cur.execute("select timesRedeemed from accounts where id=?", str(id))
        return int(self._cur.fetchall()[0][0])

    def setTimes(self, id, times):
        """Takes a new times redeemed amount in and updates the field"""
        try:
            val = int(times)
            dbIn = (str(val), str(id))
            self._cur.execute("update accounts set 'timesRedeemed'=? where id=?",dbIn)
            self._db.commit()
        except Exception:
            print("FAILED!!!!! Times was not a valid input value")

    def getTwitterLogin(self):
        """Gets twitter api info from the database and returns a tuple"""
        self._cur.execute("select * from twitterApi")
        res = self._cur.fetchall()[0]
        return dict(consumer_key=res[0], consumer_secret=res[1], access_token=res[2], access_secret=res[3])

    def __del__(self):
        """Closes the cursor and db connection upon destruction of the instance"""
        self._cur.close()
        self._db.close()
