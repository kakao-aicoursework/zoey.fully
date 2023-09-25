# state.py
import os
import sys
import asyncio
import openai
import reflex as rx

current_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.dirname(current_path)
print(project_path)
sys.path.append(project_path)

from src.gpt_bot import GPTBot

bot = GPTBot()
# user_sent = "오늘 날씨 알려줘"
# user_sent = "카카오톡 채널 고객 관리에 대해 알려주세요"
# result = bot.main(user_sent)
# print("result:",result)

class State(rx.State):
    # The current question being asked.
    question: str

    # Keep track of the chat history as a list of (question, answer) tuples.
    chat_history: list[tuple[str, str]]


    def get_summary(self, user_sent):
        print("state user_sent:", user_sent)
        result = bot.main(user_sent)
        return result

    def answer(self):

        # Add to the answer as the chatbot responds.
        answer = ""
        self.chat_history.append((self.question, answer))

        # # Clear the question input.
        # self.question = ""

        # # Yield here to clear the frontend input before continuing.
        yield
      
        answer += self.get_summary(self.question)
        self.chat_history[-1] = (
                    self.chat_history[-1][0],
                    answer,
                )
        yield