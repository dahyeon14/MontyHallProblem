# DV_08 — Waffle Chart · Word Cloud · Seaborn(Categorical / Regression)

> 표기: 📘 = 슬라이드 / 💻 = Colab 실습 노트북 / 💡 = 이해용 주석 / ➕ = 추가 설명
> 자료: `DV_08_waffle_wordcloud_regression.pdf` + `DV_08_code_waffle_wordcloud_regression.ipynb`

---
# PART A. 이론 (슬라이드)

## A-1. Waffle Chart (슬라이드 2~4)
- 📘 **범주형 데이터**를 **정사각형 타일(square tiles) / 셀(cells)** 형태로 표현
- 📘 서로 다른 범주의 **비율(proportion) 또는 퍼센트** 표시
- 📘 모든 유형의 청중에게 데이터를 **단순화**
- 📘 용도 7가지: **시장 점유율 분석**(market share) / **인구통계 표현**(demographic) / **프로젝트 진행 추적**(작업·마일스톤 완료 상태) / **예산 배분**(budget allocation) / **설문 응답 요약**(survey responses) / **선거 결과**(투표 결과를 명확히) / **제품 판매 분석**(product sales)
- 슬라이드 4: **PyWaffle 라이브러리** 예시 코드
```python
import matplotlib.pyplot as plt
from pywaffle import Waffle

# waffle chart용 데이터 생성
data = df_dsn[['Africa', 'Asia', 'Europe', 'Oceania']]      # (슬라이드 예시 변수)

# waffle chart figure 설정
fig = plt.figure(
    FigureClass=Waffle,
    rows=20,
    columns=20,
    values=data,
    legend={'labels': ['Africa', 'Asia', 'Europe', 'Oceania'],
            'loc': 'upper left', 'bbox_to_anchor': (1, 1)})

plt.show()
```

## A-2. Word Cloud (슬라이드 5~6)
- 📘 **인기 있는 데이터 시각화 방법** / 텍스트 내용의 **간결한 요약** 제시 / **단어의 중요도**를 표현 (슬라이드 그림: 긴 글 → 자주 나온 단어가 크게 보이는 구름)
- 📘 용도 5가지: **소셜 미디어 분석**(인기 주제·감성 추출) / **고객 피드백 분석**(리뷰 요약) / **콘텐츠 분석**(텍스트 분석) / **시장 조사**(설문 응답 분석) / **이력서·채용공고 분석**(핵심 기술·키워드 강조)

## A-3. Seaborn (슬라이드 7)
- 📘 **Matplotlib 기반**의 Python 시각화 라이브러리
- 📘 **내장 테마와 색 팔레트**로 plot 시각 품질 향상
- 📘 Matplotlib으로 **~20줄** 필요한 시각화를 Seaborn은 **5배 적은 줄**로 가능
- 📘 **특수 plot**: **Regression plot / Distribution plot / Categorical plot / 회귀선이 있는 scatter plot 생성**

## A-4. Regression Plot (슬라이드 8~11)
- 슬라이드 8~9 (df_total: Year, Total 열 — 1980=99137, 1981=110563 …)
```python
import seaborn as sns
ax = sns.regplot(x='year', y='total', data=df_tot)                              # 기본 (주황/빨강)
ax = sns.regplot(x='year', y='total', data=df_tot, color='green', marker='+')   # 색과 마커 변경
```
- 📘 **CI(신뢰구간) 슬라이드 10**
  - **초록 음영 영역** = 회귀선 주변의 **신뢰구간(confidence interval, CI)**
  - **같은 모집단에서 새 샘플을 뽑았을 때 회귀선이 얼마나 달라질 수 있는지** 보여줌
  - **신뢰수준(90%, 95%, 99%)** 이 **음영 폭**을 결정
  - 📘 “**90% 신뢰구간 = 참(true) 회귀선이 이 범위 안에 있다고 90% 확신**한다”
- 슬라이드 11: **95% / 90% / 99% Confidence Interval** 비교 (speed vs dist) — 💡 **신뢰수준이 높을수록(99%) 음영이 더 넓고, 낮을수록(90%) 좁음**.

