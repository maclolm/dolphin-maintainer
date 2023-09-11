import dbcontroller
import config


def is_owner(func):
    async def wrapper(*args, **kwargs):
        with dbcontroller.DataBaseController(config.dbfile) as db:
            (message,) = args
            sub_id = message.from_user.id
            if (sub_id,) in db.get_owner_ids():
                return await func(message, kwargs['state'])
            return
    return wrapper


def is_sub(func):
    async def wrapper(*args):
        with dbcontroller.DataBaseController(config.dbfile) as db:
            (message,) = args
            sub_id = message.from_user.id
            if (sub_id,) in db.get_sub_ids():
                return await func(*args)
            return
    return wrapper