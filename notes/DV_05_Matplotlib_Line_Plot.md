# DV_05 — Matplotlib 소개 + Line Plot 실습

> 표기: 📘 = 슬라이드 / 💻 = Colab 실습 노트북 / 💡 = 이해용 주석 / ➕ = 추가 설명
> 자료: `DV_05_matplotlib.pdf`(이론+Lab 안내) + `DV_05_code_matplotlib_line_plots.ipynb`(실습)

---
# PART A. 이론 (슬라이드)

## A-1. Matplotlib 소개 (슬라이드 2)
- 📘 **John Hunter**(미국 신경생물학자)가 만든 Python 데이터 시각화 라이브러리
- 📘 원래 **EEG·ECoG(뇌파) 신호 시각화**를 위해 개발
- 📘 Hunter의 팀은 **단일 라이선스의 독점 소프트웨어**를 썼고, 이를 넓게 쓰기 위해 **Matlab 기반 대안**을 만들게 됨
- 📘 Matlab처럼 **쉽게 그래픽을 생성**하는 도구로 발전
- 💡 그래서 `pyplot` 함수들이 Matlab 명령어 스타일을 닮았음 (“command style functions”).

## A-2. Matplotlib 아키텍처 — 3개 레이어 (슬라이드 3~8)
| 레이어 | 역할 | 비유(슬라이드 4) |
|---|---|---|
| **Scripting Layer (pyplot)** | 작업과 plot 생성을 단순화하는 **가벼운 스크립팅 인터페이스** | 가볍다 |
| **Artist Layer (Artist)** | 화면의 모든 요소를 객체로 다룸 | 다른 개발자와 공유하는 **무거운 프로그래밍 패러다임** |
| **Backend Layer (FigureCanvas, Renderer, Event)** | 실제로 그리고 입력을 처리 | 가장 밑바닥 |
- 💡 위(사용자와 가까움) → 아래(하드웨어와 가까움) 순: Scripting → Artist → Backend. **이 수업은 Scripting Layer(pyplot)** 를 사용.

### Backend Layer (슬라이드 5) — 3개의 내장 추상 인터페이스 클래스
1. **FigureCanvas** (`matplotlib.backend_bases.FigureCanvas`): figure가 그려지는 **영역**
2. **Renderer** (`matplotlib.backend_bases.Renderer`): FigureCanvas 위에 **그리는 방법**을 아는 객체
3. **Event** (`matplotlib.backend_bases.Event`): **키보드, 마우스 클릭** 등 사용자 입력 처리

### Artist Layer (슬라이드 6)
- 📘 핵심 객체는 **Artist** 하나. Artist는 **Renderer를 사용해 canvas에 그리는 법**을 안다.
- 📘 **제목, 선, 눈금 라벨, 이미지** 등이 각각 **개별 Artist 인스턴스**
- 📘 Artist 두 종류:
  - **Primitive(기본 요소)**: 선 `Line2D`, 텍스트 `Text`, 사각형 `Rectangle`
  - **Composite(복합 요소)**: 다른 Artist를 **포함·관리** — `Axis`, `Tick`, `Axes`, `Figure`
- 📘 복합 Artist는 다른 복합 Artist와 기본 Artist 모두 포함할 수 있음.

### Scripting Layer (슬라이드 7~8)
- 📘 주로 **pyplot**. Artist layer보다 **가벼운 스크립팅 인터페이스**
- 📘 예: 난수 10,000개 히스토그램(슬라이드 7), 슬라이드 8 제목은 100개로 표기
```python
import matplotlib.pyplot as plt     # pyplot을 plt로 import (빨간 박스)
import numpy as np
x = np.random.randn(10000)          # 표준정규분포 난수 10000개
plt.hist(x, 100)                    # 히스토그램, bin 100개 (파란 박스)
plt.title(r'Normal distribution with $\mu=0, \sigma=1$')
plt.savefig('matplotlib_histogram.png')   # 이미지로 저장
plt.show()
```
- 💡 이 코드가 pyplot 사용의 기본 틀: **import → 데이터 → plot 함수 → 꾸미기(title) → 저장/표시(show)**.

