import bcrypt

# User Authentication #

# Returns a salted, hashed password
def hash_password(password):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(12)
    return bcrypt.hashpw(password_bytes, salt)

# Takes in a plain text password and a hashed password and returns a boolean
# depending on if they are the same
def compare_password_hash(entered_password, hashed_password):
    password_bytes = entered_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)

# Returns boolean - if password is valid or not:
# 7+ chars, 1 special symbol (!@£$%)
def valid_password(password):
    special_chars = ['!', '@', "£", "$", "%"]
    if len(password) < 7:
        return False
    else:
        has_special = False
        for char in password:
            if char in special_chars:
                has_special = True
        return has_special