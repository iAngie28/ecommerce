import 'dart:convert';
import '../../core/network/api_client.dart';
import '../../core/constants/api_constants.dart';
import '../../core/storage/secure_storage.dart';
import '../../core/services/push_notification_service.dart';
import '../models/auth_tokens.dart';

class AuthRepository {
  final ApiClient _apiClient = ApiClient();
  final SecureStorageService _storage = SecureStorageService();

  Future<bool> login(String email, String password) async {
    final url = '${ApiConstants.mainBaseUrl}/clientes/login/';
    try {
      final response = await _apiClient.post(url, {
        'correo': email,
        'contrasena': password,
      });

      if (response.statusCode == 200) {
        final tokens = AuthTokens.fromJson(jsonDecode(response.body));
        await _storage.saveTokens(tokens.access, tokens.refresh);

        final token = await PushNotificationService.getToken();
        if (token != null) {
          await PushNotificationService.registerTokenWithBackend(token);
        }
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  Future<bool> register(Map<String, dynamic> data) async {
    final url = '${ApiConstants.mainBaseUrl}/clientes/';
    try {
      final response = await _apiClient.post(url, data);
      if (response.statusCode == 201) {
        final tokens = AuthTokens.fromJson(jsonDecode(response.body));
        await _storage.saveTokens(tokens.access, tokens.refresh);

        final token = await PushNotificationService.getToken();
        if (token != null) {
          await PushNotificationService.registerTokenWithBackend(token);
        }
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  Future<void> logout() async {
    try {
      final refreshToken = await _storage.getRefreshToken();
      if (refreshToken != null) {
        await _apiClient.post(
          '${ApiConstants.mainBaseUrl}${ApiConstants.logout}',
          {'refresh': refreshToken},
        );
      }
    } catch (_) {
    } finally {
      await _storage.deleteAll();
    }
  }

  Future<bool> isLoggedIn() async {
    final token = await _storage.getAccessToken();
    return token != null && token.isNotEmpty;
  }

  Future<String?> getAccessToken() async {
    return await _storage.getAccessToken();
  }

  Future<String?> getSubdomain() async {
    return await _storage.getSubdomain();
  }
}
