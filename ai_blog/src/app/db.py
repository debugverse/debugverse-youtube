from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4
from datetime import datetime, timezone


class AsyncDBHandler:
    def __init__(self):
        self.client = AsyncIOMotorClient(
            "mongodb://localhost:27017", tls=False)
        self.database = self.client["blog"]["posts"]
        print("connected to mongoDB")

    async def ping(self):
        info = await self.client.server_info()
        return info

    async def add_post(self, post):
        postresult = post.model_dump()
        postresult["uuid"] = str(uuid4())
        postresult["created"] = datetime.now(timezone.utc)

        result = await self.database.insert_one(postresult)

        if result.acknowledged:
            return True
        return False
    
    async def list_posts(self):
        posts = []
        async for post in self.database.find():
            post.pop("_id")
            post["created"] = post["created"].isoformat()
            posts.append(post)
        return posts


db = AsyncDBHandler()
