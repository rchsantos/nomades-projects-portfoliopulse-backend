import logging
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user, get_asset_service
from app.schemas.asset import AssetResponse, AssetUpdate, AssetBase, AssetCreate
from app.schemas.user import UserResponse
from app.services.asset import AssetService

router = APIRouter(
  prefix='/portfolio/{portfolio_id}/assets',
  tags=['asset']
)
#
@router.get(
  '/',
  response_model=list[AssetResponse],
  status_code=status.HTTP_200_OK,
  description='Get all assets in the portfolio',
  response_description='List of all assets in the portfolio'
)
async def get_assets(
  portfolio_id: str,
  asset_service: AssetService = Depends(get_asset_service),
  current_user: UserResponse = Depends(get_current_user)
):
  try:
    user = await current_user
    return await asset_service.get_all_assets(portfolio_id)
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post(
  '/',
  response_model=AssetResponse,
  status_code=status.HTTP_201_CREATED,
  description='Create a new asset in the portfolio',
  response_description='Asset created successfully'
)
async def create_asset(
  asset_data: AssetCreate,
  asset_service: AssetService = Depends(get_asset_service),
  current_user: UserResponse = Depends(get_current_user)
):
  try:
    user = await current_user
    return await asset_service.create_asset(asset_data)
  except ValueError as e:
    logging.error(f'Error creating asset: {e}')
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch(
  '/{asset_id}',
  response_model=AssetResponse,
  status_code=status.HTTP_200_OK,
  description='Update an asset',
  response_description='Asset updated successfully'
)
async def update_asset(
  portfolio_id: str,
  asset_id: str,
  asset_data: AssetUpdate,
  asset_service: AssetService = Depends(get_asset_service),
  current_user: UserResponse = Depends(get_current_user)
):
  try:
    user = await current_user
    return await asset_service.update_asset(asset_id, asset_data)
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete(
  '/{asset_id}',
  status_code=status.HTTP_204_NO_CONTENT,
  description='Delete an asset',
  response_description='Asset deleted successfully'
)
async def delete_asset(
  portfolio_id: str,
  asset_id: str,
  asset_service: AssetService = Depends(get_asset_service),
  current_user: UserResponse = Depends(get_current_user)
):
  try:
    user = await current_user
    await asset_service.delete_asset(asset_id, portfolio_id)
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get(
  '/{asset_id}',
  response_model=AssetResponse,
  status_code=status.HTTP_200_OK,
  description='Get an asset',
  response_description='Asset retrieved successfully'
)
async def get_asset(
  asset_id: str,
  asset_service: AssetService = Depends(get_asset_service),
  current_user: UserResponse = Depends(get_current_user)
):
  try:
    user = await current_user
    return await asset_service.get_asset_by_id(asset_id)
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
