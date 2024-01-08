from contextlib import asynccontextmanager

import uvicorn

from core.models import Base, db_helper

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static/templates")


@app.get("/")
async def hello_index(request: Request):
    return templates.TemplateResponse(name="home.html", request=request)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
