import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/resena.dart';

class ResenaService {
  // TODO: Reemplazar por la URL real del backend
  static const String baseUrl = 'http://localhost:8000/api';

  Future<Map<String, dynamic>> obtenerResenas(int productoId) async {
    try {
      // Endpoint público configurado en Django
      final response = await http.get(Uri.parse('$baseUrl/productos/$productoId/reseñas/'));
      
      if (response.statusCode == 200) {
        final decoded = json.decode(response.body);
        final List<dynamic> resenasJson = decoded['resultados'] ?? [];
        final List<Resena> resenas = resenasJson.map((json) => Resena.fromJson(json)).toList();
        final estadisticas = decoded['estadisticas'] ?? {'promedio': 0.0, 'total_reseñas': 0};
        
        return {
          'resenas': resenas,
          'estadisticas': estadisticas,
        };
      } else {
        throw Exception('Error al cargar reseñas: ${response.statusCode}');
      }
    } catch (e) {
      // Mock Data para probar UI sin backend
      await Future.delayed(const Duration(seconds: 1));
      return {
        'resenas': [
          Resena(
            id: 1, 
            clienteNombre: 'Ana García', 
            calificacion: 5, 
            comentario: '¡Excelente producto en la app móvil!', 
            fechaCreacion: '2026-06-15'
          ),
          Resena(
            id: 2, 
            clienteNombre: 'Carlos López', 
            calificacion: 4, 
            comentario: 'Muy bueno, pero el envío tardó.', 
            fechaCreacion: '2026-07-02'
          ),
        ],
        'estadisticas': {'promedio': 4.5, 'total_reseñas': 2},
      };
    }
  }

  Future<bool> enviarResena({
    required int productoId,
    required int calificacion,
    String? comentario,
    required String token, // Token JWT del usuario autenticado
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/reseñas/'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
        body: json.encode({
          'producto': productoId,
          'calificacion': calificacion,
          'comentario': comentario,
        }),
      );

      return response.statusCode == 201;
    } catch (e) {
      // Simula éxito para efectos de demostración sin backend
      await Future.delayed(const Duration(milliseconds: 800));
      return true;
    }
  }
}
