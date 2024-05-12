from openai import OpenAI

client = OpenAI()
model = "gpt-3.5-turbo-0125"

system_role = """
신조어 사전:
{
    "자만추": "자연스러운 만남 추구",
    "좋댓구알": "좋아요, 댓글, 구독, 알림 설정의 줄임말",
    "가심비": "가격 대비 심리적 만족도가 주는 효용"
}

신조어 사전에서 답하세요. 신조어 사전에 없다면 "모르는 단어입니다."라고 답하세요.
"""

template = """
신조어 {신조어}의 뜻을 알려주세요.
""".format(신조어 = "갓생")

context = [
    {"role": "system", "content": system_role},
    {"role": "user", "content": template}
]
response = client.chat.completions.create(
    model=model, 
    messages=context, 
    temperature=0,
    top_p=0
).model_dump()

print(response['choices'][0]['message']['content'])