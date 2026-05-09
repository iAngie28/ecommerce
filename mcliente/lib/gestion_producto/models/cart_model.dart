import 'product_model.dart';

class CartItemModel {
  final int? id;
  final ProductModel producto;
  final int cantidad;
  final double subtotal;

  CartItemModel({
    this.id,
    required this.producto,
    required this.cantidad,
    required this.subtotal,
  });

  factory CartItemModel.fromJson(Map<String, dynamic> json) {
    return CartItemModel(
      id: json['id'],
      producto: ProductModel.fromJson(json['producto']),
      cantidad: json['cantidad'],
      subtotal: double.parse(json['subtotal'].toString()),
    );
  }
}

class CartModel {
  final int id;
  final List<CartItemModel> items;
  final double total;
  final String estado;

  CartModel({
    required this.id,
    required this.items,
    required this.total,
    required this.estado,
  });

  factory CartModel.fromJson(Map<String, dynamic> json) {
    var itemsList = json['items'] as List;
    return CartModel(
      id: json['id'],
      items: itemsList.map((i) => CartItemModel.fromJson(i)).toList(),
      total: double.parse(json['total'].toString()),
      estado: json['estado'],
    );
  }
}
