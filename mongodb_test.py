from pymongo import MongoClient

cluster = MongoClient("localhost:27017")
db = cluster["chatbot"]
collection = db["chats"]

my_friend = {
    "name": "우엉봇",
    "age": 32,
    "job": "소프트웨어 엔지니어",
    "character": "항상 밝고 명랑한 성격임",
    "best_friend": {
        "name": "민우영",
        "situations": [
            "중고거래 앱의 알림팀에서 일하고 있음",
            "NBA를 좋아함",
            "스페인 여행을 준비하고 있음",
        ],
    },
}

# collection.insert_one(my_friend)

for result in collection.find({}):
    print(result)

# collection.delete_many({})  # 모든 데이터 삭제
