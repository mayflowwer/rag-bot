import os
from pathlib import Path
from init import init
from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, vectorstore
    client, vectorstore = init()
    app.state.client = client
    app.state.vectorstore = vectorstore
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
