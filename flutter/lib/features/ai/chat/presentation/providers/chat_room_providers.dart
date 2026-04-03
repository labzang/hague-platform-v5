import 'package:labzang_app/core/network/dio_client_provider.dart';
import 'package:labzang_app/features/ai/chat/data/datasources/chat_room_remote_datasource.dart';
import 'package:labzang_app/features/ai/chat/data/repositories/chat_room_repository_impl.dart';
import 'package:labzang_app/features/ai/chat/domain/entities/chat_room.dart';
import 'package:labzang_app/features/ai/chat/domain/repositories/chat_room_repository.dart';
import 'package:labzang_app/features/ai/chat/domain/usecases/get_chat_rooms.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'chat_room_providers.g.dart';

@riverpod
ChatRoomRemoteDataSource chatRoomRemoteDataSource(Ref ref) {
  return ChatRoomRemoteDataSource(ref.watch(dioClientProvider));
}

@riverpod
ChatRoomRepository chatRoomRepository(Ref ref) {
  return ChatRoomRepositoryImpl(ref.watch(chatRoomRemoteDataSourceProvider));
}

@riverpod
GetChatRooms getChatRooms(Ref ref) {
  return GetChatRooms(ref.watch(chatRoomRepositoryProvider));
}

@riverpod
Future<List<ChatRoom>> chatRooms(Ref ref) {
  return ref.watch(getChatRoomsProvider).call();
}
