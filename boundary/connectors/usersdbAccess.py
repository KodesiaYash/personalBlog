from boundary.connectors.mongoConnector import userDb

class UsersDBAccess:
    def __init__(self):
        self.collection = userDb['user']

    def get_user_by_id(self, user_id):
        return self.collection.find_one({"_id": user_id})

    def add_user(self, username, email):
        user = {"username": username, "email": email}
        return self.collection.insert_one(user).inserted_id

    def update_user(self, user_id, username, email):
        query = {"_id": user_id}
        new_values = {"$set": {"username": username, "email": email}}
        return self.collection.update_one(query, new_values).modified_count

    def delete_user(self, user_id):
        return self.collection.delete_one({"_id": user_id}).deleted_count
