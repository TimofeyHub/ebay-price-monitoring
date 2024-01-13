from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, SoldAd
from . import crud


async def get_sold_ad_by_id(
    sold_ad_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> SoldAd:
    scale_model = await crud.get_sold_ad(
        session=session,
        sold_ad_id=sold_ad_id,
    )
    if scale_model:
        return scale_model

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Scale model with id={sold_ad_id} not found",
    )
