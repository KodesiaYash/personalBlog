from bson.objectid import ObjectId
from .mongoConnector import blogDB, start_session

class Categories:
    def __init__(self):
        self.db = blogDB
        self.collection = self.db['category']

    async def create_category(self, title, description):
        async with await start_session() as session:
            async with session.start_transaction():
                category = {"title": title, "description": description}
                result = await self.collection.insert_one(category, session=session)
                return str(result.inserted_id)  # Convert ObjectId to string

    async def get_category_by_id(self, category_id):
        return await self.collection.find_one({"_id": ObjectId(category_id)})

    async def update_category(self, category_id, title, description):
        query = {"_id": ObjectId(category_id)}
        new_values = {"$set": {"title": title, "description": description}}
        result = await self.collection.update_one(query, new_values)
        return result.modified_count

    async def delete_category(self, category_id):
        result = await self.collection.delete_one({"_id": ObjectId(category_id)})
        return result.deleted_count

# Example usage:
# import asyncio
# categories = Categories()
# asyncio.run(categories.create_category("Tech", "All about technology"))
# category = asyncio.run(categories.get_category_by_id("some_id"))
# print(category)
