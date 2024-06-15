import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

voting_data = pd.read_csv('vote.csv')
age_data = pd.read_csv('age.csv', encoding='utf-8')

red = [230, 30, 43, 240]
alomost_red = [230, 30, 43, 180]
blue = [62, 77, 143, 240]
almost_blue = [62, 77, 143, 180]

districts_data = {
        "구": ["강남구", "서초구", "동작구", "은평구", "노원구", "강동구", "강북구", "강서구",
              "관악구", "광진구", "구로구", "금천구", "도봉구", "동대문구", "마포구", "서대문구",
              "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "종로구", "중구", "중랑구"],
        "구_eng": ['Gangnam', 'Seocho', 'Dongjak', 'Eunpyeong','Nowon', 'Gangdong', 'Gangbuk', 'Gangseo',
                  'Gwanak', 'Gwangjin', 'Guro', 'Geumcheon', 'Dobong', 'Dongdaemun', 'Mapo', 'Seodaemun',
                  'Seongdong', 'Seongbuk', 'Songpa', 'Yangcheon', 'Yeongdeunpo', 'Yongsan', 'Jongno', 'Jung', 'Jungnang'],
        "latitude": [37.5172, 37.4837, 37.5124, 37.6027, 37.6542, 37.5300, 37.6396, 37.5509,
                     37.4784, 37.5385, 37.4954, 37.4568, 37.6688, 37.5744, 37.5663, 37.5791,
                     37.5635, 37.5894, 37.5146, 37.5169, 37.5264, 37.5326, 37.5726, 37.5641, 37.6066],
        "longitude": [127.0473, 127.0323, 126.9393, 126.9291, 127.0568, 127.1237, 127.0257, 126.8497,
                      126.9516, 127.0823, 126.8874, 126.8954, 127.0471, 127.0400, 126.9016, 126.9368,
                      127.0368, 127.0167, 127.1066, 126.8664, 126.8962, 126.9900, 126.9793, 126.9979, 127.0928],
        "color": [red, red, alomost_red, blue, almost_blue, red, blue, almost_blue,
                  almost_blue, almost_blue, almost_blue, blue, almost_blue, alomost_red, almost_blue, alomost_red,
                  red, almost_blue, red, alomost_red, alomost_red, red, alomost_red, alomost_red, almost_blue],
        "size": [1000] * 25
    }
df = pd.DataFrame(districts_data)

def figure1():
    view_state = pdk.ViewState(
        latitude=37.5465,
        longitude=126.9780,
        zoom=10.4,
        pitch=50  # 지도의 틸트 각도 설정
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

def figure2():
    merged_data = pd.merge(voting_data, age_data, left_on=['구', '읍면동명'], right_on=['시군구명', '읍면동명'], how='left')
    grouped_by_district = merged_data.groupby('구').agg({'투표수': 'sum', '선거인수': 'sum'})
    grouped_by_district['투표율'] = grouped_by_district['투표수'] / grouped_by_district['선거인수'] * 100

    merged_data['weighted_age'] = merged_data['투표수'] * merged_data['전체 평균연령']
    age_by_district = merged_data.groupby('구').agg({'weighted_age': 'sum', '투표수': 'sum'})
    age_by_district['average_voting_age'] = age_by_district['weighted_age'] / age_by_district['투표수']

    candidate_columns = ['PYS', 'OSH', 'HKY', 'LSB', 'BYK', 'KJA', 'SMS', 'JDH', 'LDY', 'SJY']
    votes_per_candidate = merged_data.groupby('구')[candidate_columns].sum()
    total_votes_per_district = votes_per_candidate.sum(axis=1)
    for candidate in candidate_columns:
        votes_per_candidate[candidate + '_share'] = votes_per_candidate[candidate] / total_votes_per_district * 100
    vote_shares = votes_per_candidate[[col + '_share' for col in candidate_columns]]

    st.subheader('**서울특별시 내 구별 투표율**')
    fig1 = plt.figure(figsize=(10, 6))
    grouped_by_district['투표율'].sort_values().plot(kind='barh', color='skyblue')
    plt.title('Voter Turnout by District (%)')
    plt.xlabel('Turnout (%)')
    plt.ylabel('District')
    st.pyplot(fig1)
    st.write("서울특별시 내 각 구별 투표율을 그래프로 표현하였다. 모두 40%이상의 투표율이 나온 것으로 보궐선거 중 투표율이 높은 편임으로 데이터의 신뢰성을 확인할 수 있었다.  ")
    st.write('-'*50)

    st.subheader('**서울특별시 내 구별 평균 연령**')
    fig2 = plt.figure(figsize=(10, 6))
    age_by_district['average_voting_age'].sort_values().plot(kind='barh', color='lightgreen')
    plt.title('Average Voting Age by District')
    plt.xlabel('Average Age')
    plt.ylabel('District')
    st.pyplot(fig2)

    st.subheader('**서울특별시 내 구별 후보자별 득표율**')
    fig3 = plt.figure(figsize=(10, 6))
    sns.heatmap(vote_shares.T, annot=True, fmt=".1f", linewidths=.5, square=True, cmap='viridis')
    plt.title('Candidate Vote Share by District (%)')
    plt.xlabel('District')
    plt.ylabel('Candidate')
    st.pyplot(fig3)
    st.write("서울특별시 내 각 구별 평균연령과 후보자별 득표율을 그래프로 표현하였다. 득표율 그래프를 분석한 결과 진보 후보인 박영선 후보의 득표율 우세 지역 5개는 강북구, 금천구, 은평구, 광진구, 구로구이고 보수 후보인 오세훈 후보의 득표율 우세 5개 지역은 강남구, 서초구, 송파구, 용산구, 성동구이다. 박영선 후보의 득표율 우세 지역 5개 중 강북구, 금천구, 은평구는 평균 연령이 상위권이고 구로구는 중위권, 광진구는 하위권이고 오세훈 후보의 득표율 우세 5개 지역 중 용산구는 평균 연령이 상위권, 성동구는 중위권, 강남구, 서초구, 송파구는 하위권이다. 따라서 평균 연령이 높을 수록 진보 성향을 띄고 평균 연령이 낮을 수록 보수 성향을 띄는 경향성을 확인할 수 있었다.")

def figure3():
    district_park_votes = voting_data.groupby('구').agg({'투표수': 'sum', 'PYS': 'sum'})
    district_park_votes['득표율'] = district_park_votes['PYS'] / district_park_votes['투표수'] * 100

    district_average_age = age_data.groupby('시군구명').agg({'전체 평균연령': 'mean'})

    merged_data = pd.merge(district_park_votes, district_average_age, left_index=True, right_on='시군구명')

    # 산점도 그리기
    plt.figure(figsize=(10, 6))
    plt.scatter(merged_data['전체 평균연령'], merged_data['득표율'], alpha=0.7)

    # 추세선 계산 및 그리기
    z = np.polyfit(merged_data['전체 평균연령'], merged_data['득표율'], 1)
    p = np.poly1d(z)  # 추세선
    plt.plot(merged_data['전체 평균연령'], p(merged_data['전체 평균연령']), "r--")

    # 그래프 제목 및 라벨 설정
    plt.title('District Average Age vs Park Vote Share with Trend Line')
    plt.xlabel('Average Age')
    plt.ylabel('Park Vote Share (%)')
    plt.grid(True)
    st.pyplot(plt)

def figure4():
    district_oh_sehoon_votes = voting_data.groupby('구').agg({'투표수': 'sum', 'OSH': 'sum'})
    district_oh_sehoon_votes['득표율'] = district_oh_sehoon_votes['OSH'] / district_oh_sehoon_votes['투표수'] * 100

    # 지역별 평균 연령 계산
    district_average_age = age_data.groupby('시군구명').agg({'전체 평균연령': 'mean'})

    # 데이터 병합
    merged_data = pd.merge(district_oh_sehoon_votes, district_average_age, left_index=True, right_on='시군구명')

    # 산점도 그리기
    plt.figure(figsize=(10, 6))
    plt.scatter(merged_data['전체 평균연령'], merged_data['득표율'], alpha=0.7)

    # 추세선 계산 및 그리기
    z = np.polyfit(merged_data['전체 평균연령'], merged_data['득표율'], 1)
    p = np.poly1d(z)  # 추세선
    plt.plot(merged_data['전체 평균연령'], p(merged_data['전체 평균연령']), "r--")

    # 그래프 제목 및 라벨 설정
    plt.title('District Average Age vs Oh Vote Share with Trend Line')
    plt.xlabel('Average Age')
    plt.ylabel('Oh Vote Share (%)')
    plt.grid(True)
    st.pyplot(plt)

def figure5(district):
    voting_data['PYS_share'] = voting_data['PYS'] / voting_data['투표수'] * 100
    voting_data['OSH_share'] = voting_data['OSH'] / voting_data['투표수'] * 100

    grouped_data = voting_data.groupby(['구', '읍면동명']).agg({
        'PYS_share': 'mean',
        'OSH_share': 'mean'
    }).reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))  # 그래프 크기 설정
    district_data = grouped_data[grouped_data['구'] == district]
    district_data.sort_values(by='PYS_share', inplace=True)
    district_data.plot(x='읍면동명', y=['PYS_share', 'OSH_share'], kind='bar', ax=ax, title=f"{district} 득표율")
    plt.title(f'Vote Share in {district} by Subdistrict')
    plt.xlabel('Subdistrict')
    plt.ylabel('Vote Share (%)')
    plt.xticks(rotation=45)  # x축 레이블 회전
    plt.legend(title='Candidate')
    plt.tight_layout()  # 레이아웃 조정
    st.pyplot(plt)

