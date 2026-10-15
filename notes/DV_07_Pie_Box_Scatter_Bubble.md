# DV_07 — Pie · Box · Scatter · Bubble Plot

> 표기: 📘 = 슬라이드 / 💻 = Colab 실습 노트북 / 💡 = 이해용 주석 / ➕ = 추가 설명
> 자료: `DV_07_pie_box_scatter.pdf` + `DV_07_code_pie_box_scatter_bubble_1.ipynb` (캐나다 이민 데이터셋)

---
# PART A. 이론 (슬라이드)

## A-1. Pie Chart (슬라이드 2~5)
- 📘 **원형 통계 그래프를 조각(segment)으로 나눈 것**. 숫자의 **비율(proportion)** 을 보여줌.
- 슬라이드 3: `df_continents = df_canada.groupby('Continent', axis=0).sum()` → **대륙별 합계 표** (행 = Africa, Asia, Europe, Latin America and the Caribbean, Northern America, Oceania / 열 = 1980…2013, Total)
- 슬라이드 4: `df_continents['Total'].plot(kind='pie')` + title → 기본 파이 (Asia가 가장 큼, 레이블이 파이 바깥)
- 슬라이드 5: **`explode`** 로 조각을 **밖으로 떼어내** 강조 + 퍼센트(%) 표시 (예: 51.8%, 22.0%, 11.9%, 9.7%, 3.8%, 0.9%) + 범례를 따로 둠

## A-2. Box Plot (슬라이드 6~7)
- 슬라이드 6 그림 — 박스 플롯 구성요소: **Maximum**, **Third Quartile**(Q3), **Median**, **First Quartile**(Q1), **Minimum**, 상자 높이 = **Inter Quartile Range (IQR)**, 수염 밖 점 = **Outliers**
- 슬라이드 7 코드:
```python
df_japan = df_canada.loc[['Japan'], years].transpose()
df_japan.plot(kind='box')
plt.title('Box plot of Japanese Immigrants from 1980-2013')
plt.ylabel('Number of Immigrants')
plt.show()
```

## A-3. Scatter Plot (슬라이드 8~11)
- 📘 **두 변수**에 해당하는 값을 표시 / 두 변수 간 **상관관계(correlation)** 를 파악
- 슬라이드 9 코드: `df_total.plot(kind='scatter', x='year', y='total')` (df_total = year, total 두 열; 1980=99137, 1981=110563, …)
- 슬라이드 10: 결과 — 연도가 갈수록 총 이민자 수 증가 추세
- 슬라이드 11: 점 크기·색을 바꾼 두 scatter (왼쪽 빨간 작은 점, 오른쪽 **크기가 다른 파란 점 = bubble 형태**)

## A-4. Recap (슬라이드 12)
- **Pie chart**: 원형 통계 그래프를 조각으로 나누어 **수치 비율**을 나타냄
- **Box plot**: 데이터 분포를 통계적으로 표현. **5가지 값 = Minimum, 1st quartile, median, 3rd quartile, maximum**
- **Scatter plot**: 보통 **두 변수**를 서로에 대해 표시
- scatter plot 생성은 Matplotlib을 import해서 **큰 데이터 집합**을 시각화

---
# PART B. Colab 실습 (노트북 `DV_07_code_pie_box_scatter_bubble_1.ipynb`)

## B-0. 전체 순서
```
[준비] import → read_csv → shape → set_index('Country') → years 리스트
[Pie]     groupby('Continent').sum() → ['Total'].plot(kind='pie', autopct, startangle, shadow, labels, pctdistance, colors, explode) → plt.axis('equal') → plt.legend
[Box]     .loc[['국가'], years].transpose() → describe() → plot(kind='box', vert, color) → subplot(ax=) → decade 합산 → 이상치(1.5×IQR)
[Scatter] df[years].sum(axis=0) → DataFrame → index int → reset_index → 열 이름 변경 → plot(kind='scatter', x=, y=) → np.polyfit → 회귀선 → 예측
[Bubble]  df[years].transpose() → Year 열 만들기 → 정규화(min-max) → scatter(s=가중치*2000+10, ax=ax0)
```

