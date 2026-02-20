import bcrypt

salt = bcrypt.gensalt()

def hashPassword(password):

    hashed = bcrypt.hashpw(password, salt)

    return hashed

def checkPassword(entered_passw, hashed_passw):
    if bcrypt.checkpw(entered_passw, hashed_passw):
        return True
    else:
        return False