import 'package:dio/dio.dart';

/// Shared HTTP client. Wire base URL via [DioClient] constructor or env later.
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
