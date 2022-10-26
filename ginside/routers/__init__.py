from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from .posts import router as posts_router


router = APIRouter()

router.include_router(posts_router, prefix='/posts', tags=['posts'])


@router.get('/', include_in_schema=False)
async def redirect_to_openapi():
    return RedirectResponse('/docs')
