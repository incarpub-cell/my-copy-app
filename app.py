import streamlit as st
import google.generativeai as genai

# 1. API 키 설정
# 기존 하드코딩된 키 대신 Streamlit의 보안 기능(secrets)을 사용합니다.
import streamlit as st
MY_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=MY_KEY)

# 2. 시스템에 맞는 모델 자동 찾기 (핵심 로직)
@st.cache_resource # 모델 설정을 매번 하지 않도록 캐싱
def get_working_model():
    # 사용 가능한 모든 모델 목록을 가져옵니다.
    all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # 1.5-flash가 있으면 우선 선택, 없으면 pro 선택, 그것도 없으면 첫 번째 모델 선택
    if 'models/gemini-1.5-flash' in all_models:
        return genai.GenerativeModel('models/gemini-1.5-flash')
    elif 'models/gemini-pro' in all_models:
        return genai.GenerativeModel('models/gemini-pro')
    else:
        return genai.GenerativeModel(all_models[0])

# 웹 UI 구성
st.set_page_config(page_title="제휴마케팅 자동화 시스템", page_icon="🍪")
st.title("🍪 진짜 잘 팔리는 ‘온라인마켓 제품’ 카피 생성기")

# 입력 칸
product_name = st.text_input("1. 제품 이름", placeholder="예: 저당 타트체리 젤리")
product_features = st.text_area("2. 제품의 핵심 특징", placeholder="상세페이지의 주요 내용을 복사해서 넣어주세요.")
target_style = st.selectbox("3. 마케팅 스타일", ["MZ세대 (힙하게)", "직장인 (공감)", "주부/부모님 (신뢰)"])

if st.button("전문 마케터의 카피 생성 ✨"):
    if product_name and product_features:
        with st.spinner('사용 가능한 최적의 AI 모델을 연결 중입니다...'):
            try:
                # 작동하는 모델을 자동으로 가져옴
                model = get_working_model()
                
                prompt = f"""
                너는 광고 대행사 팀장이야. 아래 제품 정보를 바탕으로 당장 구매하고 싶게 만드는 카피를 짜줘.
                제품명: {product_name}
                핵심 장점: {product_features}
                타겟 톤앤매너: {target_style}
                
                제품의 식감이나 느낌, 특징을 ‘실감나게’ 표현해서 인스타/블로그 카피와 해시태그를 만들어줘.
                """
                
                response = model.generate_content(prompt)
                st.divider()
                st.balloons()
                st.success(f"생성 완료!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"최종 오류 발생: {e}")
    else:

        st.warning("제품 이름과 특징을 모두 입력해 주세요!")
