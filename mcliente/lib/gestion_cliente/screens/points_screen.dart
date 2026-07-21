import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../../core/theme/app_colors.dart';
import '../../core/theme/app_text_styles.dart';
import '../../core/widgets/feedback/app_toast.dart';
import '../../core/widgets/layout/app_dashboard_layout.dart';
import '../../core/widgets/layout/app_sidebar.dart';
import '../../gestion_usuario/repositories/auth_repository.dart';
import '../repositories/fidelizacion_repository.dart';

class PointsScreen extends StatefulWidget {
  const PointsScreen({super.key});

  @override
  State<PointsScreen> createState() => _PointsScreenState();
}

class _PointsScreenState extends State<PointsScreen> {
  final FidelizacionRepository _fidelizacionRepository =
      FidelizacionRepository();
  final AuthRepository _authRepository = AuthRepository();
  final NumberFormat _pointsFormat = NumberFormat.decimalPattern('es_BO');

  Map<String, dynamic>? _cuenta;
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadPoints();
  }

  Future<void> _loadPoints() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final cuenta = await _fidelizacionRepository.obtenerMiCuenta();
      if (!mounted) return;
      setState(() {
        _cuenta = cuenta;
        _isLoading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _error = e.toString().replaceAll('Exception: ', '');
        _isLoading = false;
      });
      AppToast.showError(context, 'No se pudieron cargar tus puntos');
    }
  }

  List<Map<String, dynamic>> get _tiendas {
    final raw = _cuenta?['tiendas'];
    if (raw is! List) return [];
    return raw
        .whereType<Map>()
        .map((item) => Map<String, dynamic>.from(item))
        .toList();
  }

  int get _saldoActual => _cuenta?['saldo_actual'] as int? ?? 0;
  int get _puntosHistoricos => _cuenta?['puntos_historicos'] as int? ?? 0;

  @override
  Widget build(BuildContext context) {
    return AppDashboardLayout(
      brandName: 'MiQhatu',
      tenantValue: 'Puntos',
      userName: 'Cliente',
      sidebarItems: [
        AppSidebarItem(
          icon: Icons.store,
          label: 'Explorar Tiendas',
          onTap: () => Navigator.pushReplacementNamed(context, '/tiendas'),
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
          isActive: true,
          onTap: () {},
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
          Text('Mis Puntos', style: AppTextStyles.h1),
          const SizedBox(height: 5),
          Text(
            'Consulta tu saldo acumulado por tienda',
            style: AppTextStyles.subtitle,
          ),
          const SizedBox(height: 24),
          if (_isLoading)
            const Center(
              child: CircularProgressIndicator(color: AppColors.accentTeal),
            )
          else if (_error != null)
            _buildError()
          else
            _buildContent(),
        ],
      ),
    );
  }

  Widget _buildError() {
    return Center(
      child: Column(
        children: [
          const Icon(Icons.error_outline, color: AppColors.danger, size: 58),
          const SizedBox(height: 14),
          Text(
            _error!,
            textAlign: TextAlign.center,
            style: const TextStyle(color: AppColors.textSlate),
          ),
          const SizedBox(height: 16),
          ElevatedButton.icon(
            onPressed: _loadPoints,
            icon: const Icon(Icons.refresh),
            label: const Text('Reintentar'),
          ),
        ],
      ),
    );
  }

  Widget _buildContent() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(22),
          decoration: BoxDecoration(
            color: AppColors.primaryDark,
            borderRadius: BorderRadius.circular(18),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Icon(
                Icons.card_giftcard,
                color: AppColors.accentTeal,
                size: 32,
              ),
              const SizedBox(height: 18),
              const Text(
                'Saldo total disponible',
                style: TextStyle(color: AppColors.white, fontSize: 13),
              ),
              const SizedBox(height: 4),
              Text(
                '${_pointsFormat.format(_saldoActual)} pts',
                style: const TextStyle(
                  color: AppColors.white,
                  fontSize: 34,
                  fontWeight: FontWeight.w900,
                ),
              ),
              const SizedBox(height: 10),
              Text(
                '${_pointsFormat.format(_puntosHistoricos)} pts acumulados historicamente',
                style: const TextStyle(
                  color: AppColors.textMuted,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 24),
        const Text(
          'Puntos por tienda',
          style: TextStyle(
            color: AppColors.primaryDark,
            fontSize: 18,
            fontWeight: FontWeight.w800,
          ),
        ),
        const SizedBox(height: 14),
        if (_tiendas.isEmpty)
          _buildEmptyStores()
        else
          ListView.separated(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: _tiendas.length,
            separatorBuilder: (context, index) => const SizedBox(height: 12),
            itemBuilder: (context, index) => _buildStorePoints(_tiendas[index]),
          ),
      ],
    );
  }

  Widget _buildEmptyStores() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: AppColors.bgCard,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.border),
      ),
      child: const Text(
        'Aún no tienes puntos registrados en tiendas.',
        textAlign: TextAlign.center,
        style: TextStyle(color: AppColors.textSlate),
      ),
    );
  }

  Widget _buildStorePoints(Map<String, dynamic> tienda) {
    final nombre = tienda['tienda_nombre'] ??
        tienda['nombre_comercial'] ??
        tienda['schema_name'] ??
        'Tienda';
    final saldo = tienda['saldo_actual'] as int? ?? 0;
    final historico = tienda['puntos_historicos'] as int? ?? 0;

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.bgCard,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.border),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: saldo > 0 ? AppColors.successBg : AppColors.bgSearch,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(
              Icons.storefront,
              color: saldo > 0 ? AppColors.successText : AppColors.textSlate,
            ),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  nombre.toString(),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                    color: AppColors.primaryDark,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  '${_pointsFormat.format(historico)} pts historicos',
                  style: const TextStyle(
                    color: AppColors.textSlate,
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(width: 12),
          Text(
            '${_pointsFormat.format(saldo)} pts',
            style: TextStyle(
              color: saldo > 0 ? AppColors.successText : AppColors.textSlate,
              fontWeight: FontWeight.w900,
              fontSize: 16,
            ),
          ),
        ],
      ),
    );
  }
}
