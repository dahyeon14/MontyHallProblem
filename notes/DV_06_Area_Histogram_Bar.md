# DV_06 — Area Plot · Histogram · Bar Chart (Matplotlib + pandas)

> 표기: 📘 = 슬라이드 / 💻 = Colab 실습 노트북 / 💡 = 이해용 주석 / ➕ = 추가 설명
> 자료: `DV_06_Area_Hist_Bar_plot.pdf` + `DV_06_Area_Hist_Bar.ipynb` (캐나다 이민 데이터셋, DV_05와 동일)

---
# PART A. 이론 (슬라이드)

## A-1. Area Plot (슬라이드 2, 8~9)
- 📘 **area chart / area graph** 라고도 함
- 📘 **여러 변수의 크기(magnitude)와 비율(proportion)** 을 표시
- 📘 **시간 또는 다른 순서가 있는 차원**을 나타냄
- 📘 **line plot을 기반**으로 함 (선 아래를 색으로 채운 것)
- 📘 용도: **주식 시장 성과 추적** / **인구통계(demographics) 시각화** / **자원 분포 표시**
- 슬라이드 8 예시 코드와 그림: `df_top5.plot(kind='area')` — 상위 5개국(India, China, United Kingdom, Philippines, Pakistan)의 누적 영역 그래프

## A-2. Histogram (슬라이드 10)
- 📘 데이터셋의 **빈도 분포(frequency distribution)** 를 표현
- 📘 숫자 데이터를 **bin(구간)으로 분할** → 각 데이터 포인트를 bin에 **할당** → 각 bin의 **개수를 센다**
- 슬라이드 12: `np.histogram`의 bin 표 — Bin 1(0~3412.9)=178, Bin 2(3412.9~6825.8)=11, Bin 3(~10238.7)=1, Bin 4(~13651.6)=2, Bin 5~8=0, Bin 9(27303.2~30716.1)=1, Bin 10(30716.1~34129)=2
- 슬라이드 14 코드: `import numpy as np` + `count, bin_edges = np.histogram(df['2013'])` + `plot(kind='hist', xticks=bin_edges)` (빨간 박스 3곳이 핵심)

## A-3. Bar Chart (슬라이드 15~18)
- 📘 **bar graph** 라고도 함 / 변수의 **값을 비교**
- 슬라이드 16: Iceland 이민자 세로 막대 `df_iceland.plot(kind='bar')`
- 슬라이드 17: **가로 막대** `df_iceland.plot(kind='barh', color='blue')`
- 슬라이드 18: **특정 막대만 색 강조**
```python
c = ['blue','red','blue','blue','blue','blue','blue','blue','blue','blue','red']   # 막대 개수만큼의 색 리스트
df_Iceland.plot(kind='bar', color=c, edgecolor='black')   # 1980~1990 → 1981, 1990만 빨강
```
- 📘 요약: **막대 길이는 대표하는 값에 비례**. 강조하고 싶은 막대는 **파라미터로 색을 바꿔** 강조.

## A-4. Histogram vs Bar (슬라이드 19~20) ⭐ 시험 단골 비교
| | **Histogram** | **Bar Chart** |
|---|---|---|
| 데이터 종류 | **연속형(continuous)** | **범주형(categorical)** |
| 막대 의미 | **구간(bin)** 내 빈도 | **범주** 하나의 값 또는 빈도 |
| 막대 사이 간격 | **없음** (연속이라서) | **있음** (범주가 구분되므로) |
| 순서 | **순서 유지 필수** | **순서 바꿀 수 있음** |
| 목적 | **분포(distribution)** 보기 | **범주 비교(compare categories)** |
| 예시 | 시험 점수 분포, 키 분포 (“Scores 0–10, 10–20, …”) | 전공별 학생 수, 제품 유형별 매출 (“A, B, C, D, F 학점”) |

