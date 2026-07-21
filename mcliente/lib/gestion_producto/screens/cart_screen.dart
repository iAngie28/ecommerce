import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../core/network/api_client.dart';
import '../../core/constants/api_constants.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_text_styles.dart';
import '../../core/widgets/layout/app_dashboard_layout.dart';
import '../../core/widgets/layout/app_sidebar.dart';
import '../../core/widgets/buttons/app_button.dart';
import '../../core/widgets/feedback/app_toast.dart';
import '../models/cart_model.dart';
import '../models/product_model.dart';
import '../repositories/cart_repository.dart';
import '../repositories/product_repository.dart';
import '../../gestion_pago/repositories/payment_repository.dart';
import '../../gestion_cliente/repositories/fidelizacion_repository.dart';

class CartScreen extends StatefulWidget {
  const CartScreen({super.key});

  @override
  State<CartScreen> createState() => _CartScreenState();
}

class _CartScreenState extends State<CartScreen> {
  CartModel? _cart;
  List<ProductModel> _recommendations = [];
  bool _isLoading = true;
  final CartRepository _cartRepository = CartRepository();
  final ProductRepository _productRepository = ProductRepository();
  final PaymentRepository _paymentRepository = PaymentRepository();
  final FidelizacionRepository _fidelizacionRepository =
      FidelizacionRepository();
  final TextEditingController _pointsController = TextEditingController();
  final FocusNode _pointsFocusNode = FocusNode();
  final NumberFormat _pointsFormat = NumberFormat.decimalPattern('es_BO');
  int _saldoPuntos = 0;
  double _valorPunto = 0.05;
  int? _previewPoints;
  double _previewDiscount = 0;
  String? _loyaltyError;
  bool _isLoadingPoints = false;
  bool _isCheckingOut = false;

  @override
  void initState() {
    super.initState();
    _loadCart();
  }

  @override
  void dispose() {
    _pointsController.dispose();
    _pointsFocusNode.dispose();
    super.dispose();
  }

  int get _maxPointsByTotal {
    final total = _cart?.total ?? 0;
    if (_valorPunto <= 0) return 0;
    return (total / _valorPunto).floor();
  }

  int get _maxRedeemablePoints => math.min(_saldoPuntos, _maxPointsByTotal);

  double get _finalTotal => math.max((_cart?.total ?? 0) - _previewDiscount, 0);

  Future<void> _loadCart() async {
    setState(() => _isLoading = true);
    try {
      final cart = await _cartRepository.fetchActiveCart();
      setState(() {
        _cart = cart;
        _isLoading = false;
      });
      await _loadLoyaltyData();
      _loadRecommendations();
    } catch (e) {
      setState(() => _isLoading = false);
      AppToast.showError(context, 'Error al cargar el carrito');
    }
  }

  Future<void> _loadLoyaltyData() async {
    if (_cart == null || _cart!.items.isEmpty) return;

    setState(() => _isLoadingPoints = true);
    try {
      final cuenta = await _fidelizacionRepository.obtenerMiCuenta(
        includeTenantHost: true,
      );
      final configuracion = await _fidelizacionRepository.obtenerConfiguracion(
        includeTenantHost: true,
      );

      setState(() {
        _saldoPuntos = cuenta['saldo_actual'] as int? ?? 0;
        _valorPunto = configuracion['VALOR_BS_POR_PUNTO'] ?? 0.05;
        _isLoadingPoints = false;

        if (_previewPoints != null && _previewPoints! > _maxRedeemablePoints) {
          _clearLoyaltyPreview();
        }
      });
    } catch (_) {
      setState(() => _isLoadingPoints = false);
    }
  }

  Future<void> _loadRecommendations() async {
    if (_cart == null || _cart!.items.isEmpty) return;
    try {
      final lastProductId = _cart!.items.last.producto.id;
      final recs = await _productRepository.fetchRecommendations(lastProductId);
      setState(() {
        _recommendations = recs;
      });
    } catch (_) {}
  }

  Future<void> _removeItem(int productId) async {
    if (_cart == null) return;
    try {
      final updatedCart = await _cartRepository.removeItem(
        _cart!.id,
        productId,
      );
      setState(() {
        _cart = updatedCart;
        if (updatedCart.items.isEmpty) {
          _clearLoyaltyPreview();
        }
      });
      AppToast.showSuccess(context, 'Producto removido');
      await _loadLoyaltyData();
    } catch (e) {
      AppToast.showError(context, 'No se pudo remover el producto');
    }
  }

  void _useMaxPoints() {
    if (_maxRedeemablePoints <= 0) return;
    _pointsController.text = _maxRedeemablePoints.toString();
    setState(() {
      _loyaltyError = null;
      _previewPoints = null;
      _previewDiscount = 0;
    });
  }

