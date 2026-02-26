from fastapi import APIRouter

from app.api.v1 import auth, events, generated_assets

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)

# include module routers
# api_router.include_router(users.router)  # not yet implemented
api_router.include_router(events.router)
api_router.include_router(generated_assets.router)
# api_router.include_router(templates.router)
# api_router.include_router(generation_log.router)
