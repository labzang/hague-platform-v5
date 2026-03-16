# 🐳 Docker로 Labzang API 실행하기

## 개요
api.labzang.com을 Docker를 사용해서 localhost:8080에서 실행하는 방법입니다.

## 🚀 가장 간단한 실행 방법

### Windows:
```bash
cd api.labzang.com
docker-run.bat
```

### Linux/Mac:
```bash
cd api.labzang.com
chmod +x docker-run.sh
./docker-run.sh
```

## 📋 실행 방법 옵션

### 1. 단일 Docker 컨테이너 실행

#### 자동 스크립트 사용 (권장)
```bash
# Windows
docker-run.bat

# Linux/Mac
./docker-run.sh
```

#### 수동 명령어
```bash
# 이미지 빌드
docker build -t labzang-api:latest .

# 컨테이너 실행
docker run --name labzang-api -p 8080:8080 --rm labzang-api:latest
```

### 2. Docker Compose 사용

#### 자동 스크립트 사용
```bash
# Windows
docker-compose-run.bat

# Linux/Mac
./docker-compose-run.sh
```

#### 수동 명령어
```bash
# 서비스 시작
docker-compose -f docker-compose.simple.yml up --build

# 백그라운드 실행
docker-compose -f docker-compose.simple.yml up -d --build

# 서비스 중지
docker-compose -f docker-compose.simple.yml down
```

## 🔧 생성된 스크립트 파일들

| 파일명 | 설명 | 플랫폼 |
|--------|------|--------|
| `docker-run.sh` | Docker 단일 컨테이너 실행 | Linux/Mac |
| `docker-run.bat` | Docker 단일 컨테이너 실행 | Windows |
| `docker-compose-run.sh` | Docker Compose 실행 | Linux/Mac |
| `docker-compose-run.bat` | Docker Compose 실행 | Windows |
| `docker-compose.simple.yml` | 단순 실행용 Compose 파일 | 공통 |

## 🌐 접속 정보

애플리케이션이 시작되면 다음 URL에서 접속할 수 있습니다:

- **메인 URL**: api.labzang.com
- **API 상태 확인**: api.labzang.com/api/gateway/status
- **Swagger UI**: api.labzang.com/swagger-ui.html

## 📊 Docker 컨테이너 관리

### 컨테이너 상태 확인
```bash
# 실행 중인 컨테이너 확인
docker ps

# 모든 컨테이너 확인
docker ps -a
```

### 로그 확인
```bash
# 실시간 로그 확인
docker logs -f labzang-api

# 최근 로그 확인
docker logs --tail 100 labzang-api
```

### 컨테이너 중지/삭제
```bash
# 컨테이너 중지
docker stop labzang-api

# 컨테이너 삭제
docker rm labzang-api

# 이미지 삭제
docker rmi labzang-api:latest
```

## 🔍 헬스체크

Docker 컨테이너는 자동으로 헬스체크를 수행합니다:
- **체크 주기**: 30초마다
- **타임아웃**: 10초
- **재시도**: 3회
- **시작 대기**: 60초

헬스체크 상태 확인:
```bash
docker inspect --format='{{.State.Health.Status}}' labzang-api
```

## ⚠️ 주의사항

1. **Docker 설치 필요**: Docker Desktop 또는 Docker Engine이 설치되어 있어야 합니다.
2. **포트 충돌**: 8080 포트가 이미 사용 중이면 실행이 실패할 수 있습니다.
3. **메모리 사용량**: 컨테이너는 최대 512MB 메모리를 사용합니다.
4. **데이터베이스**: 현재는 외부 DB 없이 실행됩니다 (인메모리 또는 기본 설정).

## 🛠️ 트러블슈팅

### 포트 충돌 해결
```bash
# 8080 포트 사용 프로세스 확인
netstat -tulpn | grep :8080  # Linux/Mac
netstat -ano | findstr :8080  # Windows

# 다른 포트로 실행
docker run --name labzang-api -p 8081:8080 --rm labzang-api:latest
```

### 빌드 실패 시
```bash
# Docker 캐시 클리어 후 재빌드
docker build --no-cache -t labzang-api:latest .
```

### 컨테이너 강제 정리
```bash
# 모든 중지된 컨테이너 삭제
docker container prune

# 사용하지 않는 이미지 삭제
docker image prune
```
