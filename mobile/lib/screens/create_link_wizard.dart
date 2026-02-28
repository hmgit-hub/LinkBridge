import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:linkbridge/models/symlink_request.dart';
import 'package:linkbridge/providers/file_list_provider.dart';
import 'package:linkbridge/services/link_service.dart';

class CreateLinkWizard extends ConsumerStatefulWidget {
  const CreateLinkWizard({super.key});

  @override
  ConsumerState<CreateLinkWizard> createState() => _CreateLinkWizardState();
}

class _CreateLinkWizardState extends ConsumerState<CreateLinkWizard> {
  final _pageController = PageController();
  int _currentStep = 0;

  String? _sourcePath;
  String? _targetPath;

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  Future<void> _pickSourceFile() async {
    final result = await FilePicker.platform.pickFiles();

    if (result != null && result.files.single.path != null) {
      setState(() {
        _sourcePath = result.files.single.path;
      });
    }
  }

  Future<void> _pickTargetFile() async {
    final result = await FilePicker.platform.pickFiles();

    if (result != null && result.files.single.path != null) {
      setState(() {
        _targetPath = result.files.single.path;
      });
    }
  }

  Future<void> _createSymlink() async {
    if (_sourcePath == null || _targetPath == null) {
      return;
    }

    try {
      await ref.read(linkServiceProvider).createSymlink(
            _sourcePath!,
            _targetPath!,
          );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('软链接创建成功'),
          ),
        );
        Navigator.pop(context);
        ref.read(fileListProvider.notifier).refresh('/');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('创建失败: $e'),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final steps = [
      {
        'title': '选择源文件',
        'content': Column(
          children: [
            ElevatedButton.icon(
              onPressed: _pickSourceFile,
              icon: const Icon(Icons.folder_open),
              label: const Text('选择源文件'),
            ),
            if (_sourcePath != null) Text('源文件: $_sourcePath'),
          ],
        ),
      },
      {
        'title': '选择目标位置',
        'content': Column(
          children: [
            ElevatedButton.icon(
              onPressed: _pickTargetFile,
              icon: const Icon(Icons.folder_open),
              label: const Text('选择目标位置'),
            ),
            if (_targetPath != null) Text('目标位置: $_targetPath'),
          ],
        ),
      },
      {
        'title': '确认',
        'content': Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('源文件: $_sourcePath'),
            Text('目标位置: $_targetPath'),
          ],
        ),
      },
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('创建软链接'),
      ),
      body: Stepper(
        currentStep: _currentStep,
        onStepContinue: () {
          if (_currentStep < steps.length - 1) {
            setState(() {
              _currentStep += 1;
            });
          } else {
            _createSymlink();
          }
        },
        onStepCancel: () {
          if (_currentStep > 0) {
            setState(() {
              _currentStep -= 1;
            });
          } else {
            Navigator.pop(context);
          }
        },
        steps: [
          for (final step in steps)
            Step(
              title: Text(step['title'] as String),
              content: step['content'] as Widget,
            ),
        ],
      ),
    );
  }
}
