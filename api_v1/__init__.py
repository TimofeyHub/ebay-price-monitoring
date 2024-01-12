from fastapi import APIRouter

from .scale_model.views import router as scale_model_router

router = APIRouter()
router.include_router(router=scale_model_router, prefix="/scale-models")
