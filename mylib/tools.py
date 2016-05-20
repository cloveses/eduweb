import settings

def make_verifytext_key(atext):
    from sha3._sha3 import sha3_512
    atext = sha3_512(atext.encode('utf-8')).hexdigest()
    atext += settings.VERIFY_TEXT_SALT
    atext = sha3_512(atext.encode('utf-8')).hexdigest()
    return atext

def make_password(pw):
    import hashlib
    from settings import PASSWORD_SALT
    pw = hashlib.sha512(pw.encode('utf-8')).hexdigest()
    pw += PASSWORD_SALT
    pw = hashlib.sha512(pw.encode('utf-8')).hexdigest()
    return pw