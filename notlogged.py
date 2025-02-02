def try_logged(session):
    if session.get("is_logged") != True:
        raise NotLoggedError

class NotLoggedError(Exception):
    ...
