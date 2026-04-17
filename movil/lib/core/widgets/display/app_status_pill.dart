import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';
import '../../theme/app_radius.dart';

class AppStatusPill extends StatelessWidget {
  final String label;
  final bool isOk;

  const AppStatusPill.ok({super.key, required this.label}) : isOk = true;
  const AppStatusPill.low({super.key, required this.label}) : isOk = false;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: isOk ? AppColors.successBg : AppColors.dangerBg,
        borderRadius: BorderRadius.circular(AppRadius.pill),
      ),
      child: Text(
        label,
        style: isOk ? AppTextStyles.pillOk : AppTextStyles.pillLow,
      ),
    );
  }
}