# GitHub Actions 학습 노트

## 🎯 **학습 목표**
1. **GitHub Actions란 무엇인지 이해하고 어떻게 활용할 수 있는지 알고 있어야 한다.**
2. **GitHub Actions의 동작을 위한 스크립트 작성법을 이해하고 작성할 줄 알아야 한다.**
3. **GitHub Actions에서 Cache의 동작방식에 대해서 이해하고 이를 적용하여 어떤 이점을 가질 수 있는지 이해할 수 있어야 한다.**

## 📚 **GitHub Actions 기본 개념**

### **GitHub Actions란?**
- **정의**: GitHub에서 제공하는 CI/CD(Continuous Integration/Continuous Deployment) 플랫폼
- **용도**: 코드 자동 테스트, 빌드, 배포, 코드 품질 검사
- **장점**: GitHub 저장소와 완벽 통합, 무료 사용량 제공, 다양한 러너 지원

### **핵심 구성 요소**
- **Workflow**: 전체 CI/CD 파이프라인 정의
- **Job**: 독립적으로 실행되는 작업 단위
- **Step**: Job 내의 개별 실행 단계
- **Action**: 재사용 가능한 작업 단위
- **Runner**: Workflow를 실행하는 가상 환경

## 🚀 **GitHub Actions Workflow 작성법**

### **1. 기본 Workflow 구조**
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install poetry
        poetry install
        
    - name: Run tests
      run: |
        poetry run pytest
```

### **2. Poetry 환경 설정**
```yaml
- name: Install Poetry
  uses: snok/install-poetry@v1
  with:
    version: latest
    virtualenvs-create: true
    virtualenvs-in-project: true

- name: Load cached venv
  id: cached-poetry-dependencies
  uses: actions/cache@v3
  with:
    path: .venv
    key: venv-${{ runner.os }}-${{ steps.setup-python.outputs.python-version }}-${{ hashFiles('**/poetry.lock') }}

- name: Install dependencies
  if: steps.cached-poetry-dependencies.outputs.cache-hit != 'true'
  run: poetry install --no-interaction --no-root
```

### **3. Cache 활용 전략**
```yaml
- name: Cache pip dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

- name: Cache Poetry dependencies
  uses: actions/cache@v3
  with:
    path: .venv
    key: venv-${{ runner.os }}-${{ steps.setup-python.outputs.python-version }}-${{ hashFiles('**/poetry.lock') }}
    restore-keys: |
      venv-${{ runner.os }}-${{ steps.setup-python.outputs.python-version }}-
```

## 🔧 **FastAPI 프로젝트용 Workflow**

### **1. 코드 품질 검사 Workflow**
```yaml
name: Code Quality Check

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
        
    - name: Install Poetry
      uses: snok/install-poetry@v1
      with:
        version: latest
        virtualenvs-create: true
        virtualenvs-in-project: true
        
    - name: Cache Poetry dependencies
      uses: actions/cache@v3
      with:
        path: .venv
        key: venv-${{ runner.os }}-${{ steps.setup-python.outputs.python-version }}-${{ hashFiles('**/poetry.lock') }}
        
    - name: Install dependencies
      run: poetry install --no-interaction --no-root
      
    - name: Run Black
      run: poetry run black --check .
      
    - name: Run Ruff
      run: poetry run ruff check .
      
    - name: Run MyPy
      run: poetry run mypy .
```

### **2. 테스트 및 커버리지 Workflow**
```yaml
name: Test and Coverage

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
        
    - name: Install Poetry
      uses: snok/install-poetry@v1
      with:
        version: latest
        virtualenvs-create: true
        virtualenvs-in-project: true
        
    - name: Cache Poetry dependencies
      uses: actions/cache@v3
      with:
        path: .venv
        key: venv-${{ runner.os }}-${{ steps.setup-python.outputs.python-version }}-${{ hashFiles('**/poetry.lock') }}
        
    - name: Install dependencies
      run: poetry install --no-interaction --no-root
      
    - name: Run tests with coverage
      run: |
        poetry run coverage run -m pytest
        poetry run coverage report -m
        
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

### **3. 배포 Workflow**
```yaml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
        
    - name: Install Poetry
      uses: snok/install-poetry@v1
      with:
        version: latest
        
    - name: Install dependencies
      run: poetry install --no-interaction --no-root
      
    - name: Run tests
      run: poetry run pytest
      
    - name: Deploy to server
      run: |
        # 배포 스크립트 실행
        echo "Deploying version ${{ github.ref_name }}"
```

## 💡 **Cache 동작방식 및 이점**

### **Cache 동작 원리**
1. **키 생성**: 파일 해시, OS, Python 버전 등을 조합하여 고유 키 생성
2. **캐시 검색**: GitHub Actions가 저장된 캐시에서 키와 일치하는 항목 검색
3. **캐시 복원**: 일치하는 캐시가 있으면 복원, 없으면 새로 생성
4. **캐시 저장**: 작업 완료 후 새로운 캐시 저장

### **Cache 적용 이점**
- **빌드 시간 단축**: 의존성 설치 시간 대폭 감소
- **네트워크 사용량 감소**: 이미 다운로드된 패키지 재사용
- **비용 절약**: GitHub Actions 실행 시간 단축
- **개발자 경험 향상**: 빠른 피드백 루프

### **Cache 키 전략**
```yaml
# Poetry 의존성 캐시
- name: Cache Poetry dependencies
  uses: actions/cache@v3
  with:
    path: .venv
    key: venv-${{ runner.os }}-${{ steps.setup-python.outputs.python-version }}-${{ hashFiles('**/poetry.lock') }}
    restore-keys: |
      venv-${{ runner.os }}-${{ steps.setup-python.outputs.python-version }}-
      venv-${{ runner.os }}-

# pip 캐시
- name: Cache pip
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

## 🔗 **실제 프로젝트 적용**

### **프로젝트 구조**
```
.github/
└── workflows/
    ├── ci.yml          # 코드 품질 검사
    ├── test.yml        # 테스트 및 커버리지
    └── deploy.yml      # 배포
```

### **Workflow 파일 생성**
각 Workflow는 `.github/workflows/` 디렉토리에 YAML 파일로 저장됩니다.

## 📖 **참고 자료**
- [GitHub Actions 공식 문서](https://docs.github.com/en/actions)
- [GitHub Actions Examples](https://github.com/actions/starter-workflows)
- [Poetry GitHub Actions](https://python-poetry.org/docs/ci/)
- [Cache GitHub Actions](https://github.com/actions/cache)

## 🔗 **관련 파일**
- `.github/workflows/`: GitHub Actions Workflow 파일들
- `pyproject.toml`: Poetry 의존성 설정
- `test.sh`: 로컬 테스트 스크립트

---

*이 문서는 GitHub Actions 학습 과정을 정리한 노트입니다.* 