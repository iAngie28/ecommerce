import 'dart:convert';
import '../../core/constants/api_constants.dart';
import '../../core/network/api_client.dart';

class FidelizacionRepository {
  final ApiClient _apiClient = ApiClient();

  int _toInt(dynamic value) {
    if (value is int) return value;
    if (value is num) return value.floor();
    return int.tryParse(value?.toString() ?? '') ?? 0;
  }

  double _toDouble(dynamic value, double fallback) {
    if (value is num) return value.toDouble();
    return double.tryParse(value?.toString() ?? '') ?? fallback;
  }

  Future<Map<String, dynamic>> obtenerMiCuenta({bool includeTenantHost = false}) async {
    final response = await _apiClient.get(
      '${ApiConstants.mainBaseUrl}/fidelizacion/mi-cuenta/',
      requiresAuth: true,
      includeTenantHost: includeTenantHost,
    );

    if (response.statusCode != 200) {
      throw Exception('Error al cargar puntos: ${response.body}');
    }

    final decoded = jsonDecode(response.body) as Map<String, dynamic>;
    final tiendas = (decoded['tiendas'] as List? ?? [])
        .whereType<Map>()
        .map((item) => Map<String, dynamic>.from(item))
        .toList();

    return {
      ...decoded,
      'saldo_actual': _toInt(decoded['saldo_actual']),
      'puntos_historicos': _toInt(decoded['puntos_historicos']),
      'tiendas': tiendas.map((tienda) {
        return {
          ...tienda,
          'saldo_actual': _toInt(tienda['saldo_actual']),
          'puntos_historicos': _toInt(tienda['puntos_historicos']),
        };
      }).toList(),
    };
  }

  Future<Map<String, double>> obtenerConfiguracion({bool includeTenantHost = false}) async {
    final response = await _apiClient.get(
      '${ApiConstants.mainBaseUrl}/fidelizacion/configuracion/',
      requiresAuth: true,
      includeTenantHost: includeTenantHost,
    );

    if (response.statusCode != 200) {
      return {
        'PUNTOS_POR_BS': 0.1,
        'VALOR_BS_POR_PUNTO': 0.05,
      };
    }

    final decoded = jsonDecode(response.body) as Map<String, dynamic>;
    return {
      'PUNTOS_POR_BS': _toDouble(decoded['PUNTOS_POR_BS'], 0.1),
      'VALOR_BS_POR_PUNTO': _toDouble(decoded['VALOR_BS_POR_PUNTO'], 0.05),
    };
  }
}
