class ProductModel {
  final int id;
  final String nombre;
  final String descripcion;
  final double precio;
  final int stock;

  ProductModel({
    required this.id,
    required this.nombre,
    required this.descripcion,
    required this.precio,
    required this.stock,
  });

  // JSON → Modelo (para parsear respuesta del GET)
  factory ProductModel.fromJson(Map<String, dynamic> json) {
    return ProductModel(
      id: json['id'] ?? 0,
      nombre: json['nombre'] ?? '',
      descripcion: json['descripcion'] ?? '',
      precio: double.tryParse(json['precio'].toString()) ?? 0.0,
      stock: int.tryParse(json['stock'].toString()) ?? 0,
    );
  }

  // Modelo → JSON (para enviar en POST/PUT)
  Map<String, dynamic> toJson() => {
        'nombre': nombre,
        'descripcion': descripcion,
        'precio': precio.toString(),
        'stock': stock,
      };
}