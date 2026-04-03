import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart'
    show
        BorderSide,
        Colors,
        InputBorder,
        InputDecoration,
        Material,
        OutlineInputBorder,
        TextField,
        TextStyle;
import 'package:flutter/scheduler.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:labzang_app/features/ai/chat/presentation/providers/ai_chat_providers.dart';
import 'package:labzang_app/features/ai/chat/presentation/widgets/chat_message_bubble.dart';

/// AI와 1:1 채팅 — LLM 키 연동 시 [_resolveAssistantReply] 에서 API 호출만 붙이면 됨.
/// [embedInDrawer]: true이면 공통 서랍 레이아웃 안에서만 쓰고 자체 네비게이션 바를 만들지 않습니다.
class AiChatConversationPage extends ConsumerStatefulWidget {
  const AiChatConversationPage({super.key, this.embedInDrawer = false});

  final bool embedInDrawer;

  @override
  ConsumerState<AiChatConversationPage> createState() =>
      _AiChatConversationPageState();
}

class _AiChatConversationPageState
    extends ConsumerState<AiChatConversationPage> {
  final _textController = TextEditingController();
  final _scrollController = ScrollController();
  final _inputFocusNode = FocusNode();

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    _inputFocusNode.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    SchedulerBinding.instance.addPostFrameCallback((_) {
      if (!_scrollController.hasClients) return;
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: const Duration(milliseconds: 280),
        curve: Curves.easeOutCubic,
      );
    });
  }

  Future<void> _onSend() async {
    final text = _textController.text.trim();
    if (text.isEmpty) return;
    if (ref.read(aiChatConversationProvider).isAwaitingReply) return;

    // Android 한글 IME: clear 직후 조합 세션이 깨져 '한' 등이 떠다니거나
    // 다음 입력이 안 될 수 있음 → 전송 후 한 프레임 뒤 다시 포커스.
    _textController.clear();
    await ref.read(aiChatConversationProvider.notifier).sendUserMessage(text);
    if (!mounted) return;
    _scrollToBottom();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      _inputFocusNode.requestFocus();
    });
  }

  @override
  Widget build(BuildContext context) {
    final chat = ref.watch(aiChatConversationProvider);
    final key = ref.watch(llmApiKeyProvider);
    final hasKey = key.isNotEmpty;

    ref.listen<AiChatState>(aiChatConversationProvider, (prev, next) {
      if (prev?.messages.length != next.messages.length ||
          prev?.isAwaitingReply != next.isAwaitingReply) {
        _scrollToBottom();
      }
    });

    final bottomInset = MediaQuery.viewInsetsOf(context).bottom;

    final column = Column(
      children: [
        if (!hasKey)
          Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
            decoration: BoxDecoration(
              color: CupertinoColors.systemYellow.resolveFrom(context),
            ),
            child: const Text(
              'LLM API 키가 없으면 데모 응답만 표시됩니다. '
              'flutter run --dart-define=LLM_API_KEY=... 로 연결하세요.',
              style: TextStyle(fontSize: 13, height: 1.25),
            ),
          ),
        Expanded(
          child: ListView.builder(
            controller: _scrollController,
            padding: const EdgeInsets.only(top: 8, bottom: 12),
            itemCount: chat.messages.length + (chat.isAwaitingReply ? 1 : 0),
            itemBuilder: (context, index) {
              if (chat.isAwaitingReply && index == chat.messages.length) {
                return const Padding(
                  padding: EdgeInsets.all(16),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: CupertinoActivityIndicator(),
                  ),
                );
              }
              return ChatMessageBubble(message: chat.messages[index]);
            },
          ),
        ),
        AnimatedPadding(
          padding: EdgeInsets.only(bottom: bottomInset),
          duration: const Duration(milliseconds: 120),
          curve: Curves.easeOut,
          child: Container(
            decoration: BoxDecoration(
              color: CupertinoColors.systemBackground.resolveFrom(context),
              border: Border(
                top: BorderSide(
                  color: CupertinoColors.separator.resolveFrom(context),
                ),
              ),
            ),
            padding: const EdgeInsets.fromLTRB(12, 8, 12, 8),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Expanded(
                  child: Material(
                    color: Colors.transparent,
                    child: TextField(
                      controller: _textController,
                      focusNode: _inputFocusNode,
                      keyboardType: TextInputType.text,
                      textInputAction: TextInputAction.send,
                      maxLines: 1,
                      autocorrect: true,
                      enableSuggestions: true,
                      textAlignVertical: TextAlignVertical.center,
                      style: TextStyle(
                        color: CupertinoColors.label.resolveFrom(context),
                        fontSize: 17,
                        height: 1.25,
                      ),
                      decoration: InputDecoration(
                        hintText: '메시지를 입력하세요…',
                        hintStyle: TextStyle(
                          color: CupertinoColors.placeholderText
                              .resolveFrom(context),
                        ),
                        filled: true,
                        fillColor: CupertinoColors.systemGrey6
                            .resolveFrom(context),
                        border: InputBorder.none,
                        enabledBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(20),
                          borderSide: BorderSide.none,
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(20),
                          borderSide: BorderSide.none,
                        ),
                        contentPadding: const EdgeInsets.symmetric(
                          horizontal: 14,
                          vertical: 10,
                        ),
                        isDense: true,
                      ),
                      onSubmitted: (_) => _onSend(),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                CupertinoButton(
                  padding: EdgeInsets.zero,
                  onPressed: chat.isAwaitingReply ? null : _onSend,
                  child: Icon(
                    CupertinoIcons.arrow_up_circle_fill,
                    size: 36,
                    color: chat.isAwaitingReply
                        ? CupertinoColors.inactiveGray
                        : CupertinoColors.activeBlue,
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );

    if (widget.embedInDrawer) {
      return column;
    }

    return CupertinoPageScaffold(
      backgroundColor:
          CupertinoColors.systemGroupedBackground.resolveFrom(context),
      navigationBar: CupertinoNavigationBar(
        middle: const Text('AI 채팅'),
        border: null,
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
      ),
      child: SafeArea(child: column),
    );
  }
}
