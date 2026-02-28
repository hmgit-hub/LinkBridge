import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:linkbridge/models/file_item.dart';
import 'package:linkbridge/services/link_service.dart';
import 'package:linkbridge/services/hive_service.dart';

part 'file_list_provider.g.dart';

@riverpod
class FileList extends _$FileList {
  @override
  Future<List<FileItem>> build() async {
    final linkService = ref.read(linkServiceProvider);
    return await linkService.listDirectory('/');
  }

  Future<void> refresh(String path) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final linkService = ref.read(linkServiceProvider);
      final hiveService = ref.read(hiveServiceProvider);

      final items = await linkService.listDirectory(path);
      await hiveService.cacheFileList(path, items.map((e) => e.toJson()).toList());
      return items;
    });
  }
}
