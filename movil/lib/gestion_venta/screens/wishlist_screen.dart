import 'package:flutter/material.dart';
import '../models/wishlist_item.dart';
import '../services/wishlist_service.dart';

class WishlistScreen extends StatefulWidget {
  final String token;

  const WishlistScreen({Key? key, required this.token}) : super(key: key);

  @override
  State<WishlistScreen> createState() => _WishlistScreenState();
}

class _WishlistScreenState extends State<WishlistScreen> {
  final WishlistService _wishlistService = WishlistService();
  List<WishlistItem> _items = [];
  bool _cargando = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _cargarWishlist();
  }

  Future<void> _cargarWishlist() async {
    setState(() {
      _cargando = true;
      _error = null;
    });

    try {
      final items = await _wishlistService.getWishlist(widget.token);
      setState(() {
        _items = items;
        _cargando = false;
      });
    } catch (e) {
      setState(() {
        _error = 'Ocurrió un error al cargar tu lista de deseos.';
        _cargando = false;
      });
    }
  }

  Future<void> _eliminarItem(int productoId) async {
    try {
      await _wishlistService.eliminarProducto(productoId, widget.token);
      setState(() {
        _items.removeWhere((item) => item.productoId == productoId);
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('No se pudo eliminar el producto')),
      );
    }
  }

  Future<void> _moverAlCarrito(int productoId) async {
    try {
      await _wishlistService.moverAlCarrito(productoId, widget.token);
      setState(() {
        _items.removeWhere((item) => item.productoId == productoId);
      });
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Producto movido al carrito de compras'),
          backgroundColor: Colors.green,
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Error al mover producto al carrito'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  Future<void> _mostrarDialogoVaciar() async {
    final confirmar = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('¿Vaciar lista?'),
        content: const Text('Se eliminarán todos los productos de tu lista de deseos.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancelar'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Vaciar'),
          ),
        ],
      ),
    );

    if (confirmar == true) {
      setState(() => _cargando = true);
      try {
        await _wishlistService.vaciarWishlist(widget.token);
        setState(() {
          _items.clear();
          _cargando = false;
        });
      } catch (e) {
        setState(() => _cargando = false);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Error al vaciar la lista')),
        );
      }
    }
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.favorite_border, size: 80, color: Colors.grey.shade400),
          const SizedBox(height: 16),
          const Text(
            'Tu lista de deseos está vacía',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          const Text(
            'Guarda los productos que más te gustan\npara comprarlos después.',
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.grey),
          ),
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: () {
              // Navegar al catálogo
              Navigator.pop(context);
            },
            child: const Text('Explorar Productos'),
          )
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Lista de Deseos'),
        actions: [
          if (_items.isNotEmpty && !_cargando)
            IconButton(
              icon: const Icon(Icons.delete_sweep),
              tooltip: 'Vaciar lista',
              onPressed: _mostrarDialogoVaciar,
            ),
        ],
      ),
      body: _cargando
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(child: Text(_error!, style: const TextStyle(color: Colors.red)))
              : _items.isEmpty
                  ? _buildEmptyState()
                  : ListView.builder(
                      padding: const EdgeInsets.all(12),
                      itemCount: _items.length,
                      itemBuilder: (context, index) {
                        final item = _items[index];
                        return Card(
                          margin: const EdgeInsets.only(bottom: 12),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Padding(
                            padding: const EdgeInsets.all(12.0),
                            child: Row(
                              children: [
                                // Imagen del producto
                                Container(
                                  width: 80,
                                  height: 80,
                                  decoration: BoxDecoration(
                                    color: Colors.grey.shade200,
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: item.imagenUrl != null
                                      ? ClipRRect(
                                          borderRadius: BorderRadius.circular(8),
                                          child: Image.network(item.imagenUrl!, fit: BoxFit.cover),
                                        )
                                      : const Icon(Icons.image, color: Colors.grey),
                                ),
                                const SizedBox(width: 16),
                                // Detalles
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        item.nombreProducto,
                                        style: const TextStyle(
                                          fontWeight: FontWeight.bold,
                                          fontSize: 16,
                                        ),
                                        maxLines: 2,
                                        overflow: TextOverflow.ellipsis,
                                      ),
                                      const SizedBox(height: 8),
                                      Row(
                                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                        children: [
                                          Text(
                                            '\$${item.precio.toStringAsFixed(2)}',
                                            style: const TextStyle(
                                              color: Colors.blue,
                                              fontWeight: FontWeight.bold,
                                              fontSize: 16,
                                            ),
                                          ),
                                          if (!item.activo)
                                            Container(
                                              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                              decoration: BoxDecoration(
                                                color: Colors.orange.shade100,
                                                borderRadius: BorderRadius.circular(4),
                                              ),
                                              child: const Text(
                                                'Agotado',
                                                style: TextStyle(color: Colors.deepOrange, fontSize: 12),
                                              ),
                                            ),
                                        ],
                                      ),
                                    ],
                                  ),
                                ),
                                // Acciones (Eliminar y Mover)
                                Column(
                                  children: [
                                    IconButton(
                                      icon: const Icon(Icons.close, color: Colors.grey),
                                      onPressed: () => _eliminarItem(item.productoId),
                                    ),
                                    IconButton(
                                      icon: Icon(Icons.shopping_cart, 
                                        color: item.activo ? Colors.green : Colors.grey.shade300
                                      ),
                                      onPressed: item.activo 
                                          ? () => _moverAlCarrito(item.productoId) 
                                          : null,
                                    ),
                                  ],
                                )
                              ],
                            ),
                          ),
                        );
                      },
                    ),
    );
  }
}
