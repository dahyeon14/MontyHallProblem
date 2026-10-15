# DV_09 — Folium으로 지도 만들기 (Maps · Markers · Choropleth)

> 표기: 📘 = 슬라이드 / 💻 = Colab 실습 노트북 / 💡 = 이해용 주석 / ➕ = 추가 설명
> 자료: `DV_09_folium.pdf` + `DV_09_Creating_map_by_folium_1.ipynb`
> ⭐ **중간고사 범위의 마지막 강의(~DV_09)**

---
# PART A. 이론 (슬라이드)

## A-1. Folium이란? (슬라이드 2)
- 📘 **지리공간(geospatial) 데이터 시각화**를 위해 만들어진 강력한 Python 라이브러리
- 📘 **위도(latitude)와 경도(longitude)** 값으로 **세계 어디든 지도**를 만들 수 있음. 지도 위에 **마커(marker)와 클러스터(cluster)** 를 겹쳐 시각화 가능
- 📘 **다양한 스타일의 지도** 생성 가능: **street level map, stamen map** 등

## A-2. 지도 만들기 (슬라이드 3~6)
| 슬라이드 | 코드 | 내용 |
|---|---|---|
| 3. 세계 지도 | `import folium` → `world_map = folium.Map()` → `world_map` | 파라미터 없이 **기본 세계 지도** |
| 4. 캐나다 지도 | `folium.Map(location=[56.130, -106.35], zoom_start=4)` | **location(중심 좌표)** 과 **zoom_start(초기 확대 수준)** (빨간 박스 강조) |
| 5. Stamen Toner | `folium.Map(location=[56.130, -106.35], zoom_start=4, tiles='Stamen Toner')` | **tiles 파라미터**로 스타일 지정 — 흑백 고대비 |
| 6. Stamen Terrain | `... tiles='Stamen Terrain'` | **지형(산, 숲 등)** 이 보이는 스타일 |
- 📘 Recap: **tiles 파라미터**로 다양한 지도 스타일을 만들 수 있다. **`location` 파라미터 = 지도 중심점의 위도·경도 좌표**.

## A-3. 마커가 있는 지도 (슬라이드 7~13)
- 📘 마커는 지도에 **상호작용성과 맥락을 더함**. **특정 위치/관심 지점**을 나타내며 **클릭하면 추가 정보 제공**. “**길 안내 표지판**”처럼 중요한 요소를 강조.

**① 지도 초기화 (슬라이드 8)**
```python
import folium
canada_map = folium.Map(location=[56.1304, -106.3468], zoom_start=4)   # 캐나다 중심
canada_map
```
**② 마커와 라벨 추가 (슬라이드 9)** — 온타리오 주
```python
folium.Marker(location=[51.2538, -85.3232], popup='Ontario').add_to(canada_map)
```
- 📘 `popup` = **클릭하면 나오는 라벨**. `.add_to(지도)` 로 지도에 추가.

**③ 빨간 원 마커 — FeatureGroup (슬라이드 10~11)**
```python
canada_map = folium.Map(location=[56.130, -106.35], zoom_start=4)

# 피처 그룹 생성
ontario = folium.map.FeatureGroup()

# 스타일을 가진 CircleMarker를 그룹에 추가
ontario.add_child(
    folium.features.CircleMarker([51.25, -85.32], radius=5, color='red', fill_color='Red')
)

# 피처 그룹을 지도에 추가
canada_map.add_child(ontario)

# 라벨 붙이기
folium.Marker([51.25, -85.32], popup='Ontario').add_to(canada_map)
```
- 💡 **FeatureGroup = 여러 요소를 묶는 그룹 레이어**. `add_child()` 로 요소를 넣고, 그룹을 지도에 다시 `add_child()` 로 붙임.

