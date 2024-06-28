from fastapi import APIRouter,Depends,Body,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app import auth,crud,models,schemas,config
import jwt,hashlib
from jose import JWTError
from datetime import datetime, timedelta



router=APIRouter(
    prefix="/users",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

local_storage=[]
# @router.patch("/login")
# async def login_form(form_data:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db),):
#     user = auth.check_exist_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
#     access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
#     refresh_token_expires = timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS)
#     access_token = auth.create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
#     refresh_token = auth.create_refresh_token(data={"sub":str(user.id)}, expires_delta=refresh_token_expires)
#     crud.update_refresh_token(db, refresh_token,user.id) #update the refresh_token to database
#     return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/login")
async def login_token(form_data:schemas.User_Login, db: Session = Depends(get_db),):
    user = auth.check_exist_user(db, form_data.email_or_phonenumber, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = auth.create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    refresh_token = auth.create_refresh_token(data={"sub":str(user.id)}, expires_delta=refresh_token_expires)

    crud.update_refresh_token(db, refresh_token,user.id) #update the refresh_token to database

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/request_otp")
async def login_to_Otp(form_data:schemas.User_LoginBase, db: Session = Depends(get_db)):
    user = auth.check_exist_user_email(db, form_data.email_or_phonenumber)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email")
    else:
       OTP=config.send_otp_email_for_login(user.email)
       print(OTP)
       expiry_time = datetime.utcnow() + timedelta(minutes=1)
       # hash and save the otp in database
       print(expiry_time)
       crud.update_otp(db,OTP,form_data.email_or_phonenumber,expiry_time)
       return HTTPException(status_code=status.HTTP_200_OK,detail="OTP send")
      
@router.put("/login")
async def verify_otp(otp:schemas.OTP,db:Session=Depends(get_db)):
    user = auth.Check_OTP_valid(db,otp.Otp)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = auth.create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    refresh_token = auth.create_refresh_token(data={"sub": str(user.id)}, expires_delta=refresh_token_expires)

    crud.update_refresh_token(db, refresh_token,user.id) #update the refresh_token to database

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
   
@router.get("/users/me")
async def read_users_me(current_user= Depends(auth.get_current_user)):
    return {"id": current_user.id }

@router.put("/change_password/")
async def change_password(passwords:schemas.change_password,current_user= Depends(auth.get_current_user),db:Session=Depends(get_db)):
     print(passwords.old_password)
     if  not auth.verify_password(passwords.old_password,current_user.password):
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Old password doesn't match!")
     else:
        if passwords.confirm_password != passwords.new_password:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,detail="New passwords and Confirm doesn't match")
        else:
            hash_password=auth.get_password_hash(passwords.new_password)
            user=crud.ResetPassword(db,current_user.id,hash_password)
            return HTTPException(status_code=status.HTTP_202_ACCEPTED,detail="password Change successfully")
        
@router.delete("/logout/")
async def logout(current_user=Depends(auth.get_current_user),db:Session=Depends(get_db)):
    if current_user.id :
        crud.delete_refresh_token(db,current_user.id)
        return {"message":"Successfully Logout"}

@router.post("/refresh_token/")
async def refresh_token(refresh_token:schemas.refresh_Token,db:Session=Depends(get_db)):
    try:
        access_token=auth.get_access_token_use_refresh_token(refresh_token,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return access_token

# @router.get("/data")
# def get_data(a=Depends(auth.permission_checker(["read","user"]))):
#   return {"data": "This is important data"}


