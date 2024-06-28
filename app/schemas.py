from pydantic import BaseModel,EmailStr,Field


class user(BaseModel):
      email:str
      password:str

class User_LoginBase(BaseModel):
      email_or_phonenumber:str
class User_Login(User_LoginBase):
      password:str=Field(...)

class OTP(BaseModel):
      Otp:str

class change_password(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

class refresh_Token(BaseModel):
      refresh_token:str

