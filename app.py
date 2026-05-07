import streamlit as st
from streamlit_ace import st_ace
import random
import time

st.set_page_config(
    page_title="Python 타자 연습",
    page_icon="⌨️",
    layout="wide"
)

# -----------------------------
# 문제 데이터
# -----------------------------

problems = {
    "초급": [
        '''print("Hello World")''',

        '''name = input("이름 입력: ")
print(name)''',

        '''for i in range(5):
    print(i)'''
    ],

    "중급": [
        '''def add(a, b):
    return a + b

print(add(3, 5))''',

        '''numbers = [1, 2, 3, 4]

for n in numbers:
    print(n * 2)''',

        '''student = {
    "name": "서진",
    "age": 16
}

print(student["name"])'''
    ],

    "고급": [
        '''class Student:
    def __init__(self, name):
        self.name = name

    def hello(self):
        print(f"안녕하세요 {self.name}")

s = Student("양서진")
s.hello()''',

        '''try:
    x = int(input())

except ValueError:
    print("숫자를 입력하세요")

finally:
    print("종료")''',

        '''nums = [1, 2, 3, 4]

result = list(map(lambda x: x**2, nums))

print(result)'''
    ]
}

# -----------------------------
# 학생 목록
# -----------------------------

students = [
    "양서진",
    "김민수",
    "박지우",
    "최하은",
    "이도윤"
]

# -----------------------------
# 세션 상태 초기화
# -----------------------------

if "problem_index" not in st.session_state:
    st.session_state.problem_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "current_problem" not in st.session_state:
    st.session_state.current_problem = ""

# -----------------------------
# 제목
# -----------------------------

st.title("🐍 Python 코드 타자 연습")

# -----------------------------
# 상단 설정
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    student_name = st.selectbox(
        "학생 이름 선택",
        students
    )

with col2:
    difficulty = st.selectbox(
        "난이도 선택",
        ["초급", "중급", "고급"]
    )

# -----------------------------
# 현재 문제 생성
# -----------------------------

if st.session_state.current_problem == "":
    st.session_state.current_problem = random.choice(
        problems[difficulty]
    )

target = st.session_state.current_problem

# -----------------------------
# 정보 표시
# -----------------------------

st.write(f"👤 학생: {student_name}")
st.write(f"🏆 점수: {st.session_state.score}")
st.write(f"📘 난이도: {difficulty}")

st.divider()

# -----------------------------
# 문제 표시
# -----------------------------

st.subheader("📄 아래 코드를 그대로 입력하세요")

st.code(target, language="python")

st.divider()

# -----------------------------
# 코드 입력창
# -----------------------------

user_code = st_ace(
    language="python",
    theme="monokai",
    keybinding="vscode",
    font_size=16,
    tab_size=4,
    show_gutter=True,
    wrap=True,
    auto_update=True,
    height=300,
    placeholder="여기에 Python 코드를 입력하세요...",
)

# -----------------------------
# 시작 시간
# -----------------------------

if user_code and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# -----------------------------
# 정확도 계산
# -----------------------------

def calculate_accuracy(user, target):

    correct = 0

    for i in range(min(len(user), len(target))):
        if user[i] == target[i]:
            correct += 1

    return (correct / len(target)) * 100

# -----------------------------
# 결과 처리
# -----------------------------

if user_code:

    accuracy = calculate_accuracy(user_code, target)

    st.write(f"🎯 정확도: {accuracy:.2f}%")

    # 완전히 일치하면
    if user_code.strip() == target.strip():

        elapsed = time.time() - st.session_state.start_time

        chars = len(target)

        wpm = (chars / 5) / (elapsed / 60)

        st.success("✅ 정답!")

        st.write(f"⏱ 시간: {elapsed:.2f}초")
        st.write(f"⚡ 속도: {wpm:.2f} WPM")

        # 점수 증가
        st.session_state.score += 10

        # 다음 문제 자동 생성
        next_problem = random.choice(
            problems[difficulty]
        )

        st.session_state.current_problem = next_problem

        # 타이머 초기화
        st.session_state.start_time = None

        # 자동 새로고침
        time.sleep(1)

        st.rerun()
