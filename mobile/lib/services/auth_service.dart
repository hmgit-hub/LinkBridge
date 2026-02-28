import 'package:local_auth/local_auth.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:shared_preferences/shared_preferences.dart';

part 'auth_service.g.dart';

@riverpod
AuthService authService(AuthServiceRef ref) {
  return AuthService();
}

class AuthService {
  final LocalAuthentication _localAuth = LocalAuthentication();

  Future<bool> authenticate() async {
    try {
      final isAvailable = await _localAuth.canCheckBiometrics;
      if (!isAvailable) {
        return false;
      }

      final isDeviceSupported = await _localAuth.isDeviceSupported();
      if (!isDeviceSupported) {
        return false;
      }

      final didAuthenticate = await _localAuth.authenticate(
        localizedReason: '请验证身份以访问 LinkBridge',
        options: const AuthenticationOptions(
          stickyAuth: true,
          biometricOnly: true,
        ),
      );

      return didAuthenticate;
    } catch (e) {
      return false;
    }
  }

  Future<bool> isAuthenticated() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool('isAuthenticated') ?? false;
  }

  Future<void> setAuthenticated(bool value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('isAuthenticated', value);
  }
}
