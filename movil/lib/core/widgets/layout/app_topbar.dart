import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';
import '../../theme/app_radius.dart';

// --- SUB-COMPONENTE: Búsqueda ---
class AppSearchBar extends StatelessWidget {
  final String hint;
  final ValueChanged<String>? onChanged;

  const AppSearchBar({super.key, this.hint = 'Buscar...', this.onChanged});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 300,
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      decoration: BoxDecoration(
        color: AppColors.bgSearch,
        borderRadius: BorderRadius.circular(AppRadius.sm),
      ),
      child: Row(
        children: [
          const Icon(Icons.search, size: 18, color: AppColors.textSlate),
          const SizedBox(width: 10),
          Expanded(
            child: TextField(
              onChanged: onChanged,
              decoration: InputDecoration(
                hintText: hint, border: InputBorder.none,
                isDense: true, contentPadding: EdgeInsets.zero,
                fillColor: Colors.transparent, filled: false,
              ),
              style: const TextStyle(fontSize: 14),
            ),
          ),
        ],
      ),
    );
  }
}

// --- SUB-COMPONENTE: Etiqueta de la Tienda ---
class AppTenantBadge extends StatelessWidget {
  final String label;
  final String value;

  const AppTenantBadge({super.key, required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      decoration: BoxDecoration(
        color: AppColors.tealLight,
        border: Border.all(color: AppColors.accentTeal, width: 1.5),
        borderRadius: BorderRadius.circular(AppRadius.pill),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(label, style: AppTextStyles.badgeLabel),
          const SizedBox(width: 4),
          Text(value, style: AppTextStyles.badgeValue),
        ],
      ),
    );
  }
}

// --- TOPBAR PRINCIPAL ---
class AppTopBar extends StatelessWidget implements PreferredSizeWidget {
  final String? tenantLabel;
  final String? tenantValue;
  final String userName;
  final String? userAvatarUrl;
  final ValueChanged<String>? onSearch;

  const AppTopBar({
    super.key,
    this.tenantLabel = 'Tenant',
    this.tenantValue,
    required this.userName,
    this.userAvatarUrl,
    this.onSearch,
  });

  @override
  Size get preferredSize => const Size.fromHeight(70);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 70,
      padding: const EdgeInsets.symmetric(horizontal: 40),
      decoration: const BoxDecoration(
        color: AppColors.bgCard,
        border: Border(bottom: BorderSide(color: AppColors.border)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          AppSearchBar(onChanged: onSearch),
          Row(
            children: [
              if (tenantValue != null) ...[
                AppTenantBadge(label: tenantLabel!, value: tenantValue!),
                const SizedBox(width: 25),
              ],
              Row(
                children: [
                  CircleAvatar(
                    radius: 18,
                    backgroundColor: AppColors.accentTeal,
                    backgroundImage: userAvatarUrl != null ? NetworkImage(userAvatarUrl!) : null,
                    child: userAvatarUrl == null
                        ? Text(userName[0].toUpperCase(), style: const TextStyle(color: AppColors.white, fontWeight: FontWeight.w700))
                        : null,
                  ),
                  const SizedBox(width: 10),
                  Text(userName, style: const TextStyle(fontWeight: FontWeight.w600)),
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }
}