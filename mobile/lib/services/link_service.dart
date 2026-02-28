import 'package:dio/dio.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:linkbridge/models/file_item.dart';
import 'package:linkbridge/models/symlink_request.dart';
import 'package:linkbridge/services/dio_service.dart';

part 'link_service.g.dart';

@riverpod
LinkService linkService(LinkServiceRef ref) {
  return LinkService(ref.read(dioServiceProvider));
}

class LinkService {
  final Dio _dio;

  LinkService(this._dio);

  Future<List<FileItem>> listDirectory(String path) async {
    try {
      final response = await _dio.get(
        '/list',
        queryParameters: {'path': path},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = response.data;
        return data.map((json) => FileItem.fromJson(json)).toList();
      }
      throw Exception('Failed to load directory');
    } catch (e) {
      throw Exception('Error listing directory: $e');
    }
  }

  Future<void> createSymlink(String source, String target) async {
    try {
      final response = await _dio.post(
        '/symlink/create',
        data: SymlinkCreateRequest(
          source: source,
          target: target,
        ).toJson(),
      );

      if (response.statusCode != 200) {
        throw Exception('Failed to create symlink');
      }
    } catch (e) {
      throw Exception('Error creating symlink: $e');
    }
  }

  Future<void> deleteSymlink(String symlinkPath) async {
    try {
      final response = await _dio.post(
        '/symlink/delete',
        data: SymlinkDeleteRequest(
          symlinkPath: symlinkPath,
        ).toJson(),
      );

      if (response.statusCode != 200) {
        throw Exception('Failed to delete symlink');
      }
    } catch (e) {
      throw Exception('Error deleting symlink: $e');
    }
  }

  Future<List<String>> checkBrokenSymlinks(String path) async {
    try {
      final response = await _dio.post(
        '/symlink/check-broken',
        data: BrokenSymlinkCheckRequest(path: path).toJson(),
      );

      if (response.statusCode == 200) {
        final data = BrokenSymlinkCheckResponse.fromJson(response.data);
        return data.brokenSymlinks;
      }
      throw Exception('Failed to check broken symlinks');
    } catch (e) {
      throw Exception('Error checking broken symlinks: $e');
    }
  }
}
