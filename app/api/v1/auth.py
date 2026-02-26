from fastapi import APIRouter, Depends, status

from app.api.deps import get_auth_service, get_current_user
from app.models.user import Users
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(
	payload: RegisterRequest,
	auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
	user = await auth_service.register(payload)
	return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login(
	payload: LoginRequest,
	auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
	return await auth_service.login(payload)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
	payload: RefreshRequest,
	auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
	return await auth_service.refresh(payload.refresh_token)


@router.get("/me", response_model=UserResponse)
async def me(current_user: Users = Depends(get_current_user)) -> UserResponse:
	return UserResponse.model_validate(current_user)
