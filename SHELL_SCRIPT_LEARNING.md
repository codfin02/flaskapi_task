# Shell Script 학습 노트

## 🎯 **학습 목표**
1. **Shell script란 무엇인지 이해하고 간단한 shell script 작성법에 대해서 이해하고 작성할 줄 안다.**

## 📚 **Shell Script 기본 개념**

### **Shell Script란?**
- **정의**: Unix/Linux 시스템에서 명령어들을 순차적으로 실행할 수 있게 해주는 스크립트 언어
- **용도**: 반복적인 작업 자동화, 시스템 관리, CI/CD 파이프라인 구축
- **확장자**: `.sh` (관례적, 필수는 아님)

### **기본 구조**
```bash
#!/bin/bash
# Shebang: 스크립트 실행을 위한 인터프리터 지정

# 주석: 코드 설명
echo "Hello, World!"  # 명령어 실행
```

## 🚀 **고급 Shell Script 기능**

### **1. 에러 처리 및 안전성**
```bash
set -eo pipefail
# -e: 명령어 실패 시 즉시 종료
# -o pipefail: 파이프라인 중간 실패 시 종료
```

### **2. 색상 및 로깅**
```bash
# 색상 정의
COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[0;34m'
COLOR_NC='\033[0m' # No Color

# 로깅 함수
log_info() {
    echo -e "${COLOR_BLUE}[INFO]${COLOR_NC} $1"
}

log_success() {
    echo -e "${COLOR_GREEN}[SUCCESS]${COLOR_NC} $1"
}

log_error() {
    echo -e "${COLOR_RED}[ERROR]${COLOR_NC} $1"
}
```

### **3. 옵션 파싱**
```bash
# 옵션 변수 초기화
SKIP_FORMAT=false
SKIP_LINT=false

# 명령행 인수 파싱
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-format)
            SKIP_FORMAT=true
            shift
            ;;
        --skip-lint)
            SKIP_LINT=true
            shift
            ;;
        --help)
            echo "사용법: $0 [옵션]"
            exit 0
            ;;
        *)
            log_error "알 수 없는 옵션: $1"
            exit 1
            ;;
    esac
done
```

### **4. 조건문 및 제어 구조**
```bash
# Poetry 환경 확인
if ! command -v poetry &> /dev/null; then
    log_error "Poetry가 설치되어 있지 않습니다."
    exit 1
fi

# 프로젝트 디렉토리 확인
if [ ! -f "pyproject.toml" ]; then
    log_error "pyproject.toml 파일을 찾을 수 없습니다."
    exit 1
fi

# 조건부 실행
if [ "$SKIP_FORMAT" = false ]; then
    log_info "Starting Black - 코드 포맷팅"
    # Black 실행 코드
else
    log_warning "Black 건너뛰기"
fi
```

### **5. 함수 정의 및 모듈화**
```bash
# 함수 정의
run_black() {
    log_info "Starting Black - 코드 포맷팅"
    if python3 -m poetry run black . --check; then
        log_success "Black 검사 통과"
    else
        log_info "코드 포맷팅 적용 중..."
        python3 -m poetry run black .
        log_success "Black 완료"
    fi
}

run_ruff() {
    log_info "Starting Ruff - 코드 린팅"
    python3 -m poetry run ruff check --select I --fix
    python3 -m poetry run ruff check --fix
    log_success "Ruff 완료"
}

# 함수 호출
run_black
run_ruff
```

## 🔧 **실제 프로젝트 적용 예제**

### **test.sh 스크립트 분석**
```bash
#!/bin/bash

# FastAPI 과제 프로젝트 통합 테스트 스크립트
# 사용법: ./test.sh [옵션]
# 옵션: --skip-format, --skip-lint, --skip-type, --skip-test

set -eo pipefail  # 에러 처리 및 안전성

# 색상 정의 및 로깅 함수
# ... (색상 및 로깅 코드)

# 옵션 파싱
# ... (옵션 처리 코드)

# 환경 검증
# ... (Poetry, 프로젝트 디렉토리 확인)

# 단계별 실행
# 1. Black (코드 포맷팅)
# 2. Ruff (린팅)
# 3. MyPy (타입 검사)
# 4. Pytest + Coverage (테스트)

# 최종 결과
log_success "🎉 모든 테스트가 성공적으로 완료되었습니다!"
```

## 💡 **Shell Script 작성 팁**

### **1. 안전성**
- `set -eo pipefail` 사용으로 에러 시 즉시 종료
- 명령어 존재 여부 확인 (`command -v`)
- 파일/디렉토리 존재 여부 확인 (`[ -f file ]`, `[ -d dir ]`)

### **2. 사용자 경험**
- 색상과 로깅으로 가독성 향상
- 도움말 옵션 (`--help`) 제공
- 진행 상황 표시

### **3. 유지보수성**
- 함수로 기능 모듈화
- 명확한 변수명 사용
- 주석으로 코드 설명

### **4. 호환성**
- `#!/bin/bash` 사용 (POSIX sh 대신)
- 최신 bash 기능 활용
- Poetry 환경 통합

## 📖 **참고 자료**
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
- [Shell Script Best Practices](https://google.github.io/styleguide/shellguide.html)

## 🔗 **관련 파일**
- `test.sh`: 고급 기능이 적용된 통합 테스트 스크립트
- `FASTAPI_LEARNING_NOTES.md`: FastAPI 학습 노트

---

*이 문서는 Shell Script 학습 과정을 정리한 노트입니다.* 