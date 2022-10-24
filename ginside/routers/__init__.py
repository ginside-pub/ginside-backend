from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from .samples import router as samples_router


router = APIRouter()

router.include_router(samples_router, prefix='/samples', tags=['samples'])


@router.get('/', include_in_schema=False)
async def redirect_to_openapi():
    return RedirectResponse('/docs')
