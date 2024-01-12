from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from core.models import ScaleModel
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