## B-1. 준비 (셀 2~15)
```python
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt          # (이 노트북에서는 %matplotlib inline 주석 처리)
mpl.style.use('ggplot')
print('Matplotlib version: ', mpl.__version__)

df_can = pd.read_csv('DV_04_data_canada_immigration.csv')   # 로컬 CSV 파일 사용 (파일명 주의)
df_can.head()
print(df_can.shape)                       # (195, 40)
df_can.set_index('Country', inplace=True)
print('data dimensions:', df_can.shape)   # (195, 39)
years = list(map(str, range(1980, 2014)))
```
- 💡 이번 CSV는 첫 열에 **`Unnamed: 0`**(저장 시 생긴 불필요한 index 열)이 있어 DV_05/06(열 38개)보다 열이 **하나 많음(39개)**. 분석에는 영향 없지만 `groupby().sum()` 결과에 이 열도 합산돼 나옴(의미 없는 값).

---
## B-2. Pie Chart

### Step 1: `groupby` (셀 17~19) — **Split → Apply → Combine**
1. **Split**: 어떤 기준으로 데이터를 **그룹으로 나눔**
2. **Apply**: 각 그룹에 **함수 적용** — `.sum() .count() .mean() .std() .aggregate() .apply()` 등
3. **Combine**: 결과를 **하나의 자료구조로 합침**
```python
df_continents = df_can.groupby('Continent', axis=0).sum()   # 대륙별로 묶어 합계
print(type(df_can.groupby('Continent', axis=0)))            # <class 'pandas.core.groupby.generic.DataFrameGroupBy'>
df_continents.head()
```
- 📘 **groupby의 결과는 `groupby` 객체** — `.sum()` 같은 함수를 **적용하기 전에는 더 쓸 수 없음**.
- 💡 `axis=0` 은 최신 pandas에서 **FutureWarning**(deprecated) → 빼도 됨(`groupby('Continent').sum()`).

### Step 2: plot — 주요 파라미터 (셀 20~21)
| 파라미터 | 의미 |
|---|---|
| `autopct` | 각 조각에 **숫자(퍼센트)** 를 표시하는 **문자열 또는 함수**. 포맷 문자열이면 `fmt % pct`. 조각 **안쪽**에 표시. 예: `'%1.1f%%'` = 소수 첫째 자리까지 + % |
| `startangle` | 파이 시작 위치를 x축에서 **반시계 방향으로 몇 도** 회전할지 (`90`이면 첫 조각이 위쪽에서 시작) |
| `shadow` | 파이 아래 **그림자**(입체감) |
```python
df_continents['Total'].plot(kind='pie',
                            figsize=(5, 6),
                            autopct='%1.1f%%',     # 퍼센트 표시
                            startangle=90,         # 시작 각도 90° (Africa)
                            shadow=True)           # 그림자
plt.title('Immigration to Canada by Continent [1980 - 2013]')
plt.axis('equal')                                   # 파이를 원(circle)처럼 보이게
plt.legend(labels=df_continents.index, loc='upper left')   # 범례
plt.show()
```
- 💡 `plt.axis('equal')`: x, y 비율을 같게 → **타원이 아니라 정원**.

### 개선: 글자 겹침 해결 (셀 22~23)
- 📘 개선 방법 4가지
  1. 파이 위의 **텍스트 라벨 제거**(`labels=None`) 후 **`plt.legend()` 로 별도 범례**
  2. **`pctdistance`** 로 퍼센트를 파이 **바깥쪽**으로 밀어냄
  3. **`colors`** 로 대륙별 **색 지정**
  4. **`explode`** 로 **가장 작은 세 대륙(Africa, North America, Latin America & Caribbean)** 강조
