import '../entities/chat_room.dart';

/// Port — repository interface (hexagonal).
abstract class ChatRoomRepository {
  Future<List<ChatRoom>> getChatRooms();
}
