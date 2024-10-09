from typing import List

from sqlalchemy.util import await_only

from app.models.asset import Asset
from app.repository.asset import AssetRepository
from app.schemas.asset import AssetBase, AssetResponse, AssetUpdate


class AssetService:
  def __init__(self, repository: AssetRepository):
    self.repository = repository

  async def create_asset(self, asset: AssetBase) -> AssetResponse:
    """
    Create a new asset in the database
    :param asset: AssetBase
    :rtype: AssetResponse
    """
    asset = Asset(
      name = asset.name,
      symbol = asset.symbol,
      shares = asset.shares,
      purchase_price = asset.purchase_price,
      currency = asset.currency,
      portfolio_id = asset.portfolio_id,
      user_id = asset.user_id
    )

    await self.repository.add_asset(asset)

    return AssetResponse(**asset.model_dump())

  async def get_all_assets(self, portfolio_id: str, user_id: str) -> list[AssetResponse]:
    """
    Get all assets for a given portfolio and user
    :param portfolio_id: str
    :param user_id: str
    :return: list[Asset]
    """
    assets = await self.repository.get_all_assets(portfolio_id, user_id)
    return [AssetResponse(**asset.model_dump()) for asset in assets]

  async def update_asset(
    self,
    asset: AssetUpdate,
  ) -> AssetResponse:
    """
    Update an asset in the database
    :param asset: AssetBase
    :rtype: AssetResponse
    """
    asset_to_update = await self.repository.get_asset_by_id(asset.id)
    if not asset_to_update:
      raise ValueError('Asset not found...')

    if asset.user_id != asset_to_update.user_id:
      raise ValueError('You do not have permission to update this asset...')

    await self.repository.update_asset(asset)
    return AssetResponse(**asset.model_dump(exclude_unset=True))

  async  def delete_asset(self, asset_id: str, user_id: str):
    asset = await self.repository.get_asset_by_id(asset_id)

    if not asset:
      raise ValueError('Asset not found...')

    if asset.user_id != user_id:
      raise ValueError('You do not have permission to delete this asset...')

    await self.repository.delete_asset(asset_id)

  # async def get_assets_by_portfolio(self, portfolio_id: str, user_id: str):
  #   """
  #   Get all assets by portfolio
  #   :param portfolio_id: str
  #   :param user_id: str
  #   :return:
  #   """
  #
  #   # If the user is not the owner of the portfolio, raise an error
  #   portfolio = await self.repository.get_portfolio_by_id(portfolio_id)
  #
  #   assets: list[Asset] = await self.repository.get_assets_by_portfolio(portfolio_id)
  #   if assets:
  #     return [AssetResponse(**asset.model_dump()) for asset in assets]
  #   raise ValueError('No assets found...')

  async def get_asset_by_id(self, asset_id: str, user_id: str) -> AssetResponse:
    """
    Get an asset by id
    :param asset_id: str
    :param user_id: str
    :return:
    """
    asset = await self.repository.get_asset_by_id(asset_id)
    if not asset:
      raise ValueError('Asset not found...')

    if asset.user_id != user_id:
      raise ValueError('You do not have permission to view this asset...')

    return AssetResponse(**asset.model_dump())

  async def get_asset_by_symbol(self, portfolio_id: str, symbol: str) -> AssetResponse:
    """
    Get an asset by symbol
    :param portfolio_id: str
    :param symbol: str
    :rtype: AssetResponse
    """
    asset = await self.repository.get_asset_by_symbol(portfolio_id, symbol)
    if not asset:
      raise ValueError('Asset not found...')
    return AssetResponse(**asset.model_dump())
