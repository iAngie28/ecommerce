import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/wishlist_item.dart';

class WishlistService {
  // TODO: Ajustar a la URL base de tu entorno (ej. usar variables de entorno o archivo config)
  static const String baseUrl = 'http://localhost:8000/api/wishlist';

  // Usamos un mock flag mientras la BD de Django esté apagada.
  final bool _useMockData = true;

  // Memoria temporal para mocks
  static final List<WishlistItem> _mockWishlist = [];

  Future<List<WishlistItem>> getWishlist(String token) async {
    if (_useMockData) {
      await Future.delayed(const Duration(milliseconds: 600));
      return List.from(_mockWishlist);
    }

    final response = await http.get(
      Uri.parse('$baseUrl/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final decoded = json.decode(response.body);
      final List<dynamic> resultados = decoded['resultados'] ?? [];
      return resultados.map((json) => WishlistItem.fromJson(json)).toList();
    } else {
      throw Exception('Error al obtener la wishlist');
    }
  }

  Future<bool> verificarSiContiene(int productoId, String token) async {
    if (_useMockData) {
      await Future.delayed(const Duration(milliseconds: 200));
      return _mockWishlist.any((item) => item.productoId == productoId);
    }

    final response = await http.get(
      Uri.parse('$baseUrl/contiene/$productoId/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      final decoded = json.decode(response.body);
      return decoded['en_wishlist'] ?? false;
    }
    return false;
  }

  Future<bool> toggleProducto(int productoId, String token) async {
    if (_useMockData) {
      await Future.delayed(const Duration(milliseconds: 400));
      final exists = _mockWishlist.any((item) => item.productoId == productoId);
      if (exists) {
        _mockWishlist.removeWhere((item) => item.productoId == productoId);
      } else {
        _mockWishlist.add(WishlistItem(
          id: DateTime.now().millisecondsSinceEpoch,
          productoId: productoId,
          nombreProducto: 'Producto Mock $productoId',
          precio: 99.99,
          activo: true,
        ));
      }
      return !exists;
    }

    final response = await http.post(
      Uri.parse('$baseUrl/toggle/$productoId/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      return true;
    } else {
      throw Exception('Error al modificar la wishlist');
    }
  }

  Future<bool> eliminarProducto(int productoId, String token) async {
    if (_useMockData) {
      await Future.delayed(const Duration(milliseconds: 400));
      _mockWishlist.removeWhere((item) => item.productoId == productoId);
      return true;
    }

    final response = await http.delete(
      Uri.parse('$baseUrl/eliminar/$productoId/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    return response.statusCode == 204;
  }

  Future<bool> vaciarWishlist(String token) async {
    if (_useMockData) {
      await Future.delayed(const Duration(milliseconds: 500));
      _mockWishlist.clear();
      return true;
    }

    final response = await http.delete(
      Uri.parse('$baseUrl/vaciar/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    return response.statusCode == 204;
  }

  Future<bool> moverAlCarrito(int productoId, String token) async {
    if (_useMockData) {
      await Future.delayed(const Duration(milliseconds: 600));
      _mockWishlist.removeWhere((item) => item.productoId == productoId);
      return true; // Simula éxito agregando al carrito
    }

    final response = await http.post(
      Uri.parse('$baseUrl/mover-al-carrito/$productoId/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      return true;
    } else {
      throw Exception('Error al mover producto al carrito');
    }
  }
}
