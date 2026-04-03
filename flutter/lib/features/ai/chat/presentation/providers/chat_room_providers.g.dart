// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'chat_room_providers.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

String _$chatRoomRemoteDataSourceHash() =>
    r'a4b6537cf0da75d9fb2f484ea2304061a01431e8';

/// See also [chatRoomRemoteDataSource].
@ProviderFor(chatRoomRemoteDataSource)
final chatRoomRemoteDataSourceProvider =
    AutoDisposeProvider<ChatRoomRemoteDataSource>.internal(
      chatRoomRemoteDataSource,
      name: r'chatRoomRemoteDataSourceProvider',
      debugGetCreateSourceHash: const bool.fromEnvironment('dart.vm.product')
          ? null
          : _$chatRoomRemoteDataSourceHash,
      dependencies: null,
      allTransitiveDependencies: null,
    );

@Deprecated('Will be removed in 3.0. Use Ref instead')
// ignore: unused_element
typedef ChatRoomRemoteDataSourceRef =
    AutoDisposeProviderRef<ChatRoomRemoteDataSource>;
String _$chatRoomRepositoryHash() =>
    r'1f43a73884d6826db9f9fea1c32a465105baf621';

/// See also [chatRoomRepository].
@ProviderFor(chatRoomRepository)
final chatRoomRepositoryProvider =
    AutoDisposeProvider<ChatRoomRepository>.internal(
      chatRoomRepository,
      name: r'chatRoomRepositoryProvider',
      debugGetCreateSourceHash: const bool.fromEnvironment('dart.vm.product')
          ? null
          : _$chatRoomRepositoryHash,
      dependencies: null,
      allTransitiveDependencies: null,
    );

@Deprecated('Will be removed in 3.0. Use Ref instead')
// ignore: unused_element
typedef ChatRoomRepositoryRef = AutoDisposeProviderRef<ChatRoomRepository>;
String _$getChatRoomsHash() => r'2caef13809d0c5e1f2797db9e5cc909de1c17ee8';

/// See also [getChatRooms].
@ProviderFor(getChatRooms)
final getChatRoomsProvider = AutoDisposeProvider<GetChatRooms>.internal(
  getChatRooms,
  name: r'getChatRoomsProvider',
  debugGetCreateSourceHash: const bool.fromEnvironment('dart.vm.product')
      ? null
      : _$getChatRoomsHash,
  dependencies: null,
  allTransitiveDependencies: null,
);

@Deprecated('Will be removed in 3.0. Use Ref instead')
// ignore: unused_element
typedef GetChatRoomsRef = AutoDisposeProviderRef<GetChatRooms>;
String _$chatRoomsHash() => r'4e9d0098b99f5cc5acef63ead002e9dc59639af8';

/// See also [chatRooms].
@ProviderFor(chatRooms)
final chatRoomsProvider = AutoDisposeFutureProvider<List<ChatRoom>>.internal(
  chatRooms,
  name: r'chatRoomsProvider',
  debugGetCreateSourceHash: const bool.fromEnvironment('dart.vm.product')
      ? null
      : _$chatRoomsHash,
  dependencies: null,
  allTransitiveDependencies: null,
);

@Deprecated('Will be removed in 3.0. Use Ref instead')
// ignore: unused_element
typedef ChatRoomsRef = AutoDisposeFutureProviderRef<List<ChatRoom>>;
// ignore_for_file: type=lint
// ignore_for_file: subtype_of_sealed_class, invalid_use_of_internal_member, invalid_use_of_visible_for_testing_member, deprecated_member_use_from_same_package
