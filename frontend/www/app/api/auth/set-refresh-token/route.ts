import { NextRequest, NextResponse } from 'next/server';

/**
 * Refresh Token을 HttpOnly 쿠키에 저장하는 API Route
 * 
 * 보안을 위해 HttpOnly, Secure, SameSite 속성을 설정합니다.
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { refreshToken } = body;

    if (!refreshToken) {
      return NextResponse.json(
        { success: false, error: 'Refresh token이 필요합니다.' },
        { status: 400 }
      );
    }

    // HttpOnly 쿠키로 Refresh Token 저장
    const response = NextResponse.json(
      { success: true, message: 'Refresh token이 쿠키에 저장되었습니다.' },
      { status: 200 }
    );

    // 쿠키 설정
    // HttpOnly: JavaScript에서 접근 불가 (XSS 공격 방지)
    // Secure: HTTPS에서만 전송 (프로덕션 환경)
    // SameSite=Strict: CSRF 공격 방지
    // Max-Age: 7일 (604800초)
    const isProduction = process.env.NODE_ENV === 'production';
    
    response.cookies.set('refresh_token', refreshToken, {
      httpOnly: true,
      secure: isProduction, // 프로덕션에서는 HTTPS만, 개발에서는 false
      sameSite: 'strict',
      maxAge: 60 * 60 * 24 * 7, // 7일
      path: '/',
    });

    console.log('[API] Refresh token이 HttpOnly 쿠키에 저장되었습니다.');

    return response;
  } catch (error) {
    console.error('[API] Refresh token 쿠키 설정 실패:', error);
    return NextResponse.json(
      { success: false, error: '쿠키 설정에 실패했습니다.' },
      { status: 500 }
    );
  }
}

/**
 * Refresh Token 쿠키 삭제
 */
export async function DELETE(request: NextRequest) {
  try {
    const response = NextResponse.json(
      { success: true, message: 'Refresh token 쿠키가 삭제되었습니다.' },
      { status: 200 }
    );

    // 쿠키 삭제
    response.cookies.delete('refresh_token');

    console.log('[API] Refresh token 쿠키가 삭제되었습니다.');

    return response;
  } catch (error) {
    console.error('[API] Refresh token 쿠키 삭제 실패:', error);
    return NextResponse.json(
      { success: false, error: '쿠키 삭제에 실패했습니다.' },
      { status: 500 }
    );
  }
}

