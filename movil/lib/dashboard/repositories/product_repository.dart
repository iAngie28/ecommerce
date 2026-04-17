import 'dart:convert';
import '../../core/network/api_client.dart';
import '../../core/constants/api_constants.dart';
import '../../core/storage/secure_storage.dart';
import '../models/product_model.dart';

/// Repositorio que conecta con el endpoint real:
/// GET/POST/PUT/PATCH/DELETE /api/productos/
///
/// Todas las peticiones van a la URL del tenant con nip.io:
/// http://empresa1.157.173.102.129.nip.io/api/productos/
class ProductRepository {
  final ApiClient _apiClient = ApiClient();
  final SecureStorageService _storage = SecureStorageService();

  /// Construye la URL completa del tenant para productos
  Future<String> _getProductsUrl() async {
    final schemaName = await _storage.getSchemaName();
    if (schemaName == null || schemaName.isEmpty) {
      throw Exception('No hay tenant configurado. Inicia sesión primero.');
    }
    return '${ApiConstants.tenantBaseUrl(schemaName)}${ApiConstants.productos}';
  }

  // ── GET: Listar todos los productos ──
  Future<List<ProductModel>> fetchProducts() async {
    final url = await _getProductsUrl();

    final response = await _apiClient.get(
      url,
      requiresAuth: true,
      includeTenantHost: true,
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => ProductModel.fromJson(json)).toList();
    } else if (response.statusCode == 401) {
      throw Exception('Sesión expirada. Inicia sesión nuevamente.');
    } else {
      throw Exception('Error al cargar productos: ${response.statusCode}');
    }
  }

  // ── POST: Crear un producto nuevo ──
  Future<ProductModel> createProduct(ProductModel product) async {
    final url = await _getProductsUrl();

    final response = await _apiClient.post(
      url,
      product.toJson(),
      requiresAuth: true,
      includeTenantHost: true,
    );

    if (response.statusCode == 201) {
      return ProductModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Error al crear producto: ${response.statusCode}');
    }
  }

  // ── PUT: Actualizar un producto completo ──
  Future<ProductModel> updateProduct(int id, ProductModel product) async {
    final baseUrl = await _getProductsUrl();
    final url = '$baseUrl$id/';

    final response = await _apiClient.put(
      url,
      product.toJson(),
      requiresAuth: true,
      includeTenantHost: true,
    );

    if (response.statusCode == 200) {
      return ProductModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Error al actualizar producto: ${response.statusCode}');
    }
  }

  // ── PATCH: Actualizar parcialmente un producto ──
  Future<ProductModel> patchProduct(
      int id, Map<String, dynamic> fields) async {
    final baseUrl = await _getProductsUrl();
    final url = '$baseUrl$id/';

    final response = await _apiClient.patch(
      url,
      fields,
      requiresAuth: true,
      includeTenantHost: true,
    );

    if (response.statusCode == 200) {
      return ProductModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception(
          'Error al actualizar parcialmente producto: ${response.statusCode}');
    }
  }

  // ── DELETE: Eliminar un producto ──
  Future<bool> deleteProduct(int id) async {
    final baseUrl = await _getProductsUrl();
    final url = '$baseUrl$id/';

    final response = await _apiClient.delete(
      url,
      requiresAuth: true,
      includeTenantHost: true,
    );

    if (response.statusCode == 204 || response.statusCode == 200) {
      return true;
    } else {
      throw Exception('Error al eliminar producto: ${response.statusCode}');
    }
  }
}