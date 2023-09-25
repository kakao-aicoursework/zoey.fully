# chatapp.py

from chatapp2.state import State

from rxconfig import config

import reflex as rx
from chatapp2 import style


docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(
            rx.text(question, style=style.question_style),
            text_align="right",
        ),
        rx.box(
            rx.text(answer, style=style.answer_style),
            text_align="left",
        ),
        margin_y="1em",
    )


def chat() -> rx.Component:
    return rx.box(
        rx.foreach(
            State.chat_history,
            lambda messages: qa(messages[0], messages[1]),
        ),
        height="800px",
        # weight="100%",
        overflow="auto",  # 스크롤 적용
    )


def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value=State.question,
            placeholder="질문을 입력하세요.",
            on_change=State.set_question,
            style=style.input_style,
        ),
        rx.button(
            "전송",
            on_click=State.answer,
            style=style.button_style,
        ),
    )


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("gpt chatbot", font_size="2em"),
            chat(),
            action_bar(),
            border_radius="15px",
            border_width="thick",
            background_color="#F5F5F5",
            width="80%",
            padding="5%",

        ),
        padding_top="5%",
        # width="80%",

        # background_color="yellow",
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.compile()
