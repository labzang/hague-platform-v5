import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:labzang_app/core/network/dio_client_provider.dart';
import 'package:labzang_app/features/ext/guard/data/datasources/auth_remote_datasource.dart';
import 'package:labzang_app/features/ext/guard/data/repositories/auth_repository_impl.dart';
import 'package:labzang_app/features/ext/guard/domain/repositories/auth_repository.dart';
import 'package:labzang_app/features/ext/guard/domain/usecases/register_user_usecase.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'auth_providers.g.dart';

@riverpod
AuthRemoteDataSource authRemoteDataSource(Ref ref) {
  return AuthRemoteDataSource(ref.watch(dioClientProvider).dio);
}

@riverpod
AuthRepository authRepository(Ref ref) {
  return AuthRepositoryImpl(ref.watch(authRemoteDataSourceProvider));
}

@riverpod
RegisterUserUsecase registerUserUsecase(Ref ref) {
  return RegisterUserUsecase(ref.watch(authRepositoryProvider));
}
