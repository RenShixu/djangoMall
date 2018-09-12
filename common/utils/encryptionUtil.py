import hashlib

def getencodepassword(password):
    m = hashlib.md5()
    m.update(bytes(password,encoding='utf8'))
    return m.hexdigest()