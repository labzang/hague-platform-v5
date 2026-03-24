import 'package:riverpod_annotation/riverpod_annotation.dart';

import '../../core/network/dio_client.dart';
import '../../data/datasources/chat_room_remote_datasource.dart';
import '../../data/repositories/chat_room_repository_impl.dart';
import '../../domain/entities/chat_room.dart';
import '../../domain/repositories/chat_room_repository.dart';
import '../../domain/usecases/get_chat_rooms.dart';

part 'chat_room_providers.g.dart';

@riverpod
DioClient dioClient(DioClientRef ref) => DioClient();

@riverpod
ChatRoomRemoteDataSource chatRoomRemoteDataSource(
  ChatRoomRemoteDataSourceRef ref,
) {
  return ChatRoomRemoteDataSource(ref.watch(dioClientProvider));
}

@riverpod
ChatRoomRepository chatRoomRepository(ChatRoomRepositoryRef ref) {
  return ChatRoomRepositoryImpl(ref.watch(chatRoomRemoteDataSourceProvider));
}

@riverpod
GetChatRooms getChatRooms(GetChatRoomsRef ref) {
  return GetChatRooms(ref.watch(chatRoomRepositoryProvider));
}

@riverpod
Future<List<ChatRoom>> chatRooms(ChatRoomsRef ref) {
  return ref.watch(getChatRoomsProvider).call();
}
