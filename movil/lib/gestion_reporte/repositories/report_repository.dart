import 'dart:convert';
import '../../core/network/api_client.dart';
import '../../core/constants/api_constants.dart';
import '../../core/storage/secure_storage.dart';

class ReportRepository {
  final ApiClient _apiClient = ApiClient();
  final SecureStorageService _storage = SecureStorageService();

  Future<String> _getVQueryUrl() async {
    final schemaName = await _storage.getSchemaName();
    if (schemaName == null || schemaName.isEmpty) {
      throw Exception('No hay tenant configurado.');
    }
    return '${ApiConstants.tenantBaseUrl(schemaName)}${ApiConstants.vquery}';
  }

  Future<Map<String, dynamic>> sendVoiceQuery(String filePath) async {
    final url = await _getVQueryUrl();
    
    final response = await _apiClient.multipartPost(
      url,
      filePath: filePath,
      fieldName: 'audio',
      requiresAuth: true,
      includeTenantHost: true,
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      final errorData = jsonDecode(response.body);
      throw Exception(errorData['error'] ?? 'Error al procesar la consulta.');
    }
  }
}
