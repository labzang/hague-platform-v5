import 'package:shared_preferences/shared_preferences.dart';

/// 백엔드 없이 회원가입 → 로그인 플로우를 검증하기 위한 **개발용** 임시 저장소.
///
/// 비밀번호를 평문으로 [SharedPreferences]에 둡니다. **프로덕션에서는 사용하지 말 것.**
class LocalSignupCredentialsStore {
  LocalSignupCredentialsStore(this._prefs);

  final SharedPreferences _prefs;

  static const String _kFlag = 'labzang_dev_local_signup_exists';
  static const String _kUserId = 'labzang_dev_local_signup_user_id';
  static const String _kPassword = 'labzang_dev_local_signup_password';
  static const String _kName = 'labzang_dev_local_signup_name';
  static const String _kEmail = 'labzang_dev_local_signup_email';
  static const String _kBirth = 'labzang_dev_local_signup_birth_iso';
  static const String _kGender = 'labzang_dev_local_signup_gender';
  static const String _kPhone = 'labzang_dev_local_signup_phone';
  static const String _kAddrMain = 'labzang_dev_local_signup_addr_main';
  static const String _kAddrDetail = 'labzang_dev_local_signup_addr_detail';

  bool get hasLocalSignup => _prefs.getBool(_kFlag) ?? false;

  /// 회원가입 폼 검증이 끝난 뒤 호출해 로컬에 덮어쓴다.
  Future<void> saveFromSignup({
    required String userId,
    required String password,
    required String name,
    required String email,
    required DateTime birthDate,
    required String genderLabel,
    String phone = '',
    String addressMain = '',
    String addressDetail = '',
  }) async {
    await _prefs.setString(_kUserId, userId);
    await _prefs.setString(_kPassword, password);
    await _prefs.setString(_kName, name);
    await _prefs.setString(_kEmail, email);
    await _prefs.setString(_kBirth, birthDate.toIso8601String());
    await _prefs.setString(_kGender, genderLabel);
    await _prefs.setString(_kPhone, phone);
    await _prefs.setString(_kAddrMain, addressMain);
    await _prefs.setString(_kAddrDetail, addressDetail);
    await _prefs.setBool(_kFlag, true);
  }

  /// 임시저장된 아이디·비밀번호와 일치하면 true (로그인 성공으로 간주).
  bool verifyLogin(String userId, String password) {
    if (!hasLocalSignup) {
      return false;
    }
    final String? id = _prefs.getString(_kUserId);
    final String? pw = _prefs.getString(_kPassword);
    return id == userId && pw == password;
  }

  /// 단위 테스트에서 상태 초기화.
  Future<void> clear() async {
    await _prefs.remove(_kFlag);
    await _prefs.remove(_kUserId);
    await _prefs.remove(_kPassword);
    await _prefs.remove(_kName);
    await _prefs.remove(_kEmail);
    await _prefs.remove(_kBirth);
    await _prefs.remove(_kGender);
    await _prefs.remove(_kPhone);
    await _prefs.remove(_kAddrMain);
    await _prefs.remove(_kAddrDetail);
  }

  static Future<LocalSignupCredentialsStore> open() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    return LocalSignupCredentialsStore(prefs);
  }
}
