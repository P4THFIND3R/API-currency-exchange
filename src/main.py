import uvicorn
from fastapi import FastAPI, Depends

from src.backend.db_config import get_async_session
from src.repositories.repositories import SessionRepository

app = FastAPI()


@app.get('/1')
async def get(session=Depends(get_async_session)):
    repo = SessionRepository(session)
    result = await repo.find_by_id(2)
    return result


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
