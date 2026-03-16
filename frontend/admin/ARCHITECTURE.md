# 프로젝트 아키텍처 및 플로우

## 목차
1. [전체 아키텍처](#전체-아키텍처)
2. [IIFE 패턴 구조](#iife-패턴-구조)
3. [레이어 구조](#레이어-구조)
4. [플로우 다이어그램](#플로우-다이어그램)
5. [코드 전략](#코드-전략)
6. [확장 가이드](#확장-가이드)

---

## 전체 아키텍처

### 시스템 구성

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                   │
├─────────────────────────────────────────────────────────┤
│  app/page.tsx                                            │
│  ├─ 소셜 로그인 버튼 (구글, 카카오, 네이버)                │
│  ├─ 이메일/비밀번호 로그인 폼                             │
│  └─ createSocialLoginHandlers 사용                       │
├─────────────────────────────────────────────────────────┤
│  service/mainservice.ts (IIFE 패턴)                     │
│  ├─ Private: gatewayUrl, handleLogin, handleEmailLogin  │
│  └─ Public: 팩토리 함수 (핸들러 생성)                     │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                  Backend (Spring Gateway)                │
├─────────────────────────────────────────────────────────┤
│  /auth/google/login  → 구글 OAuth URL 반환               │
│  /auth/kakao/login   → 카카오 OAuth URL 반환             │
│  /auth/naver/login   → 네이버 OAuth URL 반환             │
│  /api/auth/login     → 이메일/비밀번호 로그인             │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│              OAuth Providers / User Service              │
├─────────────────────────────────────────────────────────┤
│  Google OAuth2                                           │
│  Kakao OAuth2                                            │
│  Naver OAuth2                                            │
│  User Service (인증 처리)                                 │
└─────────────────────────────────────────────────────────┘
```

---

## IIFE 패턴 구조

### 코드 구조

```typescript
export const createSocialLoginHandlers = (() => {
    // ┌─────────────────────────────────────────┐
    // │  IIFE 내부 (Private 스코프)              │
    // └─────────────────────────────────────────┘
    
    // 1. 공통 설정 (Private)
    const gatewayUrl = process.env.NEXT_PUBLIC_GATEWAY_URL || 'api.labzang.com';
    
    // 2. Private 헬퍼 함수들
    async function handleLogin(provider, setIsLoading, setError) {
        // 소셜 로그인 공통 로직
    }
    
    async function handleEmailLogin(email, password, setIsLoading, setError, onSuccess) {
        // 이메일 로그인 로직
    }
    
    // ┌─────────────────────────────────────────┐
    // │  Public API (팩토리 함수)                │
    // └─────────────────────────────────────────┘
    
    return (setters...) => {
        // 3. 이너 함수들 (함수 선언식)
        function handleGoogleLogin() {
            handleLogin('google', setIsGoogleLoading, setError);
        }
        
        function handleKakaoLogin() {
            handleLogin('kakao', setIsKakaoLoading, setError);
        }
        
        function handleNaverLogin() {
            handleLogin('naver', setIsNaverLoading, setError);
        }
        
        function handleEmailPasswordLogin(email, password, onSuccess) {
            handleEmailLogin(email, password, setIsLoading, setError, onSuccess);
        }
        
        // 4. 핸들러 객체 반환
        return {
            handleGoogleLogin,
            handleKakaoLogin,
            handleNaverLogin,
            handleEmailPasswordLogin,
        };
    };
})(); // 즉시 실행
```

### IIFE 패턴의 장점

1. **캡슐화**: Private 변수와 함수가 외부에서 접근 불가
2. **네임스페이스 보호**: 전역 스코프 오염 방지
3. **클로저 활용**: Private 변수를 이너 함수에서 접근
4. **싱글톤 패턴**: 한 번만 실행되어 설정 공유

---

## 레이어 구조

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: IIFE Private 스코프                            │
├─────────────────────────────────────────────────────────┤
│  ├─ gatewayUrl (공통 설정)                               │
│  │   └─ 모든 API 호출에서 사용                           │
│  │                                                        │
│  ├─ handleLogin (소셜 로그인 공통 로직)                   │
│  │   ├─ provider 파라미터로 구글/카카오/네이버 구분       │
│  │   ├─ POST /auth/{provider}/login                     │
│  │   ├─ authUrl 받아서 리다이렉트                        │
│  │   └─ 에러 처리 및 로딩 상태 관리                       │
│  │                                                        │
│  └─ handleEmailLogin (이메일 로그인 로직)                 │
│      ├─ POST /api/auth/login                            │
│      ├─ 성공 시 onSuccess 콜백 실행                      │
│      └─ 에러 처리 및 로딩 상태 관리                       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 2: 팩토리 함수 (Public API)                       │
├─────────────────────────────────────────────────────────┤
│  └─ (setters...) => { ... }                             │
│      ├─ 컴포넌트의 state setter를 파라미터로 받음         │
│      └─ 핸들러 객체 생성 및 반환                          │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 3: 이너 함수들 (함수 선언식)                       │
├─────────────────────────────────────────────────────────┤
│  ├─ handleGoogleLogin()                                 │
│  │   └─ handleLogin('google', ...) 호출                 │
│  │                                                        │
│  ├─ handleKakaoLogin()                                  │
│  │   └─ handleLogin('kakao', ...) 호출                  │
│  │                                                        │
│  ├─ handleNaverLogin()                                  │
│  │   └─ handleLogin('naver', ...) 호출                  │
│  │                                                        │
│  └─ handleEmailPasswordLogin(email, password, onSuccess)│
│      └─ handleEmailLogin(...) 호출                       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 4: 컴포넌트 (app/page.tsx)                       │
├─────────────────────────────────────────────────────────┤
│  └─ useMemo로 핸들러 생성                                │
│      └─ 버튼 onClick에 핸들러 연결                        │
└─────────────────────────────────────────────────────────┘
```

---

## 플로우 다이어그램

### 1. 소셜 로그인 플로우 (구글 예시)

```
┌─────────────────────────────────────────────────────────┐
│  1. 사용자 액션                                           │
└─────────────────────────────────────────────────────────┘
                            ↓
              사용자가 "구글로 시작하기" 버튼 클릭
                            ↓
┌─────────────────────────────────────────────────────────┐
│  2. 컴포넌트 (app/page.tsx)                              │
├─────────────────────────────────────────────────────────┤
│  onClick={onGoogleLogin}                                │
│  └─ onGoogleLogin = handleGoogleLogin (from service)    │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  3. 이너 함수 실행 (service/mainservice.ts)              │
├─────────────────────────────────────────────────────────┤
│  function handleGoogleLogin() {                         │
│      handleLogin('google', setIsGoogleLoading, setError)│
│  }                                                       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  4. Private 헬퍼 함수 실행                                │
├─────────────────────────────────────────────────────────┤
│  async function handleLogin(provider, ...) {            │
│      setIsGoogleLoading(true)  // 로딩 시작              │
│      setError('')              // 에러 초기화            │
│                                                          │
│      const response = await fetch(                      │
│          `${gatewayUrl}/auth/google/login`,            │
│          { method: 'POST', ... }                        │
│      )                                                   │
│  }                                                       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  5. Backend API 호출                                     │
├─────────────────────────────────────────────────────────┤
│  POST api.labzang.com/auth/google/login          │
│                                                          │
│  Response:                                               │
│  {                                                       │
│      "success": true,                                   │
│      "message": "구글 로그인 URL 생성 성공",              │
│      "authUrl": "https://accounts.google.com/..."      │
│  }                                                       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  6. 응답 처리 및 리다이렉트                               │
├─────────────────────────────────────────────────────────┤
│  if (data.success && data.authUrl) {                    │
│      window.location.href = data.authUrl;  // 구글로 이동│
│  } else {                                                │
│      setError('구글 로그인 URL을 받아올 수 없습니다.')     │
│      setIsGoogleLoading(false)                          │
│  }                                                       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  7. 구글 OAuth 페이지                                    │
├─────────────────────────────────────────────────────────┤
│  사용자가 구글 계정으로 로그인                            │
│  └─ 권한 승인                                            │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  8. Callback 처리 (Backend)                              │
├─────────────────────────────────────────────────────────┤
│  Backend가 구글로부터 인증 코드 받음                      │
│  └─ 토큰 생성 및 /dashboard?token=xxx 로 리다이렉트      │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  9. Dashboard 페이지                                     │
├─────────────────────────────────────────────────────────┤
│  app/dashboard/page.tsx                                 │
│  ├─ URL에서 token 추출                                   │
│  ├─ localStorage에 저장                                  │
│  ├─ 사용자 정보 조회                                      │
│  └─ 로그인 성공 화면 표시                                 │
└─────────────────────────────────────────────────────────┘
```

### 2. 이메일/비밀번호 로그인 플로우

```
┌─────────────────────────────────────────────────────────┐
│  1. 사용자 액션                                           │
└─────────────────────────────────────────────────────────┘
                            ↓
          사용자가 이메일/비밀번호 입력 후 "로그인" 버튼 클릭
                            ↓
┌─────────────────────────────────────────────────────────┐
│  2. 컴포넌트 (app/page.tsx)                              │
├─────────────────────────────────────────────────────────┤
│  const handleSubmit = (e) => {                          │
│      e.preventDefault();                                │
│      handleEmailPasswordLogin(                          │
│          email,                                         │
│          password,                                      │
│          () => router.push('/dashboard')               │
│      );                                                 │
│  }                                                       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  3. 이너 함수 실행 (service/mainservice.ts)              │
├─────────────────────────────────────────────────────────┤
│  function handleEmailPasswordLogin(email, password, ...) │
│      handleEmailLogin(email, password, ...)             │
│  }                                                       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  4. Private 헬퍼 함수 실행                                │
├─────────────────────────────────────────────────────────┤
│  async function handleEmailLogin(...) {                 │
│      setIsLoading(true)                                 │
│      setError('')                                       │
│                                                          │
│      const response = await fetch(                      │
│          `${gatewayUrl}/api/auth/login`,               │
│          {                                              │
│              method: 'POST',                            │
│              body: JSON.stringify({ email, password }) │
│          }                                              │
│      )                                                   │
│  }                                                       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  5. Backend API 호출                                     │
├─────────────────────────────────────────────────────────┤
│  POST api.labzang.com/api/auth/login             │
│                                                          │
│  Request Body:                                           │
│  {                                                       │
│      "email": "user@example.com",                       │
│      "password": "password123"                          │
│  }                                                       │
│                                                          │
│  Response:                                               │
│  - 성공: 200 OK (쿠키에 세션 저장)                        │
│  - 실패: 401 Unauthorized                                │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  6. 응답 처리                                             │
├─────────────────────────────────────────────────────────┤
│  if (response.ok) {                                      │
│      onSuccess()  // router.push('/dashboard') 실행      │
│  } else {                                                │
│      const data = await response.json()                 │
│      setError(data.message || '로그인에 실패했습니다.')    │
│  }                                                       │
│  setIsLoading(false)                                    │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  7. Dashboard 페이지로 이동                               │
└─────────────────────────────────────────────────────────┘
```

---

## 코드 전략

### 1. 클로저 활용

**Private 변수를 클로저로 캡처:**

```typescript
const gatewayUrl = 'api.labzang.com'; // Private

return (setters) => {
    function handleGoogleLogin() {
        // gatewayUrl 접근 가능 (클로저)
        fetch(`${gatewayUrl}/auth/google/login`);
    }
};
```

**장점:**
- `gatewayUrl`을 한 번만 정의
- 모든 핸들러가 공유
- 외부에서 변경 불가

### 2. 공통 로직 추출

**중복 제거:**

```typescript
// ❌ Before: 중복 코드
function handleGoogleLogin() {
    setIsLoading(true);
    fetch('/auth/google/login');
    // ... 동일한 로직 반복
}

function handleKakaoLogin() {
    setIsLoading(true);
    fetch('/auth/kakao/login');
    // ... 동일한 로직 반복
}

// ✅ After: 공통 로직 추출
function handleLogin(provider, setIsLoading, setError) {
    setIsLoading(true);
    fetch(`/auth/${provider}/login`);
    // ... 공통 로직
}

function handleGoogleLogin() {
    handleLogin('google', setIsGoogleLoading, setError);
}

function handleKakaoLogin() {
    handleLogin('kakao', setIsKakaoLoading, setError);
}
```

### 3. 함수 선언식 사용

**이너 함수는 함수 선언식:**

```typescript
// ✅ 함수 선언식
function handleGoogleLogin() {
    handleLogin('google', ...);
}

// ❌ 화살표 함수 (람다)
const handleGoogleLogin = () => {
    handleLogin('google', ...);
};
```

**함수 선언식의 장점:**
- 호이스팅으로 순서에 덜 민감
- 스택 트레이스에 함수 이름 표시
- 디버깅 용이

### 4. 의존성 주입 패턴

**팩토리 함수로 setter 주입:**

```typescript
// 컴포넌트에서 setter를 주입
const handlers = createSocialLoginHandlers(
    setIsGoogleLoading,
    setIsKakaoLoading,
    setIsNaverLoading,
    setIsLoading,
    setError
);

// 핸들러는 주입받은 setter 사용
function handleGoogleLogin() {
    setIsGoogleLoading(true);  // 주입받은 setter
}
```

**장점:**
- 컴포넌트 state와 분리
- 테스트 시 mock setter 주입 가능
- 재사용성 향상

### 5. useMemo로 최적화

**불필요한 재생성 방지:**

```typescript
const handlers = useMemo(
    () => createSocialLoginHandlers(setters...),
    [setters...]  // setter가 변경될 때만 재생성
);
```

---

## 확장 가이드

### 새로운 소셜 로그인 추가 (예: GitHub)

#### 1. Backend API 엔드포인트 추가
```
POST /auth/github/login
```

#### 2. mainservice.ts 수정

```typescript
// 1. handleLogin 함수의 provider 타입에 추가
async function handleLogin(
    provider: 'google' | 'kakao' | 'naver' | 'github',  // 'github' 추가
    setIsLoading: (loading: boolean) => void,
    setError: (error: string) => void
) {
    // ... 기존 로직 (수정 불필요)
}

// 2. 팩토리 함수 파라미터에 setter 추가
return (
    setIsGoogleLoading: (loading: boolean) => void,
    setIsKakaoLoading: (loading: boolean) => void,
    setIsNaverLoading: (loading: boolean) => void,
    setIsGithubLoading: (loading: boolean) => void,  // 추가
    setIsLoading: (loading: boolean) => void,
    setError: (error: string) => void
) => {
    // ... 기존 핸들러들
    
    // 3. 새로운 핸들러 추가
    function handleGithubLogin() {
        handleLogin('github', setIsGithubLoading, setError);
    }
    
    // 4. return 객체에 추가
    return {
        handleGoogleLogin,
        handleKakaoLogin,
        handleNaverLogin,
        handleGithubLogin,  // 추가
        handleEmailPasswordLogin,
    };
};
```

#### 3. 컴포넌트 수정 (app/page.tsx)

```typescript
// 1. state 추가
const [isGithubLoading, setIsGithubLoading] = useState(false);

// 2. 핸들러 생성 시 setter 전달
const { 
    handleGoogleLogin: onGoogleLogin,
    handleKakaoLogin: onKakaoLogin,
    handleNaverLogin: onNaverLogin,
    handleGithubLogin: onGithubLogin,  // 추가
    handleEmailPasswordLogin 
} = useMemo(
    () => createSocialLoginHandlers(
        setIsGoogleLoading,
        setIsKakaoLoading,
        setIsNaverLoading,
        setIsGithubLoading,  // 추가
        setIsLoading,
        setError
    ),
    [setIsGoogleLoading, setIsKakaoLoading, setIsNaverLoading, setIsGithubLoading, setIsLoading, setError]
);

// 3. 버튼 추가
<button onClick={onGithubLogin} disabled={isGithubLoading || ...}>
    GitHub로 시작하기
</button>
```

### 새로운 로그인 방식 추가 (예: 전화번호 인증)

#### 1. mainservice.ts에 헬퍼 함수 추가

```typescript
// Private 헬퍼 함수 추가
async function handlePhoneLogin(
    phoneNumber: string,
    verificationCode: string,
    setIsLoading: (loading: boolean) => void,
    setError: (error: string) => void,
    onSuccess: () => void
) {
    try {
        setIsLoading(true);
        setError('');
        
        const response = await fetch(`${gatewayUrl}/api/auth/phone`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ phoneNumber, verificationCode }),
        });
        
        if (response.ok) {
            onSuccess();
        } else {
            const data = await response.json();
            setError(data.message || '전화번호 인증에 실패했습니다.');
        }
    } catch (err) {
        setError('서버 연결에 실패했습니다.');
    } finally {
        setIsLoading(false);
    }
}

// 팩토리 함수에 이너 함수 추가
function handlePhoneNumberLogin(phoneNumber: string, code: string, onSuccess: () => void) {
    handlePhoneLogin(phoneNumber, code, setIsLoading, setError, onSuccess);
}

// return 객체에 추가
return {
    // ... 기존 핸들러들
    handlePhoneNumberLogin,
};
```

---

## 디버깅 가이드

### 1. 로그인 실패 시

**확인 사항:**
1. 브라우저 콘솔에서 에러 메시지 확인
2. Network 탭에서 API 응답 확인
3. Backend 로그 확인

**일반적인 에러:**

```typescript
// 1. CORS 에러
// → Backend에서 CORS 설정 확인

// 2. 401 Unauthorized
// → 토큰 만료 또는 잘못된 credentials

// 3. 500 Internal Server Error
// → Backend 로그 확인

// 4. Network Error
// → Backend 서버 실행 여부 확인
// → gatewayUrl 설정 확인
```

### 2. 디버깅 팁

**console.log 추가:**

```typescript
async function handleLogin(provider, setIsLoading, setError) {
    console.log('🔍 로그인 시작:', provider);
    
    try {
        const response = await fetch(...);
        console.log('📡 응답:', response.status);
        
        const data = await response.json();
        console.log('📦 데이터:', data);
        
        // ...
    } catch (err) {
        console.error('❌ 에러:', err);
    }
}
```

---

## 성능 최적화

### 1. useMemo 사용

```typescript
// ✅ 핸들러를 메모이제이션
const handlers = useMemo(
    () => createSocialLoginHandlers(...),
    [dependencies]
);

// ❌ 매 렌더링마다 재생성
const handlers = createSocialLoginHandlers(...);
```

### 2. 로딩 상태 분리

```typescript
// ✅ 각 버튼마다 독립적인 로딩 상태
const [isGoogleLoading, setIsGoogleLoading] = useState(false);
const [isKakaoLoading, setIsKakaoLoading] = useState(false);

// ❌ 하나의 로딩 상태 공유
const [isLoading, setIsLoading] = useState(false);
```

---

## 보안 고려사항

### 1. 환경 변수 사용

```typescript
// ✅ 환경 변수 사용
const gatewayUrl = process.env.NEXT_PUBLIC_GATEWAY_URL;

// ❌ 하드코딩
const gatewayUrl = 'api.labzang.com';
```

### 2. credentials: 'include'

```typescript
// 쿠키를 포함하여 요청
fetch(url, {
    credentials: 'include',  // 중요!
    // ...
});
```

### 3. HTTPS 사용

프로덕션 환경에서는 반드시 HTTPS 사용

---

## 테스트 전략

### 1. 단위 테스트

```typescript
// Mock setter 주입
const mockSetError = jest.fn();
const mockSetIsLoading = jest.fn();

const handlers = createSocialLoginHandlers(
    mockSetIsLoading,
    mockSetIsLoading,
    mockSetIsLoading,
    mockSetIsLoading,
    mockSetError
);

// 테스트
handlers.handleGoogleLogin();
expect(mockSetIsLoading).toHaveBeenCalledWith(true);
```

### 2. 통합 테스트

```typescript
// Backend API mock
fetchMock.mockResponseOnce(JSON.stringify({
    success: true,
    authUrl: 'https://accounts.google.com/...'
}));

// 핸들러 실행
await handlers.handleGoogleLogin();

// 검증
expect(window.location.href).toBe('https://accounts.google.com/...');
```

---

## 참고 자료

- [IIFE 패턴](https://developer.mozilla.org/ko/docs/Glossary/IIFE)
- [클로저](https://developer.mozilla.org/ko/docs/Web/JavaScript/Closures)
- [함수 선언식 vs 화살표 함수](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Functions/Arrow_functions)
- [의존성 주입](https://en.wikipedia.org/wiki/Dependency_injection)
- [useMemo Hook](https://react.dev/reference/react/useMemo)

