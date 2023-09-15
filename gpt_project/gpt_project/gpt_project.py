import pynecone as pc

class State(pc.State):
    user_message: str = ""  # 사용자 입력을 저장할 상태 변수
    chat_history: list = []  # 채팅 내역을 저장할 상태 변수

    # 더미 챗봇 함수
    def get_bot_response(self):
        return "hello world"

    # 메시지 전송 함수
    def send_message(self):
        self.chat_history.append(f"You: {self.user_message}")
        bot_response = self.get_bot_response()
        self.chat_history.append(f"Bot: {bot_response}")
        self.user_message = ""

    # 사용자 메시지 상태 업데이트
    def set_user_message(self, new_text):
        self.user_message = new_text

def message(item):
    return pc.text(item)

def index():
    return pc.container(
        pc.vstack(
            pc.foreach(State.chat_history, message),  # 채팅 내역 출력
            pc.hstack(
                pc.input(
                    placeholder="Your message",
                    value=State.user_message,
                    on_input=State.user_message  # 사용자가 입력할 때 호출되는 함수
                ),
                pc.button("Send", on_click=State.send_message)  # "Send" 버튼 클릭 시 send_message 함수 호출
            )
        ),
        padding="2rem",
        background_color="skyblue",  # 박스의 배경색을 하늘색으로 설정
        max_width="600px",
        margin="auto"  # 화면 중앙에 위치
    )

# 앱 설정 및 컴파일
app = pc.App(state=State)
app.add_page(index, title="Chatbot")
app.compile()
