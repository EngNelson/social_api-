from jose import JWSError, jwt
from datetime import datetime, timedelta
from .. import schema
from fastapi import Depends, status, HTTPException 
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#Algorithm
#Expriation time

SECRET_KEY = "hdsanoorjc038fcnbndfjejmc8847hffndpkl057cnbazxdjdlck498dnsnm"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str =  payload.get("user_id")

        if id is None:
          raise credentials_exception

        token_data = schema.TokenData(id=id)
    except JWSError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)