## A-5. Recap (슬라이드 21)
- **Area plot**: 시간에 따른 **누적 합계**를 숫자 또는 퍼센트로 표현. Matplotlib import 후 DataFrame에 `plot()` 호출, **`kind='area'`**. 한 차트에서 여러 변수의 **관계와 비율**을 직관적으로 보여줌
- **Histogram**: 수치 데이터의 빈도 분포. `mpl`, `plt` import, DataFrame에 **`kind='hist'`**. **Numpy로 bin을 만들어** 사용 가능
- **Bar chart**: 막대 길이가 항목 값에 비례. 강조하려는 막대의 **색을 파라미터로 변경**

---
# PART B. Colab 실습 (노트북 `DV_06_Area_Hist_Bar.ipynb`)

## B-0. 전체 순서 요약
```
[공통 준비]
① import numpy, pandas, %matplotlib inline, matplotlib(mpl), pyplot(plt), mpl.style.use('ggplot')
② pd.read_csv() → df_can
③ df_can.head(), df_can.shape
④ df_can.set_index('Country', inplace=True)
⑤ years = list(map(str, range(1980, 2014)))

[Area]  sort_values('Total') → head() → [years].transpose() → index를 int로 → plot(kind='area', stacked=, alpha=, figsize=)
[Hist]  np.histogram으로 bin 확인 → plot(kind='hist', bins=, alpha=, xticks=bin_edges, color=, stacked=, xlim=)
[Bar]   .loc[국가, years] → plot(kind='bar'/'barh', ...) → plt.annotate()로 화살표/글자
[비교]  점수 데이터 생성 → 학점 범주화 → 히스토그램 vs 막대 나란히
```

## B-1. 공통 준비 (셀 1~13)
```python
import numpy as np
import pandas as pd
%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.style.use('ggplot')                              # (선택) ggplot 스타일
print('Matplotlib version: ', mpl.__version__)       # 3.10.0

df_can = pd.read_csv('https://...Canada.csv')
df_can.head()
print(df_can.shape)                    # (195, 39)  → 195개국, 39개 열
df_can.set_index('Country', inplace=True)
print('data dimensions:', df_can.shape)   # (195, 38)  → Country가 index로 빠져 열이 38개
years = list(map(str, range(1980, 2014)))   # '1980'..'2013'  (끝 2014 = 2013까지)
```
- 💡 열 38개 = Continent, Region, DevName + **1980~2013 (34개)** + **Total** → **`Total` 열은 CSV에 이미 들어 있음** (이전 DV_05 노트의 “Total 생성 셀 없음”은 이것으로 해결: 데이터에 포함).
- 💡 슬라이드 3~4: 원본 표는 Type, Coverage, OdName, AREA, AreaName, REG, RegName, DEV, DevName, 연도들; 정리 후 df_canada는 **Country가 index(빨간 박스)**, **Total 열(초록 박스)** 가 마지막 열.

---
## B-2. Area Plot

### 데이터 준비 (셀 16)
```python
df_can.sort_values(['Total'], ascending=False, axis=0, inplace=True)   # Total 내림차순
df_top5 = df_can.head()                       # 상위 5개 (head 기본값 5)
df_top5 = df_top5[years].transpose()          # 연도 열만 + 전치 (index=연도, 열=국가)
```
### 핵심 개념
- 📘 Area plot은 **기본이 stacked(누적)**
- 📘 stacked area는 **각 열이 모두 양수 또는 모두 음수**여야 함 (**NaN은 0으로 처리**)
- 📘 **unstacked**로 그리려면 **`stacked=False`**
- 📘 unstacked의 **기본 투명도(alpha) = 0.5**, `alpha`로 변경 (**0~1**)

### 코드 3종 (셀 18~22)
```python
df_top5.index = df_top5.index.map(int)      # 연도 index를 정수로

# ① unstacked (겹쳐서)
df_top5.plot(kind='area', stacked=False, figsize=(20, 10))
# ② stacked (쌓아서)
df_top5.plot(kind='area', stacked=True,  figsize=(20, 10))
# ③ stacked + 투명도
df_top5.plot(kind='area', alpha=0.25, stacked=True, figsize=(20, 10))

plt.title('Immigration Trend of Top 5 Countries')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')
plt.show()
```
- 💡 **stacked=True**: 각 나라 영역이 위로 쌓임 → **전체 합**과 **각 나라의 몫(기여도)** 을 봄 / **stacked=False**: 각 나라 영역이 같은 바닥(0)에서 시작해 **겹침** → 나라 간 **직접 비교**, 겹침이 보이도록 투명도 사용.

