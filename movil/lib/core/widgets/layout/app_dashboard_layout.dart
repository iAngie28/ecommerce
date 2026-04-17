import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import 'app_sidebar.dart';
import 'app_topbar.dart';

class AppDashboardLayout extends StatelessWidget {
  final String brandName;
  final List<AppSidebarItem> sidebarItems;
  final String? tenantLabel;
  final String? tenantValue;
  final String userName;
  final Widget body;

  const AppDashboardLayout({
    super.key,
    required this.brandName,
    required this.sidebarItems,
    this.tenantLabel,
    this.tenantValue,
    required this.userName,
    required this.body,
  });

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final isMobile = size.width < 800;
    // Creamos una GlobalKey para controlar el Scaffold (y abrir el drawer)
    final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();

    return Scaffold(
      key: scaffoldKey,
      backgroundColor: AppColors.bgLight,
      // Drawer lateral solo visible en móvil
      drawer: isMobile 
          ? Drawer(
              child: AppSidebar(
                brandName: brandName,
                items: sidebarItems,
              ),
            )
          : null,
      body: Row(
        children: [
          // Lado Izquierdo: El Menú Fijo (Solo en Desktop)
          if (!isMobile)
            AppSidebar(
              brandName: brandName,
              items: sidebarItems,
            ),
          
          // Lado Derecho: El contenido
          Expanded(
            child: Column(
              children: [
                // Arriba: La Barra (AppBar normal en móvil, custom en Desktop)
                if (isMobile)
                  AppBar(
                    backgroundColor: AppColors.bgCard,
                    iconTheme: const IconThemeData(color: AppColors.primaryDark),
                    elevation: 0,
                    leading: IconButton(
                      icon: const Icon(Icons.menu),
                      onPressed: () => scaffoldKey.currentState?.openDrawer(),
                    ),
                    title: Text(tenantValue ?? 'Tenant', style: const TextStyle(color: AppColors.primaryDark, fontSize: 16)),
                  )
                else
                  AppTopBar(
                    tenantLabel: tenantLabel,
                    tenantValue: tenantValue,
                    userName: userName,
                  ),
                
                // Abajo: El Cuerpo de tu DashboardScreen
                Expanded(
                  child: SingleChildScrollView(
                    padding: EdgeInsets.all(isMobile ? 20 : 40),
                    child: body,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}