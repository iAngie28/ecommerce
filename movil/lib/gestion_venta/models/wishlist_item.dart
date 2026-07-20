class WishlistItem {
  final int id;
  final int productoId;
  final String nombreProducto;
  final double precio;
  final bool activo;
  final String? imagenUrl;

  WishlistItem({
    required this.id,
    required this.productoId,
    required this.nombreProducto,
    required this.precio,
    required this.activo,
    this.imagenUrl,
  });

  factory WishlistItem.fromJson(Map<String, dynamic> json) {
    // Manejo seguro del producto anidado que viene del serializador de Django
    final productoData = json['producto'] ?? {};
    
    return WishlistItem(
      id: json['id'] ?? 0,
      productoId: productoData['id'] ?? 0,
      nombreProducto: productoData['nombre'] ?? 'Producto Desconocido',
      precio: (productoData['precio'] ?? 0.0).toDouble(),
      activo: productoData['activo'] ?? true,
      imagenUrl: productoData['imagen'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'producto': {
        'id': productoId,
        'nombre': nombreProducto,
        'precio': precio,
        'activo': activo,
        'imagen': imagenUrl,
      }
    };
  }
}