**④ 여러 마커 (슬라이드 12~13)**
```python
# 위치와 팝업 목록
locations = [
    {"location": [45.4215, -75.6989],  "popup": "Ottawa"},
    {"location": [53.5461, -113.4938], "popup": "Edmonton"},
    {"location": [49.2827, -123.1207], "popup": "Vancouver"},
    # 필요하면 더 추가
]
# 각 위치마다 마커 추가
for loc in locations:
    folium.Marker(location=loc["location"], popup=loc["popup"]).add_to(map)
map          # 마커가 있는 지도 표시
```
**⑤ MarkerCluster (슬라이드 13)** — 마커를 **군집(클러스터)** 으로 묶기
```python
from folium.plugins import MarkerCluster

marker_cluster = MarkerCluster().add_to(map)      # 클러스터 객체 생성 후 지도에 추가
for loc in locations:
    folium.Marker(location=loc["location"], popup=loc["popup"]).add_to(marker_cluster)   # 지도 대신 cluster에 추가
```
- 📘 Recap: **popup 파라미터 = 클릭 시 라벨**. 마커는 **상호작용성과 맥락**을 더함.

## A-4. Choropleth Map (슬라이드 14~17)
- 📘 슬라이드 14: 예시 — 세계 영아 사망률 지도, 미국 주별 인구밀도 지도 (값이 클수록 진한 색)
- 📘 **Recap**: **choropleth map = 통계 변수의 측정값에 비례해 지역을 음영/무늬로 표시한 주제도(thematic map)**
- 📘 슬라이드 15 — **GeoJSON 파일**: Folium은 **GeoJSON, Pandas DataFrame, NumPy 배열** 등 여러 소스로 지도를 만들 수 있음. 샘플 구조:
```json
{ "type": "FeatureCollection",
  "features": [{ "type": "Feature",
                 "properties": { "name": "Brunei" },
                 "geometry": { "type": "Polygon", "coordinates": [ [114.204017, 4.525874], ... ] },
                 "id": "BRN" }, ... ] }
```
- 💡 구조: FeatureCollection → features(국가별 Feature) → **properties.name(국가 이름)**, **geometry(경계 좌표 Polygon)**, id(국가 코드).
- 📘 **Choropleth를 만들 때 Folium은 해당 지역의 지리 데이터가 담긴 GeoJSON 파일이 필요**.

**슬라이드 16~17 코드: 캐나다 이민 세계 지도**
```python
# 기본 세계 지도 (슬라이드는 Mapbox Bright 타일 사용)
world_map = folium.Map(zoom_start=2, tiles='Mapbox Bright')

# geojson 파일
world_geo = r'world_countries.json'

# 1980~2013 캐나다 이민 총합으로 choropleth 생성
world_map.choropleth(
    geo_data=world_geo,
    data=df_canada,
    columns=['Country', 'Total'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    legend_name='Immigration to Canada')
world_map
```
- 📘 Recap: **Mapbox Bright 타일은 지도에 모든 나라 이름을 표시**.

## A-5. Recap 요약 (슬라이드 18)
- Folium = **지리공간 데이터 시각화** 라이브러리
- **tiles 파라미터**로 지도 스타일 변경 (street level, stamen 등)
- **location** = 지도 중심의 위도·경도
- **popup** = 클릭 시 라벨
- **Choropleth** = 통계 변수 값에 비례해 음영 처리 / **GeoJSON 필수**
- **Mapbox Bright** 타일 = 모든 나라 이름 표시

---
# PART B. Colab 실습 (노트북 `DV_09_Creating_map_by_folium_1.ipynb`)

## B-0. 전체 순서
```
[준비]     import numpy, pandas → import folium
[기본 지도] folium.Map() → location, zoom_start → tiles(스타일)
[마커]     경찰 사건 CSV → 상위 100건 → 샌프란시스코 지도 → FeatureGroup+CircleMarker → Marker(popup) → CircleMarker(popup) → MarkerCluster
[Choropleth] 이민 CSV + GeoJSON → 세계 지도 → folium.Choropleth(geo_data, data, columns, key_on, fill_color, ...)
```
- 💻 **Folium을 쓰는 이유**: 지리공간 시각화 전용으로 개발. **plotly** 같은 다른 라이브러리는 **API 호출 횟수 제한**이 있을 수 있지만 Folium은 **완전 무료**.
- 💻 Folium = **Leaflet 지도**를 만드는 라이브러리. **결과가 인터랙티브**라 **대시보드 제작에 유용**. 파이썬에서 데이터를 가공하고 → Leaflet 지도에 시각화(Folium 공식 문서). **GeoJSON/TopoJSON 오버레이**와 **데이터 바인딩**으로 choropleth(color-brewer 색 구성) 지원.

