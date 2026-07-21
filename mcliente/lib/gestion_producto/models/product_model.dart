class ProductModel {
  final int id;
  final String nombre;
  final String descripcion;
  final double precio;
  final int stock;
  final String sku;
  final int? categoria;
  final String? categoriaNombre;
  final String? imagenUrl;
  final bool activo;
  final double promedioCalificacion;
  final int totalResenas;
  final bool compradoPorCliente;

  ProductModel({
    required this.id,
    required this.nombre,
    required this.descripcion,
    required this.precio,
    required this.stock,
    this.sku = '',
    this.categoria,
    this.categoriaNombre,
    this.imagenUrl,
    this.activo = true,
    this.promedioCalificacion = 0,
    this.totalResenas = 0,
    this.compradoPorCliente = false,
  });

  factory ProductModel.fromJson(Map<String, dynamic> json) {
    return ProductModel(
      id: json['id'] ?? 0,
      nombre: json['nombre'] ?? '',
      descripcion: json['descripcion'] ?? '',
      precio: double.tryParse(json['precio'].toString()) ?? 0.0,
      stock: int.tryParse(json['stock'].toString()) ?? 0,
      sku: json['sku'] ?? '',
      categoria: json['categoria'],
      categoriaNombre:
          json['categoria_detail']?['nombre'] ?? json['categoria_nombre'],
      imagenUrl: _resolveImageUrl(json['imagen_url']),
      activo: json['activo'] is bool
          ? json['activo'] as bool
          : json['activo']?.toString().toLowerCase() != 'false',
      promedioCalificacion:
          double.tryParse((json['promedio_calificacion'] ?? 0).toString()) ??
          0,
      totalResenas:
          int.tryParse((json['total_reseñas'] ?? 0).toString()) ?? 0,
      compradoPorCliente: json['comprado_por_cliente'] is bool
          ? json['comprado_por_cliente'] as bool
          : json['comprado_por_cliente']?.toString().toLowerCase() == 'true',
    );
  }

  static String? _resolveImageUrl(String? url) {
    if (url == null || url.isEmpty) return null;
    if (url.startsWith('http://') || url.startsWith('https://')) return url;
    return 'http://157.173.102.129:8001$url'; // Fallback for relative URLs
  }

  Map<String, dynamic> toJson() => {
    'nombre': nombre,
    'descripcion': descripcion,
    'precio': precio.toString(),
    'stock': stock,
    'sku': sku,
    'categoria': categoria,
    'activo': activo,
    'promedio_calificacion': promedioCalificacion,
    'total_reseñas': totalResenas,
    'comprado_por_cliente': compradoPorCliente,
  };

  ProductModel copyWith({
    int? id,
    String? nombre,
    String? descripcion,
    double? precio,
    int? stock,
    String? sku,
    int? categoria,
    String? categoriaNombre,
    String? imagenUrl,
    bool? activo,
    double? promedioCalificacion,
    int? totalResenas,
    bool? compradoPorCliente,
  }) {
    return ProductModel(
      id: id ?? this.id,
      nombre: nombre ?? this.nombre,
      descripcion: descripcion ?? this.descripcion,
      precio: precio ?? this.precio,
      stock: stock ?? this.stock,
      sku: sku ?? this.sku,
      categoria: categoria ?? this.categoria,
      categoriaNombre: categoriaNombre ?? this.categoriaNombre,
      imagenUrl: imagenUrl ?? this.imagenUrl,
      activo: activo ?? this.activo,
      promedioCalificacion:
          promedioCalificacion ?? this.promedioCalificacion,
      totalResenas: totalResenas ?? this.totalResenas,
      compradoPorCliente: compradoPorCliente ?? this.compradoPorCliente,
    );
  }
}
