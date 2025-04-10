from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.database import engine

from collections.abc import AsyncIterator

from app.config import settings
from app.users.router import router_auth, router_users
from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels


from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from app.pages.router import router as router_pages
from app.images.router import router as router_images

from sqladmin import Admin

from app.admin.auth import authentication_backend

app = FastAPI()


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")


app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_bookings)

app.include_router(router_pages)
app.include_router(router_images)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)


app.mount("/static", StaticFiles(directory="app/static"), "static")
