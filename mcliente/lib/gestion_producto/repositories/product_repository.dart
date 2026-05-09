import 'dart:convert';
import '../../core/network/api_client.dart';
import '../../core/constants/api_constants.dart';
import '../../core/storage/secure_storage.dart';
import '../models/product_model.dart';

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

  Future<List<ProductModel>> fetchProducts() async {
    final url = await _getProductsUrl();
    final response = await _apiClient.get(url, requiresAuth: true, includeTenantHost: true);

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => ProductModel.fromJson(json)).toList();
    } else {
      throw Exception('Error al cargar productos');
    }
  }
}
