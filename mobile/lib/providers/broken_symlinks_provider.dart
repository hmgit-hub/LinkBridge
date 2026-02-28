import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:linkbridge/services/link_service.dart';
import 'package:linkbridge/services/notification_service.dart';

part 'broken_symlinks_provider.g.dart';

@riverpod
class BrokenSymlinks extends _$BrokenSymlinks {
  @override
  Future<List<String>> build() async {
    final linkService = ref.read(linkServiceProvider);
    return await linkService.checkBrokenSymlinks('/');
  }

  Future<void> check(String path) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final linkService = ref.read(linkServiceProvider);
      final notificationService = ref.read(notificationServiceProvider);

      final brokenSymlinks = await linkService.checkBrokenSymlinks(path);

      if (brokenSymlinks.isNotEmpty) {
        await notificationService.showBrokenSymlinkNotification(brokenSymlinks.length);
      }

      return brokenSymlinks;
    });
  }
}
