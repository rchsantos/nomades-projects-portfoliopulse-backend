from bson import ObjectId
from sqlalchemy.testing.plugin.plugin_base import logging

from app.core.database import db
from app.models.asset import Asset
import app.schemas.asset as asset_schema

class AssetRepository:
  """
    A class to represent an asset repository, and contains
    methods to interact with the database.
  """
  def __init__(self):
    self.collection = db.get_collection('assets')
    self.asset_schema = asset_schema


  async def fetch_all_assets(self, portfolio_id: str) -> list[Asset]:
    """
    Get all assets in the database from the current user
    """
    asset_cursor = self.collection.find({'portfolio_id': portfolio_id})
    assets = []
    async for asset in asset_cursor:
      asset['id'] = str(asset['_id'])
      assets.append(Asset(**asset))
    return assets

  async def add_asset(self, asset: Asset) -> Asset:
    """
    Add a new asset to the database
    :param asset: Asset
    :rtype: Asset
    """
    try:
      asset_dict = asset.model_dump()
      return await self.collection.insert_one(asset_dict)
    except Exception as e:
      logging.error(f'Error adding asset: {e}')
      raise ValueError(str(e))

  async def update_asset(self, asset_id: str, asset: dict) -> Asset:
    """
    Update an asset in the database
    :param asset_id: str
    :param asset: dict
    :rtype: Asset
    """
    try:
      await self.collection.update_one(
        {'_id': ObjectId(asset_id)},
        {
          '$set': asset,
          '$currentDate': {'lastUpdated': True}
        }
      )
      updated_asset = await self.collection.find_one({'_id': ObjectId(asset_id)})
      return updated_asset
    except Exception as e:
      raise ValueError(str(e))

  async def delete_asset(self, asset_id: str):
    """
    Delete an asset from the database
    :param asset_id: str
    """
    try:
      await self.collection.delete_one({'_id': ObjectId(asset_id)})
    except Exception as e:
      raise ValueError(str(e))

  async def find_asset_by_id(self, asset_id: str):
    """
    Find an asset by ID
    :param asset_id: str
    :rtype: Asset
    """
    asset = await self.collection.find_one({'_id': ObjectId(asset_id)})
    return asset

  #
  # async def get_asset_by_symbol(self, portfolio_id: str, symbol: str):
  #   """
  #   Get an asset by symbol
  #   :param portfolio_id: str
  #   :param symbol: str
  #   :rtype: Asset
  #   """
  #   try:
  #     asset_query = self.collection.where(
  #       filter = FieldFilter(
  #         u'portfolio_id',
  #         u'==',
  #         portfolio_id
  #       )
  #     ).where(
  #       filter = FieldFilter(
  #         u'symbol',
  #         u'==',
  #         symbol
  #       )
  #     ).get()
  #
  #     if not asset_query:
  #       raise ValueError('Asset not found...')
  #
  #     return self.firestore_to_asset(asset_query[0])
  #   except Exception as e:
  #     raise ValueError(str(e))
  #
  # @staticmethod
  # def asset_to_firestore(asset: Asset) -> dict:
  #   return {
  #     u'id': asset.id,
  #     u'name': asset.name,
  #     u'symbol': asset.symbol,
  #     u'shares': asset.shares,
  #     u'purchase_price': asset.purchase_price,
  #     u'currency': asset.currency,
  #     u'portfolio_id': asset.portfolio_id,
  #     u'user_id': asset.user_id
  #   }
  #
  # @staticmethod
  # def firestore_to_asset(asset_document: DocumentSnapshot) -> Asset:
  #   asset_data = asset_document.to_dict()
  #   return Asset(
  #     id = asset_document.id,
  #     name = asset_data['name'],
  #     symbol = asset_data['symbol'],
  #     shares = asset_data['shares'],
  #     purchase_price = asset_data['purchase_price'],
  #     currency = asset_data['currency'],
  #     portfolio_id = asset_data['portfolio_id'],
  #     user_id = asset_data['user_id'],
  #   )