## A-5. Categorical Plots (슬라이드 12~13)
- 슬라이드 12: `sns.countplot(x='Continent', data=df_canada)` — **대륙별 개수**(Asia, Europe, Africa, Oceania, LA, HK, Macao 막대; y축 = count)
- 슬라이드 13: `sns.barplot(x='Continent', y='Total', data=df_canada)` — **대륙별 Total** (막대 위의 **검은 세로선 = 신뢰구간 오차 막대**)

## A-6. Recap (슬라이드 14)
- **Waffle chart**: 범주형 데이터를 정사각형 타일/셀로 표현하는 기법. 여러 분야에서 사용 가능
- **Word cloud**: 텍스트 데이터를 시각적으로 흥미롭고 유익하게 제시. 여러 분야에서 사용
- **Seaborn**: Matplotlib 기반. **통계 그래픽을 그리기 위한 고수준(high-level) 인터페이스**
- **Scatter plot + regression line을 Seaborn으로 한 줄**로 생성
- 💡 슬라이드 15의 Lab 안내에 “Pie, Box, Scatter”라고 적혀 있으나 DV_07 슬라이드를 복사한 **오기**로 보임. 실제 Lab = waffle, wordcloud, regression.

---
# PART B. Colab 실습 (노트북 `DV_08_code_waffle_wordcloud_regression.ipynb`)

## B-0. 전체 순서
```
[준비] matplotlib/mpatches, numpy, pandas, PIL.Image, !pip install seaborn wordcloud, import seaborn as sns, wordcloud
[데이터] read_csv → set_index('Country')
[Waffle]  (직접 구현 7단계) 비율 → 크기 → 타일 수 → 행렬 채움 → matshow → 격자 → 범례   ⇒ 함수화 ⇒ PyWaffle(Waffle)
[WordCloud] WordCloud, STOPWORDS → 텍스트 읽기 → stopwords → WordCloud().generate → imshow → mask → 국가명 반복 텍스트
[Seaborn] countplot → barplot(ci) → regplot(color, marker, scatter_kws, ax.set, set_style, set(font_scale))
```

## B-1. 준비 (셀 2~10)
```python
%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches       # waffle chart(범례 사각형)에 필요
mpl.style.use('ggplot')

import numpy as np
import pandas as pd
from PIL import Image                        # 이미지를 배열로 변환 (word cloud mask용)

!pip install seaborn wordcloud
import seaborn as sns
import wordcloud

print('Matplotlib version: ', mpl.__version__)
print('Seaborn version: ', sns.__version__)          # 0.13.2
print('WordCloud version: ', wordcloud.__version__)  # 1.9.4

df_can = pd.read_csv('DV_05_data_canada_immigration.csv')
print(df_can.shape)                    # (195, 40)
df_can.set_index('Country', inplace=True)
```
- 💡 `!pip install ...` = Colab에서 **셸 명령으로 패키지 설치**(`!`로 시작).

---
## B-2. Waffle Chart

- 📘 노트북 설명: waffle chart = **목표 대비 진행 상황**을 보여주는 데 흔히 쓰임. 셀 위주 시각물(예: **Excel 대시보드**)에 효과적.
- 📘 **waffle chart는 Python 시각화 라이브러리에 기본 내장되어 있지 않음** → **처음부터 직접 만든 뒤**, 마지막에 **PyWaffle** 패키지로 같은 것을 생성.
- 사례: 덴마크·노르웨이·스웨덴의 **Total** 이민자 비율.

```python
df_dsn = df_can.loc[['Denmark', 'Norway', 'Sweden'], :]     # 3개국, 모든 열
```

