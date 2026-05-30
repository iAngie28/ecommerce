import 'dart:convert';
import '../../core/network/api_client.dart';
import '../../core/constants/api_constants.dart';
import '../../core/storage/secure_storage.dart';
import '../models/cart_model.dart';


class CartRepository {
  final ApiClient _apiClient = ApiClient();
  final SecureStorageService _storage = SecureStorageService();

  Future<String?> _buildUrl() async {
    final subdomain = await _storage.getSubdomain();
    if (subdomain == null || subdomain.isEmpty) return null;
    return '${ApiConstants.tenantBaseUrl(subdomain)}/carritos/';
  }

  Future<CartModel> fetchActiveCart() async {
    final url = await _buildUrl();
    if (url == null) throw Exception('No hay tenant configurado.');
    print('[DEBUG] Fetching cart from: $url');
    // El backend maneja obtener o crear el carrito abierto cuando se llama a POST carritos/
    final response = await _apiClient.post(url, {}, requiresAuth: true, includeTenantHost: true);
    print('[DEBUG] FetchActiveCart Status: ${response.statusCode}');

    if (response.statusCode == 200 || response.statusCode == 201) {
      return CartModel.fromJson(jsonDecode(response.body));
    } else {
      print('[DEBUG] Error al obtener el carrito: ${response.statusCode} - ${response.body}');
      throw Exception('Error al obtener el carrito: ${response.body}');
    }
  }

  Future<CartModel> addItem(int cartId, int productId, {int quantity = 1}) async {
    final baseUrl = await _buildUrl();
    if (baseUrl == null) throw Exception('No hay tenant configurado.');
    final url = '$baseUrl$cartId/agregar-item/';
    print('[DEBUG] Adding item to: $url');
    
    final response = await _apiClient.post(
      url, 
      {'producto_id': productId, 'cantidad': quantity}, 
      requiresAuth: true, 
      includeTenantHost: true
    );

    if (response.statusCode == 200) {
      return CartModel.fromJson(jsonDecode(response.body));
    } else {
      print('[DEBUG] Error al agregar item: ${response.statusCode} - ${response.body}');
      throw Exception('Error al agregar item: ${response.body}');
    }
  }

  Future<CartModel> removeItem(int cartId, int productId) async {
    final baseUrl = await _buildUrl();
    if (baseUrl == null) throw Exception('No hay tenant configurado.');
    final url = '$baseUrl$cartId/eliminar-item/';
    
    final response = await _apiClient.post(
      url, 
      {'producto_id': productId}, 
      requiresAuth: true, 
      includeTenantHost: true
    );

    if (response.statusCode == 200) {
      return CartModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Error al eliminar item: ${response.body}');
    }
  }

  Future<CartModel> clearCart(int cartId) async {
    final baseUrl = await _buildUrl();
    if (baseUrl == null) throw Exception('No hay tenant configurado.');
    final url = '$baseUrl$cartId/vaciar/';
    
    final response = await _apiClient.post(url, {}, requiresAuth: true, includeTenantHost: true);

    if (response.statusCode == 200) {
      return CartModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Error al vaciar carrito');
    }
  }

  Future<CartModel> checkout(int cartId) async {
    final baseUrl = await _buildUrl();
    if (baseUrl == null) throw Exception('No hay tenant configurado.');
    final url = '$baseUrl$cartId/cerrar/';
    
    final response = await _apiClient.post(url, {}, requiresAuth: true, includeTenantHost: true);

    if (response.statusCode == 200) {
      return CartModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Error al procesar pedido');
    }
  }
}
