from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import database, schema, model, utils

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: schema.UserLogin, db: Session = Depends(database.get_db)):

    user = db.query(model.User).filter(model.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    # Create a token
    #return token
    return {"token": "example token"}