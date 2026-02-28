import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';

class ScanPage extends StatefulWidget {
  const ScanPage({super.key});

  @override
  State<ScanPage> createState() => _ScanPageState();
}

class _ScanPageState extends State<ScanPage> {
  final MobileScannerController controller = MobileScannerController();

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('扫描二维码'),
      ),
      body: MobileScanner(
        controller: controller,
        onDetect: (capture) {
          final List<Barcode> barcodes = capture.barcodes;

          for (final barcode in barcodes) {
            debugPrint('Barcode found! ${barcode.rawValue}');
          }

          final code = capture.barcodes.first;
          if (code.rawValue != null) {
            try {
              final jsonData = jsonDecode(code.rawValue!);
              final source = jsonData['source'] as String;
              final target = jsonData['target'] as String;

              if (mounted) {
                Navigator.pop(context, {'source': source, 'target': target});
              }
            } catch (e) {
              if (mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('无效的二维码格式: $e'),
                  ),
                );
              }
            }
          } else {
            if (mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('无法读取二维码'),
                ),
              );
            }
          }
        },
      ),
    );
  }
}
