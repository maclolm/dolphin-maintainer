from dbcontroller import DataBaseController

if __name__ == "__main__":
    dbfile = "dolphin-subscribers.db"
    db = DataBaseController(dbfile)
    db.init()