def page_home():
    st.set_page_config(layout="wide")
    st.markdown(f"""
        <div style="color: gray; font-weight: bold; font-size: 30px; line-height: 0.6;">
            3614 이승민
        </div>
        """, unsafe_allow_html=True)
    st.title('4.7. 서울특별시장 보궐선거 결과 분석')
    figure1()
    st.write('4.7. 서울특별시장 선거 결과 상대적 우세 지역')

    with st.sidebar:
        st.title("데이터 분석 결과 해석")
        if st.button("구별 투표율, 평균 연령, 후보자별 득표율"):
            st.session_state.page = 'Page1'
            st.experimental_rerun()
        if st.button("평균 연령에 따른 득표율 산점도 및 추세선"):
            st.session_state.page = 'Page2'
            st.experimental_rerun()
        if st.button("성적 분석(결론)"):
            st.session_state.page = 'Page3'
            st.experimental_rerun()

def page_1():
    with st.sidebar:
        st.title("데이터 분석 결과 해석")
        if st.button("홈으로 이동"):
            st.session_state.page = 'Home'
            st.experimental_rerun()
        if st.button("구별 투표율, 평균 연령, 후보자별 득표율"):
            st.session_state.page = 'Page1'
            st.experimental_rerun()
        if st.button("평균 연령에 따른 득표율 산점도 및 추세선"):
            st.session_state.page = 'Page2'
            st.experimental_rerun()
        if st.button("구별 행정동별 득표울"):
            st.session_state.page = 'Page3'
            st.experimental_rerun()

    st.title('서울특별시 내 구별 투표율, 평균 연령, 후보자별 득표율 그래프')
    st.write("-"*50)
    figure2()
    st.write('-'*50)

