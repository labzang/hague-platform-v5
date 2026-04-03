// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'ai_chat_providers.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

String _$llmApiKeyHash() => r'7ea256b57e9ffa74a0be042bf106d51d4ee0046d';

/// `--dart-define=LLM_API_KEY=sk-...` 로 주입. 비어 있으면 데모 응답만 사용.
///
/// Copied from [llmApiKey].
@ProviderFor(llmApiKey)
final llmApiKeyProvider = AutoDisposeProvider<String>.internal(
  llmApiKey,
  name: r'llmApiKeyProvider',
  debugGetCreateSourceHash: const bool.fromEnvironment('dart.vm.product')
      ? null
      : _$llmApiKeyHash,
  dependencies: null,
  allTransitiveDependencies: null,
);

@Deprecated('Will be removed in 3.0. Use Ref instead')
// ignore: unused_element
typedef LlmApiKeyRef = AutoDisposeProviderRef<String>;
String _$aiChatConversationHash() =>
    r'87241ffed1c7ccdd3f0f542c083576634e70476b';

/// See also [AiChatConversation].
@ProviderFor(AiChatConversation)
final aiChatConversationProvider =
    AutoDisposeNotifierProvider<AiChatConversation, AiChatState>.internal(
      AiChatConversation.new,
      name: r'aiChatConversationProvider',
      debugGetCreateSourceHash: const bool.fromEnvironment('dart.vm.product')
          ? null
          : _$aiChatConversationHash,
      dependencies: null,
      allTransitiveDependencies: null,
    );

typedef _$AiChatConversation = AutoDisposeNotifier<AiChatState>;
// ignore_for_file: type=lint
// ignore_for_file: subtype_of_sealed_class, invalid_use_of_internal_member, invalid_use_of_visible_for_testing_member, deprecated_member_use_from_same_package
