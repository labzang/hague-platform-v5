import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../providers/chat_room_providers.dart';
import '../widgets/loading_view.dart';

class ChatRoomListPage extends ConsumerWidget {
  const ChatRoomListPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final rooms = ref.watch(chatRoomsProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('채팅방')),
      body: rooms.when(
        data: (items) => ListView.separated(
          itemCount: items.length,
          separatorBuilder: (_, __) => const Divider(height: 1),
          itemBuilder: (_, index) {
            final room = items[index];
            return ListTile(
              title: Text(room.title),
              subtitle: Text(room.updatedAt.toIso8601String()),
            );
          },
        ),
        loading: () => const LoadingView(),
        error: (error, _) => Center(child: Text('오류: $error')),
      ),
    );
  }
}
