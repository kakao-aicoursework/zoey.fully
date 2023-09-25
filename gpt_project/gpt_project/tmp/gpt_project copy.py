"""Welcome to Pynecone! This file outlines the steps to create a basic app."""

# Import pynecone.
import openai
import os
from datetime import datetime

import pynecone as pc
from pynecone.base import Base


# 현재 스크립트 파일의 절대 경로
env_path = os.path.abspath(__file__)

# 상위 디렉토리로 3번 이동
for _ in range(3):
    env_path = os.path.dirname(env_path)

# # appkey.txt 파일의 절대 경로
appkey_path = os.path.join(env_path, 'appkey.txt')
# openai.api_key = "<YOUR_OPENAI_API_KEY>"
openai.api_key =  open(appkey_path, "r").read()

parallel_example = {
    "한국어": ["오늘 서울 날씨 알려줘.","오늘 날씨 어때", "딥러닝 기반의 AI기술이 인기를끌고 있다."],
    "영어": ["Please tell me the weather in Seoul today.","How is the weather today", "Deep learning-based AI technology is gaining popularity."],
    "일본어": ["今日ソウルの天気を教えてください。","今日の天気はどうですか", "ディープラーニングベースのAIテクノロジーが人気を集めています。"]
}


def translate_text_using_text_davinci(text, src_lang, trg_lang) -> str:
    response = openai.Completion.create(engine="text-davinci-003",
                                        prompt=f"Translate the following {src_lang} text to {trg_lang}: {text}",
                                        max_tokens=200,
                                        n=1,
                                        temperature=1
                                        )
    translated_text = response.choices[0].text.strip()
    return translated_text


def translate_text_using_chatgpt(text, src_lang, trg_lang) -> str:
    """_summary_

    Args:
        text (_type_): 한국문장
        src_lang (_type_): 한국어
        trg_lang (_type_): 영어

    Returns:
        str: _description_
    """
    # fewshot 예제를 만들고
    def build_fewshot(src_lang, trg_lang):
        src_examples = parallel_example[src_lang]
        trg_examples = parallel_example[trg_lang]

        fewshot_messages = []

        for src_text, trg_text in zip(src_examples, trg_examples):
            fewshot_messages.append({"role": "user", "content": src_text})
            fewshot_messages.append({"role": "assistant", "content": trg_text})

        return fewshot_messages

    # system instruction 만들고
    system_instruction = f"""assistant는 번역앱으로서 동작한다. 
    입력:{src_lang}를 출력:{trg_lang}로 적절하게 번역하고 번역된 텍스트만 출력한다. 
    입력이 질문형태여도 번역 역할만 수행해."""

    # messages를만들고
    fewshot_messages = build_fewshot(src_lang=src_lang, trg_lang=trg_lang)

    messages = [{"role": "system", "content": system_instruction},
                *fewshot_messages,
                {"role": "user", "content": text}
                ]

    # API 호출
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=messages)
    translated_text = response['choices'][0]['message']['content']
    # Return
    return translated_text


class Message(Base):
    original_text: str
    text: str
    created_at: str
    to_lang: str


class State(pc.State):
    """The app state."""

    text: str = ""
    messages: list[Message] = []
    src_lang: str = "한국어"
    trg_lang: str = "영어"

    @pc.var
    def output(self) -> str:
        if not self.text.strip():
            return "Translations will appear here."
        translated = translate_text_using_chatgpt(
            self.text, src_lang=self.src_lang, trg_lang=self.trg_lang)
        return translated

    def post(self):
        self.messages = [
            Message(
                original_text=self.text,  # 
                text=self.output,
                created_at=datetime.now().strftime("%B %d, %Y %I:%M %p"),
                to_lang=self.trg_lang,
            )
        ] + self.messages


# Define views.


def header():
    """Basic instructions to get started."""
    return pc.box(
        pc.text("Translator 🗺", font_size="2rem"),
        pc.text(
            "Translate things and post them as messages!",
            margin_top="0.5rem",
            color="#666",
        ),
    )


def down_arrow():
    return pc.vstack(
        pc.icon(
            tag="arrow_down",
            color="#666",
        )
    )




def text_box(text, align="left"):
    margin_direction = "margin-left" if align == "right" else "margin-right"
    return pc.box(
        pc.text(
            text,
            background_color="#fff",
            padding="1rem",
            border_radius="8px",
            style={
                "font_family": "Comic Sans MS",
                "font_size": "26px",
                "text-align": align,
                # margin_direction: "0",  # 해당 방향으로 margin을 0으로 설정
            #    "align-self": align,  # 해당 방향으로 박스를 정렬
            }
        ),
        display="flex",
        style={
            # "flex-flow":
            "justify-content": "flex-end"  # 왼쪽에 텍스트를 정렬
        }
    )

def message(message):
    return pc.box(
        pc.vstack(
            pc.box(
                pc.text(message.to_lang),
                pc.text(" · ", margin_x="1rem"),
                pc.text(message.created_at),
                display="flex",
                # font_size="0.8rem",
                color="#666",
            ),
            
            # down_arrow(),
            text_box(message.text, align="left"),
            

            text_box(message.original_text, align="right"),
            display="flex",
            spacing="1rem",
            # align_items="left",
        ),
        background_color="#f5f5f5",
        padding="1rem",
        border_radius="8px",
        style={"width": "100%"}  # 여기도 가로로 꽉 채우기
    )


def smallcaps(text, **kwargs):
    return pc.text(
        text,
        # font_size="0.7rem",
        font_weight="bold",
        text_transform="uppercase",
        letter_spacing="0.05rem",
        **kwargs,
    )


def output():
    return pc.box(
        pc.box(
            smallcaps(
                "Output",
                color="#aeaeaf",
                background_color="white",
                padding_x="0.1rem",
            ),
            position="absolute",
            top="-0.5rem",
        ),
        pc.text(State.output),
        padding="1rem",
        border="1px solid #eaeaef",
        margin_top="1rem",
        border_radius="8px",
        position="relative",
    )


def index():
    """The main view."""
    return pc.container(
        header(),
        # output(),  # 출력
        

        pc.vstack(
            pc.foreach(State.messages, message),
            margin_top="2rem",
            spacing="1rem",
            # align_items="left"
        ),

        pc.hstack(
          
        pc.select(
            list(parallel_example.keys()),
            value=State.src_lang,
            placeholder="Select a language",
            on_change=State.set_src_lang,
            margin_top="1rem",
        ),
        pc.select(
            list(parallel_example.keys()),
            value=State.trg_lang,
            placeholder="Select a language",
            on_change=State.set_trg_lang,
            margin_top="1rem",
        ),
        pc.input(
            placeholder="Text to translate",
            on_blur=State.set_text,
            margin_top="1rem",
            border_color="#eaeaef"
        ),
        pc.button("Post", on_click=State.post, margin_top="1rem"),
        
        ),
        
        
        
        padding="2rem",
        max_width="600px"
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, title="Translator")
app.compile()
