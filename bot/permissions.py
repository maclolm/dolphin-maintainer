import dbcontroller
import config


# TODO: # TODO: https://ru.stackoverflow.com/questions/1301538/%D0%94%D0%B5%D0%BA%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80-%D0%B4%D0%BB%D1%8F-%D0%B1%D0%B4-python?ysclid=lllbwiy9rb775824071
# TODO: закрывать в декораторах подключение к бд (если оно не закрывается, проверить)
def is_owner(func):
    async def wrapper(*args, **kwargs):
        db = dbcontroller.DBcontroller(config.dbfile)
        (message,) = args
        sub_id = message.from_user.id
        if (sub_id,) in db.get_owner_ids():
            return await func(message, kwargs['state'])
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