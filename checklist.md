 #%%# 🚀 개발 전 준비 체크리스트

---

## ✅ 1. **Docker 컨테이너 확인 및 실행**

```bash
docker compose up --build
```

* 모든 서비스가 정상적으로 실행 중인지 확인합니다:

```bash
docker compose ps
```

* 정상 상태:

```
Name                  Command              State           Ports
----------------------------------------------------------------------
coinpilot-frontend    ...                  Up              0.0.0.0:3000->3000/tcp
coinpilot-backend     ...                  Up              0.0.0.0:8000->8000/tcp
coinpilot-airflow     ...                  Up              0.0.0.0:8080->8080/tcp
coinpilot-db          ...                  Up              5433/tcp
coinpilot-redis       ...                  Up              6379/tcp
```

---

## ✅ 2. **초기 개발용 서비스 접속 확인**

| 항목              | 주소                                                       | 확인할 것                             |
| --------------- | -------------------------------------------------------- | --------------------------------- |
| 🔗 SvelteKit    | [http://localhost:3000](http://localhost:3000)           | 기본 템플릿이 나오는지                      |
| 🔗 FastAPI Docs | [http://localhost:8000/docs](http://localhost:8000/docs) | FastAPI API 문서 표시되는지              |
| 🔗 Airflow      | [http://localhost:9000](http://localhost:8080)           | 로그인 화면 (기본 admin\:admin)          |
| 🔗 PostgreSQL   | localhost:5433                                           | `pgAdmin` 또는 `psql`로 접속 가능 여부     |
| 🔗 Redis        | localhost:6379                                           | `redis-cli` 또는 FastAPI 로그에서 연결 확인 |

---

## ✅ 3. **DB 초기 상태 점검**

PostgreSQL + TimescaleDB는 처음 실행 시 **DB, 유저, 테이블이 없기 때문에**, 다음 중 하나는 필수입니다:

### 방법 A. SQLAlchemy/FastAPI 코드에서 자동 생성

* `Base.metadata.create_all(bind=engine)` 사용 시 테이블 생성됨
* `alembic` 마이그레이션 도입은 추후 고려

### 방법 B. 직접 SQL로 테이블 생성

예: `user_settings`, `ohlcv_data`, `portfolio` 등

```sql
CREATE TABLE IF NOT EXISTS user_settings (
  id SERIAL PRIMARY KEY,
  user_id INT,
  default_timeframe TEXT,
  api_key TEXT,
  api_secret TEXT
);
```

---

## ✅ 4. **Redis 연결 테스트 (옵션)**

FastAPI 서버 코드에서 Redis 연결 로그 확인:

```python
import redis

r = redis.Redis.from_url("redis://redis:6379")
r.set("test", "hello")
print(r.get("test"))
```

→ 문제 없다면 로그에 `b'hello'` 표시됨

---

## ✅ 5. **Airflow 최초 초기화 작업**

Airflow는 최초에 메타데이터 DB를 초기화해야 합니다.
(일부는 Dockerfile이나 CMD에서 처리했을 수 있음)

```bash
docker compose exec airflow airflow db init
docker compose exec airflow airflow users create \
  --username admin --password admin --firstname admin \
  --lastname admin --role Admin --email admin@example.com
```

→ 이후 웹 UI에서 `http://localhost:8080` 접속, 로그인 확인

---

## ✅ 6. **SvelteKit + Tailwind 초기 구성 확인**

* `frontend/src/app.css`에 아래 코드가 있어야 합니다:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

* `tailwind.config.cjs`에 경로 설정 포함:

```js
content: ["./src/**/*.{html,js,svelte,ts}"],
```

* 실제 `/chart` 등 페이지에서 tailwind 스타일이 적용되는지 확인

---

## ✅ 7. **FastAPI 기본 라우트 확인**

* `backend/main.py` 예시:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "Backend working!"}
```

* [http://localhost:8000/](http://localhost:8000/) 접속 → `{ "msg": "Backend working!" }` 응답 확인

---

## ✅ 8. **Airflow DAG 인식 여부 테스트**

* `airflow/dags/init_dag.py`:

```python
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime

with DAG("init_dag", start_date=datetime(2023,1,1), schedule_interval="@daily", catchup=False) as dag:
    DummyOperator(task_id="start")
```

* Airflow UI에서 `init_dag` DAG이 표시되면 성공

---

## ✅ 정리된 체크리스트 요약

| 항목                                   | 상태 확인 |
| ------------------------------------ | ----- |
| 🔲 Docker 컨테이너 모두 정상 실행됨             |       |
| 🔲 웹 페이지, FastAPI, Airflow 정상 접속됨    |       |
| 🔲 PostgreSQL 접속 가능, 초기 테이블 생성 여부 확인 |       |
| 🔲 Redis 접속 확인 (`set`, `get` 작동)     |       |
| 🔲 Airflow 초기화 및 admin 계정 생성 완료      |       |
| 🔲 `/chart` 등 페이지 UI 기본 스타일 확인됨      |       |
| 🔲 `/` 또는 `/docs`에서 FastAPI 응답 확인됨   |       |
| 🔲 Airflow DAG 인식됨                   |       |

