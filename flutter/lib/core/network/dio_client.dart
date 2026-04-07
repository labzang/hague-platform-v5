import 'package:dio/dio.dart';

/// Shared HTTP client. Wire base URL via [DioClient] constructor or env later.
///
/// Android 에뮬레이터에서 PC의 `localhost`에 붙이려면 `http://10.0.2.2:8000` 등으로
/// [baseUrl]을 지정한다.
class DioClient {
  DioClient({String? baseUrl})
      : dio = Dio(
          BaseOptions(
            baseUrl: baseUrl ?? 'http://localhost:8000',
            connectTimeout: const Duration(seconds: 10),
            receiveTimeout: const Duration(seconds: 10),
          ),
        );

  final Dio dio;
}
