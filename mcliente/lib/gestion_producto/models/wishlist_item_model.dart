import 'product_model.dart';

class WishlistItemModel {
  final int id;
  final ProductModel producto;
  final DateTime? agregadoEn;
  final bool notificado;
  final String? tiendaNombre;
  final String? tiendaSchema;
  final String? tiendaHost;

  WishlistItemModel({
    required this.id,
    required this.producto,
    this.agregadoEn,
    this.notificado = false,
    this.tiendaNombre,
    this.tiendaSchema,
    this.tiendaHost,
  });

  bool get estaDisponible => producto.activo && producto.stock > 0;

  factory WishlistItemModel.fromJson(Map<String, dynamic> json) {
    final rawProduct = json['producto'];
    final productJson = rawProduct is Map
        ? Map<String, dynamic>.from(rawProduct)
        : <String, dynamic>{
            'id': json['producto_id'] ?? rawProduct ?? 0,
            'nombre': 'Producto',
            'descripcion': '',
            'precio': 0,
            'stock': 0,
            'activo': false,
          };

    return WishlistItemModel(
      id: int.tryParse((json['id'] ?? 0).toString()) ?? 0,
      producto: ProductModel.fromJson(productJson),
      agregadoEn: DateTime.tryParse(json['agregado_en']?.toString() ?? ''),
      notificado: json['notificado'] == true,
      tiendaNombre: json['tienda_nombre']?.toString(),
      tiendaSchema: json['tienda_schema']?.toString(),
      tiendaHost: json['tienda_host']?.toString(),
    );
  }
}
