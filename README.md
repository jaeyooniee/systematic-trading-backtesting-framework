# Systematic Trading Strategies Backtesting Framework

The project aims to backtest 5 well-known strategies when trading a single US equity.
I focused on getting statistically plausible results which are justified by statistic tests.
The framework ultimately reveals whether the strategies show statistically plausible differences in their **sharpe ratio**.

> The goal is not to find the highest profitable strategy but to successfully claim that 
> one strategy did show higher returns than the others. It is about answering to a methodological question.
> Therefore, the crucial point of the evaluation is focused on the statistical strictness of comparation.

---

## 0. Journey of the Project (From Start to the End)
This part will illustrate the whole steps of **how I started this project and what process I have gone through to get to the results** chronologically. 

### 0.1 Start off (What am I building exactly?)
From my deep interest in quantitative finance field, I first thought of building a trading strategies backtesting framework. Firstly, I chose the identities: **Not "Finding the best strategy" but the "Methodology that statistically justifies the comparation of the strategies"**.

In addition, I decided to build a vectorisation engine other than importing already built libraries. The big picture of the framework (e.g. pairwise comparing 5 strategies in a single stock, sharpe ratio as the main indicator, T-bill as rf ...) was drawed at this stage.

### 0.2 Selection of strategies 
I have collected trading strategies without any bias from [QuantConnect](https://www.quantconnect.com/research/), [TradingView](https://www.tradingview.com/), Peng Liu's [Quantitative Trading Strategies Using Python](https://link.springer.com/book/10.1007/978-1-4842-9675-2). Multiple equities and cross-sectional strategies were omitted since the framework I planned was only focusing on trading one stock. 

### 0.3 Choosing Data Source
I had two options for getting price data.
1. Polygon
2. yfinance

However, Polygon has been rebranded and now restricts some past data so I chose to implement **yfinance**.
Risk-free rate was selected as **FRED DTB3** (3-Month Treasury Bill Secondary Market Rate).

### 0.4 Setting final 5 strategies 
I changed strategies quite a few times before I do the code part.
- First, the sets were "MACD, Donchian, PSAR, Bollinger and Stochastic, I selected these by their popularities and the time they were mentioned. 
- But, at the end it became **MACD, RSI, Bollinger, Stochastic, PSAR** (Donchian out, RSI in) since I was more familiar with RSI. 
- The mechanisms are various, momentum/trend/mean reversion/oscillator.

### 0.5 Testing Methods - Using methods from uni modules
검증을 "그냥 표준 방법"이 아니라 **내가 배운 과목에서 출처가 확인된 방법**으로 세우기로
했다. Statistics 1과 Data Science 자료가 정리된 별도 프로젝트에 동일한 프롬프트를 던져,
각 방법이 어디서 배운 것인지 확인했다.
- 처음엔 "수익률 비교 vs Sharpe 비교"의 차이부터 짚었다 — Sharpe는 비선형 통계량이라 t검정
  공식이 없고, 그래서 부트스트랩이 필요하다는 결론.
- Statistics 1엔 부트스트랩이 **없어** 주 판정의 토대가 비었으나, Data Science Week 2에
  부트스트랩이 **있어** 본체가 다시 섰다.
- 자기상관·다중비교 보정은 두 과목 다 없음을 확인 → **"본체는 배운 것, 보정만 외부에서
  명시적으로 빌린다"(길 B)**로 결정.
- 출처를 본체/파생/외부 세 층으로 정직하게 구분했다(상세는 6·14절).

### 0.6 파라미터 사전 확정 (결과 보기 전)
결과를 보기 전에 모든 파라미터를 못박았다(사전등록): 부트스트랩 5,000회, 신뢰수준 95%,
퍼센타일 CI, 시드 42, 데이터 기간 2005~2025 고정, 최소 거래 기준 30, cost_pct 기본 0.
- 데이터 기간은 처음 "가용 최대"로 정했다가, T-bill 정렬 번거로움과 임의성 문제로 **고정
  20년**으로 변경.
- in/out 분리는 — 데이터 기반 조정이 없어 과적합 탐지 목적이 성립 안 하고 검정력만
  깎이므로 **하지 않기로** 결정.
- 블록 길이는 ACF로 정했는데, 처음 잘못된 "마지막 유의 lag" 방식(블록 30)을 폐기하고
  "연속 유의 구간" 규칙으로 재계산 → SMA 제거 후 **블록 4**로 확정(중앙값=최댓값=4).

### 0.7 구현과 검증
아래층부터 쌓으며 각 단계를 검증했다: data_loader(키를 환경변수로 분리, 기간 고정) →
engine(shift는 엔진에서 한 번, excess와 raw returns 둘 다 반환) → metrics(Sharpe raw
ddof=0, Calmar는 raw, Sortino 하방편차 수정). 엔진은 buy-and-hold로 **단순 보유 수익과
정확히 일치(차이 0.0)**함을 확인. 부트스트랩은 **알려진 분포로 검증**(차이 없으면 CI가 0
포함, 있으면 제외). 전략 5개는 우리 인터페이스(0/1 신호, shift 없음)에 맞게 정리, 효율을
위해 부트스트랩을 numpy로 벡터화.

### 0.8 결과와 방향 조정
5개 티커 실행 결과, **대부분 "통계적으로 구분 불가"**가 나왔다. 이 결과가 밋밋해 보여
"백테스트 성과 시각화를 추가"하는 쪽으로 방향을 조정했다 — 단, **검증 엄격성은 절대 낮추지
않고**(결과 보고 기준 바꾸기 금지), 시각화를 *추가*만 했다. 시각화 도구도 과목 자료에서
출처를 찾아(히스토그램: Stats 1 §2.2 / DS Wk1-2) 일관성을 유지했다. "구분 불가"는
실패가 아니라 — 프로젝트 목적(비교의 통계적 정당성)에 비추어 정직하고 유효한 결론으로
받아들였다.

> 이 여정의 핵심 교훈: 결정의 *근거와 출처*를 매 단계 명시하고, 결과가 기대와 달라도
> 사전에 정한 절차를 바꾸지 않는 것. 그것이 이 프로젝트를 "수익 자랑"이 아니라
> "방법론적으로 방어 가능한 비교 연구"로 만든다.

---

## 1. 핵심 질문

> 전략 A의 Sharpe Ratio가 전략 B보다 높을 때, 이 차이가 단지 우연(표본 변동)이 아니라
> **통계적으로 유의한 차이**라고 높은 신뢰도로 말할 수 있는가?

이 질문에 답하기 위해, 일정 기간의 Sharpe Ratio를 단순 비교하는 것을 넘어서, 부트스트랩
기반 신뢰구간과 다중비교 보정을 포함한 검증 절차를 사용한다.

---

## 2. 주요 설계 결정과 근거

| 결정 | 내용 | 근거 |
|------|------|------|
| 비교 범위 | 단일 티커 내에서 5개 전략을 pairwise 비교 (10쌍) | 모든 전략이 동일한 데이터를 보므로 survivorship bias가 비교에 무관해짐 |
| 포지션 | LONG-ONLY, 0(현금) 또는 1(보유)만 | 공매도 시 borrow cost·비대칭 위험 모델링 필요 → 제외. "매도"는 0(현금)으로 가는 것 |
| 포지션 크기 | binary (신호 on=100% 보유, off=100% 현금) | 포지션 사이징은 추가적인 과적합 축이자 교란변수 → 비교 순수성을 위해 배제 |
| 손절 | 없음 | 손절은 전략마다 다르게 작용해 "신호 비교"에 "손절 민감도"를 혼입시킴 → 순수 신호 비교 |
| 거래량 | 신호에 사용 안 함 | split 조정 부담 + 거래량의 극단적 fat tail 회피 |
| 머신러닝 | 사용 안 함 | "데이터 보기 전 파라미터 고정" 원칙과 충돌(ML은 본질적으로 데이터에서 학습) |
| 파라미터 | 이론/관례값으로 데이터 보기 전 고정 | 데이터로 튜닝 = 과적합. 모든 전략이 각 지표의 표준 설정값 사용 |
| 데이터 기간 | 고정 20년 (2005-01-01 ~ 2025-01-01) | 결과·거래횟수 보고 정하면 편향이므로 결과 보기 전 고정. 충분한 검정력 + 현대 시장 구조 반영(과도하게 오래된 데이터 제외). 끝을 고정해 재실행 시 기간이 늘지 않게 함 |

---

## 3. 데이터 레이어

- **가격 데이터:** yfinance, `auto_adjust=True` (split·배당이 모두 반영된 일관된 OHLC).
  Polygon/Massive 무료 티어는 과거 데이터 기간(약 2년)이 너무 짧아 검정력 확보가
  어려워 제외. 데이터 레이어는 소스 교체가 가능하도록 격리.
- **OHLC 전체 보존:** 주 사용은 Close지만, 캔들/intraday 기반 지표를 재요청 없이 추가할
  수 있도록 OHLC 전부 유지.
- **무위험수익률(rf):** FRED DTB3 (3-month T-bill).
  - DTB3는 **연율 %**이므로, 차감 전 일별로 변환한다: `rf_daily = rf_annual / 100 / 252`.
  - 변환 방식(÷252)은 표준 거래일 가정에 따른 것으로, 코드와 본 문서에 명시.
- **거래 캘린더:** 가격 데이터에 존재하는 날짜(=거래일)를 기준으로 rf를 정렬하고,
  결측 rf는 forward-fill, 맨 앞 결측은 back-fill로 보강(FRED와 거래일 캘린더가 달라
  생기는 누락 대응).
- **타임존/인덱스:** 날짜 인덱스의 시간 성분을 normalize로 제거해 가격·rf 타임스탬프를 정렬.

---

## 4. 전략 (5개)

모든 전략은 LONG-ONLY이며, `signal(prices) -> pd.Series` 형태로 **0/1 신호만** 반환한다.
파라미터는 전부 각 지표의 **표준(관례) 설정값**이며, 데이터로 튜닝하지 않았다.

| # | 전략 | 파라미터 | 메커니즘 유형 |
|---|------|----------|--------------|
| 1 | MACD | 12 / 26 / 9 | 이동평균 모멘텀 |
| 2 | RSI | 14, 진입 <30 / 청산 >70 (stateful) | 평균회귀 (모멘텀 오실레이터) |
| 3 | Parabolic SAR | step 0.02 / max 0.20 | 추세 전환 (stateful 재귀) |
| 4 | Bollinger Band (평균회귀) | window 20 / 2 SD | 평균회귀 |
| 5 | Stochastic Oscillator | 14 / 3 / 3 | 오실레이터(평균회귀) |

전략 풀이 이동평균류에 치우치지 않도록 모멘텀/추세전환/평균회귀/오실레이터로
메커니즘을 의도적으로 분산.

---

## 5. 엔진과 지표

### 엔진 (`engine/backtest.py`)
공정한 비교를 강제하는 변환 엔진. 모든 전략이 동일한 규칙을 거치도록 함.

```
run(prices, signal_fn, rf_daily, cost_pct=0):
    signal   = signal_fn(prices)          # 전략은 0/1 신호만 생성
    position = signal.shift(1)             # 단 하나의 shift — 엔진에서만
    returns  = position * daily_returns    # 신호는 당일, 체결은 익일
    returns  = returns - |position.diff()| * cost_pct / 100   # 거래비용(퍼센트)
    excess   = returns - rf_daily
    return returns, excess                 # raw(Calmar용) + excess(Sharpe/Sortino용)
```

- **`signal.shift(1)`은 엔진에서 한 번만.** 전략 함수 내부에서는 절대 shift하지 않음.
  신호는 당일 종가까지의 정보로 만들고 실제 거래는 다음 날 적용 → lookahead 방지.
- **`cost_pct` 파라미터 (기본값 0, 단위 퍼센트).** 거래비용을 차감하는 인자를 두되 기본값은
  0으로, 기본 실행은 거래비용 없이 순수 신호만 비교한다(손절 제외와 동일한 정신). 비용을 켜면
  `|position.diff()| * cost_pct / 100`로 포지션 전환 시 차감된다(예: cost_pct=0.1 → 0.1%).
  - 기본 실행(cost_pct=0)은 거래비용 전 순수 신호 성능을 보므로, 거래가 잦은
    전략(예: MACD)이 비용 면에서 다소 유리하게 평가될 수 있다. 비용 영향을 보고 싶으면
    인자에 값을 넣어 재실행하면 된다.
- **반환 구조:** 엔진은 `(returns, excess)`를 둘 다 반환한다. rf 차감(excess)은 Sharpe·
  Sortino용, 거래비용만 반영된 raw `returns`는 Calmar용(낙폭은 실제 자산 기준이라 rf를
  빼지 않음). rf의 연→일 변환은 데이터 레이어에서, excess 차감은 엔진에서 한다.

### 지표 (`engine/metrics.py`)
- **주 지표: 연율화 Sharpe Ratio.** 유의성 판정은 오직 Sharpe로 한다.
  - `Sharpe = mean(excess) / std(excess)` — mean·std 모두 excess에서, **std는 ddof=0**
    (부트스트랩의 numpy 계산과 값을 일치시키기 위함).
  - `metrics.sharpe()`는 **raw(연율화 안 된) 값**을 반환. √252는 부트스트랩 CI를 만든
    **후 외부에서 단 한 번** 곱한다. 절대 부트스트랩 루프 내부에서 곱하지 않음.
  - CAGR/변동성 형태가 아니라 mean/std 형태를 쓰는 이유: 부트스트랩 리샘플과 호환되고
    (순서 비의존), √252를 루프 밖으로 분리할 수 있기 때문.
- **보조 지표(서술용): Calmar, Sortino.**
  - 유의성 판정에는 사용하지 않음. 승자가 다른 측면에서도 견고한지 보여주는 서술적 증거.
  - **Calmar는 raw `returns`를 입력**으로 받는다(낙폭 MDD는 실제 자산 기준이라 rf를 빼지
    않음). 식 안에 연율화(252/n)가 이미 포함되어 √252를 곱하지 않는다.
  - **Sortino는 excess를 입력**으로 받고, 하방편차는 양수를 0으로 둔 전체 기간 RMS로
    계산(음수만 추출하지 않음). √252는 외부에서 곱한다.

### Sharpe를 주 지표로 쓰는 것의 한계 (명시)
Sharpe는 위험을 표준편차(양방향 변동)로 정의하므로 (a) 수익률 분포의 비대칭과
(b) fat tail의 심각성을 충분히 반영하지 못한다. 이를 인지하여 하방 위험 지표(Sortino)와
낙폭 기반 지표(Calmar)를 보조로 병기하고, 통계적 유의성과 함께 **효과 크기(점추정
Sharpe 차이)**를 같이 보고한다.

---

## 6. 검증 방법론

본 프레임워크의 검증은 다음 세 층으로 구성되며, 각 방법의 **출처를 명시**한다.
검증 방법은 학부 과목 **Statistics 1**과 **Data Science**에서 배운 내용을 본체로 하고,
그 범위를 벗어나는 보정만 외부 도구로 명시적으로 도입했다.

### (A) 본체 — 학부 과목에서 배운 방법

**1. 부트스트랩으로 Sharpe 차이의 신뢰구간 구성 → 0 포함 여부로 판정 (주 판정)**
- 두 전략은 같은 종목·같은 날짜라 서로 상관되어 있으므로, **paired 차이 구조**로
  상관을 흡수한다. 날짜를 묶어 함께 리샘플(joint)하여 각 리샘플에서
  `Sharpe_A − Sharpe_B`를 계산하고, 이를 **5,000회** 반복해 그 분포에서 **95% 신뢰구간**
  (퍼센타일 2.5/97.5)을 구한다. 리샘플은 **moving block bootstrap(고정 블록 길이 4,
  circular wrap)**으로 시계열 자기상관 구조를 보존한다.
- 신뢰구간이 0을 포함하면 "유의한 차이 없음", 포함하지 않으면 "유의하게 다름".
  방향은 점추정 부호로 별도 판단("A ≠ B, 효과는 A 쪽").
- 같은 부트스트랩 분포에서 **양측 p-value**도 계산한다(0 기준 양쪽 꼬리 중 작은 쪽 ×2).
  이 p-value를 Holm 보정(아래 C)에 사용한다.
- 부트스트랩이 적합한 이유: Sharpe는 비선형 통계량이라 t/z의 깔끔한 공식이 없으나
  부트스트랩은 어떤 통계량에도 적용 가능하고, fat tail·비정규를 가정 없이 처리한다.
- **출처:** 부트스트랩의 개념·절차·CI 구성 → *Data Science, Week 2 (2월 10일)
  "Data Sampling"* 강의 및 Canvas Week 2 리딩 *Measurement and their Uncertainties,
  ch.1–2*. 해당 자료는 "작은 데이터셋, 분포 미지, 비정규(긴 꼬리), 어떤 통계량에도
  적용 가능"이라고 명시함.
- CI로 가설을 판정하는 논리(구간이 기준값을 포함하면 fail to reject) →
  *Statistics 1, Section 15.2.1* (양측검정과 신뢰구간의 동치) 및 *Data Science,
  2월 10·17일* 예제.

**2. paired 차이의 t/z 검정 (교차검증)**
- 동일한 paired 차이 시계열에 단일표본 t/z 검정을 적용하여 부트스트랩 결과와 대조.
  두 독립적 방법이 같은 결론을 주면 신뢰도가 높아진다. (단, fat tail·자기상관 때문에
  단독으로 의존하지 않고 교차검증용으로만 사용.)
- **출처:** 단일표본 t/z검정, CLT, n≥30 룰 → *Statistics 1, Section 15* 및
  *Data Science, 2월 17일 (Week 3)*. 추가 리딩 *Statistics in a Nutshell, ch.3*.

### (B) 파생 — 배운 방법을 조합/적용한 것 (정직하게 표시)

다음은 위 과목들에서 **직접 그 형태로 배운 것은 아니며**, 배운 구성요소를 조합·적용한 것이다:
- **paired(대응표본) 차이 검정:** 두 과목 모두 "paired 전용 검정" 절은 없음. 배운
  단일표본 t/z검정(Stats 1 Sec 15 / DS 2월 17일)과 차이의 CI 판정(항목 A-1)을
  **조합하여 도출**한 것.
- **Sharpe(비선형 통계량)에 부트스트랩 적용:** 부트스트랩은 배웠으나(DS Week 2)
  교육 예제는 중앙값 비율이었고 Sharpe 예시는 없음. 다만 자료가 "어떤 통계량에도
  적용 가능"이라 명시했으므로 근거 있는 확장.
- **Sharpe 차이 = 0의 CI 판정:** CI 판정 논리(기준값 0/1)는 배웠으며, 기준값을
  "Sharpe 차이 = 0"으로 적용한 것.

### (C) 외부 도구 — 과목 범위 밖, 통계적 필요로 명시적 도입

다음은 두 과목 자료 어디에도 없음이 확인되었으며, 통계적 타당성을 위해 외부에서
명시적으로 빌린 것이다:
- **자기상관 보정 — Moving Block Bootstrap (고정 블록 길이):** 시계열의 자기상관
  구조를 보존하기 위해 단순 부트스트랩 대신 고정 길이 블록 단위로 리샘플(circular wrap).
  블록 길이는 차이 시계열의 ACF로 결정(아래 7절, =4). (Politis–Romano의 stationary
  bootstrap은 블록 길이를 기하분포로 무작위화하나, 여기서는 구현 단순성과 해석 용이성을
  위해 고정 길이 moving block을 사용.)
- **다중비교 보정 — Holm:** 5개 전략 = 10쌍을 동시 검정하므로 가짜 양성(family-wise
  error)을 통제. 각 쌍의 부트스트랩 양측 p-value를 오름차순 정렬해 Holm-Bonferroni로
  보정(k번째에 (m−k)를 곱하고 단조성 보장). family 범위는 단일 티커의 10쌍(티커 간 풀링 없음).

> 두 과목 모두 다중비교 보정과 자기상관 보정을 다루지 않았음이 출처 확인 과정에서
> 명확히 확인되었다. 따라서 이 두 보정은 "배운 것"이 아니라 "필요해서 명시적으로
> 도입한 외부 도구"로 정직하게 구분한다.

---

## 7. 블록 길이 결정 (ACF)

- 차이 시계열의 자기상관함수(ACF)를 numpy로 직접 계산(표준 biased 추정량).
- **규칙:** lag 1부터 보며 **연속으로** 유의한(±1.96/√n 밴드 밖) 구간만 센다. 처음으로
  밴드 안에 들어오면 멈춘다 — 멀리 떨어진 외딴 유의 lag는 다중검정상 우연일 가능성이
  크므로 무시.
- 유의한 자기상관이 없으면 블록 길이 **1**(사실상 단순 부트스트랩). 있으면
  `연속 유의 길이 + cushion`으로 자기상관 구조를 통째로 덮도록 넉넉히 설정.
- ACF는 "부트스트랩을 쓸지 말지"를 정하는 것이 아니다(부트스트랩은 fat tail 때문에
  자기상관 유무와 무관하게 항상 사용). ACF는 **블록 길이라는 파라미터만** 결정한다.

### 통일 방식과 확정값

- 10쌍(5개 전략) 각각의 차이 시계열에 ACF를 걸어 쌍별 블록 길이를 구한 뒤, **그
  중앙값을 모든 쌍에 통일 적용**한다.
- 통일하는 이유: 모든 비교가 동일 규칙을 받아 공정성이 명확하고 설명이 일관됨.

**확정값: block length = 4** (n=1,881 기준)

- 쌍별 블록 길이 분포: **min 1 / median 4 / max 4.**
- 두 그룹으로 명확히 갈림: (1) 블록 1 — 자기상관 없음(Bollinger·Stochastic·RSI가
  서로 엮인 평균회귀/오실레이터 계열 4쌍), (2) 블록 4 — 약한 자기상관(MACD 또는 PSAR이
  포함된 6쌍; lag1이 음수, 연속 2 lag 유의).
- **중앙값과 최댓값이 모두 4**이므로 통일값 선택에 논란이 없다. 어떤 통일 방식(중앙값/
  최댓값)을 택해도 동일하게 4가 된다. 모든 쌍의 초기 자기상관 구조를 충분히 덮는다.

---

## 8. 결과 보고 형식

판정과 서술을 구분하여, 여러 증거를 **나란히 제시**한다(가중치 합산 점수 없음).

| 전략 | 점추정 Sharpe (연율화) | 쌍별 Sharpe 차이 95% CI | Holm 보정 후 유의 | (보조) Calmar / Sortino |
|------|----------------------|------------------------|------------------|------------------------|

- **점추정 Sharpe:** 각 전략의 전체 기간 Sharpe. 참고용 기술 통계 (main에서 계산).
  ※ "population SR"이 아니라 모두 sample SR이며, 부트스트랩이 그 불확실성을 추정한다.
- **차이 CI + Holm:** 실제 유의성 판정. (validation에서 계산)
- **판정 원칙:** "A의 Sharpe가 B보다 크다"만으로는 승리가 아니다. 오직 **차이의 CI가
  0을 포함하지 않을 때** 유의하다고 본다. 통계적 유의성과 효과 크기를 함께 본다.
- **"최고 전략"의 정의:** 다른 모든 전략을 유의하게 이긴 전략. 가중 합산 점수가 아님.
  그런 전략이 없으면 **"통계적으로 구분 불가"**가 정직하고 유효한 결론이다. 부분 순서가
  나오면 그대로 서술한다.
- **"종합적 판단" = 여러 증거를 나란히 펼쳐 보여주는 것**이지, 여러 지표를 하나의
  점수로 합산하는 것이 아니다(자의적 가중치 → 자의적 결론 회피).

### 시각화

통계 검증(주)과 별개로, 각 전략의 성과·분포를 보조적으로 시각화한다. 시각화 도구도
배운 과목 자료에 근거를 둔다:
- **전략별 일별 수익률 분포 — 히스토그램** (전략별 subplot). 현금(수익률=0)인 날을
  제외하고 실제 포지션을 잡은 날의 수익률만 그려, 분포 형태(fat tail)를 본다.
  출처: *Statistics 1 §2.2*(연속 변수 분포), *Data Science Week 1·2*(히스토그램으로 분포
  비교). 두 과목 모두 명시적으로 가르친 시각화.
- 박스플롯도 다중 그룹 분포 비교용으로 *Statistics 1 §2.3*에 있으나, 일별 수익률은 0 근처
  집중 + 다수 이상치(fat tail)로 박스가 눌려 해석이 어려워 히스토그램을 택했다.
- 시간축 선그래프(자산곡선)는 두 과목 모두 범위 밖이라 기본 산출물에서 제외.

---

## 9. 검정력과 거래 횟수

- 거래 횟수가 적으면 성과가 소수 거래에 좌우되어 추정이 불안정해지고 검정력이 약해진다.
  특히 신호가 드문 전략(예: Bollinger 2SD — 가격이 2 표준편차 밖으로 나가는 일이 드묾)에서
  문제가 될 수 있다.
- 대응: **고정 20년 기간**으로 충분한 거래 수를 확보(2005~2025).
- **파라미터를 비틀어 거래를 인위적으로 늘리지 않는다**(과적합). 거래가 적은 것은 그
  전략의 특성이다.
- 최소 거래 기준은 전략을 **제외하는 칼이 아니라**, 결론의 신뢰도를 표시하는 **라벨**로
  사용한다(기준 미달 전략도 검증에 포함하되 "검정력 부족"을 명시).
- 부트스트랩에 대한 깔끔한 "최소 거래 수 공식"은 존재하지 않는다. 통계의 표준적 최소
  표본 관례에 따라 **최소 거래 기준 = 30**을 사전 기준으로 삼는다. 검증 기간에 거래가
  30회 미만인 전략은 검증에 포함하되 결과에 **"검정력 부족"으로 라벨링**한다(제외하지 않음).

---

## 10. 사전등록 원칙 (Pre-registration)

- 모든 파라미터(전략 설정, 검증 절차, 데이터 기간, 최소 거래 기준)는 **결과를 보기 전에**
  확정한다.
- 데이터 기간·거래 횟수·성과를 본 뒤 설정을 바꾸지 않는다(researcher's degrees of
  freedom 차단).
- **in/out-of-sample 분리를 하지 않는다(전체 기간 사용).** 그 근거:
  - 본 프로젝트는 파라미터를 데이터 보기 전에 관례값으로 고정하고, 전략·검증 절차도 모두
    사전 확정하므로 **데이터 기반 조정이 없다.** 따라서 in/out 분리의 주 목적인
    "과적합 탐지"가 성립할 여지가 거의 없다.
  - 거래 표본이 제한적이라 검정력이 약한 상황에서, 데이터를 분리해 검정용 표본을 줄이면
    검정력이 더 떨어진다. 전체 기간을 사용해 검정력을 최대화한다.
  - "절차를 결과에 맞춰 조정하지 않았다"는 증거는, out-of-sample 봉인 대신 **본 사전등록
    문서(README·도출 과정 문서)가 결과 산출 전에 작성됨**으로 대신한다.
- 본 README와 도출 과정 문서는 결과 산출 전에 작성되어, 사전등록의 증거 역할을 한다.

---

## 11. 프로젝트 구조

```
systematic-trading-backtesting-framework/
├── data_loader.py         # yfinance + FRED rf → 표준화 (rf 연→일 변환, 기간 고정)
├── engine/
│   ├── backtest.py        # signal → position(shift) → (returns, excess)
│   └── metrics.py         # Sharpe(raw, ddof=0) / Calmar(raw) / Sortino(excess)
├── validation/
│   ├── acf.py             # ACF(numpy 직접 구현) → 블록 길이
│   ├── bootstrap.py       # moving block bootstrap, Sharpe 차이 CI + p-value
│   └── holm.py            # Holm 다중비교 보정 (p-value 기반)
├── strategies/
│   ├── helpers.py         # safe_divide, stateful_signal (공용)
│   ├── macd.py
│   ├── rsi.py
│   ├── bollinger_band.py
│   ├── stochastic.py
│   ├── psar.py
│   └── buy_and_hold.py    # 엔진 검증 전용 더미 (비교 대상 아님)
├── key.env                # FRED_API_KEY (gitignore, 커밋 안 함)
└── main.py                # 티커 입력 + 메뉴 (비교 / 지표 / 히스토그램 / 티커변경)
```

- **buy-and-hold는 엔진 검증 전용**이다. "매일 신호 1"을 엔진에 넣었을 때 단순 보유
  수익률과 정확히 일치하는지로 엔진을 검증한다. 5개 비교에는 포함하지 않는다.

---

## 12. 사전 확정 파라미터 (결과 보기 전 고정)

### 확정됨

| 파라미터 | 값 | 근거 |
|----------|-----|------|
| 부트스트랩 반복 횟수 (B) | **5,000** | CI를 안정적으로 추정하기에 충분히 크며, 계산 비용도 합리적. DS 과목이 가르친 1,000을 안정성을 위해 확장한 값. |
| 신뢰수준 | **95% (α = 0.05)** | 가짜 양성을 5%로 통제해 "엄밀함" 목적을 충족하면서, 제한된 거래 표본에서의 검정력을 보존(99%는 CI가 넓어져 이미 약한 검정력을 더 죽이고 Holm 보정과 겹쳐 과도하게 보수적; 90%는 가짜 양성 10%로 너무 느슨). 두 과목 자료가 모두 95% 기준으로 가르침(출처 일치). |
| 신뢰구간 방식 | **퍼센타일 (2.5 / 97.5 백분위)** | 5,000개 리샘플 차이 분포의 2.5%·97.5% 지점을 CI 양 끝으로 사용. DS 과목이 가르친 방식과 일치(출처 있음). 표본이 충분히 커 부트스트랩 분포가 대체로 대칭이라 BCa 대비 손실이 미미하며, 직관적이고 설명이 명확. |
| 시드 고정값 | **42** | 재현성을 위한 고정 시드. |
| 블록 길이 | **4 (통일)** | 10쌍 차이 시계열 ACF 블록 길이 분포가 min 1 / median 4 / max 4. 중앙값=최댓값=4라 통일값 선택에 논란 없음. (상세는 7절) |
| 티커 | **사용자 입력** | main 실행 시 입력받음. 프레임워크는 특정 종목에 묶이지 않는 범용 구조. |
| 데이터 기간 | **2005-01-01 ~ 2025-01-01 (고정 20년)** | 결과 보기 전 고정. 충분한 검정력 + 현대 시장 구조 반영. 시작·종료 모두 고정해 재실행 시 기간 불변. |
| in/out 분리 | **하지 않음 (전체 사용)** | 데이터 기반 조정이 없어 과적합 탐지 목적이 성립 안 함 + 약한 검정력을 위해 전체 사용. 절차 사전 고정은 본 문서로 증명. (근거는 10절) |
| 최소 거래 기준 | **30** | 통계의 표준적 최소 표본 관례. 미달 전략은 제외가 아니라 "검정력 부족" 라벨. (9절) |
| 거래비용 `cost_pct` | **파라미터 존재, 기본값 0 (단위 %)** | 비용 차감 인자를 두되 기본은 0(순수 신호 비교). 퍼센트 단위(예: 0.1 → 0.1%). 필요 시 값을 넣어 비용 영향 재실행 가능. (5절) |

> **신뢰수준 95% 선택 논리(상세):** 신뢰수준은 가짜 양성(없는 차이를 있다고 함)과
> 가짜 음성(있는 차이를 못 잡음) 사이의 trade-off다. 본 프로젝트는 (a) "통계적으로
> 정당하게 우위를 말한다"는 목적상 가짜 양성이 특히 치명적이고, (b) 동시에 거래 횟수가
> 적어 검정력이 이미 약하며, (c) Holm 보정이 별도로 엄격성을 더한다. 99%는 (b)·(c)와
> 겹쳐 거의 모든 비교를 "구분 불가"로 만들고, 90%는 (a)에 어긋난다. 95%가 세 제약
> 사이의 균형점이다.

### 남은 확인 항목 (구현 검증)

- numpy 직접 구현 ACF를 statsmodels와 1회 대조 — 현재 venv 미설치로 skip됨(선택적 검증).

---

## 13. 결과 (5개 티커 실행)

5개 티커(AAPL, MSFT, TSLA, QQQ, SPY)에 대해 전체 파이프라인을 실행했다. 검증 절차와
파라미터는 모두 이 실행 **이전에** 확정되었다(사전등록).

### 핵심 발견

**1. 전략 우열은 종목에 강하게 의존하며, 일반화되지 않는다.**
- **AAPL**에서는 MACD가 Sharpe 1.002로 가장 높았고, MACD가 RSI(보정 p=0.012)와
  Bollinger(보정 p=0.047)를 **유의하게** 이겼다. 단 Stochastic(0.106)·PSAR(0.557)은
  유의하게 이기지 못해, "모두를 이긴 단일 최고 전략"은 없는 **부분 순서**였다.
- **MSFT**에서는 순위가 뒤집혀 Bollinger가 최고(0.598), MACD가 최저(0.164)였다.
  AAPL에서 최고였던 MACD가 MSFT에서는 최하위 — 종목 의존성을 단적으로 보여준다.
- **MSFT·TSLA·QQQ·SPY** 네 종목은 Holm 보정 후 **모든 쌍이 통계적으로 구분 불가**
  (대부분 보정 p=1.000)였다.

**2. 점추정 차이 ≠ 통계적 유의성.**
- MSFT에서 Bollinger(0.598)는 MACD(0.164)보다 점추정 Sharpe가 3배 이상이었으나, 차이의
  신뢰구간이 0을 포함해 통계적으로는 구분 불가로 판정되었다. "더 높아 보이는 것"과
  "유의하게 높은 것"이 다름을 실증.

**3. 다중비교 보정의 효과.**
- 보정 전 개별로는 유의해 보일 수 있는 쌍들이 Holm 보정 후 대부분 비유의(p=1.000)로
  걸러졌다. AAPL의 2개 쌍만이 보정 후에도 유의성을 유지했다.

**4. 신호가 드문 전략의 검정력.**
- RSI는 모든 종목에서 거래 수가 가장 적었다(32~36회). 최소 거래 기준 30을 간신히 넘겨,
  검정력이 약한 편이며 이것이 RSI 관련 쌍 다수가 비유의로 나온 한 요인일 수 있다.

### 결론

엄밀한 검증(부트스트랩 CI + Holm 보정)을 적용하면, 흔히 쓰이는 5개 기술적 전략은 **대부분의
종목에서 통계적으로 구분되지 않으며, 우열이 나타나는 경우에도 종목에 따라 방향이 달라진다.**
이는 "어떤 전략이 더 낫다"는 통념이 통계적 엄밀성 아래에서는 잘 지지되지 않음을 시사한다.
본 프로젝트의 목적(비교의 통계적 정당성 확보)에 비추어, 이러한 "구분 불가" 결과 역시
유효하고 정직한 결론이다.

> 위 수치는 사전등록된 절차의 1회 실행 결과이며, 데이터 기간(2005~2025)·파라미터는
> 결과 산출 전에 고정되었다.

---

## 14. 검증 방법론 도출 과정

이 절은 검증 방법을 **어떻게 결정했는지의 과정**을 기록한다. 결과를 보기 전에 이 추론을
거쳤다는 사전등록 성격의 기록이다.

### 14.0 출발점 — 목표 재정의
- 전략 비교의 **주 기준은 Sharpe Ratio** 하나. Calmar·Sortino는 구현하되 보조이며, main
  메뉴에서 사용자가 선택해 본다.
- 일정 기간 Sharpe 단순 비교로는 기간에 따라 결과가 달라져 부족하다. **"통계적으로 높은
  신뢰도로 우위를 말할 수 있는" 검증 방법**이 필요하다.
- 검증 방법은 학부 과목 **Statistics 1**과 **Data Science** 자료 안에서 찾되, 각 과목
  자료가 정리된 별도 프로젝트에 동일 프롬프트를 던져 끌어냈다.

### 14.1 핵심 질문 — 수익률 비교 vs Sharpe 비교
- **수익률 차이 비교**는 "A가 더 많이 벌었나"만 본다(변동성 무시).
- **Sharpe 차이 비교**는 "위험 대비 더 잘했나"를 본다(분모에 변동성 포함).
- A가 평균 수익은 높지만 변동성도 크면, 수익률로는 "A 승"이지만 Sharpe로는 "B 승" 또는
  "차이 없음"이 될 수 있다 → **정반대 결론**. 위험 대비 성과가 기준이므로 Sharpe 차이를 본다.
- **통계적 난점:** Sharpe는 분자·분모가 모두 추정값인 **비선형 통계량**이라 평균 차이용
  t검정 공식이 안 맞는다. → 이것이 부트스트랩 선택의 핵심 이유.

### 14.2 두 과목에 던진 질문
데이터 성격 4가지(① paired/상관, ② 비정규 fat tail, ③ 시계열 비 i.i.d., ④ Sharpe라는
비선형 통계량)를 명시하고, 각 방법의 가정·위반 여부·paired 처리·시계열 주의점·교과서
위치를 물었다.

### 14.3 Statistics 1 결과
- **있음:** CI로 가설 판정(Sec 15.2.1), 단일표본 t/z검정 + CLT(Sec 15).
- **파생:** paired 차이 검정(단일표본 검정 + 정규 차이분포 Sec 6.1.1의 조합).
- **없음:** 부트스트랩(Sec 3의 "복원추출"은 유한모집단 표집이지 부트스트랩이 아님 — 혼동
  금지), 순열검정, 다중비교, 자기상관.
- **드러난 문제:** Stats 1 도구는 평균 차이는 검정해도 Sharpe 차이는 직접 못 한다.
  부트스트랩이 통째로 빠져 주 판정의 토대가 비었다 → DS 결과에 달림.

### 14.4 Data Science 결과
- **있음:** 부트스트랩(Week 2, 2/10 — "작은 데이터셋·비정규·어떤 통계량에도 적용 가능"
  명시), CI 판정(2/10·2/17), 단일·이표본 t/z검정·CLT·n≥30(2/17).
- **파생:** paired 차이 검정. **없음:** 순열검정, 다중비교, 자기상관.
- **해결:** Stats 1엔 없던 부트스트랩이 DS Week 2에 명확히 있고, 그 설명이 정확히 우리가
  쓰려는 이유(비정규·비선형 통계량)와 일치 → **본체가 다시 섬.**
- **두 과목의 수렴:** CI 판정 논리와 t/z검정은 양쪽 모두에 존재(가장 견고). DS의
  교차검증(paired t/z)이 Stats 1의 주 추천과 동일.

### 14.5 길 A vs 길 B 결정
두 과목 모두 자기상관·다중비교 보정은 범위 밖. 그러나 10쌍 비교에서 다중비교 보정은
사실상 필수다.
- **길 A:** 배운 범위만, 보정 없이 한계만 명시 → 가짜 양성 통제 못 함(구멍 큼).
- **길 B:** 본체는 배운 것, 보정만 외부에서 명시적으로 빌림 → 통계적으로 닫힘.
- **결정: 길 B.** 다중비교 보정의 구멍이 한계 명시로 덮기엔 너무 커서.

### 14.6 출처 확인
"배웠다"고 인용하려면 정확한 위치가 필요해, 양쪽에 출처 확인 프롬프트를 던졌다(지어내지
말 것 명시). 결과로 본체/파생/외부의 출처가 6절·부록 표대로 확정됐다. 특히 — DS는 지정
교과서가 없어 강의 날짜+Canvas 리딩으로, Stats 1은 Section 번호로 인용한다. Stats 1의
"복원추출"을 부트스트랩으로 인용하면 잘못된 인용이다.

### 14.7 검토했으나 채택하지 않은 대안
- **수익률 차이 비교:** 변동성 무시 → 주 기준 부적합(보조 대조용으론 가능).
- **개별 Sharpe CI 겹침으로 판정:** 통계적 오류(상관된 두 전략의 개별 CI는 부풀려짐).
  개별 CI는 서술용, 판정은 반드시 차이 CI로.
- **z-test / Lo의 모수적 Sharpe 검정:** 정규성 위반(자기상관 + fat tail) → 부트스트랩으로 대체.
- **Ljung-Box 등으로 방법 분기:** 자기상관 유무로 검정법을 바꾸지 않음. 부트스트랩은 항상
  쓰고, ACF는 블록 길이만 정함.
- **stationary block bootstrap (Politis–Romano):** 블록 길이를 기하분포로 무작위화하는
  정통 방식을 고려했으나, 구현 단순성·해석 용이성을 위해 **고정 길이 moving block**을 택함.
- **BCa CI:** 이론적으로 더 정확하나 과목 밖 + 표본이 커 대칭이라 이점 미미 + 복잡 →
  퍼센타일 채택.
- **가중 합산 종합 점수:** 가중치가 자의적 → 채택 안 함. 증거를 나란히 제시하고 판정은
  Sharpe 차이 CI로.

---

## 부록: 검증 방법 출처 요약표

| 방법 | 분류 | 출처 |
|------|------|------|
| 부트스트랩 (개념·절차·CI) | 본체 | Data Science, Week 2 (2/10) "Data Sampling"; Canvas 리딩 *Measurement and their Uncertainties* ch.1–2 |
| CI로 가설 판정 | 본체 | Statistics 1, Section 15.2.1; Data Science 2/10·2/17 |
| 단일표본 t/z검정, CLT, n≥30 | 본체 | Statistics 1, Section 15; Data Science 2/17 (Week 3); *Statistics in a Nutshell* ch.3 |
| paired 차이 검정 | 파생 | 위 단일표본 검정 + 차이 CI 판정의 조합 (전용 절 없음) |
| Sharpe에 부트스트랩 적용 | 파생 | 부트스트랩(DS Week 2)을 비선형 통계량에 적용 ("어떤 통계량에도 적용 가능" 명시에 근거) |
| Moving Block Bootstrap | 외부 | 두 과목 범위 밖. 자기상관 보정 위해 명시적 도입 (고정 블록 길이, circular wrap) |
| Holm 다중비교 보정 | 외부 | 두 과목 범위 밖. 부트스트랩 양측 p-value에 적용해 family-wise error 통제 |
| 히스토그램 (수익률 분포 시각화) | 본체 | Statistics 1 §2.2; Data Science Week 1·2 (분포 확인·비교) |

> **인용 정확성 주의:** Data Science 과목은 지정 교과서가 없으므로 강의 날짜/주차 + Canvas
> 리딩으로 인용한다. Statistics 1은 교과서 Section 번호로 인용한다. 페이지·슬라이드
> 번호는 최종 인용 전 PDF에서 직접 확인 권장.
