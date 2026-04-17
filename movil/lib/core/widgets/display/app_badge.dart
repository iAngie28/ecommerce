import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_radius.dart';

enum AppBadgeVariant { success, danger, warning, info }

class AppBadge extends StatelessWidget {
  final String text;
  final AppBadgeVariant variant;

  const AppBadge({
    super.key,
    required this.text,
    this.variant = AppBadgeVariant.info,
  });

  @override
  Widget build(BuildContext context) {
    Color bgColor;
    Color textColor;

    switch (variant) {
      case AppBadgeVariant.success:
        bgColor = AppColors.successBg;
        textColor = AppColors.successText;
        break;
      case AppBadgeVariant.danger:
        bgColor = AppColors.dangerBg;
        textColor = AppColors.dangerText;
        break;
      case AppBadgeVariant.warning:
        bgColor = const Color(0xFFFEF3C7); // Amber claro
        textColor = const Color(0xFFB45309); // Amber oscuro
        break;
      case AppBadgeVariant.info:
      default:
        bgColor = AppColors.bgSearch;
        textColor = AppColors.textSlate;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(AppRadius.pill),
      ),
      child: Text(
        text.toUpperCase(),
        style: TextStyle(
          fontSize: 11,
          fontWeight: FontWeight.w700,
          color: textColor,
          letterSpacing: 0.5,
        ),
      ),
    );
  }
}