## 📌 프로젝트 이름

**CoinPilot** – *“당신의 매매를 자동화된 전략과 분석으로 안내하는 트레이딩 조종석”*

---

## ✅ 프로젝트 구조 개요

| 구성 요소             | 사용 기술                            |
| ----------------- | -------------------------------- |
| **Frontend**      | SvelteKit, TailwindCSS, Chart.js |
| **Backend**       | FastAPI, SQLAlchemy, JWT         |
| **Database**      | PostgreSQL + TimescaleDB         |
| **Scheduler**     | Apache Airflow (DockerOperator)  |
| **Cache/Session** | Redis                            |
| **Infra/Dev**     | Docker Compose 기반 모듈식 설계         |


---

## 🧩 주요 기능 및 페이지 구성

### 1. 📈 차트 페이지

* 관심 종목 + 타임프레임 선택 (5m\~1d)
* DB에서 기본 데이터 로딩 → 누락된 부분은 Binance API에서 400봉 단위로 배치 요청
* 모든 타임프레임(5m, 15m, 1h, 4h, 1d)의 모든 이평선(25, 50, 100, 200, 400) 동시 표시
* 로딩/대기 시 progress spinner

---

### 2. 📊 수익률 근황 페이지

* Binance/OKX API 연동 → 실현/미실현 수익률 수집
* PnL 유형별(Realized/Unrealized) 토글
* 날짜별/종목별 PnL 차트 (막대, 선형)
* 전략별 수익률 비교도 가능하게 설계 예정

---

### 3. 🧠 학습 데이터 생성 페이지

* 차트 클릭 → (심볼, timeframe, 시점) row 생성
* 테이블 형태로 목록 표시, row 제거 기능
* "학습데이터 추출" 클릭 시 → 해당 시점 기준 400봉 데이터를 DB에서 불러와 저장
* 추출된 데이터는 추후 모델 학습/분석용으로 사용

---

### 4. 💼 포트폴리오 + 전략 체크포인트 페이지

* 매매 전략 선택 + 전략별 checkpoint 설명 노출
* 메모 입력 + limit/market 가격 설정 → 매수 버튼
* 평균가 기준 -5% stop-loss 자동 등록
* 현재 분할 매수 진행상황 표시
* Swing/단타 구분 가능
* 매매일지 자동 생성 및 상태 표시

---

### 5. 🏆 상대강도 분석 페이지

* 각 타임프레임 기준 normalized 수익률 기반 랭킹 테이블
* 예: 최근 1일 상승률, 최근 3일 누적 수익률, 거래량 변화율 등
* 다중 기준 랭킹 → 최종 조합 점수 산정 → 메인 랭킹 테이블 표시

---

### 6. ⚙️ 설정 / 관리자 페이지

* Binance, OKX API Key 입력 및 유효성 테스트
* DB 연결 endpoint 설정
* 관심 종목 관리 (추가/삭제)
* 타임존 설정, 데이터 초기화 옵션

---

## ⚙️ 시스템 아키텍처 (요약)

```text
[SvelteKit Frontend]
      ↓ REST API + JWT
[FastAPI Backend] ────────────────┐
  ├─ DB 연결 (PostgreSQL + Timescale)
  ├─ Redis 연결 (세션, 캐시)
  └─ API 인증/요청 처리

[Airflow Scheduler]
  ├─ DAG 1: OHLCV 수집 (DockerOperator)
  ├─ DAG 2: 학습 데이터 추출
  └─ DAG 3: 전략 트리거
         ↓
   [Binance / OKX API]

[Redis] ⇄ [FastAPI]
   ↕       ↕
 JWT, session, 전략상태, 필터, 비동기 처리 캐시

[PostgreSQL + TimescaleDB]
   ↑
 트레이딩 기록, OHLCV, 학습데이터, 설정 저장
```


---

## 🛠 개발 환경 구성 요약

| 항목        | 구성                                                 |
| --------- | -------------------------------------------------- |
| 웹 앱 프레임워크 | SvelteKit + TailwindCSS                            |
| API 서버    | FastAPI + Uvicorn                                  |
| 시계열 DB    | PostgreSQL 15 + TimescaleDB 확장                     |
| 스케줄러      | Airflow (DockerOperator, PythonOperator)           |
| 로컬 개발 환경  | Docker Compose 기반 통합 실행                            |
| 이미지 관리    | collector, learner, trainer 등 기능별 Dockerfile 분리 빌드 |

---

## ✨ 향후 확장 고려사항

* WebSocket 실시간 가격 연동
* 전략별 백테스트 및 리포트 시각화 페이지
* Telegram 알림 연동
* 사용자별 설정 저장 (SQLite/Redis 세션 관리 or 사용자별 DB)

---

## 🧩 Redis를 활용하는 실제 시나리오 요약

|사용 목적|예시 키|설명|
|---|---|---|
|**세션 저장**|`session:<user_id>`|JWT, 로그인 유효 상태 유지|
|**전략 캐시**|`strategy_cache:BTCUSDT`|전략 체크포인트 임시 상태 유지|
|**필터/차트 옵션 캐시**|`ui:filters:<user_id>`|UI 전환 중 데이터 빠르게 로딩|
|**Airflow DAG 상태**|`task:<dag_id>`|상태/로그 추적 (선택사항)|

---