  void _previewLoyaltyDiscount() {
    final points = int.tryParse(_pointsController.text.trim()) ?? 0;

    if (points <= 0) {
      setState(() {
        _loyaltyError = 'Ingresa una cantidad de puntos mayor a cero.';
        _previewPoints = null;
        _previewDiscount = 0;
      });
      return;
    }

    if (points > _saldoPuntos) {
      setState(
        () => _loyaltyError =
            'Tienes ${_pointsFormat.format(_saldoPuntos)} puntos disponibles.',
      );
      return;
    }

    if (points > _maxPointsByTotal) {
      setState(
        () => _loyaltyError =
            'El descuento no puede superar el total del carrito.',
      );
      return;
    }

    setState(() {
      _loyaltyError = null;
      _previewPoints = points;
      _previewDiscount = math.min(points * _valorPunto, _cart?.total ?? 0);
    });
  }

  void _clearLoyaltyPreview() {
    _pointsController.clear();
    _loyaltyError = null;
    _previewPoints = null;
    _previewDiscount = 0;
  }

  void _handlePointsChanged(String _) {
    if (_loyaltyError == null &&
        _previewPoints == null &&
        _previewDiscount == 0) {
      return;
    }

    setState(() {
      _loyaltyError = null;
      _previewPoints = null;
      _previewDiscount = 0;
    });
  }

  Future<void> _processCheckout() async {
    if (_cart == null || _cart!.items.isEmpty) {
      AppToast.showInfo(context, 'Tu carrito está vacío');
      return;
    }
    if (_isCheckingOut) return;

    try {
      setState(() => _isCheckingOut = true);
      AppToast.showInfo(context, 'Procesando pedido...');
      final pointsToRedeem = _previewPoints ?? 0;

      final pedidoResponse = await ApiClient().post(
        '${ApiConstants.mainBaseUrl}/pedidos/crear-desde-carrito/',
        {
          'carrito_id': _cart!.id,
          if (pointsToRedeem > 0) 'puntos_canjeados': pointsToRedeem,
          if (pointsToRedeem > 0) 'descuento_puntos': _previewDiscount,
        },
        requiresAuth: true,
        includeTenantHost: true,
      );

      if (pedidoResponse.statusCode != 201 &&
          pedidoResponse.statusCode != 200) {
        final errorMsg =
            jsonDecode(pedidoResponse.body)['error'] ?? 'Error desconocido';
        throw Exception('Error al crear el pedido: $errorMsg');
      }

      final pedidoData = jsonDecode(pedidoResponse.body);
      final pedidoId = pedidoData['id'];

      // Vaciar carrito local (el backend ya lo marca como cerrado, actualizamos la vista localmente obteniendo uno nuevo o vaciando el actual si fuera necesario)
      setState(() {
        _cart = null;
      });

      // Intentamos procesar el pago nativo
      final success = await _paymentRepository.processPaymentSheet(
        pedidoId,
        puntosCanjeados: pointsToRedeem,
      );

      if (success) {
        AppToast.showSuccess(context, '¡Pedido realizado y pagado!');
        if (mounted) Navigator.pushReplacementNamed(context, '/pedidos');
      } else {
        AppToast.showInfo(
          context,
          'Pago cancelado o fallido. Revisa Mis Pedidos.',
        );
        if (mounted) Navigator.pushReplacementNamed(context, '/pedidos');
      }
    } catch (e) {
      AppToast.showError(context, 'Error al procesar el pago: $e');
    } finally {
      if (mounted) {
        setState(() => _isCheckingOut = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return AppDashboardLayout(
      brandName: 'MiQhatu',
      userName: 'Cliente',
      sidebarItems: [
        AppSidebarItem(
          icon: Icons.store,
          label: 'Explorar Tiendas',
          onTap: () => Navigator.pushReplacementNamed(context, '/tiendas'),
        ),
        AppSidebarItem(
          icon: Icons.storefront,
          label: 'Catálogo de Tienda',
          onTap: () => Navigator.pushReplacementNamed(context, '/tienda'),
        ),
        AppSidebarItem(
          icon: Icons.favorite_border,
          label: 'Mi Wishlist',
          onTap: () => Navigator.pushReplacementNamed(context, '/wishlist'),
        ),
        AppSidebarItem(
          icon: Icons.shopping_bag_outlined,
          label: 'Mis Pedidos',
          onTap: () => Navigator.pushReplacementNamed(context, '/pedidos'),
        ),
        AppSidebarItem(
          icon: Icons.card_giftcard,
          label: 'Mis Puntos',
          onTap: () => Navigator.pushReplacementNamed(context, '/puntos'),
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
            const Center(
              child: CircularProgressIndicator(color: AppColors.accentTeal),
            )
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
          const Icon(
            Icons.shopping_cart_outlined,
            size: 80,
            color: AppColors.textMuted,
          ),
          const SizedBox(height: 20),
          const Text(
            'Tu carrito está vacío',
            style: TextStyle(fontSize: 18, color: AppColors.textMuted),
          ),
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
                width: 50,
                height: 50,
                decoration: BoxDecoration(
                  color: AppColors.bgSearch,
                  borderRadius: BorderRadius.circular(8),
                ),
                clipBehavior: Clip.hardEdge,
                child:
                    item.producto.imagenUrl != null &&
                        item.producto.imagenUrl!.isNotEmpty
                    ? Image.network(
                        item.producto.imagenUrl!,
                        fit: BoxFit.cover,
                        errorBuilder: (_, __, ___) => const Icon(
                          Icons.image_outlined,
                          color: AppColors.textMuted,
                        ),
                      )
                    : const Icon(
                        Icons.image_outlined,
                        color: AppColors.textMuted,
                      ),
              ),
              title: Text(
                item.producto.nombre,
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
              subtitle: Text('${item.cantidad} x BS. ${item.producto.precio}'),
              trailing: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    'BS. ${item.subtotal}',
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      color: AppColors.primaryDark,
                    ),
                  ),
                  const SizedBox(width: 10),
                  IconButton(
                    icon: const Icon(
                      Icons.delete_outline,
                      color: AppColors.danger,
                    ),
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
              _buildSummaryRow(
                'Subtotal:',
                'BS. ${_cart!.total.toStringAsFixed(2)}',
                isStrong: true,
              ),
              const SizedBox(height: 18),
              _buildLoyaltyBox(),
              if (_previewPoints != null) ...[
                const SizedBox(height: 18),
                _buildSummaryRow(
                  'Descuento por puntos:',
                  '- BS. ${_previewDiscount.toStringAsFixed(2)}',
                  valueColor: AppColors.successText,
                ),
                const Divider(height: 28),
                _buildSummaryRow(
                  'Total estimado:',
                  'BS. ${_finalTotal.toStringAsFixed(2)}',
                  isStrong: true,
                  valueColor: AppColors.accentTeal,
                ),
              ],
              const SizedBox(height: 25),
              AppButton.submit(
                label: 'Proceder al Pago',
                isLoading: _isCheckingOut,
                onPressed: _processCheckout,
              ),
            ],
          ),
        ),
        if (_recommendations.isNotEmpty) _buildRecommendationsSection(),
        const SizedBox(height: 40),
      ],
    );
  }

