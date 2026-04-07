import 'package:dio/dio.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart' show Scrollbar;
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:labzang_app/core/theme/app_theme.dart';
import 'package:labzang_app/features/ext/guard/data/local_signup_credentials_store.dart';
import 'package:labzang_app/features/ext/guard/domain/entities/register_user_params.dart';
import 'package:labzang_app/features/ext/guard/presentation/providers/auth_providers.dart';

/// 회원가입 — 이름, 생년월일, 성별, 연락처(인증), 주소 찾기, 아이디·비밀번호·이메일.
/// 전화 인증·주소 검색은 개발용 목업(실서비스 시 API 교체).
/// Backend: `labzang.apps.ext.guard`
class SignupPage extends ConsumerStatefulWidget {
  const SignupPage({super.key});

  @override
  ConsumerState<SignupPage> createState() => _SignupPageState();
}

class _SignupPageState extends ConsumerState<SignupPage> {
  final ScrollController _scrollController = ScrollController();

  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _phoneController = TextEditingController();
  final TextEditingController _codeController = TextEditingController();
  final TextEditingController _addressDetailController =
      TextEditingController();
  final TextEditingController _idController = TextEditingController();
  final TextEditingController _pwController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();

  DateTime? _birthDate;
  int _genderIndex = 0;
  bool _obscurePassword = true;

  bool _phoneVerified = false;
  String? _selectedRoadAddress;

  static const List<String> _genderLabels = <String>['남성', '여성'];

  /// 인증요청·확인 버튼 동일 너비 → 양쪽 `Expanded` 입력창 너비 정렬.
  static const double _phoneAuthButtonWidth = 104;

  /// 개발용 고정 인증번호 (SMS API 연동 전).
  static const String _devAuthCode = '123456';

  @override
  void dispose() {
    _scrollController.dispose();
    _nameController.dispose();
    _phoneController.dispose();
    _codeController.dispose();
    _addressDetailController.dispose();
    _idController.dispose();
    _pwController.dispose();
    _emailController.dispose();
    super.dispose();
  }

  String _phoneDigitsOnly(String s) {
    return s.replaceAll(RegExp(r'\D'), '');
  }

  bool _isKoreanMobileLength(String digits) {
    return digits.length == 10 || digits.length == 11;
  }

  BoxDecoration _fieldDecoration(BuildContext context) {
    final Color border = CupertinoColors.label.resolveFrom(context)
        .withValues(alpha: 0.58);
    return BoxDecoration(
      color: CupertinoColors.systemBackground.resolveFrom(context),
      borderRadius: BorderRadius.circular(12),
      border: Border.all(color: border, width: 2),
    );
  }

  String _birthDisplayText() {
    if (_birthDate == null) {
      return '생년월일을 선택하세요';
    }
    final DateTime d = _birthDate!;
    return '${d.year}년 ${d.month}월 ${d.day}일';
  }

  String _addressMainDisplay() {
    return _selectedRoadAddress ?? '주소 찾기를 눌러 도로명 주소를 선택하세요';
  }

