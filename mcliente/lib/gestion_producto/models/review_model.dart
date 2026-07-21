class ReviewModel {
  final int id;
  final String clienteNombre;
  final int calificacion;
  final String comentario;
  final DateTime? fechaCreacion;

  ReviewModel({
    required this.id,
    required this.clienteNombre,
    required this.calificacion,
    required this.comentario,
    this.fechaCreacion,
  });

  factory ReviewModel.fromJson(Map<String, dynamic> json) {
    return ReviewModel(
      id: int.tryParse((json['id'] ?? 0).toString()) ?? 0,
      clienteNombre:
          json['cliente_nombre']?.toString().trim().isNotEmpty == true
          ? json['cliente_nombre'].toString()
          : 'Cliente Anonimo',
      calificacion: int.tryParse((json['calificacion'] ?? 0).toString()) ?? 0,
      comentario: json['comentario']?.toString() ?? '',
      fechaCreacion: DateTime.tryParse(json['fecha_creacion']?.toString() ?? ''),
    );
  }
}

class ProductReviewsResult {
  final List<ReviewModel> reviews;
  final double promedio;
  final int totalResenas;

  ProductReviewsResult({
    required this.reviews,
    required this.promedio,
    required this.totalResenas,
  });

  factory ProductReviewsResult.fromJson(dynamic decoded) {
    final List<dynamic> rawReviews;
    Map<String, dynamic>? stats;

    if (decoded is Map) {
      rawReviews = (decoded['results'] ?? decoded['resultados'] ?? []) is List
          ? (decoded['results'] ?? decoded['resultados'] ?? []) as List
          : [];
      if (decoded['estadisticas'] is Map) {
        stats = Map<String, dynamic>.from(decoded['estadisticas'] as Map);
      }
    } else if (decoded is List) {
      rawReviews = decoded;
    } else {
      rawReviews = [];
    }

    final reviews = rawReviews
        .whereType<Map>()
        .map((item) => ReviewModel.fromJson(Map<String, dynamic>.from(item)))
        .toList();

    return ProductReviewsResult(
      reviews: reviews,
      promedio:
          double.tryParse((stats?['promedio'] ?? 0).toString()) ??
          _averageFromReviews(reviews),
      totalResenas:
          int.tryParse((stats?['total_reseñas'] ?? reviews.length).toString()) ??
          reviews.length,
    );
  }

  static double _averageFromReviews(List<ReviewModel> reviews) {
    if (reviews.isEmpty) return 0;
    final total = reviews.fold<int>(0, (sum, item) => sum + item.calificacion);
    return double.parse((total / reviews.length).toStringAsFixed(1));
  }
}
