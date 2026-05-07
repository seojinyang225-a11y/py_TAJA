import streamlit as st
import time
import random

# 연습 문장 리스트
sentences = [
    "안녕하세요 타자 연습입니다",
    "파이썬은 재미있는 프로그래밍 언어입니다",
    "streamlit으로 웹앱 만들기",
    "github와 연동하여 배포하기",
    "오늘도 즐겁게 코딩합시다",
    "Typing practice makes you faster",
    "Python is very powerful",
    "Streamlit is simple and useful"
]

st.set_page_config(page_title="타자 연습", page_icon="⌨️")

st.title("⌨️ 타자 연습 웹앱")

# 세션 상태 초기화
if "sentence" not in st.session_state:
    st.session_state.sentence = random.choice(sentences)

if "start_time" not in st.session_state:
    st.session_state.start_time = None

# 랜덤 문장 출력
st.subheader("따라 입력하세요")
st.info(st.session_state.sentence)

# 입력창
user_input = st.text_input("여기에 입력:")

# 입력 시작 시간 기록
if user_input and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

# 결과 계산
if user_input == st.session_state.sentence:
    end_time = time.time()
    elapsed_time = end_time - st.session_state.start_time

    # 글자 수 기준 속도 계산
    chars = len(st.session_state.sentence)
    wpm = (chars / 5) / (elapsed_time / 60)

    st.success("완벽합니다! 🎉")

    st.write(f"⏱ 시간: {elapsed_time:.2f}초")
    st.write(f"⚡ 타자 속도: {wpm:.2f} WPM")

# 정확도 계산
if user_input:
    correct_chars = 0

    for i in range(min(len(user_input), len(st.session_state.sentence))):
        if user_input[i] == st.session_state.sentence[i]:
            correct_chars += 1

    accuracy = (correct_chars / len(st.session_state.sentence)) * 100

    st.write(f"🎯 정확도: {accuracy:.2f}%")

# 새 문장 버튼
if st.button("새 문장"):
    st.session_state.sentence = random.choice(sentences)
    st.session_state.start_time = None
    st.rerun()
