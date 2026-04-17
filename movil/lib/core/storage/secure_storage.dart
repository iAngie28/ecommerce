import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureStorageService {
  final _storage = const FlutterSecureStorage();

  // ── TOKENS ──

  Future<void> saveTokens(String access, String refresh) async {
    await _storage.write(key: 'ACCESS_TOKEN', value: access);
    await _storage.write(key: 'REFRESH_TOKEN', value: refresh);
  }

  Future<String?> getAccessToken() async {
    return await _storage.read(key: 'ACCESS_TOKEN');
  }

  Future<String?> getRefreshToken() async {
    return await _storage.read(key: 'REFRESH_TOKEN');
  }

  /// Guarda solo el access token (usado por el interceptor de refresh)
  Future<void> saveAccessToken(String access) async {
    await _storage.write(key: 'ACCESS_TOKEN', value: access);
  }

  // ── TENANT INFO ──
  // El login devuelve schema_name y subdomain del tenant

  Future<void> saveTenantInfo(String schemaName, String subdomain) async {
    await _storage.write(key: 'SCHEMA_NAME', value: schemaName);
    await _storage.write(key: 'SUBDOMAIN', value: subdomain);
  }

  Future<String?> getSubdomain() async {
    return await _storage.read(key: 'SUBDOMAIN');
  }

  Future<String?> getSchemaName() async {
    return await _storage.read(key: 'SCHEMA_NAME');
  }

  // ── LIMPIEZA TOTAL ──

  Future<void> deleteAll() async {
    await _storage.deleteAll();
  }
}