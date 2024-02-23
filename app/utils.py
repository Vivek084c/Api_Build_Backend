#import to handle passowrd hashing
from passlib.context import CryptContext
pwd_contenxt=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(passowrd:str):
    return pwd_contenxt.hash(passowrd)