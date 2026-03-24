import '../models/chat_room_model.dart';
import '../../core/network/dio_client.dart';

class ChatRoomRemoteDataSource {
  const ChatRoomRemoteDataSource(this._client);

  final DioClient _client;

  Future<List<ChatRoomModel>> fetchChatRooms() async {
    final response = await _client.dio.get('/chat/rooms');
    final data = (response.data as List<dynamic>)
        .map((e) => ChatRoomModel.fromJson(e as Map<String, dynamic>))
        .toList();
    return data;
  }
}
