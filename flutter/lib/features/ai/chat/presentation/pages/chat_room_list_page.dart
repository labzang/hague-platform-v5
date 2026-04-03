import 'package:flutter/cupertino.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:labzang_app/features/ai/chat/presentation/providers/chat_room_providers.dart';
import 'package:labzang_app/shared/widgets/app_drawer_layout.dart';
import 'package:labzang_app/shared/widgets/loading_view.dart';

/// 서버 채팅방 목록 — backend: `labzang.apps.ai.chat`
/// 상단에서 AI 1:1 대화 화면으로 이동 가능.
class ChatRoomListPage extends ConsumerWidget {
  const ChatRoomListPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final rooms = ref.watch(chatRoomsProvider);

    return AppDrawerLayout(
      backgroundColor:
          CupertinoColors.systemGroupedBackground.resolveFrom(context),
      title: '채팅방',
      trailing: CupertinoButton(
        padding: EdgeInsets.zero,
        onPressed: () => context.push('/home/chat'),
        child: const Icon(CupertinoIcons.chat_bubble_2_fill),
      ),
      child: rooms.when(
        data: (items) {
          if (items.isEmpty) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(32),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      CupertinoIcons.chat_bubble_text_fill,
                      size: 56,
                      color: CupertinoColors.systemGrey.resolveFrom(context),
                    ),
                    const SizedBox(height: 16),
                    const Text(
                      '채팅방이 없습니다.',
                      style: TextStyle(fontSize: 17),
                    ),
                    const SizedBox(height: 24),
                    CupertinoButton.filled(
                      onPressed: () => context.push('/home/chat'),
                      child: const Text('AI와 채팅하기'),
                    ),
                  ],
                ),
              ),
            );
          }
          return ListView(
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
                child: CupertinoButton.filled(
                  onPressed: () => context.push('/home/chat'),
                  child: const Text('AI와 새 대화'),
                ),
              ),
              CupertinoListSection.insetGrouped(
                header: const Text('내 채팅방'),
                children: [
                  for (final room in items)
                    CupertinoListTile(
                      title: Text(room.title),
                      subtitle: Text(room.updatedAt.toIso8601String()),
                      trailing: const CupertinoListTileChevron(),
                      onTap: () => context.push('/home/chat'),
                    ),
                ],
              ),
            ],
          );
        },
        loading: () => const LoadingView(),
        error: (error, _) => Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Text(
              '오류: $error',
              textAlign: TextAlign.center,
              style: const TextStyle(
                color: CupertinoColors.destructiveRed,
              ),
            ),
          ),
        ),
      ),
    );
  }
}
