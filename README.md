# FastAPI 과제 프로젝트

이 프로젝트는 FastAPI를 사용하여 사용자 관리 API를 구현한 과제입니다.

## 프로젝트 구조

```
fastapi_assignment/
│── app/
│   ├── models/          # 임시로 사용할 모델
│   │   ├── __init__.py
│   │   ├── users.py
│   ├── schemas/         # Pydantic 데이터 검증 모델
│   │   ├── __init__.py
│   │   ├── users.py
│   ├── tests/           # 테스트 코드
│   │   ├── __init__.py
│   │   ├── test_user_router.py
│   ├── __init__.py
├── main.py              # FastAPI 앱 실행 파일
├── conftest.py          # pytest 설정파일
├── test.sh              # black, ruff, mypy, coverage, pytest 통합 실행 shell script
├── pyproject.toml       # Poetry 의존성 관리
└── README.md            # 프로젝트 설명 파일
```

## 설치 및 실행

### 1. 의존성 설치
```bash
python3 -m poetry install
```

### 2. 서버 실행
```bash
python3 -m poetry run python main.py
```

### 3. 테스트 실행
```bash
./test.sh
```

## API 엔드포인트

- `POST /users` - 사용자 생성
- `GET /users` - 모든 사용자 조회
- `GET /users/{user_id}` - 특정 사용자 조회
- `PATCH /users/{user_id}` - 사용자 정보 수정
- `DELETE /users/{user_id}` - 사용자 삭제
- `GET /users/search` - 사용자 검색

## 개발 도구

- **FastAPI**: 웹 프레임워크
- **Pydantic**: 데이터 검증
- **Poetry**: 의존성 관리
- **pytest**: 테스트 프레임워크
- **black**: 코드 포맷터
- **ruff**: 린터
- **mypy**: 타입 체커
- **coverage**: 테스트 커버리지 