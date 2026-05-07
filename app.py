import streamlit as st
import random
import time
from streamlit_ace import st_ace

st.set_page_config(
    page_title="Python 타자 연습",
    page_icon="⌨️",
    layout="wide"
)

st.title("🐍 Python 코드 타자 연습")

# 난이도별 문제
problems = {
    "초급": [
        '''print("Hello World")''',

        '''name = input("이름 입력: ")
print("안녕하세요", name)''',

        '''for i in range(5):
    print(i)'''
    ],

    "중급": [
        '''numbers = [1, 2, 3, 4, 5]

for n in numbers:
    if n % 2 == 0:
        print(n)''',

        '''def add(a, b):
    return a + b

result = add(3, 5)
print(result)''',

        '''students = {
    "민수": 90,
    "지우": 85
}

for name, score in students.items():
    print(name, score)'''
    ],

    "고급": [
        '''class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"안녕하세요 {self.name}")

p = Person("서진")
p.greet()''',

        '''try:
    file = open("test.txt", "r")
    content = file.read()

except FileNotFoundError:
    print("파일이 없습니다")

finally:
    print("종료")''',

        '''nums = [1, 2, 3, 4, 5]

squared = list(map(lambda x: x**2, nums))

print(squared)'''
    ]
}

# 세션 상태
if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "target_code" not in st.session_state:
    st.session_state.target_code = ""

# 난이도 선택
difficulty = st.selectbox(
    "난이도 선택",
    ["초급", "중급", "고급"]
)

# 새 문제 버튼
if st.button("🎲 새 문제"):
    st.session_state.target_code = random.choice(
        problems[difficulty]
    )
    st.session_state.start_time = None

# 최초 실행 시 문제 생성
if st.session_state.target_code == "":
    st.session_state.target_code = random.choice(
        problems[difficulty]
    )

target = st.session_state.target_code

# 제시문 출력
st.subheader("📄 제시된 코드를 따라 입력하세요")

st.code(target, language="python")

st.divider()

st.subheader("⌨️ 코드 입력")

# 코드 입력창
user_code = st_ace(
    language='python',
    theme='monokai',
    keybinding='vscode',
    font_size=16,
    tab_size=4,
    show_gutter=True,
    wrap=True,
    auto_update=True,
    height=300,
    placeholder="여기에 Python 코드를 입력하세요...",
)

# 시작 시간
if user_code and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# 정확도 계산
def calculate_accuracy(a, b):
    correct = 0

    for i in range(min(len(a), len(b))):
        if a[i] == b[i]:
            correct += 1

    return (correct / len(b)) * 100

# 결과 표시
if user_code:

    accuracy = calculate_accuracy(user_code, target)

    st.write(f"🎯 정확도: {accuracy:.2f}%")

    # 완성 체크
    if user_code.strip() == target.strip():

        elapsed = time.time() - st.session_state.start_time

        chars = len(target)

        wpm = (chars / 5) / (elapsed / 60)

        st.success("✅ 코드 일치! 완료!")

        st.write(f"⏱ 시간: {elapsed:.2f}초")
        st.write(f"⚡ 타자 속도: {wpm:.2f} WPM")

        if wpm > 80:
            st.balloons()
