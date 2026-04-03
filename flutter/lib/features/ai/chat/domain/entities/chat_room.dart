/// Chat room entity — backend: `labzang.apps.ai.chat`
class ChatRoom {
  const ChatRoom({
    required this.id,
    required this.title,
    required this.updatedAt,
  });

  final String id;
  final String title;
  final DateTime updatedAt;
}
