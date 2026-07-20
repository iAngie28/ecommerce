import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/cuenta_puntos.dart';

class FidelizacionService {
  static const String baseUrl = 'http://localhost:8000/api/fidelizacion';
  
  // Usamos un mock flag mientras la BD de Django esté apagada.
  final bool _useMockData = true;

  Future<Map<String, dynamic>> getConfiguracion() async {
    if (_useMockData) {
      await Future.delayed(const Duration(milliseconds: 300));
      return {
        'PUNTOS_POR_BS': 0.1,
        'VALOR_BS_POR_PUNTO': 0.05
      };
    }

    final response = await http.get(Uri.parse('$baseUrl/configuracion/'));
    if (response.statusCode == 200) {
      return json.decode(response.body);
    }
    throw Exception('Error al obtener configuración de fidelización');
  }

  Future<CuentaPuntos> getMiCuenta(String token) async {
    if (_useMockData) {
      await Future.delayed(const Duration(milliseconds: 600));
      return CuentaPuntos.fromJson({
        'id': 1,
        'cliente_nombre': 'Usuario Móvil Demo',
        'saldo_actual': 850,
        'puntos_historicos': 1400,
        'fecha_actualizacion': DateTime.now().toIso8601String(),
        'historial': [
          {
            'id': 201,
            'tipo_operacion': 'ACUMULACION',
            'monto_puntos': 150,
            'referencia': 'Pedido #5021',
            'fecha': DateTime.now().subtract(const Duration(days: 1)).toIso8601String()
          },
          {
            'id': 202,
            'tipo_operacion': 'CANJE',
            'monto_puntos': -300,
            'referencia': 'Canje en Pedido #5020',
            'fecha': DateTime.now().subtract(const Duration(days: 3)).toIso8601String()
          }
        ]
      });
    }

    final response = await http.get(
      Uri.parse('$baseUrl/mi-cuenta/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      return CuentaPuntos.fromJson(json.decode(response.body));
    }
    throw Exception('Error al cargar la cuenta de puntos');
  }

  Future<Map<String, dynamic>> canjearPuntos(int puntos, String token) async {
    if (_useMockData) {
      await Future.delayed(const Duration(milliseconds: 800));
      return {
        'mensaje': 'Canje exitoso (Simulado)',
        'descuento_bs': puntos * 0.05,
      };
    }

    final response = await http.post(
      Uri.parse('$baseUrl/canjear/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: json.encode({'puntos': puntos, 'referencia': 'Canje desde App Móvil'}),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      final decoded = json.decode(response.body);
      throw Exception(decoded['detail'] ?? 'Error al canjear puntos');
    }
  }
}
