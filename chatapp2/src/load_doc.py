import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.dirname(current_path)

sys.path.append(project_path)

def read_hash_lines(file_path: str) -> list[str]:
    """주어진 파일에서 '#'으로 시작하는 라인을 찾아 리스트로 반환합니다."""
    hash_lines = []
    summary_dict = {}
    sub = ""
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()  # 양쪽 공백 제거
            
            if line.startswith('#'):
                sub = line.replace("#", "").strip()
                summary_dict[sub] = ""
                # hash_lines.append(line)
            else:
                if sub=="":
                    continue
                summary_dict[sub] += line
                
    return summary_dict


# # 사용 예
# file_path = 'datas/project_data_카카오싱크.txt'  # 실제 파일 경로로 교체
# result = read_hash_lines(file_path)
# print(result)
