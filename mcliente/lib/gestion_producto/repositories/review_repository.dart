import 'dart:convert';

import '../../core/constants/api_constants.dart';
import '../../core/network/api_client.dart';
import '../models/review_model.dart';

class ReviewRepository {
  final ApiClient _apiClient = ApiClient();

  String _errorMessage(String fallback, String body) {
    try {
      final decoded = jsonDecode(body);
      if (decoded is Map && decoded['detail'] != null) {
        return decoded['detail'].toString();
      }
      if (decoded is Map && decoded['error'] != null) {
        return decoded['error'].toString();
      }
      if (decoded is Map && decoded['mensaje'] != null) {
        return decoded['mensaje'].toString();
      }
    } catch (_) {}
    return fallback;
  }

  Future<ProductReviewsResult> fetchProductReviews(int productId) async {
    final response = await _apiClient.get(
      '${ApiConstants.mainBaseUrl}/productos/$productId/reseñas/',
      requiresAuth: true,
      includeTenantHost: true,
    );

    if (response.statusCode != 200) {
      throw Exception(_errorMessage('No se pudieron cargar las reseñas', response.body));
    }

    return ProductReviewsResult.fromJson(jsonDecode(response.body));
  }

  Future<ReviewModel> submitReview({
    required int productId,
    required int calificacion,
    required String comentario,
  }) async {
    final response = await _apiClient.post(
      '${ApiConstants.mainBaseUrl}/reseñas/',
      {
        'producto': productId,
        'calificacion': calificacion,
        'comentario': comentario,
      },
      requiresAuth: true,
      includeTenantHost: true,
    );

    if (response.statusCode != 201) {
      throw Exception(_errorMessage('No se pudo enviar la reseña', response.body));
    }

    return ReviewModel.fromJson(jsonDecode(response.body));
  }
}