### Step 1. 각 범주의 전체 대비 **비율**
```python
total_values = df_dsn['Total'].sum()
category_proportions = df_dsn['Total'] / total_values
# Denmark 0.322557, Norway 0.192409, Sweden 0.485034
```
### Step 2. waffle chart **전체 크기**
```python
width = 40       # 가로 타일 수
height = 10      # 세로 타일 수
total_num_tiles = width * height     # 400
```
### Step 3. 비율 → **범주별 타일 수**
```python
tiles_per_category = (category_proportions * total_num_tiles).round().astype(int)
# Denmark 129, Norway 77, Sweden 194
```
### Step 4. waffle 모양의 **행렬(matrix)** 만들고 채우기
```python
waffle_chart = np.zeros((height, width), dtype=np.uint)    # 0으로 채운 (10×40) 행렬

category_index = 0
tile_index = 0
for col in range(width):                 # 열 방향(왼→오)으로 먼저
    for row in range(height):            # 각 열을 위→아래로
        tile_index += 1
        # 현재 범주에 할당된 타일 수를 다 채웠으면 다음 범주로
        if tile_index > sum(tiles_per_category[0:category_index]):
            category_index += 1
        waffle_chart[row, col] = category_index     # 범주 번호(1,2,3)를 저장
```
- 💡 행렬 값 = **범주 번호**(Denmark=1, Norway=2, Sweden=3). 열 단위로 채우므로 같은 범주가 **세로 줄 단위로 연속**.
- 💡 `tile_index > sum(앞 범주들의 타일 수)` 일 때 `category_index += 1`.

### Step 5. 행렬을 **그림으로** (`matshow`)
```python
fig = plt.figure()
colormap = plt.cm.coolwarm
plt.matshow(waffle_chart, cmap=colormap)     # 행렬 값을 색으로 표시
plt.colorbar()
plt.show()
```
### Step 6. 꾸미기 — 격자(타일 경계)
```python
ax = plt.gca()                                            # 현재 axes 가져오기
ax.set_xticks(np.arange(-.5, (width), 1), minor=True)     # 보조 눈금(타일 경계 위치)
ax.set_yticks(np.arange(-.5, (height), 1), minor=True)
ax.grid(which='minor', color='w', linestyle='-', linewidth=2)   # 보조 눈금 기준 흰색 격자선
plt.xticks([])     # 일반 눈금 숫자 제거
plt.yticks([])
```
- 💡 눈금을 **−0.5, 0.5, 1.5…** 로 두는 이유: 타일의 **중심이 정수 좌표**이므로 **경계는 .5 지점**.
### Step 7. **범례** 추가
```python
values_cumsum = np.cumsum(df_dsn['Total'])            # 누적합 (색 매칭용)
total_values = values_cumsum[len(values_cumsum) - 1]  # 전체 합 (마지막 누적값)

legend_handles = []
for i, category in enumerate(df_dsn.index.values):
    label_str = category + ' (' + str(df_dsn['Total'][i]) + ')'        # 예: 'Denmark (3901)'
    color_val = colormap(float(values_cumsum[i]) / total_values)         # 차트의 색과 같은 색
    legend_handles.append(mpatches.Patch(color=color_val, label=label_str))

plt.legend(handles=legend_handles, loc='lower center',
           ncol=len(df_dsn.index.values),                    # 범례 열 수 = 범주 수
           bbox_to_anchor=(0., -0.2, 0.95, .1))
```
- 💡 **누적합(`np.cumsum`)을 쓰는 이유**: 차트의 각 범주 색은 `coolwarm` 컬러맵에서 (범주 번호/전체) 위치 값으로 결정 → 범례 색도 같은 위치 값으로 맞춤. (`mpatches.Patch` = 색 사각형 범례 항목)

