/// 서버 `users` 행에 대응하는 최소 정보 (회원가입 응답).
class RegisteredUser {
  const RegisteredUser({
    required this.id,
    required this.username,
    required this.role,
  });

  final String id;
  final String username;
  final String role;

  factory RegisteredUser.fromRegisterJson(Map<String, dynamic> json) {
    return RegisteredUser(
      id: json['id'] as String,
      username: json['username'] as String,
      role: json['role'] as String? ?? 'customer',
    );
  }
}
