import uuid
from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.deps import get_current_user, get_generated_asset_service
from app.models.user import Users
from app.schemas.generated_asset import GeneratedAssetResponse
from app.services.generated_asset_service import GeneratedAssetService

router = APIRouter(prefix="/generated-assets", tags=["GeneratedAssets"])


@router.get("/{asset_id}", response_model=GeneratedAssetResponse)
async def get_asset(
    asset_id: uuid.UUID,
    current_user: Users = Depends(get_current_user),
    asset_service: GeneratedAssetService = Depends(get_generated_asset_service),
) -> GeneratedAssetResponse:
    asset = await asset_service.get_by_id(asset_id)
    return GeneratedAssetResponse.model_validate(asset)


@router.post("/{asset_id}/resend-email", response_model=GeneratedAssetResponse)
async def resend_email(
    asset_id: uuid.UUID,
    current_user: Users = Depends(get_current_user),
    asset_service: GeneratedAssetService = Depends(get_generated_asset_service),
) -> GeneratedAssetResponse:
    asset = await asset_service.resend_email(asset_id)
    return GeneratedAssetResponse.model_validate(asset)
