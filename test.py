import streamlit as st
import pandas as pd
import pydeck as pdk

districts_data = {
        "구": ["강남구", "서초구", "동작구", "은평구", "노원구", "강동구", "강북구", "강서구",
              "관악구", "광진구", "구로구", "금천구", "도봉구", "동대문구", "마포구", "서대문구",
              "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "종로구", "중구", "중랑구"],
        "latitude": [37.5172, 37.4837, 37.5124, 37.6027, 37.6542, 37.5300, 37.6396, 37.5509,
                     37.4784, 37.5385, 37.4954, 37.4568, 37.6688, 37.5744, 37.5663, 37.5791,
                     37.5635, 37.5894, 37.5146, 37.5169, 37.5264, 37.5326, 37.5726, 37.5641, 37.6066],
        "longitude": [127.0473, 127.0323, 126.9393, 126.9291, 127.0568, 127.1237, 127.0257, 126.8497,
                      126.9516, 127.0823, 126.8874, 126.8954, 127.0471, 127.0400, 126.9016, 126.9368,
                      127.0368, 127.0167, 127.1066, 126.8664, 126.8962, 126.9900, 126.9793, 126.9979, 127.0928],
        "color": [[230, 30, 43, 180]] * 10 + [[62, 77, 143, 180]] * 7 + [[230, 30, 43, 240]] * 4 + [
            [62, 77, 143, 240]] * 4,
        "size": [1000] * 25
    }
df = pd.DataFrame(districts_data)

def figure1():
    view_state = pdk.ViewState(
        latitude=37.5665,
        longitude=126.9780,
        zoom=10,
        pitch=45  # 지도의 틸트 각도 설정
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position=["longitude", "latitude"],
        get_color="color",
        get_radius="size",
        pickable=True,
        opacity=0.8
    )

    # Render
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/light-v10'
    ))

def page_home():
    st.write('학번 이름')
    st.title('제목을 입력해 주세요')
    figure1()

    with st.sidebar:
        st.title("사이드바 제목 입력")
        if st.button("버튼 제목(구별 데이터)"):
            st.session_state.page = 'Page1'
            st.experimental_rerun()
        if st.button("테스트 응시(우세 후보 분석)"):
            st.session_state.page = 'Page2'
            st.experimental_rerun()
        if st.button("성적 분석(결론)"):
            st.session_state.page = 'Page3'
            st.experimental_rerun()

def page_1():
    st.title('하위 페이지 제목 입력')
    st.write('**소제목 입력**')
    st.text('대충 이런 거 뭐 구현 되겠지? 일단 사진으로 대체')
    st.image('sample_image1.png')

    with st.sidebar:
        st.title("사이드바 제목 입력")
        if st.button("홈으로 이동"):
            st.session_state.page = 'Home'
            st.experimental_rerun()
        if st.button("버튼 제목(구별 데이터)"):
            st.session_state.page = 'Page1'
            st.experimental_rerun()
        if st.button("테스트 응시(우세 후보 분석)"):
            st.session_state.page = 'Page2'
            st.experimental_rerun()
        if st.button("성적 분석(결론)"):
            st.session_state.page = 'Page3'
            st.experimental_rerun()

def page_2():
    st.title('하위 페이지 제목 입력')
    st.write('**소제목 입력**')
    st.text('대충 지역구별 데이터 뭔가 있었던 거 같은데..')
    option = st.selectbox("지역구를 선택하세요", df['구'])
    selected_district = df[df['구'] == option]

    view_state = pdk.ViewState(
        latitude=selected_district['latitude'].iloc[0],
        longitude=selected_district['longitude'].iloc[0],
        zoom=12
    )

    layer = pdk.Layer(
        'ScatterplotLayer',
        selected_district,
        get_position=['longitude', 'latitude'],
        get_radius=200,
        get_fill_color=[255, 0, 0, 140],
        pickable=True
    )

    # Render
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/light-v10'
    ))

    if option == '강남구':
        st.write('')
        st.write('**여기다가 지역구별 내용들 적으면 됨**')



    with st.sidebar:
        st.title("사이드바 제목 입력")
        if st.button("홈으로 이동"):
            st.session_state.page = 'Home'
            st.experimental_rerun()
        if st.button("버튼 제목(구별 데이터)"):
            st.session_state.page = 'Page1'
            st.experimental_rerun()
        if st.button("테스트 응시(우세 후보 분석)"):
            st.session_state.page = 'Page2'
            st.experimental_rerun()
        if st.button("성적 분석(결론)"):
            st.session_state.page = 'Page3'
            st.experimental_rerun()

def page_3():
    st.title('하위 페이지 제목 입력')
    st.write('**소제목 입력**')
    st.text('결론 적을 페이지')

    with st.sidebar:
        st.title("사이드바 제목 입력")
        if st.button("홈으로 이동"):
            st.session_state.page = 'Home'
            st.experimental_rerun()
        if st.button("버튼 제목(구별 데이터)"):
            st.session_state.page = 'Page1'
            st.experimental_rerun()
        if st.button("테스트 응시(우세 후보 분석)"):
            st.session_state.page = 'Page2'
            st.experimental_rerun()
        if st.button("성적 분석(결론)"):
            st.session_state.page = 'Page3'
            st.experimental_rerun()

if 'page' not in st.session_state:
    st.session_state.page = 'Home'


if st.session_state.page == 'Home':
    page_home()
elif st.session_state.page == 'Page1':
    page_1()
elif st.session_state.page == 'Page2':
    page_2()
elif st.session_state.page == 'Page3':
    page_3()