## ★ B-3. 두 가지 plotting 스타일 (셀 23~27) — 개념 이해 필수
| | **Option 1: Scripting layer** (procedural) | **Option 2: Artist layer** (object-oriented, **preferred**) |
|---|---|---|
| 사용 | `plt` (= `matplotlib.pyplot`) 함수 호출 | plot이 반환하는 **Axes 객체(`ax`)** 에 메서드 호출 |
| 제목 | `plt.title(...)` | `ax.set_title(...)` |
| x 라벨 | `plt.xlabel(...)` | `ax.set_xlabel(...)` |
| y 라벨 | `plt.ylabel(...)` | `ax.set_ylabel(...)` |
| 의미 | “**현재 활성화된 plot**의 제목 설정” — plot 하나일 때 편리 | “**`ax`가 나타내는 plot**의 제목 설정” — 어느 plot인지 명확, **여러 plot일 때 유리**, 고급 plot에 유연 |
```python
# Option 1
df_top5.plot(kind='area', alpha=0.35, figsize=(20, 10))
plt.title('Immigration trend of top 5 countries')
plt.ylabel('Number of immigrants')
plt.xlabel('Years')

# Option 2
ax = df_top5.plot(kind='area', alpha=0.35, figsize=(20, 10))   # plot 영역(Axes)을 ax에 저장
ax.set_title('Immigration Trend of Top 5 Countries')
ax.set_ylabel('Number of Immigrants')
ax.set_xlabel('Years')
```
- 💡 규칙: **plt.XXX → ax.set_XXX** (“set_”을 붙임).
- 📘 이 수업은 **scripting layer 위주**, 고급 시각화에서만 artist layer 사용.

### 연습 문제 ① (셀 28~30) 스크립팅 레이어: **가장 적게 기여한 5개국** stacked area, alpha=0.45
```python
df_least5 = df_can.tail(5)                         # Total 내림차순 정렬 상태이므로 tail = 최하위 5개국
df_least5 = df_least5[years].transpose()
df_least5.index = df_least5.index.map(int)
df_least5.plot(kind='area', alpha=0.45, figsize=(20, 10))   # stacked 기본값 True
plt.title('Immigration Trend of 5 Countries with Least Contribution to Immigration')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')
plt.show()
```
### 연습 문제 ② (셀 31~33) 아티스트 레이어: 최하위 5개국 **unstacked**, alpha=0.55
```python
ax = df_least5.plot(kind='area', alpha=0.55, stacked=False, figsize=(20, 10))
ax.set_title('Immigration Trend of 5 Countries with Least Contribution to Immigration')
ax.set_ylabel('Number of Immigrants')
ax.set_xlabel('Years')
```
- 💡 **상위 = `head()`, 하위 = `tail()`** (단, `Total` 내림차순 정렬이 되어 있을 때).

---
## B-4. Histogram

### 개념 (셀 34)
- 📘 x축을 **bin으로 분할** → 각 데이터 포인트를 bin에 **할당** → bin별 개수를 셈. **y축 = 빈도(각 bin의 데이터 수)**. **bin 크기는 바꿀 수 있고**, 분포가 잘 보이도록 조정 필요.