## B-1. 준비 (셀 5~8)
```python
import numpy as np
import pandas as pd
#!pip3 install folium==0.5.0      # 기본 설치되어 있지 않으면 설치 (주석 처리됨)
import folium
print('Folium installed and imported!')
```

## B-2. 기본 지도와 확대 수준 (셀 11~21)
```python
world_map = folium.Map()                                          # 기본 세계 지도
world_map

world_map = folium.Map(location=[56.130, -106.35], zoom_start=4)  # 캐나다 중심, 낮은 줌
world_map = folium.Map(location=[56.130, -106.35], zoom_start=8)  # 더 높은 줌 → 더 확대
```
- 📘 **지도의 모든 위치는 위도(Latitude)와 경도(Longitude)** 로 정의. 중심을 **[0, 0]** 으로 줄 수도 있음.
- 📘 **줌(zoom) 수준이 높을수록 중심을 더 확대**해서 보여줌.
- 📘 Folium 지도는 **인터랙티브**: 초기 줌과 상관없이 원하는 곳을 확대 가능.

### 연습: 한국 지도 (셀 19~21)
```python
latitude = 35.9078
longitude = 127.7669
korea_map = folium.Map(location=[latitude, longitude], zoom_start=4)    # 문제는 줌 4 (노트북 입력 셀은 6으로 되어 있음)
korea_map
```
- ⚠ 문제 문장·정답 셀은 **zoom 4**, 코드 입력 셀 예시는 **zoom 6**으로 서로 다름 → 시험 문제에서 주어진 숫자를 사용.
- 💡 **location은 [위도, 경도] 순서** (위도 먼저!). 한국 35.9, 127.8.

## B-3. 지도 스타일(tiles) (셀 22~34)
| tiles 값 | 특징 |
|---|---|
| (기본) | OpenStreetMap 스타일 |
| **`'Cartodb dark_matter'`** | **고대비 흑백(B+W)** 지도. 데이터 매시업, 강 굽이·해안 지역 탐색에 적합 |
| **`'Cartodb positron'`** | **밝고 미니멀**한 디자인(흰/밝은 배경, 단순한 선). **현대적이고 시각적으로 깔끔**. 확대하면 **국경이 나타나고 국가명이 영어로 표시** |
```python
# Cartodb dark_matter
world_map = folium.Map(location=[56.130, -106.35], zoom_start=4, tiles='Cartodb dark_matter')
# Cartodb positron
world_map = folium.Map(location=[56.130, -106.35], zoom_start=4, tiles='Cartodb positron')
```
- 💡 슬라이드는 **Stamen Toner / Stamen Terrain / Mapbox Bright**, 노트북은 **Cartodb dark_matter / Cartodb positron** — 모두 **`tiles=` 파라미터로 이름만 바꾸는 방식**.
- ➕ (슬라이드에 없는 보충) 최신 Folium에서는 Stamen·Mapbox 타일이 더 이상 기본 지원되지 않아 슬라이드 코드를 그대로 실행하면 안 나올 수 있음. 시험에서는 슬라이드/노트북 스타일명과 `tiles=` 문법만 알면 됨.

### 연습: 멕시코 지도 (밝고 현대적, 줌 6)
```python
mexico_latitude = 23.6345
mexico_longitude = -102.5528
mexico_map = folium.Map(location=[mexico_latitude, mexico_longitude], zoom_start=6, tiles='Cartodb positron')
mexico_map
```

---
## B-4. 마커가 있는 지도: 샌프란시스코 경찰 사건 데이터

