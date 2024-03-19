import uvicorn
from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.endpoints.currency import router as currency_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(currency_router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
