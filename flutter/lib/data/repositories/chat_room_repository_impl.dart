import '../../domain/entities/chat_room.dart';
import '../../domain/repositories/chat_room_repository.dart';
import '../datasources/chat_room_remote_datasource.dart';

class ChatRoomRepositoryImpl implements ChatRoomRepository {
  const ChatRoomRepositoryImpl(this._remote);

  final ChatRoomRemoteDataSource _remote;

  @override
  Future<List<ChatRoom>> getChatRooms() async {
    final models = await _remote.fetchChatRooms();
    return models.map((e) => e.toEntity()).toList();
  }
}