```python
colors_list  = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen', 'pink']
explode_list = [0.1, 0, 0, 0, 0.1, 0.1]   # 각 조각을 밖으로 떼어낼 비율

df_continents['Total'].plot(kind='pie',
                            figsize=(10, 6),
                            autopct='%1.1f%%',
                            startangle=90,
                            shadow=True,
                            labels=None,          # 파이 위 라벨 끄기
                            pctdistance=1.12,     # 각 조각 중심 ~ 퍼센트 글자 시작 위치 비율(>1이면 바깥)
                            #colors=colors_list,  # (노트북에서는 주석 처리됨)
                            #explode=explode_list # (주석 처리됨)
                            )
plt.title('Immigration to Canada by Continent [1980 - 2013]', y=1.12, fontsize=15)  # 퍼센트가 바깥으로 갔으니 제목도 12% 위로
plt.axis('equal')
plt.legend(labels=df_continents.index, loc='upper left', fontsize=7)
plt.show()
```
- 💡 `pctdistance=1.12` → 제목 `y=1.12`로 같이 올려서 안 겹치게 (노트북 주석: “scale the title up by 12% to match pctdistance”).
- 💡 `explode` 리스트 길이 = **조각 수(6)**. 0이면 붙어 있음, 0.1이면 반지름의 10%만큼 떨어짐.

### 연습 (셀 24~26): **2013년** 대륙별 비율 pie
```python
explode_list = [0.0, 0, 0, 0.1, 0.1, 0.2]     # 작은 조각들이 겹치지 않게 값 조정 (play with explode values)

df_continents['2013'].plot(kind='pie',
                           figsize=(15, 6),
                           autopct='%1.1f%%',
                           startangle=90,
                           shadow=True,
                           labels=None,
                           pctdistance=1.12,
                           explode=explode_list)
plt.title('Immigration to Canada by Continent in 2013', y=1.12)
plt.axis('equal')
plt.legend(labels=df_continents.index, loc='upper left')
plt.show()
```
- 💡 열을 `['Total']` → `['2013']` 로만 바꾸면 기간이 바뀜.

---
## B-3. Box Plot

### 개념 (셀 27~28)
- 📘 데이터 **분포를 5개 값**으로 표현: **minimum, first quartile, median, third quartile, maximum**
- 📘 pandas Series/DataFrame의 `plot`에 **`kind='box'`**

### 일본 이민자 box plot (셀 29~34)
```python
# 행 선택을 [['Japan']] 처럼 대괄호 두 겹 → 결과가 Series가 아니라 DataFrame (describe() 등에 유리)
df_japan = df_can.loc[['Japan'], years].transpose()
df_japan.head()

df_japan.plot(kind='box', figsize=(8, 6))
plt.title('Box plot of Japanese Immigrants from 1980 - 2013')
plt.ylabel('Number of Immigrants')
plt.show()
```
- 📘 **한 나라만 뽑아도 DataFrame으로** 뽑으라는 이유: `describe()`로 **백분위수** 확인 가능.
- 📘 그래프에서 읽는 값: **min ≈ 200, max ≈ 1300, median ≈ 900** / 연도의 **25%**가 연 ~500명 이하(Q1) / **75%**가 ~1100명 이하(Q3)
- `df_japan.describe()` 실제 값: count 34, mean 814.9, std 337.2, **min 198, 25% 529, 50% 902, 75% 1079, max 1284**

### 두 나라 비교: China vs India (셀 35~47)
```python
df_CI = df_can.loc[['China', 'India'], years].transpose()    # 열 = 국가
df_CI.describe()                                             # 통계 요약

df_CI.plot(kind='box', figsize=(10, 7))
plt.title('Box plots of Immigrants from China and India (1980 - 2013)')
plt.ylabel('Number of Immigrants')
plt.show()
```
- 📘 해석: **중앙값은 비슷(~20,000)**, 하지만 **중국의 범위가 인도보다 더 퍼져 있음**. 인도의 최댓값(36,210)은 중국 최댓값(42,584)보다 약 15% 낮음.
- `describe()` 값: China 25% 5512.75 / 50% 19945 / 75% 31568.5, India 25% 10637.75 / 50% 20235 / 75% 28699.5

### 가로 box plot (셀 46~47)
```python
df_CI.plot(kind='box', figsize=(10, 7), color='blue', vert=False)   # vert=False → 가로, color로 색 변경(기본은 빨강)
plt.title('Box plots of Immigrants from China and India (1980 - 2013)')
plt.xlabel('Number of Immigrants')        # 가로이므로 값 축 라벨은 xlabel
plt.show()
```

