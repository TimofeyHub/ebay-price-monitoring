from typing import Dict
import datetime

from sqlalchemy import func, select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .schemas import CollectionPriceCreateSchema

from core.models import CollectionPrice, ScaleModel, Collection, SoldAd


async def create_collection_price(
    session: AsyncSession,
    collection_price_info: CollectionPriceCreateSchema,
) -> CollectionPrice:
    collection_price = CollectionPrice(**collection_price_info.model_dump())
    session.add(collection_price)
    await session.commit()
    return collection_price


async def calculate_collection_price_by_collection_id(
    session: AsyncSession,
    collection_id: int,
) -> None:
    # stmt = (
    #     select(ScaleModel.id, func.min(SoldAd.price), func.max(SoldAd.price))
    #     .options(selectinload(ScaleModel.collections))
    #     .options(selectinload(ScaleModel.sold_ads))
    #     .where(Collection.id == collection_id)
    #     .where(
    #         SoldAd.sold_date.between(
    #             datetime.datetime.utcnow() - datetime.timedelta(days=90),
    #             datetime.datetime.utcnow(),
    #         )
    #     )
    # )
    row = (
        select(ScaleModel.id)
        .options(selectinload(ScaleModel.collections))
        .where(Collection.id == collection_id)
    )
    result = await session.scalars(row)
    print(result)
