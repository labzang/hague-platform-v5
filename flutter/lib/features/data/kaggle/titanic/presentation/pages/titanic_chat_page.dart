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
import 'package:labzang_app/features/ai/chat/domain/entities/chat_message.dart';
import 'package:labzang_app/features/ai/chat/presentation/widgets/chat_message_bubble.dart';
import 'package:labzang_app/shared/widgets/app_drawer_layout.dart';

/// Titanic 대회 Q&A (샘플) — `labzang.apps.data.kaggle` 하위 competition 모듈.
class TitanicChatPage extends StatefulWidget {
  const TitanicChatPage({super.key});

  @override
  State<TitanicChatPage> createState() => _TitanicChatPageState();
}

class _TitanicChatPageState extends State<TitanicChatPage> {
  final _textController = TextEditingController();
  final _scrollController = ScrollController();
  final _inputFocusNode = FocusNode();
  bool _isThinking = false;

  final List<ChatMessage> _messages = <ChatMessage>[
    ChatMessage.assistant(
      'Titanic 데이터셋 Q&A에 오신 것을 환영합니다.\n'
      '예: 생존 예측에 중요한 피처, 전처리 방법, 베이스라인 모델 추천',
    ),
  ];

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
        duration: const Duration(milliseconds: 260),
        curve: Curves.easeOutCubic,
      );
    });
  }

  Future<void> _onSend() async {
    final question = _textController.text.trim();
    if (question.isEmpty || _isThinking) return;

    setState(() {
      _messages.add(ChatMessage.user(question));
      _textController.clear();
      _isThinking = true;
    });
    _scrollToBottom();

    await Future<void>.delayed(const Duration(milliseconds: 450));
    final answer = _buildTitanicAnswer(question);

    if (!mounted) return;
    setState(() {
      _messages.add(ChatMessage.assistant(answer));
      _isThinking = false;
    });
    _scrollToBottom();
    _inputFocusNode.requestFocus();
  }

  String _buildTitanicAnswer(String q) {
    final text = q.toLowerCase();
    if (text.contains('피처') || text.contains('feature')) {
      return 'Titanic에서 자주 쓰는 핵심 피처는 `Pclass`, `Sex`, `Age`, `Fare`, '
          '`Embarked`, `SibSp`, `Parch`, 그리고 `FamilySize=SibSp+Parch+1`입니다.';
    }
    if (text.contains('전처리') || text.contains('결측')) {
      return '대표 전처리:\n'
          '1) Age/Embarked 결측치 보간\n'
          '2) Sex/Embarked 범주형 인코딩\n'
          '3) Fare 로그 변환(선택)\n'
          '4) 학습/검증 분리 후 스케일링은 필요 모델에서만 적용';
    }
    if (text.contains('모델') || text.contains('baseline')) {
      return '베이스라인은 `LogisticRegression` 또는 `RandomForest`가 좋습니다.\n'
          '그 다음 `XGBoost/LightGBM`으로 성능을 올리는 흐름이 일반적입니다.';
    }
    if (text.contains('평가') || text.contains('metric')) {
      return 'Titanic 대회 기본 평가지표는 Accuracy입니다. '
          '교차검증으로 과적합 여부를 함께 확인하는 것을 권장합니다.';
    }
    return '질문 감사합니다. Titanic 관점에서 더 정확히 답하려면 '
        '사용 중인 피처셋, 전처리 방식, 모델 종류를 함께 알려주세요.';
  }

  @override
  Widget build(BuildContext context) {
    final bottomInset = MediaQuery.viewInsetsOf(context).bottom;
    final bg = CupertinoColors.systemGroupedBackground.resolveFrom(context);

    return AppDrawerLayout(
      title: 'Titanic Q&A',
      backgroundColor: bg,
      child: Column(
        children: [
          _TitanicHeroBanner(),
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.only(top: 8, bottom: 12),
              itemCount: _messages.length + (_isThinking ? 1 : 0),
              itemBuilder: (context, index) {
                if (_isThinking && index == _messages.length) {
                  return const Padding(
                    padding: EdgeInsets.all(16),
                    child: Align(
                      alignment: Alignment.centerLeft,
                      child: CupertinoActivityIndicator(),
                    ),
                  );
                }
                return ChatMessageBubble(message: _messages[index]);
              },
            ),
          ),
          AnimatedPadding(
            duration: const Duration(milliseconds: 120),
            curve: Curves.easeOut,
            padding: EdgeInsets.only(bottom: bottomInset),
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
                        decoration: InputDecoration(
                          hintText: '타이타닉 관련 질문을 입력하세요…',
                          filled: true,
                          fillColor:
                              CupertinoColors.systemGrey6.resolveFrom(context),
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
                        ),
                        style: TextStyle(
                          color: CupertinoColors.label.resolveFrom(context),
                          fontSize: 16,
                        ),
                        onSubmitted: (_) => _onSend(),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  CupertinoButton(
                    padding: EdgeInsets.zero,
                    onPressed: _isThinking ? null : _onSend,
                    child: Icon(
                      CupertinoIcons.arrow_up_circle_fill,
                      size: 36,
                      color: _isThinking
                          ? CupertinoColors.inactiveGray
                          : CupertinoColors.activeBlue,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _TitanicHeroBanner extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 210,
      width: double.infinity,
      child: Stack(
        fit: StackFit.expand,
        children: [
          Image.network(
            'https://images.unsplash.com/photo-1569263979104-865ab7cd8d13?auto=format&fit=crop&w=1200&q=80',
            fit: BoxFit.cover,
          ),
          DecoratedBox(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [
                  CupertinoColors.black.withValues(alpha: 0.55),
                  CupertinoColors.black.withValues(alpha: 0.25),
                ],
              ),
            ),
          ),
          const Padding(
            padding: EdgeInsets.fromLTRB(16, 16, 16, 12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'TITANIC MACHINE\nLEARNING PROJECT',
                  style: TextStyle(
                    color: CupertinoColors.white,
                    fontSize: 24,
                    fontWeight: FontWeight.w700,
                    height: 1.08,
                    letterSpacing: 0.4,
                  ),
                ),
                SizedBox(height: 8),
                Text(
                  'STEP-BY-STEP TUTORIAL IN #PYTHON',
                  style: TextStyle(
                    color: CupertinoColors.systemGrey4,
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                    letterSpacing: 0.8,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
