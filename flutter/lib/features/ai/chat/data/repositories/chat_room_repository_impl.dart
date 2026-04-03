import 'package:labzang_app/features/ai/chat/data/datasources/chat_room_remote_datasource.dart';
import 'package:labzang_app/features/ai/chat/data/models/chat_room_model.dart';
import 'package:labzang_app/features/ai/chat/domain/entities/chat_room.dart';
import 'package:labzang_app/features/ai/chat/domain/repositories/chat_room_repository.dart';

class ChatRoomRepositoryImpl implements ChatRoomRepository {
  const ChatRoomRepositoryImpl(this._remote);

  final ChatRoomRemoteDataSource _remote;

  @override
  Future<List<ChatRoom>> getChatRooms() async {
    final models = await _remote.fetchChatRooms();
    return models.map((e) => e.toEntity()).toList();
  }
}
