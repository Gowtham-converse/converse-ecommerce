from sqlalchemy.orm import Session
from app.models import User
from datetime import datetime
from app import schemas
import bcrypt
import hashlib


def hash_otp(otp: str):
    salt = bcrypt.gensalt()
    hashed_otp = bcrypt.hashpw(str(otp).encode('utf-8'), salt)
    return hashed_otp

# def create_user(db: Session, email: str, password: str, name: str,phone_number:str):
#     db_user = User(email=email, password=password, name=name,phone_number=phone_number)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#########################
def Check_exist_user_id(db:Session,id:str):
    user=db.query(User).filter(User.id==int(id)).first()
    return user

def Check_user_email(db:Session,email:str):
    user=db.query(User).filter(User.email==email).first()
    return user

def Check_user_Phone_number(db:Session,phone_number:str):
    user=db.query(User).filter(User.phone_number==phone_number).first()
    return user

def update_otp(db: Session, OTP: str, email: str, expiry_time: datetime):
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.OTP = hashlib.sha256(str(OTP).encode()).hexdigest()
        user.expires_at = expiry_time
        db.commit()
        db.refresh(user)
    return user

def update_refresh_token(db:Session,refresh_token:str,id:int):
   
   user=db.query(User).filter(User.id==id).first() 
   if user:
    user. refresh_token=refresh_token
    db.commit()
    db.refresh(user)
   else:
      print("no")
   return user

def Otp_check(db:Session,OTP=str):
   hashed_otp=hashlib.sha256(str(OTP).encode()).hexdigest()
   user=db.query(User).filter(User.OTP==hashed_otp).first()
   return  user

def ResetPassword(db:Session,user_id:int ,hash_Pwd:str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.password = hash_Pwd
        db.commit()
        db.refresh(user)
    return user
def delete_refresh_token(db:Session,user_id:int):
    user=db.query(User).filter(User.id==user_id).first()
    if user:
        user.refresh_token=""
        db.commit()
        db.refresh(user)
        return user

 
