import React, { useState, useEffect } from 'react';
import { Button } from '../atoms';
import { SettingsView as SettingsViewType } from '../types';
import { useStore } from '../../store';
import { updateUserNickname, fetchUserById } from '../../app/hooks/useUserApi';
import { Input } from '../atoms/Input';

interface SettingsViewProps {
  settingsView: SettingsViewType;
  setSettingsView: (view: SettingsViewType) => void;
  darkMode?: boolean;
}

const getCommonStyles = (darkMode: boolean) => ({
  bg: darkMode ? 'bg-[#0a0a0a]' : 'bg-[#e8e2d5]',
  bgSecondary: darkMode ? 'bg-[#121212]' : 'bg-[#f5f1e8]',
  header: darkMode ? 'bg-[#121212] border-[#2a2a2a]' : 'bg-white border-[#d4c4a8]',
  card: darkMode ? 'bg-[#121212] border-[#2a2a2a]' : 'bg-white border-[#8B7355]',
  cardGradient: darkMode ? 'bg-gradient-to-br from-[#1a1a1a] to-[#121212] border-[#2a2a2a]' : 'bg-gradient-to-br from-white to-[#f5f0e8] border-[#8B7355]',
  title: darkMode ? 'text-white' : 'text-gray-900',
  textMuted: darkMode ? 'text-gray-400' : 'text-gray-500',
  textSecondary: darkMode ? 'text-gray-300' : 'text-gray-700',
  border: darkMode ? 'border-[#2a2a2a]' : 'border-[#d4c4a8]',
  button: darkMode ? 'bg-gradient-to-br from-[#1a1a1a] to-[#121212] border-[#2a2a2a]' : 'bg-gradient-to-br from-white to-[#f5f0e8] border-[#8B7355]',
  buttonHover: darkMode ? 'text-gray-300 hover:text-white hover:bg-[#1a1a1a]' : 'text-gray-600 hover:text-gray-900 hover:bg-[#f5f1e8]',
  cardBg: darkMode ? 'bg-[#1a1a1a]' : 'bg-[#f5f1e8]',
});

