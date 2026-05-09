import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_text_styles.dart';
import '../../core/widgets/layout/app_dashboard_layout.dart';
import '../../core/widgets/layout/app_sidebar.dart';
import '../../core/widgets/buttons/app_button.dart';
import '../../core/widgets/feedback/app_toast.dart';
import '../models/cart_model.dart';
import '../repositories/cart_repository.dart';
import '../../gestion_pago/repositories/payment_repository.dart';

class CartScreen extends StatefulWidget {
  const CartScreen({super.key});

  @override
  State<CartScreen> createState() => _CartScreenState();
}

class _CartScreenState extends State<CartScreen> {
  CartModel? _cart;
  bool _isLoading = true;
  final CartRepository _cartRepository = CartRepository();
  final PaymentRepository _paymentRepository = PaymentRepository();

  @override
  void initState() {
    super.initState();
    _loadCart();
  }

  Future<void> _loadCart() async {
    setState(() => _isLoading = true);
    try {
      final cart = await _cartRepository.fetchActiveCart();
      setState(() {
        _cart = cart;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      AppToast.showError(context, 'Error al cargar el carrito');
    }
  }

  Future<void> _removeItem(int productId) async {
    if (_cart == null) return;
    try {
      final updatedCart = await _cartRepository.removeItem(_cart!.id, productId);
      setState(() => _cart = updatedCart);
      AppToast.showSuccess(context, 'Producto removido');
    } catch (e) {
      AppToast.showError(context, 'No se pudo remover el producto');
    }
  }

  Future<void> _processCheckout() async {
    if (_cart == null || _cart!.items.isEmpty) {
      AppToast.showInfo(context, 'Tu carrito está vacío');
      return;
    }

    try {
      AppToast.showInfo(context, 'Procesando pedido...');
      // 1. Cerrar carrito (convertir en pedido)
      await _cartRepository.checkout(_cart!.id);
      
      // El backend devuelve el carrito con un ID de pedido asociado o el estado cambiado
      // Pero usualmente necesitamos el pedidoId para Stripe.
      // Vamos a asumir que el backend crea el pedido y podemos obtener el ID.
      // NOTA: En la implementación real del backend, 'cerrar' debería devolver el pedido_id.
      
      // Por ahora, simularemos que el pedido_id es el mismo que el carrito o buscaremos el último pedido.
      // TODO: Ajustar backend para devolver pedido_id en /cerrar/
      
      // Intentamos procesar el pago (usando un ID genérico por ahora si el backend no lo da)
      // En una implementación real, recibiríamos el pedido_id aquí.
      final success = await _paymentRepository.processPaymentSheet(_cart!.id);
      
      if (success) {
        AppToast.showSuccess(context, '¡Pedido realizado y pagado!');
        Navigator.pushReplacementNamed(context, '/pedidos');
      }
    } catch (e) {
      AppToast.showError(context, 'Error al procesar el pago: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return AppDashboardLayout(
      brandName: 'MiQhatu',
      userName: 'Cliente',
      sidebarItems: [
        AppSidebarItem(
          icon: Icons.storefront,
          label: 'Catálogo',
          onTap: () => Navigator.pushReplacementNamed(context, '/tienda'),
        ),
        AppSidebarItem(
          icon: Icons.shopping_bag_outlined,
          label: 'Mis Pedidos',
          onTap: () => Navigator.pushReplacementNamed(context, '/pedidos'),
        ),
        AppSidebarItem(
          icon: Icons.logout,
          label: 'Salir',
          isLogout: true,
          onTap: () => Navigator.pushReplacementNamed(context, '/login'),
        ),
      ],
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Tu Carrito', style: AppTextStyles.h1),
          const SizedBox(height: 30),
          if (_isLoading)
            const Center(child: CircularProgressIndicator(color: AppColors.accentTeal))
          else if (_cart == null || _cart!.items.isEmpty)
            _buildEmptyCart()
          else
            _buildCartContent(),
        ],
      ),
    );
  }

  Widget _buildEmptyCart() {
    return Center(
      child: Column(
        children: [
          const Icon(Icons.shopping_cart_outlined, size: 80, color: AppColors.textMuted),
          const SizedBox(height: 20),
          const Text('Tu carrito está vacío', style: TextStyle(fontSize: 18, color: AppColors.textMuted)),
          const SizedBox(height: 30),
          AppButton.primary(
            label: 'Ir a comprar',
            onPressed: () => Navigator.pushReplacementNamed(context, '/tienda'),
          ),
        ],
      ),
    );
  }

  Widget _buildCartContent() {
    return Column(
      children: [
        ListView.separated(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: _cart!.items.length,
          separatorBuilder: (context, index) => const Divider(),
          itemBuilder: (context, index) {
            final item = _cart!.items[index];
            return ListTile(
              leading: Container(
                width: 50, height: 50,
                decoration: BoxDecoration(color: AppColors.bgSearch, borderRadius: BorderRadius.circular(8)),
                child: const Icon(Icons.image_outlined, color: AppColors.textMuted),
              ),
              title: Text(item.producto.nombre, style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('${item.cantidad} x BS. ${item.producto.precio}'),
              trailing: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text('BS. ${item.subtotal}', style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.primaryDark)),
                  const SizedBox(width: 10),
                  IconButton(
                    icon: const Icon(Icons.delete_outline, color: AppColors.danger),
                    onPressed: () => _removeItem(item.producto.id),
                  ),
                ],
              ),
            );
          },
        ),
        const SizedBox(height: 40),
        Container(
          padding: const EdgeInsets.all(25),
          decoration: BoxDecoration(
            color: AppColors.bgCard,
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: AppColors.border),
          ),
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Total a pagar:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  Text('BS. ${_cart!.total}', style: AppTextStyles.h2.copyWith(color: AppColors.accentTeal)),
                ],
              ),
              const SizedBox(height: 25),
              AppButton.submit(
                label: 'Proceder al Pago',
                onPressed: _processCheckout,
              ),
            ],
          ),
        ),
      ],
    );
  }
}
