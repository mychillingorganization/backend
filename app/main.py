from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import uvicorn

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers

app = FastAPI(
    title="GDGoC Certificate System API",
    version="1.0.0",
    docs_url="/",           # ← Swagger UI tại /
    redoc_url="/redoc",     # ← ReDoc tại /redoc
    openapi_url="/openapi.json"  
)

register_exception_handlers(app)
app.include_router(api_router)


@app.get("/health", tags=["Health"])
async def health() -> dict[str, str]:
    return {"status": "ok", "version": "1.0.0"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_ENV == "development",
    )
