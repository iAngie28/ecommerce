import 'package:flutter/material.dart';

import '../../core/storage/secure_storage.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_text_styles.dart';
import '../../core/widgets/feedback/app_toast.dart';
import '../../core/widgets/layout/app_dashboard_layout.dart';
import '../../core/widgets/layout/app_sidebar.dart';
import '../../gestion_usuario/repositories/auth_repository.dart';
import '../models/wishlist_item_model.dart';
import '../repositories/wishlist_repository.dart';

class WishlistScreen extends StatefulWidget {
  const WishlistScreen({super.key});

  @override
  State<WishlistScreen> createState() => _WishlistScreenState();
}

class _WishlistScreenState extends State<WishlistScreen> {
  final WishlistRepository _wishlistRepository = WishlistRepository();
  final AuthRepository _authRepository = AuthRepository();
  final SecureStorageService _storage = SecureStorageService();

  List<WishlistItemModel> _items = [];
  bool _isLoading = true;
  bool _isClearing = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadWishlist();
  }

  Future<void> _loadWishlist() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final items = await _wishlistRepository.fetchWishlist();
      if (!mounted) return;
      setState(() {
        _items = items;
        _isLoading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _error = e.toString().replaceAll('Exception: ', '');
        _isLoading = false;
      });
    }
  }

  String? _normalizeTenantValue(String? value) {
    if (value == null || value.trim().isEmpty) return null;
    final trimmed = value.trim();
    final parsed = Uri.tryParse(trimmed);
    final host = parsed != null && parsed.hasAuthority
        ? parsed.host
        : trimmed.split('/').first;
    return host.isEmpty ? null : host;
  }

  String? _tenantHostFor(WishlistItemModel item) {
    return _normalizeTenantValue(item.tiendaHost) ??
        _normalizeTenantValue(item.tiendaSchema);
  }

  String? _tenantSchemaFor(WishlistItemModel item) {
    final schema = _normalizeTenantValue(item.tiendaSchema);
    if (schema != null && schema.isNotEmpty) return schema.split('.').first;

    final host = _normalizeTenantValue(item.tiendaHost);
    if (host != null && host.isNotEmpty) return host.split('.').first;

    return null;
  }

  Future<void> _visitStore(WishlistItemModel item) async {
    final schema = _tenantSchemaFor(item);
    final host = _tenantHostFor(item);
    if (schema == null || schema.isEmpty || host == null || host.isEmpty) {
      AppToast.showError(context, 'No se pudo abrir la tienda');
      return;
    }

    await _storage.saveTenantInfo(schema, host);
    if (!mounted) return;
    Navigator.pushReplacementNamed(context, '/tienda');
  }

  Future<void> _removeItem(WishlistItemModel item) async {
    try {
      await _wishlistRepository.removeProduct(
        item.producto.id,
        tenantHost: _tenantHostFor(item),
      );
      if (!mounted) return;
      setState(() {
        _items.removeWhere((current) => current.id == item.id);
      });
      AppToast.showSuccess(context, 'Producto eliminado');
    } catch (e) {
      if (!mounted) return;
      AppToast.showError(context, e.toString().replaceAll('Exception: ', ''));
    }
  }

  Future<void> _confirmClear() async {
    if (_items.isEmpty || _isClearing) return;

    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Vaciar lista de deseos'),
        content: const Text('Se eliminaran todos los productos guardados.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.danger,
              foregroundColor: Colors.white,
            ),
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Vaciar'),
          ),
        ],
      ),
    );

    if (confirmed != true) return;

    setState(() => _isClearing = true);
    try {
      await _wishlistRepository.clearAll();
      if (!mounted) return;
      setState(() {
        _items = [];
        _isClearing = false;
      });
      AppToast.showSuccess(context, 'Lista de deseos vaciada');
    } catch (e) {
      if (!mounted) return;
      setState(() => _isClearing = false);
      AppToast.showError(context, e.toString().replaceAll('Exception: ', ''));
    }
  }

  @override
  Widget build(BuildContext context) {
    return AppDashboardLayout(
      brandName: 'MiQhatu',
      tenantValue: 'Wishlist',
      userName: 'Cliente',
      sidebarItems: [
        AppSidebarItem(
          icon: Icons.store,
          label: 'Explorar Tiendas',
          onTap: () => Navigator.pushReplacementNamed(context, '/tiendas'),
        ),
        AppSidebarItem(
          icon: Icons.storefront,
          label: 'Catalogo de Tienda',
          onTap: () => Navigator.pushReplacementNamed(context, '/tienda'),
        ),
        AppSidebarItem(
          icon: Icons.favorite_border,
          label: 'Mi Wishlist',
          isActive: true,
          onTap: () {},
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
          icon: Icons.person_outline,
          label: 'Mi Perfil',
          onTap: () => Navigator.pushReplacementNamed(context, '/perfil'),
        ),
        AppSidebarItem(
          icon: Icons.logout,
          label: 'Salir',
          isLogout: true,
          onTap: () async {
            await _authRepository.logout();
            if (!context.mounted) return;
            Navigator.pushReplacementNamed(context, '/login');
          },
        ),
      ],
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Mi Lista de Deseos', style: AppTextStyles.h1),
                    const SizedBox(height: 5),
                    Text(
                      '${_items.length} producto${_items.length == 1 ? '' : 's'} guardado${_items.length == 1 ? '' : 's'}',
                      style: AppTextStyles.subtitle,
                    ),
                  ],
                ),
              ),
              if (_items.isNotEmpty)
                IconButton(
                  tooltip: 'Vaciar lista',
                  onPressed: _isClearing ? null : _confirmClear,
                  icon: _isClearing
                      ? const SizedBox(
                          width: 22,
                          height: 22,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Icon(Icons.delete_sweep, color: AppColors.danger),
                ),
            ],
          ),
          const SizedBox(height: 24),
          if (_isLoading)
            const Center(
              child: CircularProgressIndicator(color: AppColors.accentTeal),
            )
          else if (_error != null)
            _buildError()
          else if (_items.isEmpty)
            _buildEmpty()
          else
            _buildItems(),
        ],
      ),
    );
  }

  Widget _buildError() {
    return Center(
      child: Column(
        children: [
          const Icon(Icons.error_outline, size: 64, color: AppColors.danger),
          const SizedBox(height: 16),
          Text(_error!, textAlign: TextAlign.center),
          const SizedBox(height: 16),
          ElevatedButton.icon(
            onPressed: _loadWishlist,
            icon: const Icon(Icons.refresh),
            label: const Text('Reintentar'),
          ),
        ],
      ),
    );
  }

  Widget _buildEmpty() {
    return Center(
      child: Container(
        constraints: const BoxConstraints(maxWidth: 420),
        padding: const EdgeInsets.all(28),
        decoration: BoxDecoration(
          color: AppColors.bgCard,
          borderRadius: BorderRadius.circular(18),
          border: Border.all(color: AppColors.border),
        ),
        child: Column(
          children: [
            const Icon(
              Icons.favorite_border,
              size: 72,
              color: AppColors.textMuted,
            ),
            const SizedBox(height: 18),
            const Text(
              'Tu lista de deseos esta vacia',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w800,
                color: AppColors.primaryDark,
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              'Guarda productos desde el catalogo de una tienda para volver a ellos cuando quieras.',
              textAlign: TextAlign.center,
              style: TextStyle(color: AppColors.textSlate, height: 1.4),
            ),
            const SizedBox(height: 22),
            ElevatedButton.icon(
              onPressed: () =>
                  Navigator.pushReplacementNamed(context, '/tiendas'),
              icon: const Icon(Icons.storefront),
              label: const Text('Explorar tiendas'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildItems() {
    return LayoutBuilder(
      builder: (context, constraints) {
        final isNarrow = constraints.maxWidth < 720;
        if (isNarrow) {
          return ListView.separated(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: _items.length,
            separatorBuilder: (_, _) => const SizedBox(height: 14),
            itemBuilder: (context, index) => _WishlistCard(
              item: _items[index],
              onVisitStore: () => _visitStore(_items[index]),
              onRemove: () => _removeItem(_items[index]),
            ),
          );
        }

        final columns = constraints.maxWidth > 1100 ? 3 : 2;
        return GridView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: columns,
            crossAxisSpacing: 18,
            mainAxisSpacing: 18,
            childAspectRatio: 1.85,
          ),
          itemCount: _items.length,
          itemBuilder: (context, index) => _WishlistCard(
            item: _items[index],
            onVisitStore: () => _visitStore(_items[index]),
            onRemove: () => _removeItem(_items[index]),
          ),
        );
      },
    );
  }
}

class _WishlistCard extends StatelessWidget {
  final WishlistItemModel item;
  final VoidCallback onVisitStore;
  final VoidCallback onRemove;

  const _WishlistCard({
    required this.item,
    required this.onVisitStore,
    required this.onRemove,
  });

  @override
  Widget build(BuildContext context) {
    final product = item.producto;
    final available = item.estaDisponible;

    return Container(
      decoration: BoxDecoration(
        color: AppColors.bgCard,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.border),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.04),
            blurRadius: 12,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Row(
        children: [
          SizedBox(
            width: 120,
            height: 180,
            child: ClipRRect(
              borderRadius: const BorderRadius.horizontal(
                left: Radius.circular(15),
              ),
              child: product.imagenUrl != null && product.imagenUrl!.isNotEmpty
                  ? Image.network(product.imagenUrl!, fit: BoxFit.cover)
                  : Container(
                      color: AppColors.bgSearch,
                      child: const Icon(
                        Icons.image_outlined,
                        color: AppColors.textMuted,
                        size: 42,
                      ),
                    ),
            ),
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Expanded(
                            child: Text(
                              product.nombre,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.w800,
                                color: AppColors.primaryDark,
                              ),
                            ),
                          ),
                          IconButton(
                            tooltip: 'Eliminar',
                            onPressed: onRemove,
                            icon: const Icon(
                              Icons.close,
                              color: AppColors.danger,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Text(
                        item.tiendaNombre ?? 'Tienda',
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                        style: const TextStyle(
                          color: AppColors.textSlate,
                          fontSize: 12,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          Flexible(
                            child: Text(
                              'Bs. ${product.precio.toStringAsFixed(2)}',
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                color: AppColors.primaryDark,
                                fontSize: 18,
                                fontWeight: FontWeight.w900,
                              ),
                            ),
                          ),
                          const SizedBox(width: 10),
                          _StatusBadge(
                            label: available
                                ? '${product.stock} disp.'
                                : (product.activo
                                      ? 'Sin stock'
                                      : 'No disponible'),
                            color: available
                                ? AppColors.successText
                                : AppColors.dangerText,
                            bg: available
                                ? AppColors.successBg
                                : AppColors.dangerBg,
                          ),
                        ],
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: [
                      OutlinedButton.icon(
                        onPressed: onVisitStore,
                        icon: const Icon(Icons.storefront, size: 18),
                        label: const Text('Visitar'),
                      ),
                      OutlinedButton.icon(
                        onPressed: onRemove,
                        icon: const Icon(Icons.delete_outline, size: 18),
                        label: const Text('Eliminar'),
                        style: OutlinedButton.styleFrom(
                          foregroundColor: AppColors.danger,
                          side: const BorderSide(color: AppColors.danger),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _StatusBadge extends StatelessWidget {
  final String label;
  final Color color;
  final Color bg;

  const _StatusBadge({
    required this.label,
    required this.color,
    required this.bg,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(99),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: color,
          fontSize: 11,
          fontWeight: FontWeight.w800,
        ),
      ),
    );
  }
}
