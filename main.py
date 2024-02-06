from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1 import router as router_v1
from api_v1.auth_demo.config import COOKIE_SESSION_ID_KEY
from api_v1.user import get_user_by_session_id
from core.config import settings, TEMPLATES
from core.models import Base, db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix=settings.api_v1_prefix)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get(f"/")
async def hello_index(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
    if not session_id:
        user = None
    else:
        user = await get_user_by_session_id(
            session=session,
            session_id=session_id,
        )
    return TEMPLATES.TemplateResponse(
        name="home.html",
        context={
            "request": request,
            "user": user,
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
