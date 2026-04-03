import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

import 'dio_client.dart';

part 'dio_client_provider.g.dart';

@riverpod
DioClient dioClient(Ref ref) => DioClient();
