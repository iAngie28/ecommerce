import 'dart:convert';
import '../../core/network/api_client.dart';
import '../../core/constants/api_constants.dart';
import '../../core/storage/secure_storage.dart';
import '../models/product_model.dart';
import '../../gestion_producto/models/category_model.dart';

class ProductRepository {
  final ApiClient _apiClient = ApiClient();
  final SecureStorageService _storage = SecureStorageService();

  Future<String?> _buildUrl() async {
    final subdomain = await _storage.getSubdomain();
    if (subdomain == null || subdomain.isEmpty) return null;
    return '${ApiConstants.tenantBaseUrl(subdomain)}${ApiConstants.productos}';
  }

  Future<String?> _buildCategoriesUrl() async {
    final subdomain = await _storage.getSubdomain();
    if (subdomain == null || subdomain.isEmpty) return null;
    return '${ApiConstants.tenantBaseUrl(subdomain)}/categorias/';
  }

  // ── PRODUCTOS ──

  Future<List<ProductModel>> fetchProducts() async {
    final url = await _buildUrl();
    if (url == null) throw Exception('No hay tenant configurado.');
    final response = await _apiClient.get(url, requiresAuth: true, includeTenantHost: true);

    if (response.statusCode == 200) {
      final dynamic decoded = jsonDecode(response.body);
      final List<dynamic> data = (decoded is Map && decoded.containsKey('results')) 
          ? decoded['results'] 
          : decoded;
      return data.map((json) => ProductModel.fromJson(json)).toList();
    } else {
      String errMsg = 'Error al cargar productos: ${response.statusCode}';
      try {
        final decoded = jsonDecode(response.body);
        if (decoded is Map && decoded.containsKey('detail')) errMsg = decoded['detail'];
        else if (decoded is Map && decoded.containsKey('error')) errMsg = decoded['error'];
        else if (decoded is Map) errMsg = decoded.toString();
      } catch (_) {}
      throw Exception(errMsg);
    }
  }

  Future<ProductModel> createProduct(ProductModel product) async {
    final url = await _buildUrl();
    if (url == null) throw Exception('No hay tenant configurado.');
    final response = await _apiClient.post(url, product.toJson(), requiresAuth: true, includeTenantHost: true);

    if (response.statusCode == 201 || response.statusCode == 200) {
      return ProductModel.fromJson(jsonDecode(response.body));
    } else {
      String errMsg = 'Error al crear producto: ${response.statusCode}';
      try {
        final decoded = jsonDecode(response.body);
        if (decoded is Map && decoded.containsKey('detail')) errMsg = decoded['detail'];
        else if (decoded is Map && decoded.containsKey('error')) errMsg = decoded['error'];
        else if (decoded is Map) errMsg = decoded.toString();
      } catch (_) {}
      throw Exception(errMsg);
    }
  }

  Future<ProductModel> updateProduct(int id, ProductModel product) async {
    final url = await _buildUrl();
    if (url == null) throw Exception('No hay tenant configurado.');
    final response = await _apiClient.put('$url$id/', product.toJson(), requiresAuth: true, includeTenantHost: true);

    if (response.statusCode == 200) {
      return ProductModel.fromJson(jsonDecode(response.body));
    } else {
      String errMsg = 'Error al actualizar producto: ${response.statusCode}';
      try {
        final decoded = jsonDecode(response.body);
        if (decoded is Map && decoded.containsKey('detail')) errMsg = decoded['detail'];
        else if (decoded is Map && decoded.containsKey('error')) errMsg = decoded['error'];
        else if (decoded is Map) errMsg = decoded.toString();
      } catch (_) {}
      throw Exception(errMsg);
    }
  }

  Future<bool> deleteProduct(int id) async {
    final url = await _buildUrl();
    if (url == null) throw Exception('No hay tenant configurado.');
    final response = await _apiClient.delete('$url$id/', requiresAuth: true, includeTenantHost: true);
    return response.statusCode == 204 || response.statusCode == 200;
  }

  Future<void> adjustStock(int id, int newStock) async {
    final url = await _buildUrl();
    if (url == null) throw Exception('No hay tenant configurado.');
    final response = await _apiClient.patch('$url$id/', {'stock': newStock}, requiresAuth: true, includeTenantHost: true);
    if (response.statusCode != 200) {
      throw Exception('Error al ajustar stock');
    }
  }

  // ── CATEGORÍAS ──

  Future<List<CategoryModel>> fetchCategories() async {
    final url = await _buildCategoriesUrl();
    if (url == null) throw Exception('No hay tenant configurado.');
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
    final url = await _buildCategoriesUrl();
    if (url == null) throw Exception('No hay tenant configurado.');
    final response = await _apiClient.post(url, category.toJson(), requiresAuth: true, includeTenantHost: true);

    if (response.statusCode == 201) {
      return CategoryModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Error al crear categoría: ${response.body}');
    }
  }

  Future<CategoryModel> updateCategory(int id, CategoryModel category) async {
    final url = await _buildCategoriesUrl();
    if (url == null) throw Exception('No hay tenant configurado.');
    final response = await _apiClient.put('$url$id/', category.toJson(), requiresAuth: true, includeTenantHost: true);

    if (response.statusCode == 200) {
      return CategoryModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Error al actualizar categoría: ${response.body}');
    }
  }

  Future<bool> deleteCategory(int id) async {
    final url = await _buildCategoriesUrl();
    if (url == null) throw Exception('No hay tenant configurado.');
    final response = await _apiClient.delete('$url$id/', requiresAuth: true, includeTenantHost: true);
    return response.statusCode == 204 || response.statusCode == 200;
  }
}