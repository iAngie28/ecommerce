import 'dart:convert';
import '../../core/network/api_client.dart';
import '../../core/constants/api_constants.dart';
import '../../core/storage/secure_storage.dart';
import '../models/product_model.dart';
import '../../gestion_producto/models/category_model.dart';

class ProductRepository {
  final ApiClient _apiClient = ApiClient();
  final SecureStorageService _storage = SecureStorageService();

  Future<String> _getProductsUrl() async {
    final schemaName = await _storage.getSchemaName();
    if (schemaName == null || schemaName.isEmpty) {
      throw Exception('No hay tenant configurado.');
    }
    return '${ApiConstants.tenantBaseUrl(schemaName)}${ApiConstants.productos}';
  }

  Future<String> _getCategoriesUrl() async {
    final schemaName = await _storage.getSchemaName();
    if (schemaName == null || schemaName.isEmpty) {
      throw Exception('No hay tenant configurado.');
    }
    return '${ApiConstants.tenantBaseUrl(schemaName)}/categorias/';
  }

  // ── PRODUCTOS ──

  Future<List<ProductModel>> fetchProducts() async {
    final url = await _getProductsUrl();
    final response = await _apiClient.get(url, requiresAuth: true, includeTenantHost: true);

    if (response.statusCode == 200) {
      final dynamic decoded = jsonDecode(response.body);
      final List<dynamic> data = (decoded is Map && decoded.containsKey('results')) 
          ? decoded['results'] 
          : decoded;
      return data.map((json) => ProductModel.fromJson(json)).toList();
    } else {
      throw Exception('Error al cargar productos: ${response.statusCode}');
    }
  }

  Future<ProductModel> createProduct(ProductModel product) async {
    final url = await _getProductsUrl();
    final response = await _apiClient.post(url, product.toJson(), requiresAuth: true, includeTenantHost: true);

    if (response.statusCode == 201) {
      return ProductModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Error al crear producto: ${response.body}');
    }
  }

  Future<ProductModel> updateProduct(int id, ProductModel product) async {
    final baseUrl = await _getProductsUrl();
    final url = '$baseUrl$id/';
    final response = await _apiClient.put(url, product.toJson(), requiresAuth: true, includeTenantHost: true);

    if (response.statusCode == 200) {
      return ProductModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Error al actualizar producto: ${response.body}');
    }
  }

  Future<bool> deleteProduct(int id) async {
    final baseUrl = await _getProductsUrl();
    final url = '$baseUrl$id/';
    final response = await _apiClient.delete(url, requiresAuth: true, includeTenantHost: true);
    return response.statusCode == 204 || response.statusCode == 200;
  }

  Future<void> adjustStock(int id, int newStock) async {
    final baseUrl = await _getProductsUrl();
    final url = '$baseUrl$id/';
    final response = await _apiClient.patch(url, {'stock': newStock}, requiresAuth: true, includeTenantHost: true);
    if (response.statusCode != 200) {
      throw Exception('Error al ajustar stock');
    }
  }

  // ── CATEGORÍAS ──

  Future<List<CategoryModel>> fetchCategories() async {
    final url = await _getCategoriesUrl();
    final response = await _apiClient.get(url, requiresAuth: true, includeTenantHost: true);

    if (response.statusCode == 200) {
      final dynamic decoded = jsonDecode(response.body);
      final List<dynamic> data = (decoded is Map && decoded.containsKey('results')) 
          ? decoded['results'] 
          : decoded;
      return data.map((json) => CategoryModel.fromJson(json)).toList();
    } else {
      throw Exception('Error al cargar categorías');
    }
  }

  Future<CategoryModel> createCategory(CategoryModel category) async {
    final url = await _getCategoriesUrl();
    final response = await _apiClient.post(url, category.toJson(), requiresAuth: true, includeTenantHost: true);

    if (response.statusCode == 201) {
      return CategoryModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Error al crear categoría: ${response.body}');
    }
  }

  Future<CategoryModel> updateCategory(int id, CategoryModel category) async {
    final baseUrl = await _getCategoriesUrl();
    final url = '$baseUrl$id/';
    final response = await _apiClient.put(url, category.toJson(), requiresAuth: true, includeTenantHost: true);

    if (response.statusCode == 200) {
      return CategoryModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Error al actualizar categoría: ${response.body}');
    }
  }

  Future<bool> deleteCategory(int id) async {
    final baseUrl = await _getCategoriesUrl();
    final url = '$baseUrl$id/';
    final response = await _apiClient.delete(url, requiresAuth: true, includeTenantHost: true);
    return response.statusCode == 204 || response.statusCode == 200;
  }
}