### 7단계를 함수로: `create_waffle_chart` (셀 33~38)
| 파라미터 | 의미 |
|---|---|
| `categories` | 범주 이름들 |
| `values` | 범주에 대응하는 값 |
| `height` | waffle 높이 |
| `width` | waffle 너비 |
| `colormap` | 컬러맵 클래스 |
| `value_sign` | 값에 붙는 기호(%, $ 등). **기본값 빈 문자열**. `'%'`면 값 뒤에, 그 외 기호는 값 앞에 붙임 |
```python
width = 40; height = 10
categories = df_dsn.index.values
values = df_dsn['Total']
colormap = plt.cm.coolwarm
create_waffle_chart(categories, values, height, width, colormap)
# Total number of tiles is 400 / Denmark: 129 / Norway: 77 / Sweden: 194
```
- 💡 함수 안에서 타일 수 출력 시 `df_dsn.index.values[i]`를 직접 사용 → (코드상) 이 함수는 `df_dsn`에 의존. 실습 시 **다른 데이터에 쓰려면 이 부분 주의**.

### PyWaffle로 한 번에 (셀 39~41) ⭐
```python
!pip install pywaffle
from pywaffle import Waffle

fig = plt.figure(FigureClass=Waffle,                 # figure 클래스를 Waffle로 지정
                 rows=10, columns=40,                # 행/열 개수
                 values=df_dsn['Total'],             # 표시할 데이터
                 cmap_name='tab20',                  # 컬러 스킴
                 legend={'labels': [f"{k} ({v})" for k, v in zip(df_dsn.index.values, df_dsn.Total)],
                         'loc': 'lower left', 'bbox_to_anchor': (0, -0.1), 'ncol': 3})
plt.show()
```
- 💡 **직접 구현 ↔ PyWaffle 대응**: 비율·타일 수 계산·행렬 채움·격자·범례를 **PyWaffle이 알아서 처리**. `FigureClass=Waffle`이 핵심.
- 📘 범례 라벨은 **리스트 컴프리헨션(list comprehension)** 으로 **index와 Total**에서 생성 (노트북 주석).
- 📘 PyWaffle 파라미터: `rows`, `columns`, `values`, `cmap_name`, `legend`(= `labels`, `loc`, `bbox_to_anchor`, `ncol`)

### 연습: 중국·인도 Total 비율 waffle
```python
df_dsn = df_can.loc[['China', 'India'], :]
fig = plt.figure(FigureClass=Waffle,
                 rows=20, columns=30,
                 values=df_dsn['Total'],
                 cmap_name='tab20',
                 legend={'labels': [f"{k} ({v})" for k, v in zip(df_dsn.index.values, df_dsn.Total)],
                         'loc': 'lower left', 'bbox_to_anchor': (0, -0.1), 'ncol': 2})   # 범주 2개 → ncol=2
plt.show()
```

---
## B-3. Word Cloud

- 📘 **word cloud(= text cloud, tag cloud)**: 텍스트 자료(연설, 블로그, 데이터베이스 등)에서 **특정 단어가 많이 나올수록 더 크고 굵게** 표시.
- 📘 파이썬 패키지 **`word_cloud`** — **Andreas Mueller** 개발.
```python
from wordcloud import WordCloud, STOPWORDS      # WordCloud 클래스와 불용어 집합
```
- 💻 텍스트 예시: **Lewis Carroll의 *Alice's Adventures in Wonderland***

### 단계별 코드
```python
# 1) 텍스트 파일 읽기
with open('DV_08_data_alice_novel.txt', 'r', encoding='utf-8') as file:
    alice_novel = file.read()
print(alice_novel[:500])

# 2) 불용어(stopwords) 집합 — set()으로 중복 제거
stopwords = set(STOPWORDS)

# 3) word cloud 객체 생성 → 텍스트로 생성
alice_wc = WordCloud()
alice_wc.generate(alice_novel)

# 4) 표시
plt.imshow(alice_wc, interpolation='bilinear')    # 이미지처럼 표시
plt.axis('off')                                   # 축 숨김
plt.show()
```
- 📘 결과: 가장 흔한 단어는 **Alice, said, little, Queen** 등.
- 📘 크게 보려면 `plt.figure(figsize=(14, 18))` 로 그림 크기를 키움 (덜 흔한 단어도 보임).
- 💡 `interpolation='bilinear'`: 이미지 확대 시 **부드럽게 보간**. `plt.axis('off')`: 좌표축 제거(그림처럼 보이게).

