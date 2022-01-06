from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import model, schema, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

       #hash the password -user.password
    
    hashed_password =  utils.hash(user.password)
    user.password = hashed_password


    new_user = model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
 
@router.get('/{id}', response_model=schema.Userout)
def get_user(id: int, db: Session = Depends(get_db)):
 user = db.query(model.User).filter(model.User.id == id).first()
 if not user:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")

 return user