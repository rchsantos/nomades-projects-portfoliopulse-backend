from typing import List

from pymongo.results import InsertOneResult

from app.models.asset import Asset
from app.repository.asset import AssetRepository
from app.schemas.asset import AssetBase, AssetResponse, AssetUpdate, AssetCreate


class AssetService:
  def __init__(self, repository: AssetRepository):
    self.repository = repository

  async def get_all_assets(self, portfolio_id: str) -> list[AssetResponse]:
    """
    Get all assets in the database
    :param portfolio_id: str
    :rtype: list[AssetResponse]
    """
    assets: list[Asset] = await self.repository.fetch_all_assets(portfolio_id)
    if assets:
      return [AssetResponse(**asset.model_dump()) for asset in assets]
    raise ValueError('No assets found...')

  async def create_asset(self, asset_data: AssetCreate) -> AssetResponse:
    """
    Create a new asset in the database
    :param asset_data: AssetCreate
    :rtype: AssetResponse
    """
    asset = Asset(**asset_data.model_dump())
    result: InsertOneResult = await self.repository.add_asset(asset)
    asset.id = str(result.inserted_id)
    return AssetResponse(**asset.model_dump())

  async def update_asset(
    self,
    portfolio_id: str,
    asset_id: str,
    asset_data: AssetUpdate
  ) -> AssetResponse:
    """
    Update an asset in the database
    :param portfolio_id:
    :param asset_data: updated_asset
    :param asset_id: str
    :rtype: AssetResponse
    """
    asset = await self.repository.find_asset_by_id(asset_id)
    if not asset:
      raise ValueError('Asset not found...')

    if portfolio_id != asset['portfolio_id']:
      raise ValueError('You do not have permission to update this asset...')

    updated_asset = await self.repository.update_asset(asset_id, asset_data.model_dump(exclude_unset=True))

    return AssetResponse(**updated_asset)

  async def delete_asset(self, asset_id: str, portfolio_id: str):
    """
    Delete an asset from the database
    :param asset_id: str
    :param portfolio_id: str
    :return: None
    """
    asset = await self.repository.find_asset_by_id(asset_id)
    if not asset:
      raise ValueError('Asset not found...')

    if portfolio_id != asset['portfolio_id']:
      raise ValueError('You do not have permission to delete this asset...')

    await self.repository.delete_asset(asset_id)

  async def get_asset_by_id(self, asset_id: str) -> AssetResponse:
    """
    Get an asset by its ID
    :param asset_id: str
    :rtype: AssetResponse
    """
    asset = await self.repository.find_asset_by_id(asset_id)
    if asset:
      return AssetResponse(**asset)
    raise ValueError('Asset not found...')

  async def get_asset_by_symbol(self, symbol: str, portfolio_id: str) -> Asset:
    """
    Get an asset by its symbol
    :param portfolio_id:
    :param symbol: str
    :rtype: Asset
    """
    return await self.repository.find_asset_by_symbol(symbol, portfolio_id)

  async def get_asset_by_symbol_in_portfolio(self, symbol: str, portfolio_id: str) -> Asset|None:
    """
    Get an asset by its symbol in a portfolio
    :param symbol: str
    :param portfolio_id: str
    :rtype: Asset
    """
    asset: dict = await self.repository.find_asset_by_symbol_in_portfolio(symbol, portfolio_id)
    if not asset:
      return None
    return Asset(**asset)
