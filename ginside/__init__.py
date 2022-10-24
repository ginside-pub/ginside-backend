from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from . import routers
from .core.config import cfg
from .core.postgres import connect, disconnect


app = FastAPI(
    title='ginside',
    debug=cfg.debug,
    default_response_class=ORJSONResponse,
    on_startup=[connect],
    on_shutdown=[disconnect],
)

app.include_router(routers.router)
