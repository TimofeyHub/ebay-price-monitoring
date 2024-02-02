from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Collection
from . import crud


async def get_collection_by_id(
    collection_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Collection:
    collection = await crud.get_collection_by_id(
        session=session,
        collection_id=collection_id,
    )
    if collection:
        return collection

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Collection model with id={collection_id} not found",
    )
