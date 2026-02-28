import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:linkbridge/models/file_item.dart';
import 'package:linkbridge/providers/file_list_provider.dart';
import 'package:linkbridge/screens/scan_page.dart';

class DashboardPage extends ConsumerWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final fileListAsync = ref.watch(fileListProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('链接列表'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              ref.read(fileListProvider.notifier).refresh('/');
            },
          ),
          IconButton(
            icon: const Icon(Icons.qr_code_scanner),
            onPressed: () async {
              final result = await Navigator.push<Map<String, dynamic>>(
                context,
                MaterialPageRoute(
                  builder: (context) => const ScanPage(),
                ),
              );
              if (result != null) {
                // TODO: 创建软链接
              }
            },
          ),
        ],
      ),
      body: fileListAsync.when(
        data: (items) {
          if (items.isEmpty) {
            return const Center(
              child: Text('暂无软链接'),
            );
          }

          return ListView.builder(
            itemCount: items.length,
            itemBuilder: (context, index) {
              final item = items[index];
              return ListTile(
                leading: Icon(
                  item.type == FileType.directory
                      ? Icons.folder
                      : Icons.insert_drive_file,
                  color: item.isBroken ? Colors.red : null,
                ),
                title: Text(
                  item.name,
                  style: TextStyle(
                    color: item.isBroken ? Colors.red : null,
                    decoration: item.isBroken ? TextDecoration.lineThrough : null,
                  ),
                ),
                subtitle: Text(item.path),
                trailing: item.isSymlink
                    ? const Icon(Icons.link, color: Colors.blue)
                    : null,
                onTap: () {
                  // TODO: 进入目录
                },
              );
            },
          );
        },
        loading: () => const Center(
          child: CircularProgressIndicator(),
        ),
        error: (error, stack) => Center(
          child: Text('Error: $error'),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.pushNamed(context, '/create-link');
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