def page_2():
    with st.sidebar:
        st.title("데이터 분석 결과 해석")
        if st.button("홈으로 이동"):
            st.session_state.page = 'Home'
            st.experimental_rerun()
        if st.button("구별 투표율, 평균 연령, 후보자별 득표율"):
            st.session_state.page = 'Page1'
            st.experimental_rerun()
        if st.button("평균 연령에 따른 득표율 산점도 및 추세선"):
            st.session_state.page = 'Page2'
            st.experimental_rerun()
        if st.button("구별 행정동별 득표울"):
            st.session_state.page = 'Page3'
            st.experimental_rerun()

    st.title('서울특별시 내 구별 평균 연령에 따른 주요 후보자의 득표율 산점도 및 추세선')
    st.write('-'*50)
    st.subheader('서울특별시 내 구별 평균 연령에 따른 박영선의 득표율 산점도 및 추세선')
    figure3()
    st.subheader('서울특별시 내 구별 평균 연령에 따른 오세훈의 득표율 산점도 및 추세선')
    figure4()
    st.write('-' * 50)
    st.write('서울특별시 내 각 구별 평균 연령과 후보자별 득표율을 그래프 및 표로 표현하였고 이를 바탕으로 연령에 따른 주요 후보자들의 득표율 산점도 및 추세선을 표현하였다. 이를 분석한 결과 진보 후보인 박영선 후보의 득표율이 평균 연령에 비례하는 경향을 보였고 보수 후보인 오세훈 후보의 득표율이 평균 연령에 반비례하는 경향을 보였다.')

