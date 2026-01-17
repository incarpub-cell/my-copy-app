import streamlit as st
import google.generativeai as genai

# [보안 설정] 깃허브에 노출되지 않도록 Streamlit Secrets에서 키를 가져옵니다.
# 주의: 깃허브 코드에는 아래 'GEMINI_API_KEY'라는 이름표만 남겨둡니다.
try:
    MY_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=MY_KEY)
except Exception as e:
    st.error("API 키를 찾을 수 없습니다. Streamlit Cloud의 Settings > Secrets에 키를 설정해주세요.")
    st.stop() # 키가 없으면 실행을 중단합니다.

# [핵심 로직] 404 에러를 방지하는 모델 자동 감지 함수
@st.cache_resource
def get_working_model():
    # 현재 내 계정에서 사용 가능한 모델 목록을 호출합니다.
    all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # 성능이 좋은 모델 순서대로 자동 매칭합니다.
    if 'models/gemini-1.5-flash' in all_models:
        return genai.GenerativeModel('models/gemini-1.5-flash')
    elif 'models/gemini-pro' in all_models:
        return genai.GenerativeModel('models/gemini-pro')
    else:
        # 그 외 사용 가능한 첫 번째 모델을 강제로 연결하여 오류를 차단합니다.
        return genai.GenerativeModel(all_models[0])

# [UI] 웹 화면 구성
st.set_page_config(page_title="제휴마케팅 카피 자동화 시스템", page_icon="🍪")
st.title("🍪잘 팔리는 '제품 카피' 생성기")

st.markdown("---") # 구분선

product_name = st.text_input("1. 제품 이름", placeholder="예: 저당 타트체리 젤리")
product_features = st.text_area("2. 제품의 핵심 특징", placeholder="상세페이지 내용을 복사해 넣으세요.")
target_style = st.selectbox("3. 마케팅 스타일", ["MZ세대 (힙하게)", "직장인 (공감)", "주부/부모님 (신뢰)"])

st.markdown("---")

if st.button("전문 마케터의 카피 생성 ✨"):
    if product_name and product_features:
        with st.spinner('AI 마케터가 카피를 굽고 있습니다...'):
            try:
                model = get_working_model()
                prompt = f"""
                너는 광고 대행사 팀장이야. 아래 정보를 바탕으로 당장 구매하고 싶게 만드는 카피를 짜줘.
                제품명: {product_name}
                핵심 장점: {product_features}
                타겟 스타일: {target_style}
                
                제품 컨셉, 특징을 살려 인스타/블로그용 문구와 해시태그를 만들어줘.
                답변은 마크다운 형식으로 깔끔하게 작성해줘.
                """
                response = model.generate_content(prompt)
                st.balloons()
                st.success("맛있는 카피가 완성되었습니다!")
                st.markdown(response.text)
            except Exception as e:
                # 403 Leaked 에러 발생 시 안내 문구
                if "403" in str(e) or "leaked" in str(e).lower():
                    st.error("현재 API 키가 차단된 상태입니다. Google AI Studio에서 새 키를 발급받아 Secrets에 업데이트해주세요.")
                else:
                    st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("제품 정보와 특징을 입력해 주세요!")




