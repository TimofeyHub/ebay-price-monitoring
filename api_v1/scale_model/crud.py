import datetime

from sqlalchemy import select, desc, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import ScaleModel, SoldAd
from .schemas import ScaleModelCreateSchema, ScaleModelUpdateSchema


async def get_all_scale_models(session: AsyncSession) -> list[ScaleModel]:
    stmt = select(ScaleModel).order_by(ScaleModel.id)
    result: Result = await session.execute(stmt)
    scale_models = result.scalars().all()
    return list(scale_models)


async def get_scale_model(
    session: AsyncSession,
    scale_model_id: int,
) -> ScaleModel | None:
    return await session.get(ScaleModel, scale_model_id)


async def create_scale_model(
    session: AsyncSession,
    scale_model_info: ScaleModelCreateSchema,
) -> ScaleModel:
    scale_model = ScaleModel(**scale_model_info.model_dump())
    session.add(scale_model)
    await session.commit()
    return scale_model


async def update_scale_model(
    session: AsyncSession,
    scale_model: ScaleModel,
    scale_model_update: ScaleModelUpdateSchema,
) -> ScaleModel:
    for name, value in scale_model_update.model_dump(exclude_unset=True).items():
        setattr(scale_model, name, value)
    await session.commit()
    return scale_model


async def delete_scale_model(
    session: AsyncSession,
    scale_model: ScaleModel,
) -> None:
    await session.delete(scale_model)
    await session.commit()


async def get_all_ads_by_scale_model_id(
    session: AsyncSession,
    scale_model_id: int,
):
    stmt = (
        select(SoldAd)
        .join(ScaleModel.sold_ads)
        .where(
            ScaleModel.id == scale_model_id,
            SoldAd.include_in_calculation.is_(True),
        )
        .order_by(desc(SoldAd.sold_date))
    )
    result = await session.scalars(stmt)
    return list(result)


async def get_min_max_prices_by_scale_model_id(
    session: AsyncSession,
    scale_model_id_list: list[int],
    calculation_interval_in_days: int = 90,
):
    stmt = (
        select(ScaleModel.id, func.min(SoldAd.price), func.max(SoldAd.price))
        .join(ScaleModel.sold_ads)
        .where(
            ScaleModel.id.in_(scale_model_id_list),
            SoldAd.sold_date.between(
                datetime.datetime.utcnow()
                - datetime.timedelta(days=calculation_interval_in_days),
                datetime.datetime.utcnow(),
            ),
            SoldAd.include_in_calculation.is_(True),
        )
        .group_by(ScaleModel.id)
    )
    result_dict = {}
    result = list(await session.execute(stmt))

    # Временная конструкция, убрать при достижении оптимального решения
    for price_info in result:
        result_dict[price_info[0]] = {
            "min_price": price_info[1],
            "max_price": price_info[2],
        }

    return result_dict