  Widget _buildSummaryRow(
    String label,
    String value, {
    bool isStrong = false,
    Color? valueColor,
  }) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Expanded(
          child: Text(
            label,
            style: TextStyle(
              fontSize: isStrong ? 18 : 15,
              fontWeight: isStrong ? FontWeight.bold : FontWeight.w600,
              color: AppColors.textPrimary,
            ),
          ),
        ),
        Text(
          value,
          style:
              (isStrong
                      ? AppTextStyles.h2
                      : const TextStyle(
                          fontSize: 15,
                          fontWeight: FontWeight.w700,
                        ))
                  .copyWith(color: valueColor ?? AppColors.primaryDark),
        ),
      ],
    );
  }

  Widget _buildLoyaltyBox() {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.bgSurface,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppColors.border),
      ),
      child: Column(
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: AppColors.accentTeal.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: const Icon(
                  Icons.card_giftcard,
                  color: AppColors.accentTeal,
                  size: 20,
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Puntos MiQhatu',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: AppColors.primaryDark,
                      ),
                    ),
                    Text(
                      _isLoadingPoints
                          ? 'Consultando saldo...'
                          : '${_pointsFormat.format(_saldoPuntos)} pts disponibles en esta tienda',
                      style: const TextStyle(
                        color: AppColors.textSlate,
                        fontSize: 12,
                      ),
                    ),
                  ],
                ),
              ),
              if (_isLoadingPoints)
                const SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    color: AppColors.accentTeal,
                  ),
                ),
            ],
          ),
          const SizedBox(height: 14),
          LayoutBuilder(
            builder: (context, constraints) {
              final isNarrow = constraints.maxWidth < 420;
              final input = _buildPointsInput();
              final maxButton = _buildMaxPointsButton();
              final calculateButton = _buildCalculatePointsButton(
                fullWidth: isNarrow,
              );

              if (isNarrow) {
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Row(
                      children: [
                        Expanded(child: input),
                        const SizedBox(width: 8),
                        maxButton,
                      ],
                    ),
                    const SizedBox(height: 10),
                    calculateButton,
                  ],
                );
              }

              return Row(
                children: [
                  Expanded(child: input),
                  const SizedBox(width: 8),
                  maxButton,
                  const SizedBox(width: 8),
                  calculateButton,
                ],
              );
            },
          ),
          const SizedBox(height: 10),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Flexible(
                child: Text(
                  'Máximo usable en este carrito',
                  style: TextStyle(color: AppColors.textSlate, fontSize: 12),
                ),
              ),
              Text(
                '${_pointsFormat.format(_maxRedeemablePoints)} pts',
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  color: AppColors.primaryDark,
                  fontSize: 12,
                ),
              ),
            ],
          ),
          if (_loyaltyError != null) ...[
            const SizedBox(height: 10),
            Align(
              alignment: Alignment.centerLeft,
              child: Text(
                _loyaltyError!,
                style: const TextStyle(
                  color: AppColors.dangerText,
                  fontSize: 12,
                ),
              ),
            ),
          ],
          if (_previewPoints != null) ...[
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppColors.successBg,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppColors.success.withOpacity(0.25)),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Descuento estimado',
                          style: TextStyle(
                            color: AppColors.successText,
                            fontSize: 12,
                          ),
                        ),
                        Text(
                          'BS. ${_previewDiscount.toStringAsFixed(2)}',
                          style: const TextStyle(
                            color: AppColors.successText,
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                        ),
                      ],
                    ),
                  ),
                  TextButton(
                    onPressed: () => setState(_clearLoyaltyPreview),
                    child: const Text('Quitar'),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildPointsInput() {
    return TextField(
      key: const ValueKey('cart_points_input'),
      controller: _pointsController,
      focusNode: _pointsFocusNode,
      keyboardType: TextInputType.number,
      textInputAction: TextInputAction.done,
      onTap: () {
        if (!_pointsFocusNode.hasFocus) {
          _pointsFocusNode.requestFocus();
        }
      },
      decoration: InputDecoration(
        hintText: '0',
        suffixText: 'pts',
        filled: true,
        fillColor: AppColors.bgSearch,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: AppColors.border),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: AppColors.border),
        ),
        contentPadding: const EdgeInsets.symmetric(
          horizontal: 12,
          vertical: 10,
        ),
      ),
      onChanged: _handlePointsChanged,
    );
  }

  Widget _buildMaxPointsButton() {
    return OutlinedButton(
      onPressed: _maxRedeemablePoints > 0 ? _useMaxPoints : null,
      child: const Text('Máx.'),
    );
  }

  Widget _buildCalculatePointsButton({required bool fullWidth}) {
    final button = ElevatedButton(
      onPressed: _maxRedeemablePoints > 0 ? _previewLoyaltyDiscount : null,
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.accentTeal,
        foregroundColor: AppColors.white,
        padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
      ),
      child: const Text('Calcular'),
    );

    if (!fullWidth) return button;
    return SizedBox(width: double.infinity, child: button);
  }

  Widget _buildRecommendationsSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 40),
        const Text(
          'Te podría interesar',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 15),
        SizedBox(
          height: 180,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            itemCount: _recommendations.length,
            separatorBuilder: (context, index) => const SizedBox(width: 15),
            itemBuilder: (context, index) {
              final rec = _recommendations[index];
              return Container(
                width: 140,
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: AppColors.bgCard,
                  borderRadius: BorderRadius.circular(15),
                  border: Border.all(color: AppColors.border),
                ),
                child: Column(
                  children: [
                    Expanded(
                      child: rec.imagenUrl != null && rec.imagenUrl!.isNotEmpty
                          ? Image.network(
                              rec.imagenUrl!,
                              fit: BoxFit.cover,
                              width: double.infinity,
                              errorBuilder: (_, __, ___) => Icon(
                                Icons.shopping_bag_outlined,
                                color: AppColors.accentTeal.withOpacity(0.5),
                                size: 40,
                              ),
                            )
                          : Icon(
                              Icons.shopping_bag_outlined,
                              color: AppColors.accentTeal.withOpacity(0.5),
                              size: 40,
                            ),
                    ),
                    Text(
                      rec.nombre,
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 12,
                      ),
                      maxLines: 2,
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 5),
                    Text(
                      'BS. ${rec.precio}',
                      style: const TextStyle(
                        color: AppColors.accentTeal,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 5),
                    InkWell(
                      onTap: () async {
                        await _cartRepository.addItem(_cart!.id, rec.id);
                        _loadCart();
                      },
                      child: const Text(
                        'Añadir',
                        style: TextStyle(
                          color: AppColors.primaryDark,
                          fontSize: 11,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}
