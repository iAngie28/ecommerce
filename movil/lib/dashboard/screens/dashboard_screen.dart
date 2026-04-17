import 'dart:convert';
import 'package:flutter/material.dart';

// 1. UI Kit (Estilos y Componentes)
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_text_styles.dart';
import '../../core/widgets/layout/app_dashboard_layout.dart';
import '../../core/widgets/layout/app_sidebar.dart';
import '../../core/widgets/buttons/app_button.dart';
import '../../core/widgets/cards/app_stat_card.dart';
import '../../core/widgets/display/app_status_pill.dart';
import '../../core/widgets/cards/app_table_card.dart';

// 2. Lógica de negocio
import '../models/product_model.dart';
import '../repositories/product_repository.dart';
import '../../gestion_usuario/repositories/auth_repository.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  // ── ESTADOS ──
  List<ProductModel> _products = [];
  bool _isLoading = true;
  String? _error;

  // Tenant dinámico (se carga del storage)
  String _tenant = '';
  String _schemaName = '';
  String _storeName = 'Cargando...';
  String _userName = 'Admin';

  final ProductRepository _productRepository = ProductRepository();
  final AuthRepository _authRepository = AuthRepository();

  // ── CARGA INICIAL ──
  @override
  void initState() {
    super.initState();
    _inicializar();
  }

  Future<void> _inicializar() async {
    // Cargar info del tenant desde el storage
    final subdomain = await _authRepository.getSubdomain();
    final schemaName = await _authRepository.getSchemaName();

    String decodedUser = 'Admin';
    final token = await _authRepository.getAccessToken();
    if (token != null) {
      final payload = _decodeJwt(token);
      if (payload != null) {
        decodedUser = payload['full_name'] ?? payload['username'] ?? 'Admin';
      }
    }

    setState(() {
      _tenant = subdomain ?? 'sin-tenant';
      _schemaName = schemaName ?? '';
      _storeName = _formatStoreName(_schemaName);
      _userName = decodedUser;
    });

    // Cargar productos del API real
    await _cargarProductos();
  }

  String _formatStoreName(String schema) {
    if (schema.isEmpty) return 'Mi Tienda';
    return schema.split(RegExp(r'[x_]+')).map((word) {
      if (word.isEmpty) return '';
      return word[0].toUpperCase() + word.substring(1).toLowerCase();
    }).join(' ');
  }

  Map<String, dynamic>? _decodeJwt(String token) {
    try {
      final parts = token.split('.');
      if (parts.length != 3) return null;
      var payload = parts[1];
      while (payload.length % 4 != 0) {
        payload += '=';
      }
      return jsonDecode(utf8.decode(base64Url.decode(payload)));
    } catch (_) {
      return null;
    }
  }

  Future<void> _cargarProductos() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final productos = await _productRepository.fetchProducts();
      setState(() {
        _products = productos;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString().replaceAll('Exception: ', '');
        _isLoading = false;
      });

      // Si la sesión expiró, redirigir al login
      if (e.toString().contains('Sesión expirada')) {
        if (!mounted) return;
        Navigator.pushReplacementNamed(context, '/login');
      }
    }
  }

  // ── CÁLCULOS DINÁMICOS ──
  double get _valorTotal {
    return _products.fold(0, (acc, curr) => acc + (curr.precio * curr.stock));
  }

  int get _stockCritico {
    return _products.where((p) => p.stock < 10).length;
  }

  @override
  Widget build(BuildContext context) {
    return AppDashboardLayout(
      brandName: 'MiQhatu',
      tenantLabel: 'Tienda Activa:',
      tenantValue: _storeName,
      userName: _userName,
      sidebarItems: [
        AppSidebarItem(icon: Icons.dashboard, label: 'Panel', isActive: true),
        AppSidebarItem(icon: Icons.inventory_2, label: 'Productos'),
        AppSidebarItem(icon: Icons.shopping_cart, label: 'Ventas'),
        AppSidebarItem(icon: Icons.people, label: 'Clientes'),
        AppSidebarItem(icon: Icons.settings, label: 'Configuración'),
        AppSidebarItem(
          icon: Icons.logout,
          label: 'Salir',
          isLogout: true,
          onTap: () async {
            // Llamar al endpoint /api/logout/ para invalidar el refresh
            await _authRepository.logout();

            if (!context.mounted) return;
            Navigator.pushReplacementNamed(context, '/login');
          },
        ),
      ],
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // ── HEADER ──
          LayoutBuilder(builder: (context, constraints) {
            final isMobile = constraints.maxWidth < 600;
            return Flex(
              direction: isMobile ? Axis.vertical : Axis.horizontal,
              crossAxisAlignment: isMobile ? CrossAxisAlignment.start : CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Bienvenido a $_storeName', style: AppTextStyles.h1),
                    const SizedBox(height: 5),
                    Text(
                      'Resumen en tiempo real de tu tienda',
                      style: AppTextStyles.subtitle,
                    ),
                  ],
                ),
                if (isMobile) const SizedBox(height: 15),
                AppButton.add(
                  label: 'Nuevo Producto',
                  icon: Icons.add,
                  onPressed: () {
                    // TODO: Abrir modal de crear producto
                  },
                ),
              ],
            );
          }),
          const SizedBox(height: 30),

          // ── STATS CARDS ──
          LayoutBuilder(
            builder: (context, constraints) {
              final isMobile = constraints.maxWidth < 700;
              
              if (isMobile) {
                return Column(
                  children: [
                    AppStatCard(
                      label: 'Valor del Inventario',
                      value: 'BS. ${_valorTotal.toStringAsFixed(2)}',
                      changeText: 'Calculado en tiempo real',
                      isPositive: true,
                    ),
                    const SizedBox(height: 15),
                    AppStatCard(
                      label: 'Productos Activos',
                      value: '${_products.length}',
                      changeText: 'Sincronizado con API',
                      isPositive: true,
                    ),
                    const SizedBox(height: 15),
                    AppStatCard(
                      label: 'Stock Crítico',
                      value: '$_stockCritico',
                      changeText: _stockCritico > 0
                          ? 'Requieren atención'
                          : 'Todo en orden',
                      isPositive: _stockCritico == 0,
                    ),
                  ],
                );
              }
              
              return Row(
                children: [
                  Expanded(
                    child: AppStatCard(
                      label: 'Valor del Inventario',
                      value: 'BS. ${_valorTotal.toStringAsFixed(2)}',
                      changeText: 'Calculado en tiempo real',
                      isPositive: true,
                    ),
                  ),
                  const SizedBox(width: 25),
                  Expanded(
                    child: AppStatCard(
                      label: 'Productos Activos',
                      value: '${_products.length}',
                      changeText: 'Sincronizado con API',
                      isPositive: true,
                    ),
                  ),
                  const SizedBox(width: 25),
                  Expanded(
                    child: AppStatCard(
                      label: 'Stock Crítico',
                      value: '$_stockCritico',
                      changeText: _stockCritico > 0
                          ? 'Requieren atención'
                          : 'Todo en orden',
                      isPositive: _stockCritico == 0,
                    ),
                  ),
                ],
              );
            }
          ),
          const SizedBox(height: 40),

          // ── TABLA DE PRODUCTOS ──
          if (_isLoading)
            const Center(
                child: CircularProgressIndicator(color: AppColors.accentTeal))
          else if (_error != null)
            Center(
              child: Column(
                children: [
                  const Icon(Icons.error_outline,
                      size: 40, color: AppColors.danger),
                  const SizedBox(height: 10),
                  Text(_error!,
                      style: const TextStyle(color: AppColors.danger)),
                  const SizedBox(height: 20),
                  AppButton.add(
                    label: 'Reintentar',
                    icon: Icons.refresh,
                    onPressed: _cargarProductos,
                  ),
                ],
              ),
            )
          else if (_products.isEmpty)
            const Center(
                child: Text('No hay productos registrados para este tenant.'))
          else
            AppTableCard(
              title: 'Inventario de la Base de Datos',
              columns: const [
                'Producto',
                'Descripción',
                'Precio',
                'Stock',
                'Estado'
              ],
              rows: _products.map((prod) {
                return [
                  Text(prod.nombre,
                      style: const TextStyle(fontWeight: FontWeight.bold)),
                  Text(
                    prod.descripcion.isEmpty
                        ? 'Sin descripción'
                        : prod.descripcion,
                    style: const TextStyle(
                        fontSize: 12, color: AppColors.textGray),
                  ),
                  Text('BS. ${prod.precio.toStringAsFixed(2)}'),
                  Text('${prod.stock} un.'),
                  prod.stock < 10
                      ? const AppStatusPill.low(label: 'Bajo Stock')
                      : const AppStatusPill.ok(label: 'Disponible'),
                ];
              }).toList(),
            ),
        ],
      ),
    );
  }
}