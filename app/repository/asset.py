from bson import ObjectId
from pymongo.results import InsertOneResult
from sqlalchemy.testing.plugin.plugin_base import logging

from app.core.database import db
from app.models.asset import Asset
from app.schemas.asset import AssetResponse


class AssetRepository:
    """
      A class to represent an asset repository, and contains
      methods to interact with the database.
    """

    def __init__(self):
        self.collection = db.get_collection('assets')

    async def fetch_all_assets(self, portfolio_id: str) -> list[Asset]:
        """
        Get all assets in the database from the portfolio ID
        """
        asset_cursor = self.collection.find({'portfolio_ids': portfolio_id})
        assets = []
        async for asset in asset_cursor:
            asset['id'] = str(asset['_id'])
            assets.append(Asset(**asset))
        return assets

    async def add_asset(self, asset: Asset) -> InsertOneResult:
        """
        Add a new asset to the database
        :param asset: Asset
        :rtype: Asset
        """
        try:
            return await self.collection.insert_one(asset.model_dump())
        except Exception as e:
            logging.error(f'Error adding asset: {e}')
            raise ValueError(str(e))

    async def update_asset(self, asset_id: str, asset: dict) -> dict:
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
            return await self.collection.find_one({'_id': ObjectId(asset_id)})
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

    async def find_asset_by_id(self, asset_id: str) -> dict:
        """
        Find an asset by ID
        :param asset_id: str
        :rtype: Asset
        """
        return await self.collection.find_one({'_id': ObjectId(asset_id)})

    async def find_asset_by_symbol(self, symbol: str):
        """
        Find an asset by symbol
        :param symbol: str
        """
        return await self.collection.find_one({'symbol': symbol})

    # async def find_assets_by_ids(self, asset_ids: list) -> list:
    #
    #     assets = await self.collection.find_many({'_id': {'$in': asset_ids}})
    #     # assets = await self.collection.findMany({'_id': {'$in': asset_ids}})
    #     return assets
