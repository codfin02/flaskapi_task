# FastAPI 정리 - 학습 노트

## 🎯 **학습 목표 달성 현황**

### ✅ **완료된 목표**
1. **FastAPI 공식 문서를 활용하여 학습하는 방법을 배웁니다.**
   - ✅ 프로젝트 구성 및 의존성 관리
   - ✅ API 엔드포인트 작성법
   - ✅ FastAPI 애플리케이션 구조

2. **FastAPI에서 Pydantic Model을 활용하여 데이터를 검증하는 방법을 배웁니다.**
   - ✅ `UserCreateRequest`, `UserUpdateRequest`, `UserResponse` 스키마
   - ✅ 데이터 타입 검증 및 직렬화
   - ✅ `conint(gt=0)` 같은 고급 검증

3. **FastAPI에서 경로 매개변수를 사용하여 route를 작성하는 방법을 배웁니다.**
   - ✅ `@app.get("/users/{user_id}")` - 동적 경로
   - ✅ `@app.patch("/users/{user_id}")` - 리소스 수정
   - ✅ `@app.delete("/users/{user_id}")` - 리소스 삭제

4. **FastAPI에서 경로 매개변수를 검증하는 방법을 배웁니다.**
   - ✅ `user_id: int = Path(gt=0)` - 양수 검증
   - ✅ `Path` 객체를 통한 매개변수 제약 조건

5. **FastAPI에서 쿼리 매개변수를 사용하여 route를 작성하는 방법을 배웁니다.**
   - ✅ `@app.get("/users/search")` - 검색 API
   - ✅ 단순 쿼리 파라미터 처리

6. **FastAPI에서 Pydantic 모델과 Query 객체를 사용하여 쿼리 매개변수를 검증하는 방법을 배웁니다.**
   - ✅ `UserSearchParams` + `Annotated[UserSearchParams, Query()]`
   - ✅ `model_config = {"extra": "forbid"}` - 추가 필드 금지
   - ✅ `conint(gt=0)` - 고급 타입 검증

### 🔄 **진행 중인 목표**
1. **Shell script 이해 및 작성법**
   - 🔄 고급 shell script 작성 (옵션 처리, 에러 핸들링, 로깅)
   - 🔄 Poetry 환경 통합

2. **GitHub Actions 이해 및 활용**
   - 🔄 CI/CD 파이프라인 구축
   - 🔄 자동화된 테스트 및 배포

3. **GitHub Actions Cache 동작방식 및 이점**
   - 🔄 의존성 캐싱 전략
   - 🔄 빌드 시간 단축

4. **Spec API 이해 및 활용**
   - 🔄 OpenAPI 스펙 생성
   - 🔄 API 문서화

5. **FastAPI 내부 모듈/함수를 이용한 라우터 구성**
   - 🔄 APIRouter 활용
   - 🔄 모듈화된 구조

## 📖 **학습 자료 및 참고 문서**

### **FastAPI 공식 문서**
- [FastAPI 공식 튜토리얼](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic 문서](https://docs.pydantic.dev/)
- [Path 매개변수](https://fastapi.tiangolo.com/tutorial/path-params/)
- [Query 매개변수](https://fastapi.tiangolo.com/tutorial/query-params/)

### **실습 예제**
```python
# 경로 매개변수 검증 예제
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int = Path(gt=0)) -> UserModel:
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    return user

# Pydantic 모델 + Query 객체 검증 예제
@app.get("/users/search", response_model=List[UserResponse])
async def search_users(query_params: Annotated[UserSearchParams, Query()]) -> List[UserModel]:
    valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
    filtered_users = UserModel.filter(**valid_query)
    if not filtered_users:
        raise HTTPException(status_code=404)
    return filtered_users
```

## 🚀 **프로젝트 구조 및 특징**

### **TDD 방식 개발**
- 테스트 코드 우선 작성
- 테스트 통과를 위한 API 구현
- 99% 테스트 커버리지 달성

### **코드 품질 관리**
- **Black**: 코드 포맷팅
- **Ruff**: 린팅 및 코드 품질 검사
- **MyPy**: 타입 검증
- **Coverage**: 테스트 커버리지 측정

### **의존성 관리**
- **Poetry**: 가상환경 및 패키지 관리
- **Python 3.12+**: 최신 Python 기능 활용

## 📅 **학습 일정 및 진행 상황**

| 날짜 | 학습 내용 | 완료 여부 | 비고 |
|------|-----------|-----------|------|
| 2025-01-XX | FastAPI 기본 구조 및 API 작성 | ✅ | CRUD API 구현 완료 |
| 2025-01-XX | Pydantic 모델 및 데이터 검증 | ✅ | 스키마 정의 완료 |
| 2025-01-XX | 경로/쿼리 매개변수 검증 | ✅ | Path, Query 객체 활용 |
| 2025-01-XX | Shell script 고급 기능 | 🔄 | 옵션 처리, 로깅 추가 |
| 2025-01-XX | GitHub Actions CI/CD | 🔄 | 워크플로우 구축 예정 |
| 2025-01-XX | Spec API 및 문서화 | 🔄 | OpenAPI 스펙 생성 예정 |

## 💡 **학습 팁 및 주의사항**

### **경로 매개변수 순서 주의**
```python
# 올바른 순서: 구체적인 경로가 먼저
@app.get("/users/search")  # 먼저 정의
@app.get("/users/{user_id}")  # 나중에 정의

# 잘못된 순서: 동적 경로가 먼저면 /users/search가 /users/{user_id}로 인식됨
@app.get("/users/{user_id}")  # 먼저 정의하면 문제 발생
@app.get("/users/search")  # 이 경로가 제대로 동작하지 않음
```

### **Pydantic 모델 검증**
```python
class UserSearchParams(BaseModel):
    model_config = {"extra": "forbid"}  # 추가 필드 금지
    
    username: Optional[str] = None
    age: Optional[Annotated[int, conint(gt=0)]] = None  # 고급 검증
    gender: Optional[GenderEnum] = None
```

### **에러 처리 패턴**
```python
# 404 에러: 리소스 없음
if user is None:
    raise HTTPException(status_code=404)

# 422 에러: 데이터 검증 실패
if age is not None and age <= 0:
    raise HTTPException(status_code=422, detail="Age must be greater than 0")
```

## 🔗 **관련 링크**
- [GitHub 저장소](https://github.com/codfin02/flaskapi_task)
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Pydantic 공식 문서](https://docs.pydantic.dev/)
- [Python Poetry 문서](https://python-poetry.org/docs/)

---

*이 문서는 FastAPI 학습 과정을 정리한 노트입니다. 지속적으로 업데이트됩니다.* 