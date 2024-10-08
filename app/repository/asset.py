from google.cloud.firestore_v1 import FieldFilter

from app.core.firestore_db import db
from app.models.asset import Asset
import app.schemas.asset as asset_schema

class AssetRepository:
  """
    A class to represent an asset repository, and contains
    methods to interact with the database.
  """
  def __init__(self):
    self.collection = db.collection(u'assets')
    self.asset_schema = asset_schema

  async def get_assets(self, portfolio_id: str) -> list[Asset]:
    """
    Get all assets from the database
    :param portfolio_id: str
    :rtype: list[Asset]
    """
    return [
      self.firestore_to_asset(asset) for asset in self.collection.where(
        filter = FieldFilter(
          u'portfolio_id',
          u'==',
          portfolio_id
        )
      ).get()
    ]

  async def add_asset(self, asset: Asset) -> Asset:
    """
    Add a new asset to the database
    :param asset: Asset
    :rtype: Asset
    """
    try:
      _, asset_ref = self.collection.add(self.asset_to_firestore(asset))
      asset.id = asset_ref.id
      return asset
    except Exception as e:
      raise ValueError(str(e))

  async def update_asset(self, asset_id: str, asset: dict) -> Asset:
    """
    Update an asset in the database
    :param asset_id: str
    :param asset: AssetUpdate
    :rtype: Asset
    """
    try:
      asset_ref = self.collection.document(asset_id)
      asset_ref.update(asset)
      updated_asset = asset_ref.get()
      return self.firestore_to_asset(updated_asset)
    except Exception as e:
      raise ValueError(str(e))

  async def delete_asset(self, asset_id: str) -> None:
    """
    Delete an asset from the database
    :param asset_id: str
    :rtype: None
    """
    try:
      self.collection.document(asset_id).delete()
    except Exception as e:
      raise ValueError(str(e))

  async def get_asset_by_id(self, asset_id: str):
    try:
      asset = self.collection.document(asset_id).get()
      return self.firestore_to_asset(asset)
    except Exception as e:
      raise ValueError(str(e))

  @staticmethod
  def asset_to_firestore(asset: Asset) -> dict:
    return {
      u'name': asset.name,
      u'symbol': asset.symbol,
      u'quantity': asset.quantity,
      u'purchase_price': asset.purchase_price,
      u'currency': asset.currency,
      u'portfolio_id': asset.portfolio_id,
      u'user_id': asset.user_id
    }

  @staticmethod
  def firestore_to_asset(asset) -> Asset:
    return Asset(
      id = asset.id,
      name = asset.get(u'name'),
      symbol = asset.get(u'symbol'),
      quantity = asset.get(u'quantity'),
      purchase_price = asset.get(u'purchase_price'),
      currency = asset.get(u'currency'),
      portfolio_id = asset.get(u'portfolio_id'),
      user_id = asset.get(u'user_id')
    )
