import pickledb as pickle

PATH = "resources/"
primary = pickle.load(PATH + "storage.db", False)
secondary = pickle.load(PATH + "authorized.db", False)

def exists(uid: int):
    return primary.get(str(uid)) is not False

def get(uid: int):
    return primary.get(str(uid))

def update(uid: int, value: str):
    uid = str(uid)
    if exists(uid):
        primary.append(uid, ", " + value)
    else:
        primary.set(uid, value)
    primary.dump()

def clear(uid: int):
    primary.rem(str(uid))
    primary.dump()

def is_authorized(uid: int):
    # check if they exist in the secondary db 
    return secondary.get(str(uid)) is not False 

def authorize(uid: int):
    secondary.set(str(uid), True)
    secondary.dump()

def revoke(uid: int):
    secondary.rem(str(uid))
    secondary.dump()