  Future<void> _pickBirthDate() async {
    DateTime temp = _birthDate ?? DateTime(2000, 1, 1);
    final DateTime now = DateTime.now();
    final DateTime last = DateTime(now.year, now.month, now.day);

    await showCupertinoModalPopup<void>(
      context: context,
      builder: (BuildContext ctx) {
        return StatefulBuilder(
          builder: (BuildContext context, void Function(void Function()) setModalState) {
            final Color bg =
                CupertinoColors.systemBackground.resolveFrom(context);
            return Container(
              decoration: BoxDecoration(
                color: bg,
                borderRadius: const BorderRadius.vertical(
                  top: Radius.circular(14),
                ),
              ),
              child: SafeArea(
                top: false,
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        CupertinoButton(
                          onPressed: () => Navigator.of(ctx).pop(),
                          child: const Text('취소'),
                        ),
                        CupertinoButton(
                          onPressed: () {
                            setState(() => _birthDate = temp);
                            Navigator.of(ctx).pop();
                          },
                          child: const Text(
                            '완료',
                            style: TextStyle(fontWeight: FontWeight.w600),
                          ),
                        ),
                      ],
                    ),
                    SizedBox(
                      height: 216,
                      child: CupertinoDatePicker(
                        mode: CupertinoDatePickerMode.date,
                        initialDateTime: temp,
                        minimumDate: DateTime(1900, 1, 1),
                        maximumDate: last,
                        onDateTimeChanged: (DateTime d) {
                          setModalState(() => temp = d);
                        },
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        );
      },
    );
  }

  Future<void> _sendVerificationCode() async {
    final String digits = _phoneDigitsOnly(_phoneController.text);
    if (!_isKoreanMobileLength(digits)) {
      await _alert('휴대폰 번호 10~11자리를 입력해 주세요.');
      return;
    }
    setState(() {
      _phoneVerified = false;
      _codeController.clear();
    });
    if (!mounted) return;
    await showCupertinoDialog<void>(
      context: context,
      builder: (BuildContext context) => CupertinoAlertDialog(
        title: const Text('인증번호 발송'),
        content: Text(
          '개발용: 인증번호는 $_devAuthCode 입니다.\n'
          '(실서비스에서는 SMS로 발송됩니다.)',
        ),
        actions: [
          CupertinoDialogAction(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('확인'),
          ),
        ],
      ),
    );
  }

  Future<void> _confirmVerificationCode() async {
    final String digits = _phoneDigitsOnly(_phoneController.text);
    if (!_isKoreanMobileLength(digits)) {
      await _alert('먼저 올바른 휴대폰 번호를 입력하고 인증번호를 받아 주세요.');
      return;
    }
    if (_codeController.text.trim() == _devAuthCode) {
      setState(() => _phoneVerified = true);
      await _alert('휴대폰 인증이 완료되었습니다.');
    } else {
      setState(() => _phoneVerified = false);
      await _alert('인증번호가 올바르지 않습니다.\n(개발용: $_devAuthCode)');
    }
  }

  Future<void> _openAddressFinder() async {
    final String? picked = await showCupertinoModalPopup<String>(
      context: context,
      builder: (BuildContext context) => const _AddressSearchSheet(),
    );
    if (picked != null && picked.isNotEmpty) {
      setState(() => _selectedRoadAddress = picked);
    }
  }

  bool _looksLikeEmail(String s) {
    return RegExp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$').hasMatch(s);
  }

  Future<void> _submit() async {
    final String name = _nameController.text.trim();
    final String id = _idController.text.trim();
    final String pw = _pwController.text;
    final String email = _emailController.text.trim();
    final String phone = _phoneDigitsOnly(_phoneController.text);
    final String addrDetail = _addressDetailController.text.trim();

    if (name.isEmpty) {
      await _alert('이름을 입력해 주세요.');
      return;
    }
    if (_birthDate == null) {
      await _alert('생년월일을 선택해 주세요.');
      return;
    }
    if (!_isKoreanMobileLength(phone)) {
      await _alert('휴대폰 번호를 입력해 주세요.');
      return;
    }
    if (!_phoneVerified) {
      await _alert('휴대폰 인증을 완료해 주세요.');
      return;
    }
    if (_selectedRoadAddress == null || _selectedRoadAddress!.isEmpty) {
      await _alert('주소 찾기로 도로명 주소를 선택해 주세요.');
      return;
    }
    if (id.isEmpty) {
      await _alert('아이디를 입력해 주세요.');
      return;
    }
    if (pw.isEmpty) {
      await _alert('비밀번호를 입력해 주세요.');
      return;
    }
    if (email.isEmpty || !_looksLikeEmail(email)) {
      await _alert('올바른 이메일을 입력해 주세요.');
      return;
    }

    final String gender = _genderLabels[_genderIndex];
    final RegisterUserParams params = RegisterUserParams(
      username: id,
      password: pw,
      name: name,
      email: email,
      phone: phone,
      birthDate: _birthDate!,
      gender: gender,
      addressMain: _selectedRoadAddress!,
      addressDetail: addrDetail,
    );

    try {
      await ref.read(registerUserUsecaseProvider).call(params);
    } on DioException catch (e) {
      await _alert(e.message ?? '서버 회원가입에 실패했습니다.');
      return;
    }

    final LocalSignupCredentialsStore store =
        await LocalSignupCredentialsStore.open();
    await store.saveFromSignup(
      userId: id,
      password: pw,
      name: name,
      email: email,
      birthDate: _birthDate!,
      genderLabel: gender,
      phone: phone,
      addressMain: _selectedRoadAddress!,
      addressDetail: addrDetail,
    );

    if (!mounted) return;
    await showCupertinoDialog<void>(
      context: context,
      builder: (BuildContext context) => CupertinoAlertDialog(
        title: const Text('가입 요약'),
        content: Text(
          '이름: $name\n'
          '생년월일: ${_birthDisplayText()}\n'
          '성별: $gender\n'
          '휴대폰: $phone\n'
          '주소: $_selectedRoadAddress\n'
          '${addrDetail.isNotEmpty ? "상세: $addrDetail\n" : ""}'
          '아이디: $id\n'
          '이메일: $email\n\n'
          '서버에 저장되었습니다 (role: customer).\n'
          '로컬 임시저장으로 동일 계정 로그인도 가능합니다.\n'
          '(개발용)',
        ),
        actions: [
          CupertinoDialogAction(
            onPressed: () {
              Navigator.of(context).pop();
              context.pop();
            },
            child: const Text('확인'),
          ),
        ],
      ),
    );
  }

  Future<void> _alert(String message) async {
    if (!mounted) return;
    await showCupertinoDialog<void>(
      context: context,
      builder: (BuildContext context) => CupertinoAlertDialog(
        content: Text(message),
        actions: [
          CupertinoDialogAction(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('확인'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final Color label = CupertinoColors.label.resolveFrom(context);
    final Color secondary = CupertinoColors.secondaryLabel.resolveFrom(context);
    final double bottomInset = MediaQuery.viewInsetsOf(context).bottom;

    return CupertinoPageScaffold(
      backgroundColor:
          CupertinoColors.systemGroupedBackground.resolveFrom(context),
      navigationBar: CupertinoNavigationBar(
        border: null,
        backgroundColor:
            CupertinoColors.systemBackground.resolveFrom(context),
        leading: CupertinoNavigationBarBackButton(
          onPressed: () => context.pop(),
        ),
        middle: const Text('회원가입'),
      ),
      child: SafeArea(
        top: false,
        child: Scrollbar(
          controller: _scrollController,
          thumbVisibility: true,
          thickness: 6,
          radius: const Radius.circular(8),
          child: SingleChildScrollView(
            controller: _scrollController,
            padding: EdgeInsets.fromLTRB(24, 16, 16, 24 + bottomInset),
            keyboardDismissBehavior: ScrollViewKeyboardDismissBehavior.onDrag,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  '랩장 아카데미',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.w800,
                    color: label,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  '필수 정보를 입력해 주세요',
                  style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w500,
                    color: secondary,
                  ),
                ),
                const SizedBox(height: 22),
                CupertinoTextField(
                  controller: _nameController,
                  placeholder: '이름',
                  padding: const EdgeInsets.symmetric(
                    horizontal: 14,
                    vertical: 14,
                  ),
                  decoration: _fieldDecoration(context),
                  textInputAction: TextInputAction.next,
                ),
                const SizedBox(height: 14),
                GestureDetector(
                  onTap: _pickBirthDate,
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 14,
                      vertical: 16,
                    ),
                    decoration: _fieldDecoration(context),
                    child: Row(
                      children: [
                        Expanded(
                          child: Text(
                            _birthDisplayText(),
                            style: TextStyle(
                              fontSize: 17,
                              color: _birthDate == null
                                  ? CupertinoColors.placeholderText
                                      .resolveFrom(context)
                                  : label,
                            ),
                          ),
                        ),
                        Icon(
                          CupertinoIcons.calendar,
                          size: 22,
                          color: secondary,
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 14),
                Text(
                  '성별',
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: secondary,
                  ),
                ),
                const SizedBox(height: 8),
                CupertinoSlidingSegmentedControl<int>(
                  groupValue: _genderIndex,
                  thumbColor: CupertinoColors.white,
                  backgroundColor: CupertinoColors.systemGrey5.resolveFrom(
                    context,
                  ),
                  onValueChanged: (int? value) {
                    if (value != null) {
                      setState(() => _genderIndex = value);
                    }
                  },
                  children: <int, Widget>{
                    0: Padding(
                      padding: const EdgeInsets.symmetric(vertical: 10),
                      child: Text(
                        _genderLabels[0],
                        style: TextStyle(
                          fontWeight: FontWeight.w600,
                          color: _genderIndex == 0
                              ? AppBrand.purple
                              : label,
                        ),
                      ),
                    ),
                    1: Padding(
                      padding: const EdgeInsets.symmetric(vertical: 10),
                      child: Text(
                        _genderLabels[1],
                        style: TextStyle(
                          fontWeight: FontWeight.w600,
                          color: _genderIndex == 1
                              ? AppBrand.purple
                              : label,
                        ),
                      ),
                    ),
                  },
                ),
                const SizedBox(height: 18),
                Text(
                  '휴대폰',
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: secondary,
                  ),
                ),
                const SizedBox(height: 8),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(
                      child: CupertinoTextField(
                        controller: _phoneController,
                        placeholder: '01012345678',
                        padding: const EdgeInsets.symmetric(
                          horizontal: 14,
                          vertical: 14,
                        ),
                        decoration: _fieldDecoration(context),
                        keyboardType: TextInputType.phone,
                        inputFormatters: <TextInputFormatter>[
                          FilteringTextInputFormatter.digitsOnly,
                          LengthLimitingTextInputFormatter(11),
                        ],
                        onChanged: (_) {
                          if (_phoneVerified) {
                            setState(() => _phoneVerified = false);
                          }
                        },
                      ),
                    ),
                    const SizedBox(width: 10),
                    SizedBox(
                      width: _phoneAuthButtonWidth,
                      child: CupertinoButton(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 8,
                          vertical: 12,
                        ),
                        color: AppBrand.purpleMuted,
                        borderRadius: BorderRadius.circular(12),
                        onPressed: _sendVerificationCode,
                        child: Text(
                          '인증요청',
                          textAlign: TextAlign.center,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w700,
                            color: AppBrand.purple,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(
                      child: CupertinoTextField(
                        controller: _codeController,
                        placeholder: '인증번호 6자리',
                        padding: const EdgeInsets.symmetric(
                          horizontal: 14,
                          vertical: 14,
                        ),
                        decoration: _fieldDecoration(context),
                        keyboardType: TextInputType.number,
                        inputFormatters: <TextInputFormatter>[
                          FilteringTextInputFormatter.digitsOnly,
                          LengthLimitingTextInputFormatter(6),
                        ],
                      ),
                    ),
                    const SizedBox(width: 10),
                    SizedBox(
                      width: _phoneAuthButtonWidth,
                      child: CupertinoButton(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 8,
                          vertical: 12,
                        ),
                        color: _phoneVerified
                            ? AppBrand.greenMuted
                            : CupertinoColors.systemGrey5.resolveFrom(context),
                        borderRadius: BorderRadius.circular(12),
                        onPressed: _confirmVerificationCode,
                        child: Text(
                          _phoneVerified ? '완료' : '확인',
                          textAlign: TextAlign.center,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w700,
                            color: _phoneVerified
                                ? AppBrand.green
                                : label,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
                if (_phoneVerified)
                  Padding(
                    padding: const EdgeInsets.only(top: 6),
                    child: Text(
                      '휴대폰 인증 완료',
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: AppBrand.green,
                      ),
                    ),
                  ),
                const SizedBox(height: 18),
                Text(
                  '주소',
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: secondary,
                  ),
                ),
                const SizedBox(height: 8),
                GestureDetector(
                  onTap: _openAddressFinder,
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 14,
                      vertical: 16,
                    ),
                    decoration: _fieldDecoration(context),
                    child: Row(
                      children: [
                        Expanded(
                          child: Text(
                            _addressMainDisplay(),
                            style: TextStyle(
                              fontSize: 16,
                              height: 1.25,
                              color: _selectedRoadAddress == null
                                  ? CupertinoColors.placeholderText
                                      .resolveFrom(context)
                                  : label,
                            ),
                          ),
                        ),
                        Icon(
                          CupertinoIcons.search,
                          size: 22,
                          color: AppBrand.purple,
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 8),
                CupertinoButton(
                  padding: const EdgeInsets.symmetric(vertical: 4),
                  onPressed: _openAddressFinder,
                  child: const Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      '주소 찾기',
                      style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 6),
                CupertinoTextField(
                  controller: _addressDetailController,
                  placeholder: '상세주소 (동·호수 등)',
                  padding: const EdgeInsets.symmetric(
                    horizontal: 14,
                    vertical: 14,
                  ),
                  decoration: _fieldDecoration(context),
                  textInputAction: TextInputAction.next,
                ),
                const SizedBox(height: 14),
                CupertinoTextField(
                  controller: _idController,
                  placeholder: '아이디',
                  padding: const EdgeInsets.symmetric(
                    horizontal: 14,
                    vertical: 14,
                  ),
                  decoration: _fieldDecoration(context),
                  autocorrect: false,
                  textInputAction: TextInputAction.next,
                ),
                const SizedBox(height: 14),
                CupertinoTextField(
                  controller: _pwController,
                  placeholder: '비밀번호',
                  obscureText: _obscurePassword,
                  padding: const EdgeInsets.symmetric(
                    horizontal: 14,
                    vertical: 14,
                  ),
                  decoration: _fieldDecoration(context),
                  textInputAction: TextInputAction.next,
                  suffix: Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: CupertinoButton(
                      padding: EdgeInsets.zero,
                      minimumSize: Size.zero,
                      onPressed: () {
                        setState(() => _obscurePassword = !_obscurePassword);
                      },
                      child: Icon(
                        _obscurePassword
                            ? CupertinoIcons.eye_slash
                            : CupertinoIcons.eye,
                        size: 22,
                        color: secondary,
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 14),
                CupertinoTextField(
                  controller: _emailController,
                  placeholder: '이메일',
                  padding: const EdgeInsets.symmetric(
                    horizontal: 14,
                    vertical: 14,
                  ),
                  decoration: _fieldDecoration(context),
                  keyboardType: TextInputType.emailAddress,
                  autocorrect: false,
                  textInputAction: TextInputAction.done,
                  onSubmitted: (_) => _submit(),
                ),
                const SizedBox(height: 28),
                CupertinoButton.filled(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  borderRadius: BorderRadius.circular(12),
                  onPressed: _submit,
                  child: const Text(
                    '가입하기',
                    style: TextStyle(
                      fontSize: 17,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

/// 우편번호/도로명 검색 UI와 유사한 목록 선택 (키워드 필터).
class _AddressSearchSheet extends StatefulWidget {
  const _AddressSearchSheet();

  static const List<String> mockRoadAddresses = <String>[
    '서울특별시 강남구 테헤란로 152 (역삼동, 강남파이낸스센터)',
    '서울특별시 종로구 세종대로 209 (세종로, 정부서울청사)',
    '서울특별시 마포구 월드컵북로 396 (상암동, 누리꿈스퀘어)',
    '부산광역시 해운대구 해운대해변로 264 (우동)',
    '대구광역시 중구 동성로 123 (동성로)',
    '경기도 성남시 분당구 판교역로 235 (삼평동)',
    '인천광역시 연수구 컨벤시아대로 165 (송도동)',
    '제주특별자치도 제주시 연동 123-45',
  ];

  @override
  State<_AddressSearchSheet> createState() => _AddressSearchSheetState();
}

class _AddressSearchSheetState extends State<_AddressSearchSheet> {
  final TextEditingController _query = TextEditingController();

  @override
  void dispose() {
    _query.dispose();
    super.dispose();
  }

  List<String> get _filtered {
    final String q = _query.text.trim();
    if (q.isEmpty) {
      return _AddressSearchSheet.mockRoadAddresses;
    }
    return _AddressSearchSheet.mockRoadAddresses
        .where((String e) => e.contains(q))
        .toList();
  }

  @override
  Widget build(BuildContext context) {
    final Color label = CupertinoColors.label.resolveFrom(context);
    final Color secondary = CupertinoColors.secondaryLabel.resolveFrom(context);
    final double h = MediaQuery.sizeOf(context).height * 0.72;

    return Container(
      height: h,
      decoration: BoxDecoration(
        color: CupertinoColors.systemBackground.resolveFrom(context),
        borderRadius: const BorderRadius.vertical(top: Radius.circular(14)),
      ),
      child: SafeArea(
        top: false,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(8, 8, 8, 0),
              child: Row(
                children: [
                  CupertinoButton(
                    onPressed: () => Navigator.of(context).pop(),
                    child: const Text('닫기'),
                  ),
                  const Expanded(
                    child: Text(
                      '주소 찾기',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                  const SizedBox(width: 64),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 8),
              child: CupertinoSearchTextField(
                controller: _query,
                placeholder: '도로명·지번·건물명 검색 (목업)',
                onChanged: (_) => setState(() {}),
              ),
            ),
            Expanded(
              child: _filtered.isEmpty
                  ? Center(
                      child: Text(
                        '검색 결과가 없습니다.\n다른 키워드를 입력해 보세요.',
                        textAlign: TextAlign.center,
                        style: TextStyle(color: secondary),
                      ),
                    )
                  : ListView.separated(
                      padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
                      itemCount: _filtered.length,
                      separatorBuilder: (_, _) => const SizedBox(height: 6),
                      itemBuilder: (BuildContext context, int i) {
                        final String line = _filtered[i];
                        return CupertinoButton(
                          padding: EdgeInsets.zero,
                          onPressed: () => Navigator.of(context).pop(line),
                          child: Container(
                            width: double.infinity,
                            alignment: Alignment.centerLeft,
                            padding: const EdgeInsets.symmetric(
                              horizontal: 14,
                              vertical: 14,
                            ),
                            decoration: BoxDecoration(
                              border: Border.all(
                                color: CupertinoColors.separator
                                    .resolveFrom(context),
                              ),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text(
                              line,
                              style: TextStyle(
                                fontSize: 15,
                                height: 1.3,
                                color: label,
                              ),
                            ),
                          ),
                        );
                      },
                    ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
              child: Text(
                '실서비스에서는 다음·카카오 등 주소 API를 연동합니다.',
                style: TextStyle(fontSize: 12, color: secondary),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
