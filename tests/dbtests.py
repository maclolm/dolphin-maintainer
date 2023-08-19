from dbcontroller import DBcontroller

if __name__ == "__main__":
    dbfile = "dolphin-subscribers.db"
    db = DBcontroller(dbfile)
    db.init()