### 질문 1: 2013년 신규 이민자 수(195개국)의 빈도 분포 (셀 35~44)
```python
df_can['2013'].head()                                  # 확인 (Series: index=국가, 값=2013 이민자 수)

count, bin_edges = np.histogram(df_can['2013'], bins=10)   # np.histogram은 2개 값 반환!
print(count)       # [178  11   1   2   0   0   0   0   1   2]   ← 빈도
print(bin_edges)   # [0. 3412.9 6825.8 ... 34129.]               ← bin 경계 (기본 10 bins → 경계 11개)
```
- 📘 **178개국이 0~3412.9명, 11개국이 3412.9~6825.8명, 1개국이 6825.8~10238.7명 …** 기여.
```python
df_can['2013'].plot(kind='hist', figsize=(8, 5))
plt.title('Histogram of Immigration from 195 Countries in 2013')
plt.ylabel('Number of Countries')     # y = 나라 수 (빈도)
plt.xlabel('Number of Immigrants')    # x = 이민자 수 구간
plt.show()
```
- 문제점 📘: **x축 눈금이 bin 크기와 안 맞음** → **`xticks=bin_edges`** 로 해결
```python
count, bin_edges = np.histogram(df_can['2013'], bins=10)
df_can['2013'].plot(kind='hist', figsize=(8, 5), xticks=bin_edges)
```
- 📘 **Side note**: `data.plot(kind='hist')` ≡ `data.plot.hist()` (**kind 인자 방식과 메서드 방식은 동일**, 모든 plot 종류에서 성립)

### 질문 2: 덴마크·노르웨이·스웨덴 1980~2013 분포 (셀 45~55)
```python
df_can.loc[['Denmark', 'Norway', 'Sweden'], years].plot.hist()     # ❌ 이상한 그래프
```
- 📘 이유: 3개국의 이민자 분포가 아니라 **연도(years)별 분포**를 그림. **데이터 구조(행/열) 문제**.
- ✅ **해결: transpose 후 plot**
```python
df_t = df_can.loc[['Denmark', 'Norway', 'Sweden'], years].transpose()   # 열 = 국가, 행 = 연도
df_t.plot(kind='hist', figsize=(10, 6))
plt.title('Histogram of Immigration from Denmark, Norway, and Sweden from 1980 - 2013')
plt.ylabel('Number of Years')            # y = 해당 구간에 속한 "연도 수"
plt.xlabel('Number of Immigrants')
plt.show()
```
- 💡 **y축 의미가 다름**: 질문 1의 y = “나라 수”(행=국가 195개), 질문 2의 y = “연도 수”(행=연도 34개). **히스토그램의 y = 행(관측값)의 개수** → 행에 무엇이 오는지가 중요.

### 꾸미기: bins, alpha, xticks, color (셀 51~52) — 겹친(unstacked) 히스토그램
```python
count, bin_edges = np.histogram(df_t, 15)        # 15 bins로 경계 계산 (xticks용)

df_t.plot(kind='hist',
          figsize=(10, 6),
          bins=15,                                # bin 개수 15
          alpha=0.6,                              # 투명도 60%
          xticks=bin_edges,                       # x축 눈금 = bin 경계
          color=['coral', 'darkslateblue', 'mediumseagreen'])   # 열(국가)별 색
```
- 📘 노트북 설명: bin 크기 15 / 투명도 60% / (x-label) / **색 변경은 `color` 파라미터**
- 📘 Tip: Matplotlib의 전체 색 목록 → `matplotlib.colors.cnames.items()` 순회 출력

### 겹치지 않게: stacked + xlim (셀 54~55)
```python
count, bin_edges = np.histogram(df_t, 15)
xmin = bin_edges[0] - 10      # 첫 bin 값(31.0) 앞에 여백 10
xmax = bin_edges[-1] + 10     # 마지막 bin 값(308.0) 뒤에 여백 10

df_t.plot(kind='hist', figsize=(10, 6), bins=15, xticks=bin_edges,
          color=['coral', 'darkslateblue', 'mediumseagreen'],
          stacked=True,                 # 쌓기 (겹치지 않음)
          xlim=(xmin, xmax))            # x축 범위 (min, max) 튜플 → 양 끝 여백 조절
```
- 📘 `stacked` = 서로 겹치지 않게 쌓기 / `xlim=(min, max)` = 양쪽 가장자리의 불필요한 빈 공간 제거
- 💡 **bin_edges[0]** = 첫 경계, **bin_edges[-1]** = 마지막 경계.

