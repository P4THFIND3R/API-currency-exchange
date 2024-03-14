import uvicorn
from fastapi import FastAPI

from src.auth.router import auth_router

app = FastAPI()
app.include_router(auth_router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
