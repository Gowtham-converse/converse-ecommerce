from fastapi import FastAPI,HTTPException,status
from app.routers.users import router as Users_router


app=FastAPI()
app.include_router(Users_router)

@app.get("/")
async def Index():
    return HTTPException(status_code=status.HTTP_100_CONTINUE,detail="Index page")