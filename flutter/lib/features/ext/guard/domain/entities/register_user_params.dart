/// `POST /auth/register` 본문 — [id]·[role]은 서버에서 부여.
class RegisterUserParams {
  const RegisterUserParams({
    required this.username,
    required this.password,
    required this.name,
    required this.email,
    required this.phone,
    required this.birthDate,
    required this.gender,
    required this.addressMain,
    this.addressDetail = '',
  });

  final String username;
  final String password;
  final String name;
  final String email;
  final String phone;
  final DateTime birthDate;
  final String gender;
  final String addressMain;
  final String addressDetail;

  Map<String, dynamic> toJson() {
    final String y = birthDate.year.toString().padLeft(4, '0');
    final String m = birthDate.month.toString().padLeft(2, '0');
    final String d = birthDate.day.toString().padLeft(2, '0');
    return <String, dynamic>{
      'username': username,
      'password': password,
      'name': name,
      'email': email,
      'phone': phone,
      'birth_date': '$y-$m-$d',
      'gender': gender,
      'address_main': addressMain,
      'address_detail': addressDetail,
    };
  }
}