### 데이터 (셀 36~47)
- 💻 **San Francisco Police Department Incidents (2016)** — SFPD 범죄 신고 시스템 데이터. 주소·위치는 **익명화**(블록 중간 또는 교차로로 이동).
```python
df_incidents = pd.read_csv('DV_09_data_police_2016.csv')
df_incidents.head(10)
df_incidents.shape          # (38571, 13)
```
**13개 열(features)**
| # | 열 | 의미 |
|---|---|---|
| 1 | IncidntNum | 사건 번호 |
| 2 | **Category** | 범죄/사건 **범주** |
| 3 | Descript | 사건 설명 |
| 4 | DayOfWeek | 요일 |
| 5 | Date | 날짜 |
| 6 | Time | 시간 |
| 7 | PdDistrict | 경찰서 관할 구역 |
| 8 | Resolution | 처리 결과(체포 여부) |
| 9 | Address | 사건 발생 근처 주소 |
| 10 | **X** | **경도(longitude)** |
| 11 | **Y** | **위도(latitude)** |
| 12 | Location | (위도, 경도) 튜플 |
| 13 | PdId | 경찰서 ID |
- ⚠ **X = 경도, Y = 위도** (헷갈리기 쉬움!). Folium은 `[위도, 경도]` = `[Y, X]` 순서로 넣어야 함.
- 📘 노트북 본문은 “150,500건”이라 적혀 있지만 실제 `shape`은 **(38571, 13)**. 연산량을 줄이려고 **처음 100건만** 사용:
```python
limit = 100
df_incidents = df_incidents.iloc[0:limit, :]     # 행 0~99, 모든 열
df_incidents.shape                                # (100, 13)
```
### 지도 만들기 (셀 48~50)
```python
latitude = 37.77
longitude = -122.42
sanfran_map = folium.Map(location=[latitude, longitude], zoom_start=12)   # 기본 스타일, 줌 12
```
### 방법 ①: FeatureGroup + CircleMarker로 위치 표시 (셀 51~52)
- 📘 Folium에서 지도에 데이터 위치를 겹치려면 **feature group을 만들어 자체 feature/스타일을 부여한 뒤 지도에 추가**.
```python
incidents = folium.map.FeatureGroup()                 # 피처 그룹 생성

for lat, lng, in zip(df_incidents.Y, df_incidents.X):  # 위도(Y), 경도(X)를 짝지어 순회
    incidents.add_child(
        folium.vector_layers.CircleMarker(
            [lat, lng],
            radius=5,              # 원 크기
            color='yellow',        # 테두리색
            fill=True,
            fill_color='blue',     # 채움색
            fill_opacity=0.6))     # 채움 투명도

sanfran_map.add_child(incidents)                       # 그룹을 지도에 추가
```
- 💡 `zip(a, b)` = 두 리스트를 **같은 순번끼리 쌍**으로 묶어 순회.

### 방법 ②: 팝업 텍스트 — `Marker(popup=)` (셀 53~54)
- 📘 마커 위에 **마우스를 올리면(노트북 표현)/클릭하면 범죄 범주(Category)** 가 표시되도록.
```python
latitudes  = list(df_incidents.Y)
longitudes = list(df_incidents.X)
labels     = list(df_incidents.Category)

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label).add_to(sanfran_map)
sanfran_map.add_child(incidents)
```
- 문제: 마커가 너무 많아 지도가 **혼잡(congested)**. 해결책 2가지 ↓

### 해결책 A (간단): 위치 마커 제거 후 **원형 마커 자체에 팝업** (셀 55~56)
```python
sanfran_map = folium.Map(location=[latitude, longitude], zoom_start=12)
for lat, lng, label in zip(df_incidents.Y, df_incidents.X, df_incidents.Category):
    folium.vector_layers.CircleMarker(
        [lat, lng],
        radius=5, color='yellow', fill=True,
        popup=label,                                  # 원형 마커에 팝업
        fill_color='blue', fill_opacity=0.6
    ).add_to(sanfran_map)                             # 지도에 직접 추가
```
### 해결책 B (정석): **MarkerCluster로 묶기** (셀 57~59) ⭐
- 📘 마커를 **군집(cluster)** 으로 묶어, 각 클러스터에 **그 지역의 범죄 수**를 표시. 클러스터는 **샌프란시스코의 지역별 묶음(pocket)** 으로 따로 분석 가능.
```python
from folium import plugins

sanfran_map = folium.Map(location=[latitude, longitude], zoom_start=12)

incidents = plugins.MarkerCluster().add_to(sanfran_map)      # MarkerCluster 객체를 지도에 추가

for lat, lng, label in zip(df_incidents.Y, df_incidents.X, df_incidents.Category):
    folium.Marker(location=[lat, lng], icon=None, popup=label).add_to(incidents)   # 지도가 아니라 cluster에 추가
sanfran_map
```
- 📘 해석: **최대로 축소하면 모든 마커가 하나의 “전역 클러스터(global cluster)” = 100개(전체 범죄 수)** 로 합쳐짐. **확대할수록 작은 클러스터로 쪼개지고**, 끝까지 확대하면 **개별 마커**가 됨.
- 💡 핵심 차이: 일반 마커는 `.add_to(지도)`, 클러스터 마커는 **`.add_to(cluster)`**.