def page_3():
    with st.sidebar:
        st.title("데이터 분석 결과 해석")
        if st.button("홈으로 이동"):
            st.session_state.page = 'Home'
            st.experimental_rerun()
        if st.button("구별 투표율, 평균 연령, 후보자별 득표율"):
            st.session_state.page = 'Page1'
            st.experimental_rerun()
        if st.button("평균 연령에 따른 득표율 산점도 및 추세선"):
            st.session_state.page = 'Page2'
            st.experimental_rerun()
        if st.button("구별 행정동별 득표울"):
            st.session_state.page = 'Page3'
            st.experimental_rerun()

    st.title('서울특별시 내 구별 투표율, 평균 연령, 후보자별 득표율 그래프')
    st.write('서울특별시 내 구별 행정동별 주요 후보자 득표율 그래프를 구별로 그래프로 표현하였다. 경제적,지역적 특성이 비슷한 주요 구별 평균 연령과 주요 후보자의 득표율 관계를 분석한 결과는 다음과 같다.')
    st.write('**종로구** 인접한 두 지역인 JR1·2·3·4와 JR5·6에서 평균 연령이 약 4살 높은 JR1·2·3·4rk JR5·6에 비해 오세훈 후보가 우세하고 SI1과 SI2에서 평균 연령이 약 3살 높은 SI1가 SI2에 비해 오세훈 후보가 우세하는 등 종로구 내 행정동 내에서는 평균 연령이 높을수록 보수 성향을 띄고 낮을수록 진보 성향을 띄는 경향성을 확인할 수 있다.')
    st.write('**중구** 인접한 두 지역인 M와 HH에서 평균 연령이 약 2살 높은 HH가 M에 비해 오세훈 후보가 우세하고 JCH과 P에서 평균 연령이 약 3살 높은 P가 JCH에 비해 오세훈 후보가 우세하는 등 중구 내 행정동 내에서는 평균 연령이 높을수록 보수 성향을 띄고 낮을수록 진보 성향을 띄는 경향성을 확인할 수 있다.')
    st.write('**노원구** 인접한 두 지역인 SK8와 SK9에서 평균 연령이 약 4살 높은 SK9가 SK8에 비해 오세훈 후보가 우세하고 HK1과 HK2에서 평균 연령이 약 2살 높은 HK1가 HK2에 비해 오세훈 후보가 우세하는 등 노원구 내 행정동 내에서는 평균 연령이 높을수록 보수 성향을 띄고 낮을수록 진보 성향을 띄는 경향성을 확인할 수 있다.')
    st.write('**양천구** 인접한 두 지역인 SJ3와 SJ7에서 평균 연령이 약 2살 높은 SJ7가 SJ3에 비해 오세훈 후보가 우세하고 SW4과 SW7에서 평균 연령이 약 3살 높은 SW7가 SW4에 비해 오세훈 후보가 우세하는 등 노원구 내 행정동 내에서는 평균 연령이 높을수록 보수 성향을 띄고 낮을수록 진보 성향을 띄는 경향성을 확인할 수 있다.')
    st.write('**영등포구** 인접한 두 지역인 DR2와 DR3에서 평균 연령이 약 2살 높은 DR2가 DR3에 비해 오세훈 후보가 우세하고 YI과 YDP에서 평균 연령이 약 4살 높은 YI가 YDP에 비해 오세훈 후보가 우세하는 등 노원구 내 행정동 내에서는 평균 연령이 높을수록 보수 성향을 띄고 낮을수록 진보 성향을 띄는 경향성을 확인할 수 있다.')
    st.write('위와 같이 서울특별시 내 대부분의 구에서 평균 연령이 높을수록 보수 성향을 띄고 낮을수록 진보 성향을 띄는 것을 확인할 수 있었다.')
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
        get_radius=1000,
        get_fill_color=selected_district['color'].iloc[0],
        pickable=True
    )

    # Render
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/light-v10'
    ))

    st.subheader(f'{option} 행정동별 주요 후보자의 특표율')
    figure5(df[df['구'] == option]["구_eng"].item())



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
