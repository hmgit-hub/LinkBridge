import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:linkbridge/screens/dashboard_page.dart';
import 'package:linkbridge/screens/create_link_wizard.dart';
import 'package:linkbridge/services/notification_service.dart';
import 'package:linkbridge/services/hive_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final container = ProviderContainer();

  await container.read(notificationServiceProvider).init();
  await container.read(hiveServiceProvider.future).then((service) => service.init());

  runApp(
    UncontrolledProviderScope(
      container: container,
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ProviderScope(
      child: MaterialApp(
        title: 'LinkBridge',
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
          useMaterial3: true,
        ),
        darkTheme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: Colors.deepPurple,
            brightness: Brightness.dark,
          ),
          useMaterial3: true,
        ),
        initialRoute: '/',
        routes: {
          '/': (context) => const DashboardPage(),
          '/create-link': (context) => const CreateLinkWizard(),
        },
      ),
    );
  }
}