---
## B-5. Choropleth Map: 세계 이민 지도

### 개념 (셀 60~61)
- 📘 **Choropleth** = **통계 변수의 측정값에 비례해 지역을 음영/무늬로 표시**한 주제도. **인구밀도, 1인당 소득** 같은 값이 **지역별로 어떻게 달라지는지**, **한 지역 내 변동 수준**을 쉽게 보여줌. (예: 주별 제곱마일당 인구 지도)

### 데이터 (셀 62~67)
```python
df_can = pd.read_csv('DV_05_data_canada_immigration.csv')
print(df_can.shape)        # (195, 40)
```
### GeoJSON + 기본 지도 (셀 68~69)
- 📘 Choropleth에는 관심 지역(주/카운티/국가)의 **경계를 정의한 GeoJSON 파일**이 필요. 세계 지도 → **모든 나라 경계가 있는 GeoJSON**.
```python
world_geo = r'DV_09_json_world_countries.json'                 # GeoJSON 파일 경로 (r'' = raw string)
world_map = folium.Map(location=[0, 0], zoom_start=2)         # [0, 0] 중심, 초기 줌 2
```
### `choropleth` 주요 파라미터 (셀 70~71) ⭐ 시험 단골
| 파라미터 | 의미 |
|---|---|
| **`geo_data`** | **GeoJSON 파일**(경계 데이터) |
| **`data`** | 데이터가 들어 있는 **DataFrame** |
| **`columns`** | choropleth에 쓸 DataFrame의 **열** — `['Country', 'Total']` (**[키 열, 값 열]**) |
| **`key_on`** | **GeoJSON 안에서 관심 변수(국가 이름)를 담은 키**. GeoJSON을 텍스트 편집기로 열어 국가 이름이 들어 있는 키를 확인해야 함. 여기서는 `name`. **대소문자 구분** — GeoJSON에 있는 그대로 `'feature.properties.name'` |
```python
world_map = folium.Map(location=[56.1304, -106.3468], zoom_start=2)

folium.Choropleth(
    geo_data=world_geo,                   # 경계 GeoJSON 경로/객체
    data=df_can,                          # 국가별 이민 데이터가 든 DataFrame
    columns=['Country', 'Total'],         # 사용할 열
    key_on='feature.properties.name',     # DataFrame의 Country와 GeoJSON의 국가 이름을 연결
    fill_color='YlOrRd',                  # 색 스케일 (노랑-주황-빨강)
    fill_opacity=0.7,                     # 채움 투명도
    line_opacity=0.2,                     # 경계선 투명도
    nan_fill_color='lightgray',           # 결측값(NaN) 국가 색
    nan_fill_opacity=0.4,                 # 결측값 국가 투명도
    legend_name='Immigration to Canada',  # 범례 제목
    reset=True                            # 다시 불러올 때 리셋
).add_to(world_map)
world_map
```
- 📘 해석: 범례상 **색이 진하고 빨간색에 가까울수록 이민자가 많음**. 1980~2013년 **가장 많은 이민: China, India, Philippines**, 이어서 **Poland, Pakistan, 그리고 (흥미롭게도) US**.
- 💡 **연결 원리**: `data`의 `Country` 값 ↔ GeoJSON의 `feature.properties.name` 값이 **글자 그대로 일치해야** 그 나라가 칠해짐. 일치하지 않으면 **NaN → `nan_fill_color`(회색)**.
- 💡 슬라이드는 `world_map.choropleth(...)`(구 방식), 노트북은 `folium.Choropleth(...).add_to(world_map)`(신 방식). **파라미터 이름은 동일**(`geo_data, data, columns, key_on, fill_color, legend_name ...`).
- 📘 확장 아이디어: **개별 연도나 10년 단위**로 choropleth를 만들어 전체 기간(1980~2013)과 비교.