### 불용어 추가
- 📘 `said`는 별 의미가 없는 단어 → **stopwords에 추가 후 재생성**
```python
stopwords.add('said')                              # 불용어 추가
alice_wc = WordCloud(stopwords=stopwords)          # 불용어 지정
alice_wc.generate(alice_novel)
```

### 마스크(mask)로 모양 만들기 (셀 62~67)
- 📘 단어를 **임의 모양(mask) 위에** 입힐 수 있음 (앨리스와 토끼 모양).
```python
alice_mask = np.array(Image.open('DV_08_data_alice_mask.png'))     # 이미지 → numpy 배열

alice_wc = WordCloud(background_color='white',      # 배경색
                     max_words=2000,                # 최대 단어 수
                     mask=alice_mask,               # 모양 마스크
                     stopwords=stopwords)           # 불용어
alice_wc.generate(alice_novel)
fig = plt.figure(figsize=(14, 18))
plt.imshow(alice_wc, interpolation='bilinear')
plt.axis('off')
plt.show()
```
| `WordCloud()` 파라미터 | 의미 |
|---|---|
| `stopwords` | 제외할 단어 집합 |
| `background_color` | 배경 색 |
| `max_words` | 그릴 최대 단어 수 |
| `mask` | 모양(이미지 배열) |
- ➕ `max_words`의 기본값은 200 (이 노트북은 마스크 예제에서 2000으로 지정).

### 이민 데이터로 word cloud 만들기 (셀 69~79)
- 📘 이민 데이터는 **텍스트가 없음** → **국가 이름을 “기여도 비율만큼 반복”한 문자열**을 만들어 사용 (총 90단어 기준).
```python
total_immigration = df_can['Total'].sum()        # 6409153 (1980~2013 전체 이민자)

max_words = 90
word_string = ''
for country in df_can.index.values:
    if country.count(" ") == 0:        # 띄어쓰기 없는 한 단어 국가명만 (단어 하나로 취급하려고)
        repeat_num_times = int(df_can.loc[country, 'Total'] / total_immigration * max_words)
        word_string = word_string + ((country + ' ') * repeat_num_times)    # 국가명을 비율만큼 반복

wordcloud = WordCloud(background_color='white').generate(word_string)
plt.figure(figsize=(14, 18))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
```
- 📘 **불용어 불필요**(국가명만 있으므로). 결과: 이민자 대부분이 **15개국** 출신 (China, India, Philippines, Pakistan 등이 크게 표시).
- 💡 **word cloud = “단어 빈도(반복 횟수)”가 글자 크기**. 숫자 데이터를 word cloud로 만들려면 값에 비례해 **단어를 반복**시키면 됨.
- 📘 아이디어: 캐나다 지도를 mask로 써서 위에 word cloud 얹기.

---
## B-4. Seaborn

- 📘 노트북 설명: 이전 DV_07에서 scatter + 회귀선을 만드는 데 **~20줄**이 필요했음 → seaborn으로 얼마나 효율적인지 확인.

### Categorical plot — `countplot` (셀 82~89)
```python
df_can['Continent'].unique()        # ['Asia','Europe','Africa','Oceania','Latin America and the Caribbean','Northern America']
sns.countplot(x='Continent', data=df_can)      # 대륙별 "행 개수"(= 나라 수)
```
- 📘 **countplot = 범주형 변수에 대한 히스토그램**(양적 변수 대신 범주형 변수).
- 문제: x축 라벨이 길어 겹침 → 이름을 줄이고 figure 키움
```python
df_can1 = df_can.replace('Latin America and the Caribbean', 'L-America')
df_can1 = df_can1.replace('Northern America', 'N-America')
plt.figure(figsize=(15, 10))
sns.countplot(x='Continent', data=df_can1)
```
- 💡 `df.replace(old, new)`: 값 치환.

