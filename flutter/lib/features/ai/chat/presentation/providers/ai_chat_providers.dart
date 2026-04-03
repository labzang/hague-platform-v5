import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:labzang_app/features/ai/chat/domain/entities/chat_message.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'ai_chat_providers.g.dart';

/// `--dart-define=LLM_API_KEY=sk-...` 로 주입. 비어 있으면 데모 응답만 사용.
@riverpod
String llmApiKey(Ref ref) {
  return const String.fromEnvironment('LLM_API_KEY', defaultValue: '');
}

class AiChatState {
  const AiChatState({
    this.messages = const [],
    this.isAwaitingReply = false,
  });

  final List<ChatMessage> messages;
  final bool isAwaitingReply;

  AiChatState copyWith({
    List<ChatMessage>? messages,
    bool? isAwaitingReply,
  }) {
    return AiChatState(
      messages: messages ?? this.messages,
      isAwaitingReply: isAwaitingReply ?? this.isAwaitingReply,
    );
  }
}

@riverpod
class AiChatConversation extends _$AiChatConversation {
  @override
  AiChatState build() {
    return AiChatState(
      messages: [
        ChatMessage.assistant(
          '안녕하세요! Labzang AI 채팅입니다.\n'
          '메시지를 보내보세요. LLM API 키를 설정하면 실제 모델 응답으로 전환할 수 있어요.',
        ),
      ],
    );
  }

  Future<void> sendUserMessage(String raw) async {
    final text = raw.trim();
    if (text.isEmpty || state.isAwaitingReply) return;

    state = state.copyWith(
      messages: [...state.messages, ChatMessage.user(text)],
      isAwaitingReply: true,
    );

    try {
      final reply = await _resolveAssistantReply(text);
      state = state.copyWith(
        messages: [...state.messages, ChatMessage.assistant(reply)],
        isAwaitingReply: false,
      );
    } catch (e) {
      state = state.copyWith(
        messages: [
          ...state.messages,
          ChatMessage.assistant('오류가 발생했습니다: $e'),
        ],
        isAwaitingReply: false,
      );
    }
  }

  /// 키 유무에 따라 데모 / 향후 실제 LLM HTTP 호출 분기
  Future<String> _resolveAssistantReply(String userText) async {
    await Future<void>.delayed(const Duration(milliseconds: 450));

    final key = ref.read(llmApiKeyProvider);
    if (key.isEmpty) {
      return '[데모 응답]\n'
          '질문: "$userText"\n\n'
          '실제 대화를 쓰려면 빌드 시 다음을 지정하세요:\n'
          'flutter run --dart-define=LLM_API_KEY=your_key\n\n'
          '연결 후 이 메서드에서 백엔드 또는 OpenAI 호환 API를 호출하면 됩니다.';
    }

    // TODO: LLM_API_KEY 가 있을 때 Dio 등으로 `/v1/chat/completions` 또는 백엔드 프록시 호출
    return '[LLM 키 감지됨]\n'
        '여기서 API를 호출해 응답 문자열을 반환하도록 연결하세요.\n'
        '사용자 입력: $userText';
  }
}
