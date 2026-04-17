import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';

class AppDropdown<T> extends StatelessWidget {
  final String label;
  final T? value;
  final List<T> items;
  final String Function(T) itemLabelBuilder;
  final void Function(T?)? onChanged;
  final String? Function(T?)? validator;

  const AppDropdown({
    super.key,
    required this.label,
    required this.value,
    required this.items,
    required this.itemLabelBuilder,
    this.onChanged,
    this.validator,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: AppTextStyles.label),
        const SizedBox(height: 8),
        DropdownButtonFormField<T>(
          value: value,
          icon: const Icon(Icons.keyboard_arrow_down, color: AppColors.textSlate),
          decoration: const InputDecoration(
            // El diseño se hereda automáticamente de tu AppTheme (InputDecorationTheme)
            contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          ),
          items: items.map((T item) {
            return DropdownMenuItem<T>(
              value: item,
              child: Text(
                itemLabelBuilder(item),
                style: const TextStyle(fontSize: 14, color: AppColors.textPrimary),
              ),
            );
          }).toList(),
          onChanged: onChanged,
          validator: validator,
        ),
      ],
    );
  }
}