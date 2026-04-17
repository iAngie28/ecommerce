import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';
import '../../theme/app_radius.dart';
import '../../theme/app_shadows.dart';

class AppStatCard extends StatelessWidget {
  final String label;
  final String value;
  final String? changeText;
  final bool isPositive;

  const AppStatCard({
    super.key,
    required this.label,
    required this.value,
    this.changeText,
    this.isPositive = true,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(25),
      decoration: BoxDecoration(
        color: AppColors.bgCard,
        borderRadius: BorderRadius.circular(AppRadius.lg),
        boxShadow: AppShadows.card,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: AppTextStyles.statLabel),
          const SizedBox(height: 10),
          Text(value, style: AppTextStyles.statValue),
          if (changeText != null) ...[
            const SizedBox(height: 4),
            Text(
              changeText!,
              style: AppTextStyles.statChange.copyWith(
                color: isPositive ? AppColors.success : AppColors.dangerText,
              ),
            ),
          ],
        ],
      ),
    );
  }
}