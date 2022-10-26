from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from .posts import router as posts_router
from .samples import router as samples_router


router = APIRouter()

router.include_router(posts_router, prefix='/posts', tags=['posts'])
router.include_router(samples_router, prefix='/samples', tags=['samples'])


@router.get('/', include_in_schema=False)
async def redirect_to_openapi():
    return RedirectResponse('/docs')
