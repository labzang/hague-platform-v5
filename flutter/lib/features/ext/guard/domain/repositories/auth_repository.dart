import 'package:labzang_app/features/ext/guard/domain/entities/register_user_params.dart';
import 'package:labzang_app/features/ext/guard/domain/entities/registered_user.dart';

abstract class AuthRepository {
  Future<RegisteredUser> register(RegisterUserParams params);
}
