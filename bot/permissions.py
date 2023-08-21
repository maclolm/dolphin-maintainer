import dbcontroller
import config


# TODO: подумать над (db = dbcontroller.DBcontroller(config.dbfile))
def is_owner(func):
    async def wrapper(*args):
        db = dbcontroller.DBcontroller(config.dbfile)
        (message,) = args
        sub_id = message.from_user.id
        if (sub_id,) in db.get_owner_ids():
            return await func(*args)
        return
    return wrapper


def is_sub(func):
    async def wrapper(*args):
        db = dbcontroller.DBcontroller(config.dbfile)
        (message,) = args
        sub_id = message.from_user.id
        if (sub_id,) in db.get_sub_ids():
            return await func(*args)
        return
    return wrapper