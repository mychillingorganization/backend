import uuid

from app.core.exceptions import NotFoundException, BadRequestException
from app.models.generated_asset import GeneratedAssets
from app.repositories.generated_asset_repository import GeneratedAssetRepository
from app.services.gmail_service import GmailService


class GeneratedAssetService:
    def __init__(self, asset_repo: GeneratedAssetRepository, gmail_service: GmailService) -> None:
        self.asset_repo = asset_repo
        self.gmail_service = gmail_service

    async def get_all(self) -> list[GeneratedAssets]:
        return await self.asset_repo.get_all()

    async def get_by_id(self, asset_id: uuid.UUID) -> GeneratedAssets:
        asset = await self.asset_repo.get_by_id(asset_id)
        if not asset:
            raise NotFoundException("Generated asset không tồn tại.")
        return asset

    async def resend_email(self, asset_id: uuid.UUID) -> GeneratedAssets:
        asset = await self.get_by_id(asset_id)
        if asset.email_status != "FAILED":
            raise BadRequestException("Chỉ có bản ghi thất bại mới được gửi lại email.")

        success = await self.gmail_service.send_generated_asset(asset)
        asset.email_status = "SENT" if success else "FAILED"
        await self.asset_repo.update(asset)
        return asset
