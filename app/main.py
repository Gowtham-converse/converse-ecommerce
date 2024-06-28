from fastapi import FastAPI
from app.routers.users import router as Users_router


app=FastAPI()
app.include_router(Users_router)

