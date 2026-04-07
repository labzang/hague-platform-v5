import 'package:labzang_app/features/ext/guard/domain/entities/register_user_params.dart';
import 'package:labzang_app/features/ext/guard/domain/entities/registered_user.dart';
import 'package:labzang_app/features/ext/guard/domain/repositories/auth_repository.dart';

class RegisterUserUsecase {
  const RegisterUserUsecase(this._repository);

  final AuthRepository _repository;

  Future<RegisteredUser> call(RegisterUserParams params) {
    return _repository.register(params);
  }
}
