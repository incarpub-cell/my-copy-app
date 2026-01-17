import streamlit as st
import google.generativeai as genai

# 보안을 위해 Secrets 금고에서 키를 가져옵니다.
try:
    MY_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=MY_KEY)
except Exception as e:
    st.error("API 키 설정에 문제가 있습니다. Secrets를 확인해주세요.")

st.title("🍪 쿠키 카피 생성기")

# 입력창
topic = st.text_input("어떤 상품의 카피를 만들까요?")

if st.button("쿠키 굽기"):
    if topic:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"{topic}에 대한 마케팅 문구 3개 만들어줘")
        st.success("완성된 쿠키입니다!")
        st.write(response.text)
    else:
        st.warning("상품명을 입력해주세요!")
