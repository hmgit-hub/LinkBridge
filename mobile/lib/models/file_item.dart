import 'package:hive/hive.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'file_item.g.dart';

@HiveType(typeId: 0)
enum FileType {
  @HiveField(0)
  file,
  @HiveField(1)
  directory,
}

@HiveType(typeId: 1)
class FileItem {
  @HiveField(0)
  final String name;

  @HiveField(1)
  final String path;

  @HiveField(2)
  final FileType type;

  @HiveField(3)
  final int size;

  @HiveField(4)
  final bool isSymlink;

  @HiveField(5)
  final String? symlinkTarget;

  @HiveField(6)
  final bool isBroken;

  FileItem({
    required this.name,
    required this.path,
    required this.type,
    this.size = 0,
    this.isSymlink = false,
    this.symlinkTarget,
    this.isBroken = false,
  });

  factory FileItem.fromJson(Map<String, dynamic> json) {
    return FileItem(
      name: json['name'] as String,
      path: json['path'] as String,
      type: FileType.values.firstWhere(
        (e) => e.name == json['type'],
        orElse: () => FileType.file,
      ),
      size: json['size'] as int? ?? 0,
      isSymlink: json['is_symlink'] as bool? ?? false,
      symlinkTarget: json['symlink_target'] as String?,
      isBroken: json['is_broken'] as bool? ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'path': path,
      'type': type.name,
      'size': size,
      'is_symlink': isSymlink,
      'symlink_target': symlinkTarget,
      'is_broken': isBroken,
    };
  }
}