---
# PART C. 정리표

## C-1. Folium 객체·함수 정리
| 하고 싶은 것 | 코드 | 핵심 파라미터 |
|---|---|---|
| 지도 만들기 | `folium.Map(...)` | `location=[위도, 경도]`, `zoom_start`(클수록 확대), `tiles`(스타일) |
| 지도 스타일 | `tiles='Cartodb dark_matter'`, `'Cartodb positron'` (슬라이드: `'Stamen Toner'`, `'Stamen Terrain'`, `'Mapbox Bright'`) | |
| 마커(핀) | `folium.Marker(location, popup=).add_to(map)` | `popup`(클릭 라벨) |
| 원형 마커 | `folium.vector_layers.CircleMarker([lat,lng], radius, color, fill, fill_color, fill_opacity, popup)` (슬라이드: `folium.features.CircleMarker`) | |
| 마커 묶음 레이어 | `folium.map.FeatureGroup()` + `.add_child(...)` → `map.add_child(group)` | |
| 군집 | `plugins.MarkerCluster().add_to(map)` → 마커를 `.add_to(cluster)` | `from folium import plugins` / `from folium.plugins import MarkerCluster` |
| Choropleth | `folium.Choropleth(geo_data, data, columns, key_on, fill_color, fill_opacity, line_opacity, nan_fill_color, nan_fill_opacity, legend_name, reset).add_to(map)` | GeoJSON 필수 |

## C-2. plot별 사용 변수(데이터)
| 지도 | 데이터 | 위치 정보 | 값/라벨 |
|---|---|---|---|
| 기본 지도 | 없음 | `location=[위도, 경도]` | — |
| 마커 지도 | `df_incidents` | **Y(위도), X(경도)** | `Category`(popup) |
| 클러스터 지도 | 동일 | Y, X | `Category` |
| Choropleth | `df_can` + GeoJSON | **Country ↔ GeoJSON name** (`key_on`) | **`Total`** (색 농도) |

## C-3. 시험 대비 포인트
1. **Folium = 지리공간 시각화** / 위도·경도 / 마커·클러스터 / 다양한 스타일 / **무료**(plotly는 API 호출 제한 가능).
2. `folium.Map(location=[위도, 경도], zoom_start=N, tiles='스타일')` — **location은 [위도, 경도] 순서**, **zoom_start↑ = 확대**.
3. **tiles**로 스타일 변경 (Cartodb dark_matter = 흑백 고대비, Cartodb positron = 밝고 미니멀, Stamen Toner/Terrain, Mapbox Bright = 모든 나라 이름 표시).
4. **popup** = 클릭하면 나타나는 라벨. **마커 많으면 → ① CircleMarker에 popup ② MarkerCluster**.
5. **MarkerCluster**: 전체 축소 시 전역 클러스터(전체 개수, 예: 100), 확대하면 분리 → 개별 마커. 마커를 **cluster에 add**.
6. **데이터프레임 X = 경도, Y = 위도** → 지도에는 `[Y, X]`.
7. **Choropleth** = 값에 비례해 지역 색칠. **GeoJSON 필수**. 파라미터 `geo_data / data / columns / key_on / fill_color / legend_name`. **`key_on='feature.properties.name'`은 대소문자 구분**, GeoJSON 키 이름 확인 필요.
8. 색이 **진한 빨강일수록 이민자 많음**(YlOrRd). 상위: China, India, Philippines.
9. GeoJSON 구조: FeatureCollection → features → (properties.name, geometry.Polygon, id).
