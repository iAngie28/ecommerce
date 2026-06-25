import 'dart:convert';
import '../../core/network/api_client.dart';
import '../../core/constants/api_constants.dart';
import '../models/pedido.dart';

class VentaRepository {
  final ApiClient _apiClient = ApiClient();

  Future<List<Pedido>> getPedidos() async {
    final url = '${ApiConstants.mainBaseUrl}/pedidos/';
    
    final response = await _apiClient.get(
      url,
      requiresAuth: true,
      includeTenantHost: true,
    );

    if (response.statusCode == 200) {
      final decoded = jsonDecode(response.body);
      final List<dynamic> data = decoded is List ? decoded : decoded['results'] ?? [];
      return data.map((json) => Pedido.fromJson(json)).toList();
    } else {
      throw Exception('Error al obtener pedidos');
    }
  }

  Future<void> cambiarEstado(int pedidoId, String nuevoEstado) async {
    final url = '${ApiConstants.mainBaseUrl}/pedidos/$pedidoId/cambiar-estado/';
    
    final response = await _apiClient.post(
      url,
      {'estado': nuevoEstado},
      requiresAuth: true,
      includeTenantHost: true,
    );

    if (response.statusCode != 200) {
      throw Exception('Error al cambiar el estado del pedido');
    }
  }
}