### ★ Subplots (셀 48~51) — figure를 나눠 여러 그래프
- 📘 **figure(전체 캔버스)** 를 **subplots**로 나눠 각각에 plot. 이때 보통 **artist layer** 사용.
```python
fig = plt.figure()                                  # figure 생성
ax = fig.add_subplot(nrows, ncols, plot_number)     # subplot 생성
```
- `nrows`, `ncols` = 그리드의 행/열 수 / `plot_number` = **1부터 시작**, **행 방향(가로)으로 증가**, 최대 nrows×ncols
- **어느 subplot에 그릴지는 `plot()`의 `ax=` 파라미터**로 지정
```python
fig = plt.figure()
ax0 = fig.add_subplot(1, 2, 1)     # 1행 2열 중 첫 번째
ax1 = fig.add_subplot(1, 2, 2)     # 1행 2열 중 두 번째

# Subplot 1: Box plot
df_CI.plot(kind='box', color='blue', vert=False, figsize=(20, 6), ax=ax0)
ax0.set_title('Box Plots of Immigrants from China and India (1980 - 2013)')
ax0.set_xlabel('Number of Immigrants')
ax0.set_ylabel('Countries')

# Subplot 2: Line plot
df_CI.plot(kind='line', figsize=(20, 6), ax=ax1)
ax1.set_title('Line Plots of Immigrants from China and India (1980 - 2013)')
ax1.set_ylabel('Number of Immigrants')
ax1.set_xlabel('Years')
plt.show()
```
- 📘 **Tip**: `nrows, ncols, plot_number`가 모두 10 미만이면 **3자리 숫자**로 축약 가능 — **백의 자리=nrows, 십의 자리=ncols, 일의 자리=plot_number**. `subplot(211) == subplot(2, 1, 1)` (2행 1열의 맨 위 plot).

### 고급: 상위 15개국 **10년 단위(decade)** box plot (셀 52~66)
```python
# Step 1: 상위 15개국
df_top15 = df_can.sort_values(['Total'], ascending=False, axis=0).head(15)

# Step 2: 10년 단위 합계 DataFrame
years_80s = list(map(str, range(1980, 1990)))
years_90s = list(map(str, range(1990, 2000)))
years_00s = list(map(str, range(2000, 2010)))

df_80s = df_top15.loc[:, years_80s].sum(axis=1)    # 국가별(행별) 합계 → axis=1
df_90s = df_top15.loc[:, years_90s].sum(axis=1)
df_00s = df_top15.loc[:, years_00s].sum(axis=1)

new_df = pd.DataFrame({'1980s': df_80s, '1990s': df_90s, '2000s': df_00s})   # 3개 Series를 합침
new_df.describe()

# Step 3: box plot
new_df.plot(kind='box', figsize=(10, 6))
plt.title('Immigration from top 15 countries for decades 80s, 90s and 2000s')
plt.show()
```
- 💡 `sum(axis=1)` = **행(국가)별로 열(연도)을 가로로 합산** / `sum(axis=0)` = 열별 합(연도별 전체 합).
- 💡 이 plot의 **x축 = 10년 구간(범주)**, y = 그 구간의 국가별 합계(분포).

### ★ 이상치(Outlier) 판단 규칙 (셀 65~66)
- 📘 box plot은 데이터를 훑어 **이상치를 자동 식별**. 이상치 조건:
  - **Q3보다 1.5×IQR 이상 큰 값**, 또는
  - **Q1보다 1.5×IQR 이상 작은 값**
- 📘 예 (2000s): Q1 = 36,101.5 / Q3 = 105,505.5 / **IQR = Q3 − Q1 = 69,404** → 이상치 기준 **> 105,505.5 + 1.5×69,404 = 209,611.5** → **China와 India가 이상치**(2000년대 합계가 209,611.5 초과)
- 📘 box plot은 **고급 시각화 도구**로 옵션이 많음(Matplotlib 문서 참고).
- ➕ (DV_04에 추가해 둔 설명과 일치) 일반 공식: `하한 = Q1 − 1.5×IQR`, `상한 = Q3 + 1.5×IQR`, 이를 벗어나면 이상치 점.

---
## B-4. Scatter Plot

