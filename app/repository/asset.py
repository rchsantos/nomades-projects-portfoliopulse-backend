from google.cloud.firestore_v1 import FieldFilter, DocumentSnapshot
from sqlalchemy.testing.plugin.plugin_base import logging

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

  async def update_asset(self, asset: asset_schema.AssetUpdate) -> Asset:
    """
    Update an asset in the database
    :param asset: AssetUpdate
    :rtype: Asset
    """
    try:
      print('Asset ID:', asset.id)
      asset_ref = self.collection.document(asset.id)
      asset_ref.update(asset.model_dump(exclude_unset=True))
      updated_asset = asset_ref.get()
      return self.firestore_to_asset(updated_asset)
    except Exception as e:
      logging.error(f'Error updating asset: {e}')
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

  async def get_asset_by_symbol(self, portfolio_id: str, symbol: str):
    """
    Get an asset by symbol
    :param portfolio_id: str
    :param symbol: str
    :rtype: Asset
    """
    try:
      asset_query = self.collection.where(
        filter = FieldFilter(
          u'portfolio_id',
          u'==',
          portfolio_id
        )
      ).where(
        filter = FieldFilter(
          u'symbol',
          u'==',
          symbol
        )
      ).get()

      if not asset_query:
        raise ValueError('Asset not found...')

      return self.firestore_to_asset(asset_query[0])
    except Exception as e:
      raise ValueError(str(e))

  @staticmethod
  def asset_to_firestore(asset: Asset) -> dict:
    return {
      u'id': asset.id,
      u'name': asset.name,
      u'symbol': asset.symbol,
      u'shares': asset.shares,
      u'purchase_price': asset.purchase_price,
      u'currency': asset.currency,
      u'portfolio_id': asset.portfolio_id,
      u'user_id': asset.user_id
    }

  @staticmethod
  def firestore_to_asset(asset_document: DocumentSnapshot) -> Asset:
    asset_data = asset_document.to_dict()
    return Asset(
      id = asset_document.id,
      name = asset_data['name'],
      symbol = asset_data['symbol'],
      shares = asset_data['shares'],
      purchase_price = asset_data['purchase_price'],
      currency = asset_data['currency'],
      portfolio_id = asset_data['portfolio_id'],
      user_id = asset_data['user_id']
    )
