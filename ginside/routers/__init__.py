from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from .auth import router as auth_router
from .posts import router as posts_router
from .users import router as users_router


router = APIRouter()

router.include_router(auth_router, prefix='/auth', tags=['auth'])
router.include_router(posts_router, prefix='/posts', tags=['posts'])
router.include_router(users_router, prefix='/users', tags=['users'])


@router.get('/', include_in_schema=False)
async def redirect_to_openapi():
    return RedirectResponse('/docs')
