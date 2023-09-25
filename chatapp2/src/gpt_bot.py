import os
import sys

import openai

current_path = os.path.dirname(os.path.realpath(__file__))
PROJECT_PATH = os.path.dirname(current_path)
print(PROJECT_PATH)
sys.path.append(PROJECT_PATH)

openai.api_key = os.environ["OPENAI_API_KEY"]


class GPTBot:
    def __init__(self):
        """초기 설정"""
        self.project_path = PROJECT_PATH
        self.datas_path = os.path.join(PROJECT_PATH, 'datas')
        print("self.datas_path:", self.datas_path)
        self.doc_file_name_list = self.get_txt_files()
        print("self.doc_file_name_list:", self.doc_file_name_list)
        self.doc_info = self.load_datas_info()
        self.history = ""

    def get_txt_files(self):
        """datas 디렉터리에서 .txt 파일 목록을 가져옵니다."""
        return [f for f in os.listdir(self.datas_path) if f.endswith('.txt')]

    def read_hash_lines(self, file_path: str) -> dict:
        """주어진 파일에서 '#'으로 시작하는 라인을 찾아 딕셔너리로 반환"""
        summary_dict = {}
        sub = ""
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    sub = line.replace("#", "").strip()
                    summary_dict[sub] = ""
                else:
                    if sub == "":
                        continue
                    summary_dict[sub] += line

        return summary_dict

    def load_datas_info(self):
        """datas의 정보를 불러오기"""
        doc_file_name_list = self.doc_file_name_list

        doc_info = {}
        for doc_file_name in doc_file_name_list:
            doc_file_path = os.path.join(self.datas_path, doc_file_name)

            # 파일에서 '#'으로 시작하는 라인을 해시태그로 읽어서 딕셔너리 생성
            summary_dict = self.read_hash_lines(doc_file_path)

            doc_info[doc_file_name] = summary_dict

        return doc_info

    def get_gpt_default_chat(self, user_sent: str) -> str:
        """gpt를 사용일반 대화"""

        system_msg = {
            "role": "system",
            "content": """
            대답은 한국어로 해. 한국어로 대답하겠다고 말하지마.
            """
        }

        user_msg = {
            "role": "user",
            "content": user_sent
        }

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[system_msg, user_msg],
            temperature=1,
            max_tokens=256,
        )

        return completion.choices[0].message.content

    def get_gpt_keyword_index(self, summary_keys: list, user_sent: str) -> int:
        """gpt를 사용하여 키워드 인덱스 추출"""
        system_msg = {
            "role": "system",
            "content": f"""
            심호흡을 하고 단계적으로 생각해보자.
            너는 키워드 추출 bot 이다. 
            user_sent 를 보고 summary_keys에서 가장 유사한 result=index 를 출력해라.
            index 만 출력하고,절대로 다른 답변은 하지마세요.

            <user_sent>
            {user_sent}
            </user_sent>

            <summary_keys>
            {summary_keys}
            </summary_keys>

            <result>
            int 타입의 index
            </result>

            출력:
            result
            """
        }
        user_msg = {
            "role": "user",
            "content": user_sent
        }

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[system_msg, user_msg],
            temperature=1.5,
            max_tokens=256
        )

        return int(completion.choices[0].message.content)

    def get_gpt_summary(self, keyword_doc: str) -> str:
        """gpt를 사용하여 문장 요약"""
        system_msg = {
            "role": "system",
            "content": """
        심호흡을 하고 단계적으로 생각해보자.
        너는 문장 요약 bot 이다. 
        user의 문장에서 핵심 단어를 추출해.
        그리고 핵심단어에 해당하는 설명을 요약해주세요. 핵심 내용만 작성하세요.
        다른 답변은 하지마세요. 

    
        ---답변 형식
        {핵심 단어}: {요약된 설명}
        {핵심 단어}: {요약된 설명}
        ---
    
    """
        }
        user_msg = {
            "role": "user",
            "content": f"{keyword_doc}"
        }

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[system_msg, user_msg],
            temperature=1,
            max_tokens=1024,
        )

        return completion.choices[0].message.content

    def get_title_keyword(self, user_sent: str) -> str:
        """gpt를 사용하여 타이틀 키워드 추출"""
        file_name_list = self.doc_file_name_list

        system_msg = {

                "role": "system",
                "content":
                f"""
            심호흡하고 순차적으로 생각하세요. 
            너는 키워드 추출 bot 이다. 
            user의 문장에서
            file_name_list 와 가장 적합한 키워드를 추출해라. 
            그리고 file_name_list 에 존재하는 키워드를 출력해라.
            다른 답변은 하지마세요. 키워드 추출관련 질문이 아니면 False 를 대답하세요.

            <file_name_list>
            {file_name_list}
            </file_name_list>
            
            <Example1>
            user:카카오싱크에 어떤 기능이 있는지 알려줘.
            you:project_data_카카오싱크.txt

            <Example2>
            user: 오늘 날씨 알려줘
            you:False

            <Example3>
            user: 1+1 =?
            you:False
            """
            }
        user_msg = {
            "role": "user",
            "content": user_sent
        }

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[system_msg, user_msg],
            temperature=1,
            max_tokens=512,
        )

        return completion.choices[0].message.content

    def check_past_question(self, user_sent: str) -> str:
        """gpt를 사용하여 타이틀 키워드 추출"""
        system_msg = {

            "role": "system",
            "content":
            """
            심호흡하고 순차적으로 생각하세요. 
            너는 문장이 과거의 것을 질문한것인지 확인하는 bot 이다. 
            user가 과거에 대한 질문을 하고 있는지 확인해.
            만약 과거 질문이면 result=True. 그렇지 않으면 result=False

            <과거 질문>
            이전, 위에, 아까, 조금전에, 앞에서 말한, 너가 대답한 등 과거에 질문과 관련된 내용
            </과거 질문>
                
            <result>
            만약 과거 질문이면 result=True
            그렇지 않으면 result=False
            </result>
            
            <Example1>
            user:카카오싱크에 어떤 기능이 있는지 알려주세요.
            False

            <Example2>
            user:위의 기능 설정을 위해 도움 받을 수 있는 URL을 알려줘.
            True

            <Example3>
            user: 아까 어떤 기능이 있다고 했지?
            True

            <Example4>
            user: 1+1 =?
            False
            """
        }
        user_msg = {
            "role": "user",
            "content": user_sent
        }

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[system_msg, user_msg],
            temperature=1,
            max_tokens=128,
        )

        return completion.choices[0].message.content

    def get_question_with_history(self, user_sent: str) -> str:
        """과거 대화 히스토리와 함께 질문을 처리"""

        hist_sent = self.history
        system_msg = {
            "role": "system",
            "content": f"""
            심호흡하고 순차적으로 생각하고 답변하세요.
            너는 답변 bot 이다. 순차적으로 수행하고 result 값을 반환해.
            hist_sent 에서 user_sent 의 정답을 찾아라. 정답을 찾으면 정답을 출력해.
            
            필요한 대답만 정중하고 간결하게 하세요.
            다른 답변은 하지마세요. 불필요한 말은 하지마세요. 간결하게 중요한 대답만 하세요.


            <user_sent>
            {user_sent}
            </user_sent>
            
            <hist_sent>
            {hist_sent}
            </hist_sent>

            <result>
             doc_sent 에서 찾은 user_sent 의 정답.
            </result>

            출력:
            result

            """
        }
        user_msg = {
            "role": "user",
            "content": user_sent
        }

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[system_msg, user_msg],
            temperature=1.5,
            max_tokens=512,
        )

        return completion.choices[0].message.content

    def main(self, user_sent):
        """kakao gpt bot 메인 함수"""

        print("main user_sent:",user_sent)
        result = False
        is_first_q = True

        try:
            # 1. 과거의 질문인지 확인하기.
            if self.history != "":
                print("check self.history")
                is_past = self.check_past_question(user_sent)
                print("is_past:",is_past)
                if str(is_past)=="True":
                    result = self.get_question_with_history(user_sent)
                    is_first_q = False

            print("is_first_q:", is_first_q)
            if is_first_q:
                # GPT를 사용해 사용자 문장에 가장 적합한 파일을 선택
                gpt_select_title = self.get_title_keyword(user_sent)
                print("gpt_select_title", gpt_select_title)
                if str(gpt_select_title) != 'False':
                    # 해시태그의 키만 리스트로 생성
                    summary_dict = self.doc_info[gpt_select_title]
                    summary_keys = list(summary_dict.keys())

                    # GPT를 사용해 사용자 문장과 가장 관련이 높은 해시태그의 인덱스를 찾음
                    gpt_keyword_idx = self.get_gpt_keyword_index(
                        summary_keys, user_sent)

                    # 인덱스에 해당하는 키워드 문서(해시태그)를 선택
                    keyword_doc = summary_keys[gpt_keyword_idx]

                    # 선택된 키워드에 대한 문서 내용
                    doc_sent = summary_dict[keyword_doc]
                    self.history = doc_sent

                    # GPT를 사용해 문서를 요약
                    summary_sent = self.get_gpt_summary(doc_sent)
                    result = summary_sent
                else:
                    pass
        except Exception as e:
            print("e:",e)
            result = "죄송합니다. 알수없는 오류가 발생했습니다. 잠시 후 다시 질문해 주세요."

        print("result:", result)
        if str(result) == 'False':
            result = self.get_gpt_default_chat(user_sent)

        return result


if __name__ == "__main__":
    bot = GPTBot()
    # user_sent = "오늘 날씨 알려줘"
    user_sent = "카카오톡 채널 고객 관리에 대해 알려주세요"
    result = bot.main(user_sent)
    print(result)
