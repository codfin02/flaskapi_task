#!/bin/bash

# FastAPI 과제 프로젝트 통합 테스트 스크립트
# 사용법: ./test.sh [옵션]
# 옵션: --skip-format, --skip-lint, --skip-type, --skip-test

set -eo pipefail

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

log_warning() {
    echo -e "${COLOR_YELLOW}[WARNING]${COLOR_NC} $1"
}

log_error() {
    echo -e "${COLOR_RED}[ERROR]${COLOR_NC} $1"
}

# 옵션 파싱
SKIP_FORMAT=false
SKIP_LINT=false
SKIP_TYPE=false
SKIP_TEST=false

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
        --skip-type)
            SKIP_TYPE=true
            shift
            ;;
        --skip-test)
            SKIP_TEST=true
            shift
            ;;
        --help)
            echo "사용법: $0 [옵션]"
            echo "옵션:"
            echo "  --skip-format    코드 포맷팅 건너뛰기"
            echo "  --skip-lint      린팅 건너뛰기"
            echo "  --skip-type      타입 검사 건너뛰기"
            echo "  --skip-test      테스트 건너뛰기"
            echo "  --help           도움말 표시"
            exit 0
            ;;
        *)
            log_error "알 수 없는 옵션: $1"
            exit 1
            ;;
    esac
done

# Poetry 환경 확인
if ! command -v poetry &> /dev/null; then
    log_error "Poetry가 설치되어 있지 않습니다."
    exit 1
fi

# 프로젝트 디렉토리 확인
if [ ! -f "pyproject.toml" ]; then
    log_error "pyproject.toml 파일을 찾을 수 없습니다. 올바른 프로젝트 디렉토리에서 실행하세요."
    exit 1
fi

log_info "FastAPI 과제 프로젝트 테스트 시작..."

# 1. Black (코드 포맷팅)
if [ "$SKIP_FORMAT" = false ]; then
    log_info "Starting Black - 코드 포맷팅"
    if python3 -m poetry run black . --check; then
        log_success "Black 검사 통과"
    else
        log_info "코드 포맷팅 적용 중..."
        python3 -m poetry run black .
        log_success "Black 완료"
    fi
else
    log_warning "Black 건너뛰기"
fi

# 2. Ruff (린팅)
if [ "$SKIP_LINT" = false ]; then
    log_info "Starting Ruff - 코드 린팅"
    python3 -m poetry run ruff check --select I --fix
    python3 -m poetry run ruff check --fix
    log_success "Ruff 완료"
else
    log_warning "Ruff 건너뛰기"
fi

# 3. MyPy (타입 검사)
if [ "$SKIP_TYPE" = false ]; then
    log_info "Starting MyPy - 타입 검사"
    if python3 -m poetry run mypy .; then
        log_success "MyPy 완료"
    else
        log_error "타입 검사 실패"
        exit 1
    fi
else
    log_warning "MyPy 건너뛰기"
fi

# 4. Pytest + Coverage (테스트)
if [ "$SKIP_TEST" = false ]; then
    log_info "Starting Pytest with Coverage - 테스트 실행"
    python3 -m poetry run coverage run -m pytest . -v
    python3 -m poetry run coverage report -m
    python3 -m poetry run coverage html
    log_success "테스트 완료"
else
    log_warning "테스트 건너뛰기"
fi

# 5. 최종 결과
log_success "🎉 모든 테스트가 성공적으로 완료되었습니다!"
log_info "커버리지 리포트: htmlcov/index.html"

# 성공 시 종료 코드 0
exit 0 