### 데이터 준비 (셀 67~69): 연도별 **전체 국가 합계**
```python
df_tot = pd.DataFrame(df_can[years].sum(axis=0))    # 열(연도)별 합계 → 연도별 총 이민자 (Series → DataFrame)
df_tot.index = map(int, df_tot.index)               # 연도를 int로 (나중에 회귀에 유용)
df_tot.reset_index(inplace=True)                    # index(연도)를 일반 열로 되돌림
df_tot.columns = ['year', 'total']                  # 열 이름 변경
df_tot.head()                                       # 1980 99137 / 1981 110563 / 1982 104271 / ...
```
- 💡 **scatter는 x, y가 모두 “열”이어야** 하므로 index였던 연도를 `reset_index`로 열로 꺼냄.

### plot (셀 70~72)
```python
df_tot.plot(kind='scatter', x='year', y='total', figsize=(10, 6), color='darkblue')
plt.title('Total Immigration to Canada from 1980 - 2013')
plt.xlabel('Year')
plt.ylabel('Number of Immigrants')
plt.show()
```
- 📘 **`kind='scatter'`** + **`x=`, `y=`로 x/y에 올 열 이름을 지정**해야 함 (line/bar와 다른 점!).
- 📘 scatter는 점을 **연결하지 않음**. **연도가 갈수록 총 이민자 수 증가**하는 상승 추세 → **회귀선(line of best fit)** 으로 수학적 분석 가능.

### 회귀선과 예측 (셀 73~77)
```python
x = df_tot['year']
y = df_tot['total']
fit = np.polyfit(x, y, deg=1)      # 최적 다항식 계수 → array([ 5567.09228, -10926195.2 ])
```
| `np.polyfit` 인자 | 의미 |
|---|---|
| `x` | x 좌표 |
| `y` | y 좌표 |
| `deg` | **다항식 차수**: 1 = 선형, 2 = 이차 … |
- 📘 출력은 **높은 차수부터** 나열된 계수 배열. 선형 y = a·x + b 이므로 **[0] = 기울기(slope), [1] = 절편(intercept)**
```python
df_tot.plot(kind='scatter', x='year', y='total', figsize=(10, 6), color='darkblue')
plt.title('Total Immigration to Canada from 1980 - 2013')
plt.xlabel('Year'); plt.ylabel('Number of Immigrants')

plt.plot(x, fit[0] * x + fit[1], color='red')                       # 회귀선
plt.annotate('y={0:.0f} x + {1:.0f}'.format(fit[0], fit[1]), xy=(2000, 150000))   # 식 표시
plt.show()

'No. Immigrants = {0:.0f} * Year + {1:.0f}'.format(fit[0], fit[1])  # 'No. Immigrants = 5567 * Year + -10926195'
```
- 📘 **2015년 예측**: 5567 × 2015 − 10,926,195 = **291,310명**. 실제 CIC 2016 보고서 **271,845명** → 예측값이 실제와 **약 7% 이내**(UN 데이터가 CIC와 다소 다를 수 있음을 감안하면 양호).
- 💡 `'{0:.0f}'.format(값)` = 소수점 0자리(정수)로 서식.

### 연습 (셀 78~84): 덴마크+노르웨이+스웨덴 **합계** scatter
```python
df_countries = df_can.loc[['Denmark', 'Norway', 'Sweden'], years].transpose()
df_total = pd.DataFrame(df_countries.sum(axis=1))      # 행(연도)별로 세 나라 합산
df_total.reset_index(inplace=True)
df_total.columns = ['year', 'total']
df_total['year'] = df_total['year'].astype(int)        # 연도 문자열 → int

df_total.plot(kind='scatter', x='year', y='total', figsize=(10, 6), color='darkblue')
plt.title('Immigration from Denmark, Norway, and Sweden to Canada from 1980 - 2013')
plt.xlabel('Year'); plt.ylabel('Number of Immigrants')
plt.show()
```

---
## B-5. Bubble Plot

### 개념 (셀 85)
- 📘 **bubble plot = scatter plot의 변형**으로 **3차원(x, y, z) 데이터**를 표시. 점 대신 **버블**을 쓰고, **버블 크기는 세 번째 변수 `z`(가중치, weight)** 가 결정.
- 📘 Matplotlib에서는 `plot()`의 **`s` 파라미터**에 **배열 또는 스칼라**(각 점의 가중치)를 넘김.
- 💻 사례: **아르헨티나 대공황(1998~2002)** 영향 — 이웃 **브라질**과 비교. 가중치는 **연도별 이민자 수의 정규화(normalized) 값**.

