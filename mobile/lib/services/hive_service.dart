import 'package:hive_flutter/hive_flutter.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:io';

part 'hive_service.g.dart';

@riverpod
Future<Directory> appDirectory(AppDirectoryRef ref) async {
  return await getApplicationDocumentsDirectory();
}

@riverpod
Future<HiveService> hiveService(HiveServiceRef ref) async {
  final dir = await ref.watch(appDirectoryProvider.future);
  await Hive.initFlutter(dir.path);
  return HiveService();
}

class HiveService {
  late Box _fileCacheBox;

  Future<void> init() async {
    _fileCacheBox = await Hive.openBox('fileCache');
  }

  Future<void> cacheFileList(String path, List<dynamic> items) async {
    await _fileCacheBox.put(path, items);
  }

  List<dynamic>? getCachedFileList(String path) {
    return _fileCacheBox.get(path);
  }

  Future<void> clearCache() async {
    await _fileCacheBox.clear();
  }
}
