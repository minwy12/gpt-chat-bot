import pytz
from datetime import datetime, timedelta
from openai import OpenAI
from dataclasses import dataclass


@dataclass(frozen=True)
class Model:
    basic: str = "gpt-3.5-turbo-1106"
    advanced: str = "gpt-4-1106-preview"


model = Model()
client = OpenAI(timeout=30, max_retries=1)


def makeup_response(message, finish_reason="ERROR"):
    return {
        "choices": [
            {
                "finish_reason": finish_reason,
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": message,
                },
            }
        ],
        "usage": {
            "total_tokens": 0,
        },
    }


def today():
    korea = pytz.timezone("Asia/Seoul")
    now = datetime.now(korea)
    return now.strftime("%Y%m%d")


def yesterday():
    korea = pytz.timezone("Asia/Seoul")
    now = datetime.now(korea)
    one_day = timedelta(days=1)
    yesterday = now - one_day
    return yesterday.strftime("%Y%m%d")


def currTime():
    korea = pytz.timezone("Asia/Seoul")
    now = datetime.now(korea)
    return now.strftime("%Y.%m.%d %H:%M:%S")
