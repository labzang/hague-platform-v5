import '../entities/chat_room.dart';

abstract class ChatRoomRepository {
  Future<List<ChatRoom>> getChatRooms();
}
