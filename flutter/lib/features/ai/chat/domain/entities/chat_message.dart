/// 채팅 메시지 (사용자 / 어시스턴트)
enum ChatRole {
  user,
  assistant,
}

class ChatMessage {
  const ChatMessage({
    required this.id,
    required this.role,
    required this.content,
    required this.createdAt,
  });

  factory ChatMessage.user(String content) {
    final t = DateTime.now();
    return ChatMessage(
      id: 'u-${t.microsecondsSinceEpoch}',
      role: ChatRole.user,
      content: content,
      createdAt: t,
    );
  }

  factory ChatMessage.assistant(String content) {
    final t = DateTime.now();
    return ChatMessage(
      id: 'a-${t.microsecondsSinceEpoch}',
      role: ChatRole.assistant,
      content: content,
      createdAt: t,
    );
  }

  final String id;
  final ChatRole role;
  final String content;
  final DateTime createdAt;
}
