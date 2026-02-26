import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.generated_asset import GeneratedAssets


class GeneratedAssetRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_by_id(self, asset_id: uuid.UUID) -> GeneratedAssets | None:
        result = await self._db.execute(select(GeneratedAssets).where(GeneratedAssets.id == asset_id))
        return result.scalar_one_or_none()

    async def update(self, asset: GeneratedAssets) -> GeneratedAssets:
        await self._db.flush()
        await self._db.refresh(asset)
        return asset
