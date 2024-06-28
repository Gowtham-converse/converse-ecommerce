from datetime import datetime, timedelta
from sqlalchemy import Column,Integer,String,DateTime
from .database import Base,engine
 
class User(Base):
    __tablename__="users"
 
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String, index=True)
    email=Column(String,unique=True ,index=True)
    phone_number=Column(Integer,unique=True,index=True)
    password=Column(String,index=True)
    OTP=Column(String,index=True,nullable=True)
    expires_at = Column(DateTime, nullable=True)
    #created_at = Column(DateTime)
    refresh_token = Column(String, nullable=True)
    is_active=True
Base.metadata.create_all(bind=engine)


# from sqlalchemy import Column, Integer, String, DateTime, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from datetime import datetime

# # SQLite database URL (relative path to your database file)
# DATABASE_URL = "sqlite:///./test.db"

# # Create the SQLAlchemy engine
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# # Create a session maker to interact with the database
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Create a base class for our declarative models
# Base = declarative_base()

# # Define our User model
# class User(Base):
#     __tablename__ = "users"  # Ensure this matches the table name in your database

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     email = Column(String, index=True)
#     phone_number = Column(String, index=True)
#     password = Column(String)
#     OTP = Column(String, nullable=True)
#     expires_at = Column(DateTime, nullable=True)
#     refresh_token = Column(String, nullable=True)

# # Create the tables in the database (this will create 'users' table)
# Base.metadata.create_all(bind=engine)

