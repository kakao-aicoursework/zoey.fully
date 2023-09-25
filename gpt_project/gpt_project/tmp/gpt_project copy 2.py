import time
import pynecone as pc
from pynecone.base import Base

class Message(Base):
    text: str
    # bot_text: str
    # created_at: str
    # to_lang: str


class State(pc.State):
    text: str = ""  # 사용자 입력을 저장할 상태 변수
    # bot_text: str = ""  # 사용자 입력을 저장할 상태 변수
    # chat_history: list = []  # (author, message) 튜플을 저장할 상태 변수
    messages: list[Message] = []
    

    @pc.var
    def output(self) -> str:
        if not str(self.text).strip():
            return "Translations will appear here."

        return str(self.text) + "hello world"

    @pc.var
    def delayed_output(self):
        # 여기서는 딜레이를 2초로 설정했지만, 실제 상황에 따라 다를 수 있습니다.
        time.sleep(0.3)
        return str(self.text) + " hello world"

    # 메시지 전송 함수
    def send_message(self):
        # 먼저 사용자 메시지만 보여주기 위해 임시 bot_text로 빈 문자열을 설정합니다.
        new_message = Message(
            text=self.text
        )
        self.messages.append(new_message)


def text_box(text):
    return pc.text(
        text,
        background_color="#fff",
        padding="1rem",
        border_radius="8px",
    )

def message(message):
    return pc.box(
        pc.vstack(
            text_box(message.text),
            # down_arrow(),
            # text_box(message.bot_text),
         
            # spacing="0.3rem",
            # align_items="left",
        ),
        background_color="blue",
        padding="1rem",
        border_radius="8px",
    )

def index():
    return pc.container(
        pc.vstack(
        #     pc.vstack(
        #     pc.foreach(State.messages, message),
        #     margin_top="2rem",
        #     spacing="1rem",
        #     align_items="left"
        # ),

            pc.foreach(State.messages, message),  # 채팅 내역 출력
            pc.hstack(
                pc.input(
                    placeholder="Your message",
                    on_blur=State.set_text,
                    # value=State.user_message,
                    # on_input=State.user_message  # 사용자가 입력할 때 호출되는 함수
                ),
                # "Send" 버튼 클릭 시 send_message 함수 호출
                pc.button("Send", on_click=State.send_message)
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