### 연습 문제 (셀 56~58): 그리스·알바니아·불가리아, **겹침(overlapping) 15 bins, alpha=0.35**
```python
df_cof = df_can.loc[['Greece', 'Albania', 'Bulgaria'], years].transpose()
count, bin_edges = np.histogram(df_cof, 15)
df_cof.plot(kind='hist', figsize=(10, 6), bins=15, alpha=0.35,
            xticks=bin_edges, color=['coral', 'darkslateblue', 'mediumseagreen'])
plt.title('Histogram of Immigration from Greece, Albania, and Bulgaria from 1980 - 2013')
plt.ylabel('Number of Years')
plt.xlabel('Number of Immigrants')
plt.show()
```

---
## B-5. Bar Chart

### 개념 (셀 59~60)
- 📘 bar plot: **막대의 길이 = 변수의 크기**. 보통 **수치형·범주형 변수를 구간으로 묶어** 표현.
- 📘 `plot()`의 **`kind`**: **`'bar'` = 세로(vertical)** / **`'barh'` = 가로(horizontal)**
- 📘 **세로 막대**: x축 = 라벨, y축 막대 길이 = 값. **시계열 분석에 유용**. 단점: 각 막대 아래 **글자 라벨 공간이 부족**.
- 📘 **가로 막대**: y축 = 라벨, x축 길이 = 값. **범주 이름 쓸 공간이 넉넉**.

### 사례: 아이슬란드 금융위기 (2008~2011) — 아이슬란드 → 캐나다 이민
```python
df_iceland = df_can.loc['Iceland', years]       # Series
df_iceland.plot(kind='bar', figsize=(10, 6))
plt.xlabel('Year'); plt.ylabel('Number of immigrants')
plt.title('Icelandic immigrants to Canada from 1980 to 2013')
plt.show()
```
- 📘 해석: **2008년 이후 이민자 수가 급증** → 금융위기의 영향.

### `plt.annotate()` — 화살표/글자 주석 (셀 63~66)
| 파라미터 | 의미 |
|---|---|
| `s` | 주석 **텍스트** (문자열). 비우면 글자 없음(화살표만) |
| `xy` | 주석할 **(x, y) 지점** (= **화살표 머리**) |
| `xytext` | **텍스트를 놓을 (x, y)** (= **화살표 시작점**) |
| `xycoords` | xy가 쓰는 **좌표계**. `'data'`(기본) = 주석 대상 객체의 좌표계 |
| `arrowprops` | 화살표 속성 **딕셔너리**: `arrowstyle`(`'->'` 표준 화살표), `connectionstyle`(`'arc3'` = 직선), `color`, `lw`(선 굵기) |
| `rotation` | 텍스트 **회전각**(도, 반시계) |
| `va` | 세로 정렬 `'center' / 'top' / 'bottom' / 'baseline'` |
| `ha` | 가로 정렬 `'center' / 'right' / 'left'` |
```python
df_iceland.plot(kind='bar', figsize=(10, 6), rot=90)       # rot=90: x축 눈금 글자를 90도 회전

plt.xlabel('Year'); plt.ylabel('Number of Immigrants')
plt.title('Icelandic Immigrants to Canada from 1980 to 2013')

# (1) 화살표
plt.annotate('',                       # 글자 없음
             xy=(32, 70),              # 화살표 머리: x=32(=2012년), y=70
             xytext=(28, 20),          # 화살표 꼬리: x=28(=2008년), y=20
             xycoords='data',
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='blue', lw=2))

# (2) 화살표 위 글자
plt.annotate('2008 - 2011 Financial Crisis',
             xy=(28, 30),              # 글자 시작 위치 (2008년, 30)
             rotation=72.5,            # 화살표 각도에 맞추려 시행착오로 정한 값
             va='bottom', ha='left')
plt.show()
```
- 💡 **bar plot의 x좌표는 연도 값이 아니라 “막대 순번(0부터)”**: 1980=0 → 2008=**28**, 2012=**32**. (DV_05 `plt.text`에서 문자열 index일 때 순번을 쓰는 것과 같은 원리)
- 💡 `plt.text(x, y, 글자)`는 단순 텍스트, `plt.annotate()`는 **화살표까지** 가능.

