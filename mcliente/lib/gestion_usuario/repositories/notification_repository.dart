import 'dart:convert';
import '../../core/constants/api_constants.dart';
import '../../core/network/api_client.dart';

class NotificationRepository {
  final ApiClient _apiClient = ApiClient();

  Future<List<dynamic>> getNotifications() async {
    final response = await _apiClient.get(
      '${ApiConstants.mainBaseUrl}/notificaciones/',
      requiresAuth: true,
    );
    if (response.statusCode == 200) {
      final decoded = json.decode(utf8.decode(response.bodyBytes));
      if (decoded is Map<String, dynamic> && decoded.containsKey('results')) {
        return decoded['results'] as List<dynamic>;
      } else if (decoded is List) {
        return decoded;
      }
      return [];
    }
    throw Exception('Error al obtener notificaciones');
  }

  Future<void> markAsRead(
    int notificacionId, {
    String? tenantHost,
    String? tenantSchema,
  }) async {
    final body = {
      'leido': true,
      if ((tenantHost == null || tenantHost.isEmpty) &&
          tenantSchema != null &&
          tenantSchema.isNotEmpty)
        'tenant_schema': tenantSchema,
    };

    await _apiClient.patch(
      '${ApiConstants.mainBaseUrl}/notificaciones/$notificacionId/',
      body,
      requiresAuth: true,
      includeTenantHost: tenantHost != null && tenantHost.isNotEmpty,
      tenantHostOverride: tenantHost,
    );
  }

  Future<void> markAllAsRead() async {
    await _apiClient.post(
      '${ApiConstants.mainBaseUrl}/notificaciones/marcar-todas-leidas/',
      {},
      requiresAuth: true,
    );
  }
}
