import bcrypt
import hashlib
import base64

# TODO: convert this to use native bcrypt functions for hashing and validation


# generates random characters to use as salt default is 64
def generate_nonce(length=64):
    salt = ""
    while len(salt) < length:
        salt += hashlib.sha3_256(str(bcrypt.gensalt()).encode('utf-8')).hexdigest()
    return salt[0:length]


# hashes password with salt
def hash_password(password, salt):
    return hashlib.sha3_256(str(salt + password).encode('utf-8')).hexdigest()


# checks the password vs the hashed password
def bc_hashpw(pword, as_string=True, gensalt_rounds=12):
    # en_pword = pword.encode('utf-8')
    # hashed_encoded = hashlib.sha256(en_pword).digest()
    # b64_en = base64.b64encode(hashed_encoded)

    normalized = normalize_password(pword).encode('utf-8')

    hashed = bcrypt.hashpw(normalized, bcrypt.gensalt(gensalt_rounds))
    if as_string:
        return str(hashed, 'utf-8')
    else:
        return hashed


def bc_checkpw(pword, pw_hash):
    if type(pw_hash) == str:
        pw_hash = pw_hash.encode('utf-8')
    normalized = normalize_password(pword).encode('utf-8')
    return bcrypt.checkpw(normalized, pw_hash)


def normalize_password(password):
    if type(password) == bytes:
        password = str(password, 'utf-8')
    encoded_password = password.encode('utf-8')
    hashed_encoded = hashlib.sha256(encoded_password).digest()
    b64_encoded = base64.b64encode(hashed_encoded)
    return str(b64_encoded, 'utf-8')


# TODO needs to be adjusted to not need alchemy
# TODO wont work until get_user(user) is fixed
# compares stored hash with newly generated hash
# def check_hash(user, password):
#     usr = get_user(user)
#     salt = usr.salt
#     if hash_password(password, salt) == usr.hash:
#         return True
#     else:
#         return False


# TODO needs to be adjusted to not need alchemy
# tests if user is in the database
# def user_exists(uname):
#     count = pyBook.models.User.query.filter_by(user_name=uname).count()
#     if count == 1:
#         return True
#     else:
#         return False


# TODO needs to be adjusted to not need alchemy
# gets user object
# def get_user(uname):
#     return pyBook.models.User.query.filter_by(user_name=uname).first()

# if __name__ == '__main__':
#     hashed = bc_hashpw("test password")
#     print(bc_checkpw("test password", hashed))
