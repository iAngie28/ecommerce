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
  final Widget? topBarTrailing;

  const AppDashboardLayout({
    super.key,
    required this.brandName,
    required this.sidebarItems,
    this.tenantLabel,
    this.tenantValue,
    required this.userName,
    required this.body,
    this.topBarTrailing,
  });

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final isMobile = size.width < 800;
    final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();

    return Scaffold(
      key: scaffoldKey,
      backgroundColor: AppColors.bgLight,
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
          if (!isMobile)
            AppSidebar(
              brandName: brandName,
              items: sidebarItems,
            ),
          
          Expanded(
            child: Column(
              children: [
                if (isMobile)
                  AppBar(
                    backgroundColor: AppColors.bgCard,
                    iconTheme: const IconThemeData(color: AppColors.primaryDark),
                    elevation: 0,
                    leading: IconButton(
                      icon: const Icon(Icons.menu),
                      onPressed: () => scaffoldKey.currentState?.openDrawer(),
                    ),
                    title: Text(tenantValue ?? 'Tienda', style: const TextStyle(color: AppColors.primaryDark, fontSize: 16)),
                    actions: [
                      if (topBarTrailing != null) topBarTrailing!,
                    ],
                  )
                else
                  AppTopBar(
                    tenantLabel: tenantLabel,
                    tenantValue: tenantValue,
                    userName: userName,
                    trailing: topBarTrailing,
                  ),
                
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
