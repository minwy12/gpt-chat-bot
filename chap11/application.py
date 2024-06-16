from flask import Flask, render_template, request
import sys
from chatbot import Chatbot
from common import model
from characters import system_role, instruction
from parallel_function_calling import FunctionCalling, tools
import atexit

# jjinchin 인스턴스 생성
jjinchin = Chatbot(
    model=model.basic,
    system_role=system_role,
    instruction=instruction,
    user="우영",
    assistant="우엉봇",
)
func_calling = FunctionCalling(model=model.basic)
application = Flask(__name__)


@application.route("/")
def hello():
    return "Hello world!"


@application.route("/welcome")
def welcome():  # 함수명은 꼭 welcome일 필요는 없습니다.
    return "Welcome!"


@application.route("/chat-app")
def chat_app():
    return render_template("chat.html")


# 메아리 코드
# @application.route('/chat-api', methods=['POST'])
# def chat_api():
#     print("request.json:", request.json)
#     return {"response_message": "나도 " + request.json['request_message']}


@application.route("/chat-api", methods=["POST"])
def chat_api():
    request_message = request.json["request_message"]
    print("request_message:", request_message)

    jjinchin.add_user_message(request_message)

    # ChatGPT에게 함수 사양을 토대로 사용자 메시지에 호응하는 함수 정보를 분석해달라고 요청
    analyzed_message, analyzed_dict = func_calling.analyze(request_message, tools)
    # ChatGPT가 함수 호출이 필요하다고 분석했는지 여부 체크
    if analyzed_dict.get("tool_calls"):
        # ChatGPT가 분석해준대로 함수 호출
        response = func_calling.run(
            analyzed_message, analyzed_dict, jjinchin.context[:]
        )
    else:
        response = jjinchin.send_request()

    print(response)
    jjinchin.add_response(response)
    response_message = jjinchin.get_response_content()
    jjinchin.handle_token_limit(response)
    jjinchin.clear_instructions()
    print("response_message:", response_message)

    return {"response_message": response_message}


@atexit.register
def shutdown():
    print("Flask shutting down...")
    jjinchin.save_chat()


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=int(sys.argv[1]))