### Categorical plot — `barplot` (셀 90~95)
- 📘 **범주형 변수로 groupby를 수행하고 집계 값(기본 평균)을 막대로, 신뢰구간(CI)과 함께** 표시.
```python
plt.figure(figsize=(15, 10))
sns.barplot(x='Continent', y='Total', data=df_can1)     # 대륙별 Total의 평균 + 오차 막대(CI)

df_Can2 = df_can1.groupby('Continent')['Total'].mean()    # 값 검증 (평균과 일치)
# Africa 11462.0 / Asia 67710.08 / Europe 32812.72 / L-America 23186.30 / N-America 120571.0 / Oceania 3941.0
```
- 📘 **CI를 90%로 변경**: `ci=90` (⚠ 최신 seaborn에서 **deprecated** → `errorbar=('ci', 90)` 로 대체, 노트북 출력 경고)
```python
sns.barplot(x='Continent', y='Total', data=df_can1, ci=90)       # (구 방식)
# sns.barplot(..., errorbar=('ci', 90))                           # (신 방식)
```
- 💡 **barplot의 막대 높이 = 합계가 아니라 평균(mean)**. pandas `plot(kind='bar')`와 다름.
- 💡 **countplot vs barplot**: countplot은 **y를 지정하지 않음**(개수를 셈) / barplot은 **y 변수의 집계값(평균)** 을 그림.

### Regression plot — `regplot` (셀 96~114)
- 📘 seaborn에서는 **`regplot` 함수 호출만으로** 회귀 plot 생성.
```python
years = list(map(str, range(1980, 2014)))
df_tot = pd.DataFrame(df_can[years].sum(axis=0))      # 연도별 총 이민자
df_tot.index = map(float, df_tot.index)               # 연도를 float으로 (회귀용)
df_tot.reset_index(inplace=True)
df_tot.columns = ['year', 'total']
```
- ⚠ DV_07은 `int`, 이번엔 `float`으로 변환 (둘 다 회귀 가능).

**점진적으로 꾸미기 (한 줄 → 5줄)**
```python
sns.regplot(x='year', y='total', data=df_tot, ci=95)                                  # ① 기본: scatter + 회귀선 + 95% CI 음영
sns.regplot(x='year', y='total', data=df_tot, ci=95, color='green')                   # ② 색 변경
ax = sns.regplot(x='year', y='total', data=df_tot, ci=95, color='green', marker='+')  # ③ 마커 모양 '+'

plt.figure(figsize=(15, 10))                                                          # ④ 크기 키우기
sns.regplot(..., marker='+')

plt.figure(figsize=(15, 10))                                                          # ⑤ 마커 크기 + 제목/라벨
ax = sns.regplot(x='year', y='total', data=df_tot, ci=95, color='green', marker='+',
                 scatter_kws={'s': 200})                          # 점(scatter) 옵션 딕셔너리: 크기 s=200
ax.set(xlabel='Year', ylabel='Total Immigration')                 # x/y 라벨 (한 번에 설정)
ax.set_title('Total Immigration to Canada from 1980 - 2013')      # 제목

plt.figure(figsize=(15, 10))                                                          # ⑥ 글자 크기
sns.set(font_scale=1.5)                                           # 눈금, 제목, 라벨 글자 크기 1.5배
ax = sns.regplot(...)
```
**배경 스타일 변경**
```python
sns.set_style('ticks')        # 흰 배경 (격자 없음, 눈금 표시)
sns.set_style('whitegrid')    # 흰 배경 + 격자선
```
| regplot 파라미터 | 의미 |
|---|---|
| `x=`, `y=`, `data=` | 열 이름과 DataFrame (DataFrame 친화적) |
| `ci` | 신뢰구간 수준 (기본 95). 음영 폭 |
| `color` | 점과 회귀선 색 |
| `marker` | 점 모양 (`'+'`, `'o'` …) |
| `scatter_kws={'s': 200}` | scatter(점)에 전달할 옵션 딕셔너리 (`s` = 점 크기) |
- 💡 `ax.set(xlabel=..., ylabel=...)` 는 seaborn plot이 반환한 **Axes 객체(`ax`)** 에 설정 (DV_06의 artist layer 방식).
- 📘 결론: “scatter + 회귀선 + 꾸미기를 **5줄**로.”