### 가로 막대 연습 (셀 67~73): 이민 총합 상위 15개국 `barh` + 막대에 숫자 라벨
```python
# Step 1: Total 기준 오름차순 정렬 → 마지막 15개 = 상위 15개
df_can.sort_values(by='Total', ascending=True, inplace=True)
df_top15 = df_can['Total'].tail(15)           # Series (국가별 Total)

# Step 2: 가로 막대 + 값 표시
df_top15.plot(kind='barh', figsize=(12, 12), color='steelblue')
plt.xlabel('Number of Immigrants')
plt.title('Top 15 Conuntries Contributing to the Immigration to Canada between 1980 - 2013')

for index, value in enumerate(df_top15):            # 각 막대를 순회
    label = format(int(value), ',')                  # 정수에 천 단위 쉼표 (예: 691,904)
    plt.annotate(label, xy=(value - 47000, index - 0.10), color='white')   # 막대 끝 안쪽에 흰 글씨

plt.show()
```
- 💡 **왜 ascending=True + tail(15)?** `barh`는 **아래에서 위로** 그려서 첫 행이 맨 아래에 옴 → **오름차순으로 정렬 후 tail**하면 **가장 큰 값이 맨 위**에 표시됨.
- 💡 `enumerate(df_top15)`: index = 막대 순번(y좌표), value = 값(x좌표). `value - 47000`은 글자를 **막대 끝에서 왼쪽(막대 안)** 으로 옮겨 넣는 보정.
- 💡 `format(int(value), ',')`: 숫자를 `'691,904'` 형태로.

---
## B-6. Histogram vs Bar 직접 비교 (셀 74~82)

### ① 예시 데이터 생성 (셀 76)
```python
np.random.seed(42)                                       # 재현 가능하도록 시드 고정
scores = np.random.normal(loc=70, scale=15, size=200)    # 정규분포: 평균 70, 표준편차 15, 학생 200명
scores = np.clip(scores, 0, 100)                         # 0~100 범위로 자르기
df = pd.DataFrame({"Score": scores})
```
### ② 학점 범주화 (셀 77~79) — bar chart는 **범주화된 데이터**가 필요
- 기준: 90~100 → A / 80~90 → B / 70~80 → C / 60~70 → D / 60 미만 → F
```python
def grade(score):
    if score >= 90: return "A"
    elif score >= 80: return "B"
    elif score >= 70: return "C"
    elif score >= 60: return "D"
    else: return "F"

df["Grade"] = df["Score"].apply(grade)                       # 각 점수에 함수 적용 → 새 열
grade_counts = df["Grade"].value_counts().sort_index()       # 학점별 인원 수 (A,B,C,D,F 순 정렬)
```
### ③ 나란히 그리기 (셀 80~82) — `plt.subplot`
```python
plt.figure(figsize=(12,5))

# 오른쪽(subplot 1,2,2): Histogram — 연속형 점수 분포
plt.subplot(1,2,2)
plt.hist(df["Score"], bins=10, color="skyblue", edgecolor="black")
plt.title("Histogram (Continuous: Score Distribution)")
plt.xlabel("Score"); plt.ylabel("Frequency")

# 왼쪽(subplot 1,2,1): Bar Chart — 범주형 학점
plt.subplot(1,2,1)
plt.bar(grade_counts.index, grade_counts.values, color="lightgreen", edgecolor="black")
plt.title("Bar Chart (Categorical: Number of Students by Grade)")
plt.xlabel("Grade"); plt.ylabel("Number of Students")

plt.tight_layout()      # 겹치지 않게 간격 자동 조정
plt.show()
```
- 💡 `plt.subplot(행, 열, 위치번호)`: `(1,2,1)` = 1행 2열 중 **첫 번째(왼쪽)**, `(1,2,2)` = **두 번째(오른쪽)**. 노트북 코드의 주석 순서는 (1) Histogram이 먼저지만 위치는 **오른쪽(2번)** 이니 헷갈리지 말 것.
- 💡 이 셀은 **pandas가 아니라 pyplot 함수**(`plt.hist`, `plt.bar`)를 직접 사용: `plt.hist(데이터, bins=, color=, edgecolor=)`, `plt.bar(x(범주), height(값), color=, edgecolor=)`.

