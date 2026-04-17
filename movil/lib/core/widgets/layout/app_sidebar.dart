import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';
import '../../theme/app_radius.dart';
import '../display/app_brand.dart';

// 1. La clase que define cada botón del menú
class AppSidebarItem {
  final IconData icon;
  final String label;
  final bool isActive;
  final bool isLogout;
  final VoidCallback? onTap;

  const AppSidebarItem({
    required this.icon,
    required this.label,
    this.isActive = false,
    this.isLogout = false,
    this.onTap,
  });
}

// 2. El contenedor del menú lateral
class AppSidebar extends StatelessWidget {
  final String brandName;
  final IconData brandIcon;
  final List<AppSidebarItem> items;

  const AppSidebar({
    super.key,
    required this.brandName,
    this.brandIcon = Icons.inventory_2, // Usando tu icono vectorial
    required this.items,
  });

  @override
  Widget build(BuildContext context) {
    final navItems = items.where((i) => !i.isLogout).toList();
    final logout = items.where((i) => i.isLogout).firstOrNull;

    return Container(
      width: 260,
      color: AppColors.sidebar,
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 30),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          AppBrand(name: brandName, icon: brandIcon, darkBackground: true),
          const SizedBox(height: 40),
          
          // Renderiza los botones normales
          ...navItems.map((item) => _SidebarNavItem(item: item)),
          
          const Spacer(),
          
          // Renderiza el botón de salir abajo del todo
          if (logout != null) _SidebarNavItem(item: logout),
        ],
      ),
    );
  }
}

// 3. El diseño visual de cada botoncito del menú
class _SidebarNavItem extends StatelessWidget {
  final AppSidebarItem item;

  const _SidebarNavItem({required this.item});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: item.onTap,
      child: Container(
        margin: const EdgeInsets.only(bottom: 4),
        padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 12),
        decoration: BoxDecoration(
          color: item.isActive ? AppColors.bgSidebarItem : Colors.transparent,
          borderRadius: BorderRadius.circular(AppRadius.sm),
        ),
        child: Row(
          children: [
            Icon(
              item.icon,
              size: 20,
              color: item.isLogout
                  ? AppColors.danger
                  : (item.isActive ? AppColors.accentTeal : AppColors.textMuted),
            ),
            const SizedBox(width: 12),
            Text(
              item.label,
              style: item.isLogout
                  ? AppTextStyles.navItem.copyWith(color: AppColors.danger)
                  : (item.isActive ? AppTextStyles.navItemActive : AppTextStyles.navItem),
            ),
          ],
        ),
      ),
    );
  }
}