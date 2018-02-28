from bingBot import BingBot
from userAccounts import DataLink

def main():
    data = DataLink()
    loginCount = data.rowCount()
    for i in range(1,loginCount+1):
        bot = BingBot(i)
        bot.desktop()
        bot.mobile()




if __name__ == "__main__":
    main()