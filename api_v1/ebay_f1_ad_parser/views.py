from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.ebay_ad_parser import SearchScaleModelInfo, create_search_url

router = APIRouter(tags=["EbayF1AdParser"])


@router.post("/")
async def search_and_add_in_db(
    scale_model_info: SearchScaleModelInfo,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    create_search_url(search_info=scale_model_info)
