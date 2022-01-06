from passlib.context import CryptContext
pwd_context = CryptContext(schema=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)