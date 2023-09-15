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
    input_disabled: bool = False  # 입력 상자 활성화 상태를 저장할 변수
    messages: list[Message] = []
    

    @pc.var
    def output(self) -> str:

        time.sleep(0.5)
        if not str(self.text).strip():
            return "Translations will appear here."

        o_text = str(self.text) + "hello world"
        return o_text

    # 메시지 전송 함수
    def send_message(self):
        new_message = Message(
            text=self.text
        )
        self.messages.append(new_message)

        # self.update_bot_message()

    # 메시지 전송 함수
    def update_bot_message(self):
        # 먼저 사용자 메시지만 보여주기 위해 임시 bot_text로 빈 문자열을 설정합니다.
        new_message = Message(
            text=self.output
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
            # 채팅 내역 출력을 위한 스크롤 가능한 영역 설정
            pc.box(
                pc.foreach(State.messages, message),
                overflow="auto",  # 스크롤 적용
                max_height="400px"  # 최대 높이 설정
            ),
            # 사용자 입력 영역
            pc.hstack(
                pc.input(
                    placeholder="Your message",
                    on_blur=State.set_text
                ),
                pc.button("Send", on_click=State.send_message),
                pc.button("gpt", on_click=State.update_bot_message)
            )
        ),
        padding="2rem",
        background_color="skyblue",  # 박스의 배경색을 하늘색으로 설정
        max_width="600px",
        margin="auto",  # 화면 중앙에 위치
        min_height="600px"  # 최대 높이 설정
        # position="absolute",  # 중앙 정렬을 위한 설정
    

        # max_width="600px",
        # margin="auto",
        # position="absolute",  # 중앙 정렬을 위해 position을 absolute로 설정
        # top="50%",  # 상위 요소 대비 50% 위치
        # left="50%",  # 상위 요소 대비 50% 위치
        # transform="translate(-50%, -50%)"  # 자기 자신의 크기에 대한 50%만큼 이동하여 중앙에 배치
    )


# 앱 설정 및 컴파일
app = pc.App(state=State)
app.add_page(index, title="Chatbot")
app.compile()
