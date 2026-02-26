from fastapi import APIRouter

from app.api.v1 import auth, generation_log, templates

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(templates.router)
api_router.include_router(generation_log.router)

# Placeholder includes (other modules will be added later):
# api_router.include_router(users.router)
# api_router.include_router(events.router)
# api_router.include_router(generation_log.router)
