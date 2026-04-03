import '../entities/chat_room.dart';
import '../repositories/chat_room_repository.dart';

class GetChatRooms {
  const GetChatRooms(this._repository);

  final ChatRoomRepository _repository;

  Future<List<ChatRoom>> call() => _repository.getChatRooms();
}
