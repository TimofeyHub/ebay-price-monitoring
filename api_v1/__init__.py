from fastapi import APIRouter

from .scale_model.views import router as scale_model_router
from .sold_ad.views import router as sold_ad_router

router = APIRouter()
router.include_router(router=scale_model_router, prefix="/scale-models")
router.include_router(router=sold_ad_router, prefix="/sold_ad")
