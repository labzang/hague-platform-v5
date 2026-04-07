import 'package:dio/dio.dart';

/// `labzang.apps.ext.guard` HTTP API (`POST /auth/register` 등).
class AuthRemoteDataSource {
  AuthRemoteDataSource(this._dio);

  final Dio _dio;

  /// 백엔드 [create_response](https://github.com) 래핑 본문 전체 반환.
  Future<Map<String, dynamic>> register(Map<String, dynamic> body) async {
    final Response<Map<String, dynamic>> res = await _dio.post<Map<String, dynamic>>(
      '/auth/register',
      data: body,
    );
    final Map<String, dynamic>? data = res.data;
    if (data == null) {
      throw DioException(
        requestOptions: res.requestOptions,
        message: '빈 응답',
      );
    }
    return data;
  }
}
