import 'package:freezed_annotation/freezed_annotation.dart';

import '../../domain/entities/chat_room.dart';

part 'chat_room_model.freezed.dart';
part 'chat_room_model.g.dart';

@freezed
class ChatRoomModel with _$ChatRoomModel {
  const factory ChatRoomModel({
    required String id,
    required String title,
    required DateTime updatedAt,
  }) = _ChatRoomModel;

  factory ChatRoomModel.fromJson(Map<String, dynamic> json) =>
      _$ChatRoomModelFromJson(json);
}

extension ChatRoomModelX on ChatRoomModel {
  ChatRoom toEntity() {
    return ChatRoom(id: id, title: title, updatedAt: updatedAt);
  }
}