### Step 1: 데이터 (셀 86~87) — **국가 열**이 되도록 전치 + Year 열 만들기
```python
df_can_t = df_can[years].transpose()          # 행=연도, 열=국가(195개)
df_can_t.index = map(int, df_can_t.index)     # 연도를 int
df_can_t.index.name = 'Year'                  # index 이름 → reset_index 시 열 이름이 됨
df_can_t.reset_index(inplace=True)            # Year를 열로
```

### Step 2: 정규화 (셀 88~89) — **Feature scaling(min-max)** 으로 값을 [0, 1]로
```
X' = (X − X_min) / (X_max − X_min)       → 최댓값 = 1, 최솟값 = 0
```
```python
norm_brazil    = (df_can_t['Brazil']    - df_can_t['Brazil'].min())    / (df_can_t['Brazil'].max()    - df_can_t['Brazil'].min())
norm_argentina = (df_can_t['Argentina'] - df_can_t['Argentina'].min()) / (df_can_t['Argentina'].max() - df_can_t['Argentina'].min())
```
- 💡 정규화 이유: 국가마다 이민자 규모가 다르므로 **0~1로 맞춰 버블 크기를 비교 가능**하게.

### Step 3: plot (셀 90~92)
- 📘 두 scatter를 **한 그래프에** 그리려면 **`ax` 파라미터**로 첫 plot의 axes를 둘째 plot에 넘김.
- 📘 가중치는 **`s`** 로 전달. 정규화 값(0~1)은 너무 작아 안 보이므로 **×2000**으로 키우고, 최솟값(0)도 보이도록 **+10**.
```python
# Brazil
ax0 = df_can_t.plot(kind='scatter',
                    x='Year', y='Brazil',
                    figsize=(14, 8),
                    alpha=0.5,                       # 투명도
                    color='green',
                    s=norm_brazil * 2000 + 10,       # 버블 크기(가중치)
                    xlim=(1975, 2015))               # x축 범위

# Argentina  (ax=ax0 → 같은 그래프에 겹쳐 그림)
ax1 = df_can_t.plot(kind='scatter',
                    x='Year', y='Argentina',
                    alpha=0.5, color="blue",
                    s=norm_argentina * 2000 + 10,
                    ax=ax0)

ax0.set_ylabel('Number of Immigrants')
ax0.set_title('Immigration from Brazil and Argentina from 1980 to 2013')
ax0.legend(['Brazil', 'Argentina'], loc='upper left', fontsize='x-large')
```
- 📘 해석: **버블이 클수록** 그 해 이민자 수가 (1980~2013 데이터 대비) **더 많음**. 아르헨티나는 **1998~2002 대공황** 때 이민 증가, **1985~1993** 에도 유사한 급증(1974~1990 대공황). 브라질은 1999년 **헤알화 ~35% 하락(Samba Effect)** 과 긴축 프로그램 후 **2010년 급증**.

### 연습 (셀 93~99): 중국 vs 인도 bubble plot
```python
norm_china = (df_can_t['China'] - df_can_t['China'].min()) / (df_can_t['China'].max() - df_can_t['China'].min())
norm_india = (df_can_t['India'] - df_can_t['India'].min()) / (df_can_t['India'].max() - df_can_t['India'].min())

ax0 = df_can_t.plot(kind='scatter', x='Year', y='China', figsize=(14, 8),
                    alpha=0.5, color='green', s=norm_china * 2000 + 10, xlim=(1975, 2015))
ax1 = df_can_t.plot(kind='scatter', x='Year', y='India',
                    alpha=0.5, color='blue', s=norm_india * 2000 + 10, ax=ax0)
ax0.set_ylabel('Number of Immigrants')
ax0.set_title('Immigration from China and India from 1980 - 2013')
ax0.legend(['China', 'India'], loc='upper left', fontsize='x-large')
```

---
# PART C. 정리표

## C-1. plot별 사용 변수·데이터

