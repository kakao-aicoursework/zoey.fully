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

from src.load_doc import read_hash_lines

openai.api_key = os.environ["OPENAI_API_KEY"]


def get_gpt_keyword(summary_keys, user_sent):
    """gpt를 사용한 키워드 추출"""

    system_msg = {
    
        "role":"system",
        "content":
        f"""
            너는 키워드 추출 bot 이다. 
            user의 문장에서
            {summary_keys} 와 가장 적합한 키워드를 추출해라. 
            그리고 {summary_keys} 에 존재하는 키워드를 출력해라.
            다른 답변은 하지마세요.
            
            예시:
            user:카카오싱크에 어떤 기능이 있는지 알려줘.
            you:기능 소개
            """
    }
    
    user_msg = {
             "role": "user",
             "content": user_sent
             }

    completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    system_msg,
                    user_msg
                ],
                temperature=1,
                max_tokens=512,
            )

    gpt_select_keyword = completion.choices[0].message.content
    return gpt_select_keyword

def get_gpt_summary(keyword_doc):
    """gpt를 사용한 문장 요약"""

    system_msg = {
    
        "role":"system",
        "content":
        """
        너는 문장 요약 bot 이다. 
        user의 문장에서 핵심 단어를 추출해.
        그리고 핵심단어에 해당하는 설명을 요약해.
    
        ---답변 형식
        {핵심 단어}: {핵심 단어 설명}
        {핵심 단어}: {핵심 단어 설명}
        ---
    
    """}
    
    user_msg = {
             "role": "user",
             "content": f"{keyword_doc}"
             }
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            system_msg,
            user_msg
        ],
        temperature=1,
        max_tokens=1024,
    )

    summary_sent = completion.choices[0].message.content
    return summary_sent


file_path = os.path.join(project_path, 'datas/project_data_카카오싱크.txt')  # 실제 파일 경로로 교체
summary_dict = read_hash_lines(file_path)
summary_keys = list(summary_dict.keys())
print("summary_keys:",summary_keys)

class State(rx.State):
    # The current question being asked.
    question: str

    # Keep track of the chat history as a list of (question, answer) tuples.
    chat_history: list[tuple[str, str]]

 

    def get_summary(self, user_sent):
        gpt_select_keyword = get_gpt_keyword(summary_keys, user_sent)
        keyword_doc = summary_dict[gpt_select_keyword]
        summary_sent = get_gpt_summary(keyword_doc)
        return summary_sent

    def answer(self):
        # Our chatbot has some brains now!
        # session = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "user", "content": self.question}
        #     ],
        #     stop=None,
        #     temperature=0.7,
        #     stream=True,
        # )

        # Add to the answer as the chatbot responds.
        answer = ""
        self.chat_history.append((self.question, answer))

        # Clear the question input.
        self.question = ""

        # Yield here to clear the frontend input before continuing.
        yield

      
        answer += self.get_summary(self.question)
        self.chat_history[-1] = (
                    self.chat_history[-1][0],
                    answer,
                )
        yield

        # for item in session:
        #     if hasattr(item.choices[0].delta, "content"):
        #         answer += item.choices[0].delta.content
        #         self.chat_history[-1] = (
        #             self.chat_history[-1][0],
        #             answer,
        #         )
        #         yield
