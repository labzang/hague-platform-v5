@echo off
REM =============================================================================
REM Labzang API Service - Docker Compose 실행 스크립트 (Windows)
REM =============================================================================

echo 🐳 Labzang API Service Docker Compose 실행
echo 포트: 8080
echo URL: api.labzang.com
echo.

REM 현재 디렉토리 확인
if not exist "docker-compose.simple.yml" (
    echo ❌ 오류: api.labzang.com 디렉토리에서 실행해주세요.
    pause
    exit /b 1
)

REM 기존 컨테이너 정리
echo 🧹 기존 컨테이너 정리 중...
docker-compose -f docker-compose.simple.yml down >nul 2>&1

REM Docker Compose로 실행
echo 🚀 Docker Compose로 서비스 시작 중...
echo Ctrl+C로 종료할 수 있습니다.
echo.

REM 포그라운드에서 실행 (로그 확인 가능)
docker-compose -f docker-compose.simple.yml up --build

echo.
echo ✅ Docker Compose 서비스가 종료되었습니다.
pause
