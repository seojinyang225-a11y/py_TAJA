import streamlit as st
from streamlit_ace import st_ace
import random
import time

st.set_page_config(
    page_title="Python 타자 연습",
    page_icon="⌨️",
    layout="wide"
)

# -----------------------------------
# 문제 데이터
# -----------------------------------

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
    print("종료")'''
    ]
}

# -----------------------------------
# 학생 목록
# -----------------------------------

students = [
    "양서진",
    "김민수",
    "박지우",
    "최하은",
    "이도윤"
]

# -----------------------------------
# 세션 상태
# -----------------------------------

if "score" not in st.session_state:
    st.session_state.score = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "current_problem" not in st.session_state:
    st.session_state.current_problem = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "editor_key" not in st.session_state:
    st.session_state.editor_key = 0

# -----------------------------------
# 제목
# -----------------------------------

st.title("🐍 Python 코드 타자 연습")

# -----------------------------------
# 설정
# -----------------------------------

col1, col2 = st.columns(2)

with col1:
    student_name = st.selectbox(
        "학생 이름",
        students
    )

with col2:
    difficulty = st.selectbox(
        "난이도",
        ["초급", "중급", "고급"]
    )

# -----------------------------------
# 문제 생성
# -----------------------------------

if st.session_state.current_problem == "":
    st.session_state.current_problem = random.choice(
        problems[difficulty]
    )

target = st.session_state.current_problem

# -----------------------------------
# 정보 표시
# -----------------------------------

st.write(f"👤 학생: {student_name}")
st.write(f"🏆 점수: {st.session_state.score}")

st.divider()

# -----------------------------------
# 문제 출력
# -----------------------------------

st.subheader("📄 아래 코드를 그대로 입력하세요")

st.code(target, language="python")

st.divider()

# -----------------------------------
# 코드 입력창
# -----------------------------------

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
    placeholder="코드를 입력하고 마지막에 Enter...",
    key=f"editor_{st.session_state.editor_key}"
)

# -----------------------------------
# 시작 시간
# -----------------------------------

if user_code and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# -----------------------------------
# 정확도 계산
# -----------------------------------

def calculate_accuracy(user, target):

    correct = 0

    for i in range(min(len(user), len(target))):
        if user[i] == target[i]:
            correct += 1

    return (correct / len(target)) * 100

# -----------------------------------
# 결과 처리
# -----------------------------------

if user_code:

    accuracy = calculate_accuracy(user_code, target)

    st.write(f"🎯 정확도: {accuracy:.2f}%")

    # 정답 판정
    if user_code.strip() == target.strip():

        elapsed = time.time() - st.session_state.start_time

        chars = len(target)

        wpm = (chars / 5) / (elapsed / 60)

        st.success("✅ 정답! Enter를 누르면 다음 문제")

        st.write(f"⏱ 시간: {elapsed:.2f}초")
        st.write(f"⚡ 속도: {wpm:.2f} WPM")

        # 결과 저장
        result = {
            "학생": student_name,
            "난이도": difficulty,
            "속도": round(wpm, 2),
            "정확도": round(accuracy, 2)
        }

        # 중복 저장 방지
        if len(st.session_state.history) == 0 or \
           st.session_state.history[-1] != result:

            st.session_state.history.append(result)

        # Enter 입력 감지
        if user_code.endswith("\n"):

            st.session_state.score += 10

            st.session_state.current_problem = random.choice(
                problems[difficulty]
            )

            st.session_state.start_time = None

            # 입력창 초기화
            st.session_state.editor_key += 1

            st.rerun()

# -----------------------------------
# 결과 기록
# -----------------------------------

st.divider()

st.subheader("📊 결과 기록")

if st.session_state.history:

    for i, h in enumerate(reversed(st.session_state.history), 1):

        st.write(
            f"{i}. 👤 {h['학생']} | "
            f"📘 {h['난이도']} | "
            f"⚡ {h['속도']} WPM | "
            f"🎯 {h['정확도']}%"
        )

else:
    st.info("아직 기록이 없습니다.")
