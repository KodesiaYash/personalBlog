from bson.objectid import ObjectId
from .mongoConnector import blogDB, start_session

class Blogs:
    def __init__(self):
        self.db = blogDB
        self.collection = self.db['blog']

    async def create_blog(self, categoryId, title, content):
        async with await start_session() as session:
            async with session.start_transaction():
                blog_data = {
                    "categoryId": categoryId,
                    "title": title,
                    "content": content
                }
                result = await self.collection.insert_one(blog_data, session=session)
                return str(result.inserted_id)  # Convert ObjectId to string

    async def get_blog(self, blog_id):
        return await self.collection.find_one({"_id": ObjectId(blog_id)})

    async def update_blog(self, blog_id, title=None, content=None):
        update_data = {}
        if title:
            update_data["title"] = title
        if content:
            update_data["content"] = content

        if not update_data:
            return 0  # No updates to be made

        result = self.collection.update_one(
            {"_id": ObjectId(blog_id)},
            {"$set": update_data}
        )
        return result.modified_count

    async def delete_blog(self, blog_id):
        result = self.collection.delete_one({"_id": ObjectId(blog_id)})
        return result.deleted_count

    def list_blogs(self, filter_data=None):
        if filter_data is None:
            filter_data = {}
        blogs = self.collection.find(filter_data)
        return list(blogs)

    def list_blogs_by_category(self, category_id):
        blogs = self.collection.find({"categoryId": category_id})
        return list(blogs)

# Example usage:
# blogs_db_access = Blogs()
# blog_id = blogs_db_access.create_blog("category1", "My Blog", "This is my blog content")
# print(blogs_db_access.get_blog(blog_id))
# blogs_db_access.update_blog(blog_id, title="Updated Title")
# blogs_db_access.delete_blog(blog_id)
# print(blogs_db_access.list_blogs_by_category("category1"))
