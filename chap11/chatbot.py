from common import client, model, makeup_response
from warning_agent import WarningAgent
from memory_manager import MemoryManager
from pprint import pprint
import math


class Chatbot:
    def __init__(self, model, system_role, instruction, **kwargs):
        self.context = [{"role": "system", "content": system_role}]
        self.model = model
        self.instruction = instruction
        self.max_token_size = 16 * 1024
        self.available_token_rate = 0.9

        self.kwargs = kwargs
        self.user = kwargs.get("user")
        self.assistant = kwargs.get("assistant")

        self.warningAgent = self._create_warning_agent()
        self.memoryManager = MemoryManager()
        self.context.extend(self.memoryManager.restore_chat())

    def _create_warning_agent(self):
        return WarningAgent(model=self.model, user=self.user, assistant=self.assistant)

    def add_user_message(self, message):
        self.context.append({"role": "user", "content": message, "isSaved": False})

    def send_request(self):
        # if self.warningAgent.monitor_user(self.context):
        # return makeup_response(self.warningAgent.warn_user(), "warning")

        try:
            self.context[-1]["content"] += self.instruction
            print("@@CONTEXT@@")
            print(self.context)

            response = client.chat.completions.create(
                model=self.model,
                messages=self.to_openai_context(),
                temperature=0.5,
                top_p=1,
                max_tokens=256,
                frequency_penalty=0,
                presence_penalty=0,
            ).model_dump()
        except Exception as e:
            print(f"Exception 오류({type(e)}) 발생: {e}")
            if isinstance(
                e, openai.error.InvalidRequestError
            ) and "maximum context length" in str(e):
                self.context.pop()
                return makeup_response("메시지 좀 짧게 보내줄래?")
            else:
                return makeup_response(
                    "챗봇에 문제가 발생했습니다. 잠시 후 다시 시도해주세요."
                )

        return response

    def add_response(self, response):
        self.context.append(
            {
                "role": response["choices"][0]["message"]["role"],
                "content": response["choices"][0]["message"]["content"],
                "isSaved": False,
            }
        )

    def get_response_content(self):
        return self.context[-1]["content"]

    def clear_instructions(self):
        for idx in reversed(range(len(self.context))):
            if self.context[idx]["role"] == "user":
                self.context[idx]["content"] = (
                    self.context[idx]["content"].split("instruction:\n")[0].strip()
                )
                break

    def handle_token_limit(self, response):
        try:
            curr_usage_rate = response["usage"]["total_tokens"] / self.max_token_size
            # print("curr usage rate:", curr_usage_rate)

            if curr_usage_rate > self.available_token_rate:
                remove_size = math.ceil(len(self.context) / 10)
                self.context = [self.context[0]] + self.context[remove_size + 1 :]

        except Exception as e:
            print(f"handle_token_limit exception: {e}")

    def to_openai_context(self):
        return [{"role": v["role"], "content": v["content"]} for v in self.context]

    def save_chat(self):
        self.memoryManager.save_chat(self.context)


if __name__ == "__main__":
    # step-3: 테스트 시나리오에 따라 실행 코드 작성 및 예상 출력결과 작성
    chatbot = Chatbot(model.basic)

    # chatbot.add_user_message("Who won the world series in 2020?")
    chatbot.add_user_message("Who won the NBA final in 2021?")

    # 시나리오1-4: 현재 context를 openai api 입력값으로 설정하여 전송
    response = chatbot.send_request()

    # 시나리오1-5: 응답 메시지를 context에 추가
    chatbot.add_response(response)

    # 시나리오1-7: 응답 메시지 출력
    print(chatbot.get_response_content())
    print()

    # 시나리오2-2: 사용자가 채팅창에 "Where was it played?" 입력
    # chatbot.add_user_message("Where was it played?")
    chatbot.add_user_message("Where was it played?")

    # 다시 요청 보내기
    response = chatbot.send_request()

    # 응답 메시지를 context에 추가
    chatbot.add_response(response)

    # 응답 메시지 출력
    print(chatbot.get_response_content())
    print()
    print("-----------------")
    pprint(chatbot.context)
