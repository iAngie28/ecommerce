import 'dart:convert';

import '../../core/constants/api_constants.dart';
import '../../core/network/api_client.dart';
import '../../core/storage/secure_storage.dart';
import '../models/wishlist_item_model.dart';

class WishlistRepository {
  final ApiClient _apiClient = ApiClient();
  final SecureStorageService _storage = SecureStorageService();

  List<dynamic> _extractItems(dynamic decoded) {
    if (decoded is Map && decoded['items'] is List) {
      return decoded['items'] as List;
    }
    if (decoded is List) return decoded;
    return [];
  }

  String _errorMessage(String fallback, String body) {
    try {
      final decoded = jsonDecode(body);
      if (decoded is Map && decoded['error'] != null) {
        return decoded['error'].toString();
      }
      if (decoded is Map && decoded['detail'] != null) {
        return decoded['detail'].toString();
      }
      if (decoded is Map && decoded['mensaje'] != null) {
        return decoded['mensaje'].toString();
      }
    } catch (_) {}
    return fallback;
  }

  Future<String?> _currentTenantHost() async {
    return await _storage.getSubdomain();
  }

  Future<List<WishlistItemModel>> fetchWishlist() async {
    final response = await _apiClient.get(
      '${ApiConstants.mainBaseUrl}/wishlist/',
      requiresAuth: true,
    );

    if (response.statusCode != 200) {
      throw Exception(
        _errorMessage('Error al cargar la wishlist', response.body),
      );
    }

    final decoded = jsonDecode(response.body);
    return _extractItems(decoded)
        .whereType<Map>()
        .map(
          (item) => WishlistItemModel.fromJson(Map<String, dynamic>.from(item)),
        )
        .toList();
  }

  Future<Set<int>> fetchProductIdsForCurrentStore() async {
    final response = await _apiClient.get(
      '${ApiConstants.mainBaseUrl}/wishlist/',
      requiresAuth: true,
      includeTenantHost: true,
    );

    if (response.statusCode != 200) return <int>{};

    final decoded = jsonDecode(response.body);
    return _extractItems(decoded)
        .whereType<Map>()
        .map((item) => item['producto'])
        .whereType<Map>()
        .map((product) => int.tryParse((product['id'] ?? '').toString()) ?? 0)
        .where((id) => id > 0)
        .toSet();
  }

  Future<bool> containsProduct(int productId) async {
    final response = await _apiClient.get(
      '${ApiConstants.mainBaseUrl}/wishlist/contiene/$productId/',
      requiresAuth: true,
      includeTenantHost: true,
    );

    if (response.statusCode != 200) return false;

    final decoded = jsonDecode(response.body);
    return decoded is Map && decoded['en_wishlist'] == true;
  }

  Future<bool> toggleProduct(int productId) async {
    final response = await _apiClient.post(
      '${ApiConstants.mainBaseUrl}/wishlist/toggle/$productId/',
      {},
      requiresAuth: true,
      includeTenantHost: true,
    );

    if (response.statusCode != 200) {
      throw Exception(
        _errorMessage('Error al actualizar la wishlist', response.body),
      );
    }

    final decoded = jsonDecode(response.body);
    return decoded is Map && decoded['accion'] == 'agregado';
  }

  Future<void> removeProduct(int productId, {String? tenantHost}) async {
    final host = tenantHost ?? await _currentTenantHost();
    final response = await _apiClient.delete(
      '${ApiConstants.mainBaseUrl}/wishlist/eliminar/$productId/',
      requiresAuth: true,
      includeTenantHost: host != null && host.isNotEmpty,
      tenantHostOverride: host,
    );

    if (response.statusCode != 200) {
      throw Exception(
        _errorMessage('No se pudo eliminar el producto', response.body),
      );
    }
  }

  Future<void> moveToCart(int productId, {String? tenantHost}) async {
    final host = tenantHost ?? await _currentTenantHost();
    final response = await _apiClient.post(
      '${ApiConstants.mainBaseUrl}/wishlist/mover-al-carrito/$productId/',
      {},
      requiresAuth: true,
      includeTenantHost: host != null && host.isNotEmpty,
      tenantHostOverride: host,
    );

    if (response.statusCode != 200) {
      throw Exception(
        _errorMessage('No se pudo mover al carrito', response.body),
      );
    }
  }

  Future<void> clearAll() async {
    final response = await _apiClient.delete(
      '${ApiConstants.mainBaseUrl}/wishlist/vaciar/',
      requiresAuth: true,
    );

    if (response.statusCode != 200) {
      throw Exception(
        _errorMessage('No se pudo vaciar la wishlist', response.body),
      );
    }
  }
}
