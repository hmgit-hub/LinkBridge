class SymlinkCreateRequest {
  final String source;
  final String target;

  SymlinkCreateRequest({
    required this.source,
    required this.target,
  });

  Map<String, dynamic> toJson() {
    return {
      'source': source,
      'target': target,
    };
  }
}

class SymlinkDeleteRequest {
  final String symlinkPath;

  SymlinkDeleteRequest({
    required this.symlinkPath,
  });

  Map<String, dynamic> toJson() {
    return {
      'symlink_path': symlinkPath,
    };
  }
}

class BrokenSymlinkCheckRequest {
  final String path;

  BrokenSymlinkCheckRequest({
    required this.path,
  });

  Map<String, dynamic> toJson() {
    return {
      'path': path,
    };
  }
}

class BrokenSymlinkCheckResponse {
  final List<String> brokenSymlinks;

  BrokenSymlinkCheckResponse({
    required this.brokenSymlinks,
  });

  factory BrokenSymlinkCheckResponse.fromJson(Map<String, dynamic> json) {
    return BrokenSymlinkCheckResponse(
      brokenSymlinks:
          (json['broken_symlinks'] as List<dynamic>).cast<String>(),
    );
  }
}
