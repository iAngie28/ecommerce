class Resena {
  final int id;
  final String clienteNombre;
  final int calificacion;
  final String? comentario;
  final String fechaCreacion;

  Resena({
    required this.id,
    required this.clienteNombre,
    required this.calificacion,
    this.comentario,
    required this.fechaCreacion,
  });

  factory Resena.fromJson(Map<String, dynamic> json) {
    return Resena(
      id: json['id'],
      clienteNombre: json['cliente_nombre'] ?? 'Usuario',
      calificacion: json['calificacion'],
      comentario: json['comentario'],
      fechaCreacion: json['fecha_creacion'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'cliente_nombre': clienteNombre,
      'calificacion': calificacion,
      'comentario': comentario,
      'fecha_creacion': fechaCreacion,
    };
  }
}
