import 'package:dio/dio.dart';
import 'package:labzang_app/features/ext/guard/data/datasources/auth_remote_datasource.dart';
import 'package:labzang_app/features/ext/guard/domain/entities/register_user_params.dart';
import 'package:labzang_app/features/ext/guard/domain/entities/registered_user.dart';
import 'package:labzang_app/features/ext/guard/domain/repositories/auth_repository.dart';

class AuthRepositoryImpl implements AuthRepository {
  AuthRepositoryImpl(this._remote);

  final AuthRemoteDataSource _remote;

  @override
  Future<RegisteredUser> register(RegisterUserParams params) async {
    try {
      final Map<String, dynamic> envelope =
          await _remote.register(params.toJson());
      if (envelope['status'] != 'success') {
        final String msg = envelope['message']?.toString() ?? '회원가입 실패';
        throw DioException(
          requestOptions: RequestOptions(path: '/auth/register'),
          message: msg,
        );
      }
      final Object? data = envelope['data'];
      if (data is! Map<String, dynamic>) {
        throw DioException(
          requestOptions: RequestOptions(path: '/auth/register'),
          message: '응답 형식 오류',
        );
      }
      return RegisteredUser.fromRegisterJson(data);
    } on DioException catch (e) {
      final String msg = _messageFromDio(e);
      throw DioException(
        requestOptions: e.requestOptions,
        response: e.response,
        type: e.type,
        message: msg,
      );
    }
  }

  String _messageFromDio(DioException e) {
    final dynamic d = e.response?.data;
    if (d is Map && d['detail'] != null) {
      final Object det = d['detail']!;
      if (det is String) return det;
      if (det is List && det.isNotEmpty) {
        final Object first = det.first;
        if (first is Map) {
          return first['msg']?.toString() ??
              first['message']?.toString() ??
              e.message ??
              '오류';
        }
      }
    }
    return e.message ?? '네트워크 오류';
  }
}
