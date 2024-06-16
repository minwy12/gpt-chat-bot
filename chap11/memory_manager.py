from pymongo import MongoClient
import os
from common import today

mongo_cluster = MongoClient("localhost:27017")
mongo_chats_collection = mongo_cluster["chatbot"]["chats"]


class MemoryManager:
    def save_chat(self, context):
        messages = []
        for message in context:
            if message.get("isSaved", True):
                continue

            messages.append(
                {
                    "date": today(),
                    "role": message["role"],
                    "content": message["content"],
                }
            )
        if len(messages) > 0:
            mongo_chats_collection.insert_many(messages)

    def restore_chat(self, date=None):
        search_date = date if date is not None else today()
        search_results = mongo_chats_collection.find({"date": search_date})
        restored_chat = [
            {
                "role": v["role"],
                "content": v["content"],
                "isSaved": True,
            }
            for v in search_results
        ]

        return restored_chat
