from sqlalchemy.util import await_only

from app.models.asset import Asset
from app.repository.asset import AssetRepository
from app.schemas.asset import AssetBase, AssetResponse


class AssetService:
  def __init__(self, repository: AssetRepository):
    self.repository = repository

  async def get_all_assets(self, portfolio_id: str, current_user_id: str):
    """
    Get all assets from the database
    :param portfolio_id: str
    :param current_user_id: str
    :rtype: list[AssetResponse]
    """
    assets: list[Asset] = await self.repository.get_assets(portfolio_id)
    if assets:
      return [AssetResponse(**asset.model_dump()) for asset in assets]
    raise ValueError('No assets found...')

  async def create_asset(self, portfolio_id: str, asset: AssetBase, current_user_id: str) -> AssetResponse:
    """
    Create a new asset in the database
    :param portfolio_id: str
    :param asset: AssetBase
    :param current_user_id: str
    :rtype: AssetResponse
    """
    asset = Asset(
      name = asset.name,
      symbol = asset.symbol,
      quantity = asset.quantity,
      purchase_price = asset.purchase_price,
      currency = asset.currency,
      portfolio_id = portfolio_id,
      user_id = current_user_id
    )

    await self.repository.add_asset(asset)
    return AssetResponse(**asset.model_dump())

  async def update_asset(
    self,
    portfolio_id: str,
    asset_id: str,
    asset: AssetBase,
    user_id: str
  ) -> AssetResponse:
    """
    Update an asset in the database
    :param portfolio_id:
    :param asset_id: str
    :param asset: AssetBase
    :param user_id: str
    :rtype: AssetResponse
    """
    if asset.user_id != user_id:
      raise ValueError('You do not have permission to update this asset...')

    asset = await self.repository.get_asset_by_id(asset_id)
    if not asset:
      raise ValueError('Asset not found...')

    await self.repository.update_asset(asset_id, asset)
    return AssetResponse(**asset.model_dump(exclude_unset=True))

  async  def delete_asset(self, asset_id: str, user_id: str):
    asset = await self.repository.get_asset_by_id(asset_id)

    if not asset:
      raise ValueError('Asset not found...')

    if asset.user_id != user_id:
      raise ValueError('You do not have permission to delete this asset...')

    await self.repository.delete_asset(asset_id)



  def get_asset_by_id(self):
    pass
