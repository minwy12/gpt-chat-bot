from openai import OpenAI
import json

client = OpenAI()
model = "gpt-3.5-turbo-0125"

agenda = """
'인공지능이 인간의 일자리를 위협합니다. 이에 대한 대응 방안을 논의합니다.'
"""

sampling_template = """
{agenda}에 대해 논의 중입니다.
```

[이전 의견]:
{prev_opinion}
```

[이전 의견]에 대한 구체적이며 실질적인 구현 방안을 아래 JSON 형식으로 답하세요.
{{
    "주제": <주제>,
    "구현": <50단어 이내로 작성하세요>,
    "근거": <[이전 의견]의 어떤 대목에서 그렇게 생각했는지>
}}
"""

evaluation_template = """
{agenda}에 대해 논의하고 있습니다.
```

[의견]:
{opinion}
```

위의 [의견]을 아래 JSON 형식으로 평가해주세요.
{{
    "창의적이고 혁신적인 방법인가": <15점 만점 기준 점수>,
    "단기간 내에 실현 가능한 방법인가": <10점 만점 기준 점수>,
    "총점": <총점>
}}
"""

def request_gpt(message, model, temperature, type="json_object"):
    message = [{"role": "user", "content": message}]
    response = client.chat.completions.create(
        model=model, 
        messages=message, 
        temperature=temperature,
        response_format={"type": type},
    ).model_dump()

    if type == "json_object":
        response_content = json.loads(response["choices"][0]["message"]["content"])
    else:
        response_content = response["choices"][0]["message"]["content"]

    return response_content

def generate_opinion(prev_opinion, n=5):
    prev_opinion = "없음" if len(prev_opinion) == 0 else prev_opinion
    samples = []
    message = sampling_template.format(agenda = agenda, prev_opinion = prev_opinion)

    for _ in range(n):
        sample = request_gpt(message, model, temperature=1.2)
        samples.append(sample['구현'])
        print("Sampled opinion:", sample['구현'])

    return samples

def evaluate_opinion(opinions):
    values = []
    for opinion in opinions:
        message = evaluation_template.format(agenda = agenda, opinion = opinion)
        value = request_gpt(message, model, temperature=1.2)
        values.append({
            "opinion": opinion,
            "value": value
        })
        print("Evaluated value:", value)

    return values

def get_top_n(values, n):
    return sorted(values, key=lambda x: x["value"]["총점"], reverse=True)[:n]

if __name__=="__main__":
    selected_opinions = []
    selected = ""

    for step in range(3):
        opinions = generate_opinion(prev_opinion=selected)
        print()
        values = evaluate_opinion(opinions)
        selected = get_top_n(values, 1)[0]['opinion']
        selected_opinions.append(selected)
        print(f"{step+1}단계: {selected}")

    print()
    print("\n".join(selected_opinions))