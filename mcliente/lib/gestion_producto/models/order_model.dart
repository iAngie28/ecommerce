import 'cart_model.dart';

class OrderModel {
  final int id;
  final String numero;
  final String estado;
  final double total;
  final DateTime fecha;
  final List<CartItemModel>? items;
  final String? tenantName;

  OrderModel({
    required this.id,
    required this.numero,
    required this.estado,
    required this.total,
    required this.fecha,
    this.items,
    this.tenantName,
  });

  factory OrderModel.fromJson(Map<String, dynamic> json) {
    return OrderModel(
      id: json['id'],
      numero: json['numero_pedido'] ?? 'PED-${json['id']}',
      estado: json['estado'],
      total: double.parse(json['total'].toString()),
      fecha: DateTime.parse(json['created_at']),
      tenantName: json['tenant_name'],
      items: json['carrito'] != null && json['carrito']['items'] != null
          ? (json['carrito']['items'] as List).map((i) => CartItemModel.fromJson(i)).toList()
          : null,
    );
  }
}
