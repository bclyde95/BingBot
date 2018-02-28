import sqlite3

class DataLink:
    """Provides link to database and functions to get and set fields"""

    def __init__(self):
        """Initializes the database connection and cursor for executing queries"""
        self._db = sqlite3.connect("accounts.db")
        self._cur = self._db.cursor()

    def getCount(self):
        """Returns the row count from the database"""
        self._cur.execute("select count(*) from accounts")
        count = int(self._cur.fetchone()[0])
        return count

    def getRow(self, id):
        """Gets the row from the db and returns a tuple"""
        self._cur.execute("select * from accounts where id=?", str(id))
        res = self._cur.fetchall()
        return res[0]

    def getLogin(self, id):
        """Gets login email and password from the db and returns a tuple"""
        self._cur.execute("select email,password from accounts where id=?", str(id))
        res = self._cur.fetchall()
        return res[0]

    def getPoints(self, id):
        """Gets point amount from db and returns the int amount"""
        self._cur.execute("select points from accounts where id=?", str(id))
        res = self._cur.fetchall()
        return int(res[0][0])

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
        res = self._cur.fetchall()
        return int(res[0][0])

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
        return self._cur.fetchall()[0]

    def __del__(self):
        self._cur.close()
        self._db.close()