| Plot | 데이터 준비 | x | y | (z) | 핵심 코드 |
|---|---|---|---|---|---|
| **Pie** | `groupby('Continent').sum()` | — (조각 = 대륙) | `['Total']` 또는 `['2013']` 값 → 비율 | — | `plot(kind='pie', autopct=, startangle=, shadow=, labels=None, pctdistance=, colors=, explode=)` |
| **Box** (1국가) | `.loc[['Japan'], years].transpose()` | 열(국가) | 연도별 값 분포 | — | `plot(kind='box')` |
| **Box** (여러 국가) | `.loc[['China','India'], years].transpose()` | 열별 상자 | 값 | — | `plot(kind='box', vert=False, color=)` |
| **Box** (decade) | top15 → decade별 `sum(axis=1)` → `new_df` | 1980s/1990s/2000s | 국가별 10년 합계 | — | `new_df.plot(kind='box')` |
| **Scatter** | `df[years].sum(axis=0)` → `reset_index` → `['year','total']` | `year` | `total` | — | `plot(kind='scatter', x='year', y='total')` |
| **Bubble** | `df[years].transpose()` + `Year` 열 + 정규화 | `Year` | 국가 열(`'Brazil'`) | **`s` = 정규화값×2000+10** | `plot(kind='scatter', ..., s=, alpha=, ax=)` |

## C-2. 파라미터 사전 (DV_07 신규)
| 파라미터 | 적용 | 의미 |
|---|---|---|
| `autopct='%1.1f%%'` | pie | 조각 안에 퍼센트 표시 |
| `startangle` | pie | 시작 각도(반시계) |
| `shadow` | pie | 그림자 |
| `labels=None` | pie | 파이 위 라벨 끄기 (→ `plt.legend`) |
| `pctdistance` | pie | 퍼센트 글자 위치(중심 대비 비율) |
| `colors` | pie | 조각 색 리스트 |
| `explode` | pie | 조각 떼어내기 비율 리스트 |
| `vert=False` | box | 가로 상자 |
| `color` | box, scatter | 색 |
| `x=`, `y=` | scatter | **열 이름**으로 축 지정 |
| `s` | scatter(bubble) | 점(버블) 크기 — 스칼라 또는 배열 |
| `alpha` | scatter | 투명도 |
| `xlim=(min,max)` | scatter 등 | x축 범위 |
| `ax=` | 전부 | **어느 axes에 그릴지** (subplot 배치, 겹쳐 그리기) |

## C-3. 시험 대비 포인트
1. **Pie**: `groupby().sum()` 필요 / `autopct`, `explode`, `startangle`, `pctdistance`, `labels=None`+`legend` 의미 / `plt.axis('equal')` = 원형 유지.
2. **groupby = Split → Apply → Combine**, groupby 객체는 함수를 적용해야 결과가 나옴.
3. **Box**: 5개 숫자(min, Q1, median, Q3, max) / IQR = Q3−Q1 / **이상치 = Q3+1.5·IQR 초과 또는 Q1−1.5·IQR 미만** / `describe()`로 수치 확인 / `vert=False`는 가로.
4. 한 나라만 box plot할 때는 `.loc[['Japan'], ...]` **(대괄호 두 겹 → DataFrame)**.
5. **Subplot**: `fig.add_subplot(nrows, ncols, plot_number)`, `plot_number`는 1부터 행 방향 증가, `plot(..., ax=ax0)`, 축약형 `subplot(211) == subplot(2,1,1)`.
6. **Scatter**는 `x=`, `y=` **열 이름 지정이 필수**. 연도가 index면 `reset_index()`로 열로.
7. **회귀선**: `np.polyfit(x, y, deg=1)` → `[기울기, 절편]` → `plt.plot(x, fit[0]*x + fit[1])`.
8. **Bubble = scatter + 세 번째 변수(`s`)**. 정규화(min-max)로 [0,1] → `×2000 + 10`.
9. 두 plot 겹치기: 첫 plot의 반환값 `ax0` → 두번째 `plot(..., ax=ax0)`.
10. `sum(axis=0)` = 열별(위→아래) 합, `sum(axis=1)` = 행별(좌→우) 합.