export const SettingsView: React.FC<SettingsViewProps> = ({
  settingsView,
  setSettingsView,
  darkMode = false,
}) => {
  const styles = getCommonStyles(darkMode);
  const user = useStore((state) => state.user?.user);
  const login = useStore((state) => state.user?.login);
  
  const [nickname, setNickname] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);

  // 로그아웃 헬퍼 함수 (함수가 없을 때 사용)
  const performLogout = () => {
    console.log('[SettingsView] performLogout 호출됨 - 강제 로그아웃 처리');
    if (typeof window !== 'undefined') {
      // 모든 상태 정리
      useStore.getState().user?.clearAccessToken();
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('auth_provider');
      localStorage.removeItem('app-storage');
      sessionStorage.clear();
      
      // 모든 쿠키 삭제
      const cookies = document.cookie.split(';');
      cookies.forEach(cookie => {
        const eqPos = cookie.indexOf('=');
        const name = eqPos > -1 ? cookie.substring(0, eqPos).trim() : cookie.trim();
        // 모든 경로와 도메인에서 쿠키 삭제 시도
        document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`;
        document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=${window.location.hostname}`;
        document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=.${window.location.hostname}`;
        document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=localhost`;
      });
      
      // Zustand 상태도 초기화 (set 함수 사용)
      const store = useStore.getState();
      useStore.setState((state) => ({
        user: {
          ...state.user,
          user: null,
          isLoggedIn: false,
        },
      }));
      
      console.log('[SettingsView] 강제 로그아웃 완료 (쿠키 포함) - 페이지 이동');
      setTimeout(() => {
        window.location.replace('/');
      }, 100);
    }
  };

  // 사용자 정보 로드
  useEffect(() => {
    const loadUserInfo = async () => {
      if (user?.id && !isInitialized) {
        try {
          setIsLoading(true);
          const userInfo = await fetchUserById(user.id);
          if (userInfo) {
            // 닉네임을 명시적으로 String으로 변환하여 설정
            const nicknameValue = userInfo.nickname || userInfo.name || '';
            const cleanNickname = String(nicknameValue).trim();
            console.log('[SettingsView] API에서 받은 닉네임:', cleanNickname);
            setNickname(cleanNickname);
            setIsInitialized(true);
          }
        } catch (err) {
          console.error('[SettingsView] 사용자 정보 로드 실패:', err);
          // 에러 시에도 빈 문자열로 설정 (깨진 값 사용 안 함)
          setNickname('');
          setIsInitialized(true);
        } finally {
          setIsLoading(false);
        }
      } else if (!isInitialized) {
        // user?.name을 사용하지 않고 빈 문자열로 초기화
        // API 호출이 필요하지만 id가 없는 경우
        setNickname('');
        setIsInitialized(true);
      }
    };

    loadUserInfo();
  }, [user?.id, isInitialized]); // user 전체가 아니라 user.id만 의존성으로 사용

  const validateNickname = (value: string): string | null => {
    if (!value.trim()) {
      return '닉네임을 입력해주세요.';
    }
    if (value.length < 2 || value.length > 20) {
      return '닉네임은 2자 이상 20자 이하로 입력해주세요.';
    }
    // 특수문자 및 공백 검사 (한글, 영어, 숫자만 허용)
    const regex = /^[가-힣a-zA-Z0-9\s]*$/;
    if (!regex.test(value)) {
      return '닉네임에는 한글, 영어, 숫자만 사용할 수 있습니다.';
    }
    return null;
  };

  const handleNicknameUpdate = async () => {
    if (!user?.id) {
      setError('사용자 정보를 찾을 수 없습니다.');
      return;
    }

    const validationError = validateNickname(nickname);
    if (validationError) {
      setError(validationError);
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      setSuccess(null);

      const updatedUser = await updateUserNickname(user.id, nickname.trim());
      
      console.log('[SettingsView] 업데이트된 사용자 정보:', updatedUser);
      console.log('[SettingsView] 업데이트된 닉네임:', updatedUser?.nickname);
      
      if (updatedUser) {
        // 닉네임을 명시적으로 String으로 변환
        const newNickname = String(updatedUser.nickname || updatedUser.name || nickname.trim());
        console.log('[SettingsView] 새 닉네임으로 state 업데이트:', newNickname, '타입:', typeof newNickname);
        setNickname(newNickname);
        
        // Zustand 스토어 업데이트
        if (login) {
          login({
            id: user.id,
            name: String(newNickname),
            email: String(updatedUser.email || user.email || ''),
          });
        }
      }

      setSuccess('닉네임이 성공적으로 변경되었습니다.');
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
    } catch (err) {
      console.error('닉네임 업데이트 실패:', err);
      setError(err instanceof Error ? err.message : '닉네임 변경에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  // Home 뷰
  if (settingsView === 'home') {
    return (
      <div className={`flex-1 overflow-y-auto p-4 md:p-6 ${styles.bg}`} style={{ WebkitOverflowScrolling: 'touch' }}>
        <div className="max-w-4xl mx-auto space-y-6">
          <div className="text-center py-4">
            <h1 className={`text-3xl font-bold ${styles.title}`}>설정</h1>
          </div>

          <div className={`rounded-2xl border-2 p-8 shadow-lg ${styles.cardGradient}`}>
            <div className="grid grid-cols-1 gap-6">
              <Button
                onClick={() => setSettingsView('profile')}
                className={`rounded-2xl border-2 p-6 hover:shadow-lg hover:scale-105 transition-all ${styles.button}`}
              >
                <div className="flex flex-col items-center space-y-3">
                  <span className="text-4xl">👤</span>
                  <p className={`text-xl font-bold ${styles.title}`}>프로필</p>
                  <p className={`text-sm ${styles.textMuted}`}>닉네임 및 개인정보 관리</p>
                </div>
              </Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Profile 뷰
  if (settingsView === 'profile') {
    return (
      <div className={`flex-1 flex flex-col ${styles.bg}`}>
        <div className={`border-b shadow-sm p-4 ${styles.header}`}>
          <div className="max-w-4xl mx-auto flex items-center gap-4">
            <button
              onClick={() => setSettingsView('home')}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg transition-colors ${styles.buttonHover}`}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <h1 className={`text-2xl font-bold ${styles.title}`}>프로필</h1>
          </div>
        </div>
        <div className="flex-1 overflow-y-auto p-4 md:p-6" style={{ WebkitOverflowScrolling: 'touch' }}>
          <div className="max-w-2xl mx-auto space-y-6">
            <div className={`rounded-2xl border-2 p-8 shadow-lg ${styles.card}`}>
              <h2 className={`text-xl font-bold mb-6 ${styles.title}`}>닉네임 변경</h2>
              
              <div className="space-y-4">
                <div>
                  <label className={`block text-sm font-medium mb-2 ${styles.textSecondary}`}>
                    닉네임
                  </label>
                  <Input
                    type="text"
                    value={String(nickname || '')}
                    onChange={(e) => {
                      const newValue = String(e.target.value || '');
                      console.log('[SettingsView] 입력 변경:', newValue);
                      setNickname(newValue);
                      setError(null);
                      setSuccess(null);
                    }}
                    placeholder="닉네임을 입력하세요 (2~20자)"
                    maxLength={20}
                    className="w-full"
                    disabled={isLoading}
                    aria-label="닉네임 입력"
                  />
                  <p className={`text-sm mt-1 ${styles.textMuted}`}>
                    {nickname.length}/20자
                  </p>
                  {error && (
                    <p className="text-red-400 text-sm mt-2">{error}</p>
                  )}
                  {success && (
                    <p className="text-green-400 text-sm mt-2">{success}</p>
                  )}
                </div>

                <div className="flex justify-end gap-3 pt-4">
                  <Button
                    onClick={handleNicknameUpdate}
                    disabled={isLoading || !nickname.trim()}
                    className="min-w-[120px]"
                  >
                    {isLoading ? '저장 중...' : '저장'}
                  </Button>
                </div>
              </div>
            </div>

            <div className={`rounded-2xl border-2 p-8 shadow-lg ${styles.card}`}>
              <h2 className={`text-xl font-bold mb-4 ${styles.title}`}>계정 정보</h2>
              <div className="space-y-3">
                <div>
                  <p className={`text-sm ${styles.textMuted}`}>이메일</p>
                  <p className={`text-base ${styles.title}`}>{user?.email || '-'}</p>
                </div>
                {user?.id && (
                  <div>
                    <p className={`text-sm ${styles.textMuted}`}>사용자 ID</p>
                    <p className={`text-base ${styles.title}`}>{user.id}</p>
                  </div>
                )}
              </div>
            </div>

            <div className={`rounded-2xl border-2 p-8 shadow-lg ${styles.card}`}>
              <h2 className={`text-xl font-bold mb-4 ${styles.title}`}>계정 관리</h2>
              <div className="space-y-3">
                <button
                  type="button"
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    console.log('[SettingsView] 로그아웃 버튼 클릭됨');
                    
                    // useStore에서 직접 logout 함수 가져오기
                    const store = useStore.getState();
                    const logoutFn = store.user?.logout;
                    
                    console.log('[SettingsView] store.user:', store.user);
                    console.log('[SettingsView] logoutFn 함수 존재:', !!logoutFn);
                    console.log('[SettingsView] logoutFn 함수 타입:', typeof logoutFn);
                    
                    if (logoutFn && typeof logoutFn === 'function') {
                      console.log('[SettingsView] logout 함수 호출 시작');
                      try {
                        // logout 함수 내에서 모든 상태 정리 및 랜딩 페이지로 리다이렉트 처리
                        logoutFn();
                      } catch (error) {
                        console.error('[SettingsView] logout 함수 실행 중 에러:', error);
                        // 에러 발생 시에도 강제로 로그아웃 처리
                        performLogout();
                      }
                    } else {
                      console.warn('[SettingsView] logout 함수가 없거나 함수가 아닙니다. 강제 로그아웃 수행');
                      // 함수가 없어도 강제로 로그아웃 처리
                      performLogout();
                    }
                  }}
                  className="w-full bg-red-600 hover:bg-red-700 text-white border-red-600 rounded-lg px-4 py-3 font-medium transition-colors active:scale-95 transition-transform"
                >
                  로그아웃
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