## A-3. Anatomy of a figure (슬라이드 9)
figure를 구성하는 요소 이름 (https://matplotlib.org/stable/gallery/showcase/anatomy.html) — 그림에 표기된 요소와 대응 코드:

| 요소 | 의미 | 대응 코드(그림 표기) |
|---|---|---|
| **Figure** | 전체 그림 | `plt.figure` |
| **Axes** | 그래프가 그려지는 영역 | `fig.subplots` |
| **Title** | 제목 | `ax.set_title` |
| **Legend** | 범례 (예: Blue signal / Orange signal) | `ax.legend` |
| **Grid** | 격자 | `ax.grid` |
| **Line** | 선 | `ax.plot` |
| **Markers** | 점 표시 | `ax.scatter` |
| **Spine** | 축 테두리선 | `ax.spines` |
| **X Axis / Y Axis** | 축 | `ax.xaxis` / `ax.yaxis` |
| **x label / y label (Axis label)** | 축 이름 | `ax.set_xlabel` / `ax.set_ylabel` |
| **Major tick / Minor tick** | 주 눈금 / 보조 눈금 | `ax.xaxis.set_major_locator` / `set_minor_locator` |
| **Major tick label / Minor tick label** | 눈금 글자 | `ax.xaxis.set_major_formatter` / `set_minor_formatter` |

## A-4. Recap (슬라이드 10)
- Matplotlib은 Python에서 **가장 널리 쓰이는 시각화 라이브러리** 중 하나
- 초기에는 **EEG/ECoG 시각화 도구**로 개발
- 3개 레이어: **Backend / Artist / Scripting**
- plot의 **anatomy** = 데이터의 시각적 표현을 이루는 여러 구성 요소
- 더 읽기: https://aosabook.org/en/v2/matplotlib.html

## A-5. Lab 세션 안내 (슬라이드 11~16)
### 가장 기본적인 plot — 점 하나 (슬라이드 11~12)
```python
import matplotlib.pyplot as plt
plt.plot(5, 5, 'o')     # 점 (5,5), 'o'는 원 모양 marker
plt.show()
```
- 📘 **`%matplotlib inline`** 을 첫 줄에 쓰면 Jupyter/Colab 안에서 그래프가 **inline으로 표시**(슬라이드 12 빨간 박스)
- 📘 라벨·제목은 **`plt.show()` 앞에** 추가해야 함: 
```python
plt.plot(5, 5, 'o')
plt.ylabel('Y')
plt.xlabel('X')
plt.title('Plotting Example')
plt.show()          # ← 꾸미는 줄은 반드시 show() 전에!
```

### 데이터셋 (슬라이드 14~15)
- 📘 **캐나다 이민(Immigration to Canada)** 데이터셋
- 📘 **UN 인구국(Population Division)** 이 **45개국** 자료를 모음
- 📘 국가별 **연간 국제 이주 흐름** + 기타 메타데이터
- 📘 이 수업에서는 **캐나다로의 이민** UN 데이터를 주로 사용 (슬라이드 15는 원본 엑셀 화면: Type, Coverage, OdName, AREA, AreaName, REG, RegName, DEV, DevName, 1980~ 연도 열)

### Line plot 이론 (슬라이드 16)
- 📘 **line chart/plot** = 정보를 **‘markers’라 불리는 데이터 점들을 직선 구간으로 연결**해 보여주는 plot. 여러 분야에서 쓰는 기본 차트
- 📘 **연속적인 데이터셋**일 때 사용. **일정 기간에 걸친 추세(trend) 기반 시각화**에 최적
- 📘 **언제 쓰나(When to use)**: 시간에 따른 **추세·변화** 시각화 / **관계** 보여주기 / **여러 데이터 시리즈 비교** / **급격한 변화·이상 현상** 강조

---
# PART B. Colab 실습 — Line Plot (노트북 `DV_05_code_matplotlib_line_plots.ipynb`)

## B-0. 전체 순서 요약 (이것만 보면 흐름이 잡힘)
```
① import numpy, pandas
② pd.read_csv() 로 데이터 읽기
③ df.head() 로 확인
④ df.set_index('Country', inplace=True)  → 국가명을 index로
⑤ (선택) df.index.name = None
⑥ %matplotlib inline, import matplotlib as mpl / matplotlib.pyplot as plt
⑦ (선택) mpl.style.use(['ggplot'])
⑧ years = list(map(str, range(1980, 2013+1)))   # 연도 문자열 리스트
⑨ 데이터 뽑기: df_can.loc[행(국가), 열(연도)]
⑩ .plot(kind='line')  (+ transpose 필요 여부 확인)
⑪ plt.title / ylabel / xlabel / text
⑫ plt.show()
```

## B-1. 준비 (셀 3~13)
```python
import numpy as np   # 과학 계산
import pandas as pd  # 주 데이터 구조 라이브러리

df_can = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/.../Canada.csv')
# df_can = pd.read_csv('DV_05_data_canada_immigration.csv')   # (대안) 로컬 CSV 파일
print('Data read into a pandas dataframe!')

df_can.head()                         # 앞 5행 확인 (df_can.head(10) 처럼 행 수 지정 가능)

df_can.set_index('Country', inplace=True)   # Country 열을 index로 (inplace=True: 원본을 직접 변경, 반환값 None)
df_can.index.name = None                    # (선택) index 이름 제거
```
- 💡 **왜 Country를 index로?** → `df.loc['Haiti', ...]` 처럼 **국가 이름으로 바로 행을 찾을 수 있고**, plot 시 국가명이 범례에 자동으로 들어감.
- 💡 데이터 구조: **행 = 국가(Country)**, **열 = Continent, Region, DevName, 1980~2013(연도), Total**.
- 📘 노트북 주석: “Recall that we created a **Total** column” — 국가별 누적 이민자 수(**Total**) 열이 **CSV에 이미 포함**되어 있음 (DV_06에서 set_index 후 열 38개 = 메타 3 + 연도 34 + Total 1로 확인).

## B-2. Matplotlib 불러오기 (셀 14~21)
```python
%matplotlib inline                  # inline backend 사용
import matplotlib as mpl
import matplotlib.pyplot as plt

print('Matplotlib version: ', mpl.__version__)   # 버전 확인 (>= 2.0.0), 출력 예: 3.10.0
print(plt.style.available)                       # 사용 가능한 스타일 목록
mpl.style.use(['ggplot'])                        # (선택) ggplot 스타일 적용
```
- 📘 `matplotlib.pyplot` = **Matplotlib의 scripting layer**. MATLAB처럼 동작하는 **command style 함수 모음**.
- 📘 각 pyplot 함수는 figure에 변화를 줌: **figure 생성 → figure 안에 plotting 영역 생성 → 선 그리기 → 라벨 등으로 꾸미기**.
- 💡 이번 실습은 **scripting layer**만 사용, Artist layer는 이후 실습에서.
- 사용 가능 스타일 예: Solarize_Light2, bmh, classic, dark_background, fast, fivethirtyeight, ggplot …

## B-3. pandas로 plot 그리기 (셀 22)
- 📘 pandas는 Matplotlib이 **내장**되어 있어, **Series/DataFrame 뒤에 `.plot()`** 만 붙이면 됨.

## B-4. 사례: 아이티 지진 Line plot (셀 24~34)
> 2010년 아이티 규모 7.0 지진 → 캐나다가 난민 수용 확대 → 이민자 급증을 line plot으로 확인

### 1) 연도 리스트 만들기 / 데이터 Series 추출
```python
years = list(map(str, range(1980, 2013+1)))   # ['1980','1981',...,'2013']  ← 열 이름이 문자열이라 문자열로!
haiti = df_can.loc['Haiti', years]            # 행: 'Haiti', 열: 1980~2013 (Total 열 제외)
```
- 💡 `range(1980, 2013+1)`: 끝 값은 포함 안 되므로 **+1** 해야 2013까지.
- 💡 `df.loc[행, 열]`: **index 이름**으로 선택. 결과는 **Series**(연도 = index, 값 = 이민자 수).

### 2) 기본 plot
```python
haiti.plot()              # 반환: <Axes: >
```
- 📘 pandas는 **x축에 index 값(연도), y축에 열 값(이민자 수)** 을 자동으로 채움.

### 3) 제목·축 이름 붙이기
```python
haiti.plot(kind='line')
plt.title('Immigration from Haiti')
plt.ylabel('Number of immigrants')
plt.xlabel('Years')
plt.show()          # 변경 사항을 보려면 반드시 필요
```

### 4) 텍스트 주석 `plt.text()`
```python
haiti.index = haiti.index.map(int)     # index(연도)를 문자열 → 정수로 변환
haiti.plot(kind='line')
plt.title('Immigration from Haiti')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')
plt.text(2000, 6000, '2010 Earthquake')   # 문법: plt.text(x, y, label)
plt.show()
```
- 📘 **x좌표 지정법 주의**:
  - 연도가 **정수(int)** → x = **실제 연도 값** → `plt.text(2000, 6000, ...)`
  - 연도가 **문자열(string)** → x = **index 위치(순번)** → 1980 기준 20번째가 2000 → `plt.text(20, 6000, ...)`
- 💡 y축은 정수이므로 그냥 값(6000)을 지정.
- 💡 2010년부터 급증 → 지진과 난민 수용 확대의 영향. (고급 주석 방법은 이후 모듈)

## B-5. 여러 나라 비교: India vs China (셀 35~48)
**Step 1. 두 나라 데이터 추출**
```python
df_CI = df_can.loc[['India', 'China'], years]   # 국가 여러 개 = 리스트로 전달!
df_CI
```
**Step 2. 그냥 plot 하면 이상하게 나옴**
```python
df_CI.plot(kind='line')       # ❌ 의도와 다르게 나옴 ("That doesn't look right...")
```
- 💡 **이유**: pandas는 **index → x축, 각 열(column) → 하나의 선**으로 그림. 그런데 df_CI는 **index = 국가, 열 = 연도**라서 축이 뒤집힘.

**Step 3. 전치(transpose)**
```python
df_CI = df_CI.transpose()     # 행/열 교환 → index=연도, 열=India, China
df_CI.head()
```
**Step 4. 다시 plot**
```python
df_CI.index = df_CI.index.map(int)     # 연도 index를 정수로 (plot용)
df_CI.plot(kind='line')
plt.title('Immigrants from China and India')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')
plt.show()
```
- 📘 `kind` 파라미터로 plot 종류를 명시적으로 지정.
- 📘 결과 해석: 중국과 인도는 연도별 이민 추세가 **매우 비슷**.

### ❓ 아이티는 왜 transpose 안 했나? (셀 48)
- `haiti`는 **Series**라 이미 **연도가 index**임. (DataFrame이 아니라서 불필요)
```python
print(type(haiti))     # <class 'pandas.core.series.Series'>
```
- 💡 **핵심 규칙**: *Series: index가 x축 / DataFrame: index = x축, 각 열 = 한 줄 → x축에 올 것(연도)이 index가 되도록 맞춰라.*

## B-6. 이민 상위 5개국 추세 (셀 49~52)
- 📘 line plot은 **하나의 독립변수에 대해 여러 종속변수**를 보여주기 좋음. 단, **한 그래프에 5~10개 선 이하** 권장 (더 많으면 해석 어려움).
```python
# Step 1: 데이터 — Total 열로 정렬해서 상위 5개국
df_can.sort_values(by='Total', ascending=False, axis=0, inplace=True)   # 내림차순, 원본 변경
df_top5 = df_can.head(5)                      # 상위 5개
df_top5 = df_top5[years].transpose()          # 연도 열만 선택 + 전치
print(df_top5)

# Step 2: plot — figsize로 크기 키우기
df_top5.index = df_top5.index.map(int)
df_top5.plot(kind='line', figsize=(14, 8))    # (가로, 세로) 튜플
plt.title('Immigration Trend of Top 5 Countries')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')
plt.show()
```
- 💡 `sort_values(by=정렬할 열, ascending=False(내림차순), axis=0(행 기준), inplace=True)`
- 💡 상위 5개국 중 India, China, United Kingdom of Great Britain and Northern Ireland 등이 포함 (출력 열 확인).

---
# PART C. Line Plot 정리 — “plot별 사용 변수” 표

| 실습 | 데이터 | x축 | y축 | 함수/옵션 |
|---|---|---|---|---|
| Haiti | Series `df_can.loc['Haiti', years]` | 연도(index) | 이민자 수 | `haiti.plot(kind='line')` |
| India vs China | DataFrame `df_can.loc[['India','China'], years]` → **transpose** | 연도(index) | 국가별 이민자 수(열 = 선) | `df_CI.plot(kind='line')` |
| Top 5 | `sort_values('Total')` → `head(5)` → `[years].transpose()` | 연도(index) | 국가별 이민자 수 | `plot(kind='line', figsize=(14,8))` |

## 꾸미기 함수 모음
| 함수 | 역할 |
|---|---|
| `plt.title('...')` | 제목 |
| `plt.xlabel('...')` / `plt.ylabel('...')` | 축 이름 |
| `plt.text(x, y, '...')` | 좌표 (x, y)에 텍스트 주석 |
| `plt.show()` | 그림 표시 (**꾸미는 코드는 이 앞에**) |
| `plt.savefig('name.png')` | 파일 저장 (슬라이드 예시) |
| `mpl.style.use(['ggplot'])` | 스타일 적용 |
| `plot(kind='line', figsize=(w, h))` | plot 종류, 그림 크기 |

## 자주 틀리는 포인트 (시험 대비)
1. 연도 열 이름은 **문자열**(`'1980'`) → `years = list(map(str, range(1980, 2014)))`
2. 여러 국가 선택은 **리스트**: `.loc[['India','China'], years]`
3. 국가별 선을 그리려면 **transpose** (index=x축, 열=선)
4. `plt.text()` 의 x값: **연도가 int면 연도 값, str이면 순번**
5. 라벨/제목은 **`plt.show()` 전에**
6. 선은 **5~10개 이하**
7. `inplace=True`는 원본 변경(반환 None)
