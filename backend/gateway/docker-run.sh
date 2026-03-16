#!/bin/bash

# =============================================================================
# Labzang API Service - Docker 실행 스크립트 (Linux/Mac)
# =============================================================================

echo "🐳 Labzang API Service Docker 실행"
echo "포트: 8080"
echo "URL: api.labzang.com"
echo ""

# 현재 디렉토리 확인
if [ ! -f "Dockerfile" ]; then
    echo "❌ 오류: api.labzang.com 디렉토리에서 실행해주세요."
    exit 1
fi

# 기존 컨테이너 정리
echo "🧹 기존 컨테이너 정리 중..."
docker stop labzang-api 2>/dev/null || true
docker rm labzang-api 2>/dev/null || true

# Docker 이미지 빌드
echo "🔨 Docker 이미지 빌드 중..."
docker build -t labzang-api:latest .

if [ $? -ne 0 ]; then
    echo "❌ Docker 빌드 실패!"
    exit 1
fi

echo "✅ Docker 이미지 빌드 완료!"
echo ""

# Docker 컨테이너 실행
echo "🚀 Docker 컨테이너 실행 중..."
echo "컨테이너명: labzang-api"
echo "Ctrl+C로 종료할 수 있습니다."
echo ""

docker run --name labzang-api -p 8080:8080 --rm labzang-api:latest

echo ""
echo "✅ Docker 컨테이너가 종료되었습니다."
