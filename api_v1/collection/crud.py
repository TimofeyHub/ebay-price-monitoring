from sqlalchemy import select, insert
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.scale_model.crud import create_scale_model
from api_v1.scale_model.schemas import ScaleModelCreateSchema
from core.models import ScaleModel, Collection


async def add_scale_model_in_collection(
    session: AsyncSession,
    scale_model_info: ScaleModelCreateSchema,
    collection_id: int,
) -> None:
    # Временная конструкция для тестирования функции
    stmt = select(Collection).where(Collection.id == 1)
    result: Result = await session.execute(stmt)
    collection = result.scalars().first()
    print(collection)
    if not collection:
        session.add(Collection())
        await session.commit()
    collection = await session.scalar(
        select(Collection)
        .where(Collection.id == collection_id)
        .options(selectinload(Collection.scale_models))
    )
    # проверяем, что такой модели нет
    stmt = select(ScaleModel).where(
        ScaleModel.keywords == f"{scale_model_info.keywords}",
        ScaleModel.year == f"{scale_model_info.year}",
        ScaleModel.scale == f"{scale_model_info.scale}",
        ScaleModel.brand == f"{scale_model_info.brand}",
    )
    result: Result = await session.execute(stmt)
    found_scale_model = result.scalars().first()
    if not found_scale_model:
        create_info = ScaleModelCreateSchema(
            keywords=scale_model_info.keywords,
            year=scale_model_info.year,
            scale=scale_model_info.scale,
            brand=scale_model_info.brand,
        )

        new_scale_model = await create_scale_model(
            session=session,
            scale_model_info=create_info,
        )

        collection.scale_models.append(new_scale_model)
        await session.commit()
    # На основе полученной инфы формируем url для поиска
    # Получаем инфу об объявлениях и записываем их в табицу объявлений
