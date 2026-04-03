import 'package:flutter/cupertino.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:labzang_app/features/ai/chat/presentation/pages/ai_chat_conversation_page.dart';
import 'package:labzang_app/features/ai/chat/presentation/providers/ai_chat_providers.dart';
import 'package:labzang_app/shared/widgets/app_drawer_layout.dart';

/// `labzang.apps.ai.chat` — AI 1:1 대화 화면
class AiChatHomePage extends ConsumerWidget {
  const AiChatHomePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final key = ref.watch(llmApiKeyProvider);
    final hasKey = key.isNotEmpty;

    return AppDrawerLayout(
      title: 'AI · 채팅',
      backgroundColor:
          CupertinoColors.systemGroupedBackground.resolveFrom(context),
      trailing: hasKey
          ? const Icon(
              CupertinoIcons.check_mark_circled_solid,
              color: CupertinoColors.activeGreen,
              size: 22,
            )
          : Icon(
              CupertinoIcons.lock_fill,
              color: CupertinoColors.systemGrey.resolveFrom(context),
              size: 20,
            ),
      child: const AiChatConversationPage(embedInDrawer: true),
    );
  }
}