---
# PART C. 정리표

## C-1. plot별 사용 변수·함수

| Plot | 사용한 데이터 | x축 | y축 | 핵심 코드 | 주요 파라미터 |
|---|---|---|---|---|---|
| **Area** (상위/하위 5개국) | `sort_values('Total')` → `head()`/`tail(5)` → `[years].transpose()` | 연도(index, int) | 국가별 이민자 수(열=영역) | `df.plot(kind='area')` | `stacked`(기본 True), `alpha`(0~1), `figsize` |
| **Histogram** 1개 열 | `df_can['2013']` (Series) | 이민자 수 구간(bin) | 나라 수(빈도) | `plot(kind='hist')` | `xticks=bin_edges`, `bins` |
| **Histogram** 여러 국가 | `df_can.loc[[국가...], years].transpose()` | 이민자 수 구간 | 연도 수(빈도) | `plot(kind='hist')` | `bins`, `alpha`, `xticks`, `color=[...]`, `stacked`, `xlim=(min,max)` |
| **Bar (세로)** | `df_can.loc['Iceland', years]` (Series) | 연도(범주) | 이민자 수 | `plot(kind='bar')` | `rot=90`, `color=`, `edgecolor=` |
| **Bar (가로)** | `df_can['Total'].tail(15)` (Series) | 이민자 총합 | 국가(범주) | `plot(kind='barh')` | `color`, `figsize` |
| **Hist vs Bar** | `df['Score']`(연속), `grade_counts`(범주) | 점수 구간 / 학점 | 빈도 / 학생 수 | `plt.hist`, `plt.bar` | `bins`, `edgecolor`, `plt.subplot` |

## C-2. 파라미터 사전
| 파라미터 | 적용 plot | 의미 |
|---|---|---|
| `kind` | 전부 | plot 종류: `'line' 'area' 'hist' 'bar' 'barh'` (`.plot.hist()` 도 동일) |
| `stacked` | area, hist | 쌓기 여부 (area 기본 True / hist 기본 겹침) |
| `alpha` | area, hist | 투명도 0~1 (area unstacked 기본 0.5) |
| `figsize=(가로,세로)` | 전부 | 그림 크기 |
| `bins` | hist | bin 개수 |
| `xticks` | hist | x축 눈금 위치 (보통 `bin_edges`) |
| `xlim=(min,max)` | hist | x축 범위 |
| `color` | hist, bar | 색 (한 개 또는 리스트) |
| `edgecolor` | bar | 막대 테두리 색 |
| `rot` | bar | 눈금 글자 회전각 |

## C-3. 시험 대비 포인트
1. **Area plot은 기본 stacked**. 겹치게 하려면 `stacked=False`. 투명도 기본 0.5.
2. **여러 국가를 그리는 plot(area/hist)은 `transpose()`** 필수 (index=x 또는 관측치, 열=그룹).
3. **np.histogram은 (count, bin_edges) 2개 반환**. bin_edges는 `xticks=`에 넣어 눈금과 bin을 맞춤.
4. **`plt.xxx()` ↔ `ax.set_xxx()`**: scripting vs artist layer. `ax = df.plot(...)`.
5. **bar = 범주 / histogram = 연속**. 간격 유무, 순서, 목적 차이 설명할 수 있어야 함 (슬라이드 20).
6. **`bar` = 세로, `barh` = 가로**. 라벨이 길면 가로.
7. `plt.annotate` 좌표(bar의 x)는 연도가 아니라 **막대 순번**.
8. 상위 N = `sort_values(내림차순).head(N)`, 하위 N = `.tail(N)`. barh 상위 N을 위에 보이게 하려면 **오름차순 + tail(N)**.
9. 슬라이드 정의: **area = line plot 기반, 크기와 비율 표현**.
