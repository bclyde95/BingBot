import sqlite3

class DataLink:
    """Provides link to database and functions to get and set fields"""

    def __init__(self):
        """Initializes the database connection and cursor for executing queries"""
        self._db = sqlite3.connect("accounts.db")
        self._cur = self._db.cursor()

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
            print("FAILED!!!!! Points was not a valid input value")






d = DataLink()

print(d.getLogin(0))
print(d.getPoints(0))
d.setPoints(0,3500)
print(d.getPoints(0))
print(d.getTimes(0))
d.setTimes(0,0)
print(d.getTimes(0))
print(d.getRow(0))