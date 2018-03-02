"""Runs the rewards search continuously until all accounts in db reach their daily limit"""

from bingBot import BingBot
from dataLink import DataLink

def main():
    data = DataLink()
    loginCount = data.rowCount()
    for i in range(1,loginCount+1):
        bot = BingBot(i)
        bot.desktop()
        bot.mobile()




if __name__ == "__main__":
    main()
