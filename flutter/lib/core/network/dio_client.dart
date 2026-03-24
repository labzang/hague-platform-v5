import 'package:dio/dio.dart';

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
