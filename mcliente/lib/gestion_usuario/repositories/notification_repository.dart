import 'dart:convert';
import '../../core/network/api_client.dart';

class NotificationRepository {
  final ApiClient _apiClient = ApiClient();

  Future<List<dynamic>> getNotifications() async {
    final response = await _apiClient.get('/notificaciones/');
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

  Future<void> markAsRead(int notificacionId) async {
    await _apiClient.patch('/notificaciones/$notificacionId/', {
      'leido': true,
    });
  }

  Future<void> markAllAsRead() async {
    await _apiClient.post('/notificaciones/marcar-todas-leidas/', {});
  }
}