### 연습: 덴마크·스웨덴·노르웨이 합계 regplot
```python
df_countries = df_can.loc[['Denmark', 'Norway', 'Sweden'], years].transpose()
df_total = pd.DataFrame(df_countries.sum(axis=1))
df_total.reset_index(inplace=True)
df_total.columns = ['year', 'total']
df_total['year'] = df_total['year'].astype(int)

plt.figure(figsize=(15, 10))
sns.set(font_scale=1.5)
sns.set_style('whitegrid')
ax = sns.regplot(x='year', y='total', data=df_total, ci=95, color='green', marker='+', scatter_kws={'s': 200})
ax.set(xlabel='Year', ylabel='Total Immigration')
ax.set_title('Total Immigration from Denmark, Sweden, and Norway to Canada from 1980 - 2013')
```

---
# PART C. 정리표

## C-1. plot별 사용 변수·함수

| Plot | 라이브러리 | 데이터 | 핵심 코드 | 주요 파라미터 |
|---|---|---|---|---|
| **Waffle** (직접) | matplotlib | 범주별 `Total` → 비율 → 타일 수 → 행렬 | `np.zeros`, 이중 for, `plt.matshow`, `mpatches.Patch`, `plt.legend` | `width`, `height`, `colormap` |
| **Waffle** (PyWaffle) | pywaffle | `values=df['Total']` | `plt.figure(FigureClass=Waffle, ...)` | `rows`, `columns`, `values`, `cmap_name`, `legend` |
| **Word cloud** | wordcloud | **텍스트(문자열)** | `WordCloud(...).generate(text)` → `plt.imshow` | `stopwords`, `background_color`, `max_words`, `mask` |
| **countplot** | seaborn | 범주형 열 (**y 없음**) | `sns.countplot(x='Continent', data=df)` | — |
| **barplot** | seaborn | 범주형 x + 수치 y | `sns.barplot(x=, y=, data=)` | `ci`/`errorbar` (CI), 막대 = 평균 |
| **regplot** | seaborn | 수치 x + 수치 y (열 이름) | `sns.regplot(x='year', y='total', data=df_tot)` | `ci`, `color`, `marker`, `scatter_kws` |

## C-2. 시험 대비 포인트
1. **Waffle chart = 범주형 데이터의 비율을 타일로**. 용도(시장 점유율, 예산, 설문, 선거 등).
2. **Waffle 직접 구현 7단계**: ① 비율 ② 전체 크기 ③ 타일 수 ④ 행렬 채우기 ⑤ `matshow` ⑥ 격자(minor ticks) ⑦ 범례. → **PyWaffle은 `FigureClass=Waffle`** 로 대체.
3. **Word cloud**: 단어 **빈도가 클수록 크게**. `stopwords`(불용어), `mask`(모양), `max_words`. 숫자 데이터는 **반복 텍스트**로 변환.
4. `plt.imshow(wc, interpolation='bilinear')` + `plt.axis('off')`.
5. **Seaborn**: Matplotlib 기반 / 짧은 코드(~20줄→5배 적게) / 테마·팔레트 / 통계 plot(regression, distribution, categorical).
6. **countplot**: 범주별 **개수**(y 없음). **barplot**: 범주별 **평균 + CI 오차 막대**.
7. **regplot**: scatter + **회귀선 + 신뢰구간 음영**. `ci`↑ → 음영 폭↑ (90% < 95% < 99%). **“90% CI = 참 회귀선이 이 범위에 있다고 90% 확신”**.
8. regplot 꾸미기: `color`, `marker`, `scatter_kws={'s':...}`, `ax.set(xlabel=, ylabel=)`, `ax.set_title`, `sns.set(font_scale=)`, `sns.set_style('ticks' | 'whitegrid')`.
9. Seaborn은 **`x='열이름', y='열이름', data=df`** 형태 (**pandas DataFrame 친화적**, DV_04 Matplotlib vs Seaborn 비교표와 연결).
