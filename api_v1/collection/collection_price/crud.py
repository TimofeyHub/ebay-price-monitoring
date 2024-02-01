import datetime

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from core.models import CollectionPrice, ScaleModel, Collection, SoldAd
from .schemas import CollectionPriceCreateSchema


async def get_all_prices_by_collection_id(
    session: AsyncSession,
    collection_id: int,
):
    stmt = select(CollectionPrice).where(CollectionPrice.id_collection == collection_id)
    result: Result = await session.execute(stmt)
    prices = result.scalars().all()
    return list(prices)


async def create_collection_price(
    session: AsyncSession,
    collection_price_info: CollectionPriceCreateSchema,
) -> CollectionPrice:
    collection_price = CollectionPrice(**collection_price_info.model_dump())
    session.add(collection_price)
    await session.commit()
    return collection_price


async def calculate_price_by_collection_id(
    session: AsyncSession,
    collection_id: int,
    calculate_interval: int = 90,
    force_calculation: bool = False,
    calculation_lifespan=1,
) -> CollectionPrice:
    # Смотрим, считалась ли цена за последние сутки
    stmt_last_calc = select(CollectionPrice).where(
        CollectionPrice.id == collection_id,
        CollectionPrice.update_date.between(
            datetime.datetime.utcnow() - datetime.timedelta(days=calculation_lifespan),
            datetime.datetime.utcnow(),
        ),
    )
    last_calc_result = await session.execute(stmt_last_calc)
    last_calc = last_calc_result.scalars().first()
    print(last_calc.min_price)
    if last_calc:
        return last_calc

    if force_calculation or not last_calc:
        get_scale_model_id = (
            select(ScaleModel.id)
            .join(Collection, ScaleModel.collections)
            .where(Collection.id == collection_id)
        )

        get_scale_models_min_max_prices = (
            select(
                func.min(SoldAd.price).label("min_price"),
                func.max(SoldAd.price).label("max_price"),
            )
            .where(
                SoldAd.scale_model_id.in_(get_scale_model_id),
                SoldAd.sold_date.between(
                    datetime.datetime.utcnow()
                    - datetime.timedelta(days=calculate_interval),
                    datetime.datetime.utcnow(),
                ),
            )
            .group_by(SoldAd.scale_model_id)
        ).subquery()
        collection_min_max_price = select(
            func.sum(get_scale_models_min_max_prices.c.min_price),
            func.sum(get_scale_models_min_max_prices.c.max_price),
        )
        result = await session.execute(collection_min_max_price)
        min_max_prices = result.first()

        return await create_collection_price(
            session=session,
            collection_price_info=CollectionPriceCreateSchema(
                id_collection=collection_id,
                min_price=min_max_prices[0],
                max_price=min_max_prices[1],
            ),
        )
