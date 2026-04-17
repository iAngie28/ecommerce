import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';
import '../../theme/app_radius.dart';
import '../buttons/app_button.dart'; 

class AppDialog {
  static Future<bool?> showConfirmation({
    required BuildContext context,
    required String title,
    required String content,
    String confirmText = 'Confirmar',
    String cancelText = 'Cancelar',
    bool isDestructive = false,
  }) {
    return showDialog<bool>(
      context: context,
      builder: (context) {
        return AlertDialog(
          backgroundColor: AppColors.bgCard,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppRadius.lg),
          ),
          title: Text(title, style: AppTextStyles.h3),
          content: Text(content, style: AppTextStyles.body),
          actionsPadding: const EdgeInsets.only(right: 20, bottom: 20),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(false),
              child: Text(
                cancelText,
                style: const TextStyle(color: AppColors.textSlate),
              ),
            ),
            // Reusando tu AppButton. Si es destructivo, idealmente tendrías una variante roja.
            AppButton.primary(
              label: confirmText,
              onPressed: () => Navigator.of(context).pop(true),
            ),
          ],
        );
      },
    );
  }
}