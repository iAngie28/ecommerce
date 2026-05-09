class CategoryModel {
  final int id;
  final String nombre;
  final String descripcion;
  final int? parent;
  final bool activo;
  final String? rutaCompleta;

  CategoryModel({
    required this.id,
    required this.nombre,
    required this.descripcion,
    this.parent,
    this.activo = true,
    this.rutaCompleta,
  });

  factory CategoryModel.fromJson(Map<String, dynamic> json) {
    return CategoryModel(
      id: json['id'],
      nombre: json['nombre'],
      descripcion: json['descripcion'] ?? '',
      parent: json['parent'],
      activo: json['activo'] ?? true,
      rutaCompleta: json['ruta_completa'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'nombre': nombre,
      'descripcion': descripcion,
      'parent': parent,
      'activo': activo,
    };
  }
}
