from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, ScaleModel
from . import crud


async def get_scale_model_by_id(
    scale_model_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ScaleModel:
    scale_model = await crud.get_scale_model(
        session=session,
        scale_model_id=scale_model_id,
    )
    if scale_model:
        return scale_model

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Scale model with id={scale_model_id} not found",
    )
