import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';
import '../../theme/app_radius.dart';

class AppBrand extends StatelessWidget {
  final String name;
  final IconData icon; 
  final bool darkBackground; 

  const AppBrand({
    super.key,
    required this.name,
    this.icon = Icons.inventory_2, 
    this.darkBackground = false,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 35,
          height: 35,
          decoration: BoxDecoration(
            color: AppColors.accentTeal,
            borderRadius: BorderRadius.circular(AppRadius.xs),
          ),
          child: Center(
            child: Icon(icon, color: AppColors.white, size: 20),
          ),
        ),
        const SizedBox(width: 12),
        Text(
          name,
          style: darkBackground ? AppTextStyles.brandNameTeal : AppTextStyles.brandName,
        ),
      ],
    );
  }
}