import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_radius.dart';
import '../../theme/app_shadows.dart';

enum _AppButtonVariant { primary, secondary, add, submit, navRegister }

class AppButton extends StatelessWidget {
  final String label;
  final IconData? icon;
  final VoidCallback? onPressed;
  final Color? color;
  final bool isLoading;
  final bool fullWidth;
  final _AppButtonVariant _variant;

  const AppButton.primary({
    super.key,
    required this.label,
    this.icon,
    this.onPressed,
    this.isLoading = false,
    this.fullWidth = false,
  }) : _variant = _AppButtonVariant.primary,
       color = null;

  const AppButton.secondary({
    super.key,
    required this.label,
    this.icon,
    this.onPressed,
    this.isLoading = false,
    this.fullWidth = false,
  }) : _variant = _AppButtonVariant.secondary,
       color = null;

  const AppButton.add({
    super.key,
    required this.label,
    this.icon,
    this.onPressed,
    this.color,
    this.isLoading = false,
    this.fullWidth = false,
  }) : _variant = _AppButtonVariant.add;

  const AppButton.submit({
    super.key,
    required this.label,
    this.onPressed,
    this.isLoading = false,
    this.fullWidth = true,
  }) : _variant = _AppButtonVariant.submit,
       icon = null,
       color = null;

  const AppButton.navRegister({
    super.key,
    required this.label,
    this.onPressed,
    this.isLoading = false,
    this.fullWidth = false,
  }) : _variant = _AppButtonVariant.navRegister,
       icon = null,
       color = null;

  @override
  Widget build(BuildContext context) {
    Widget button;
    switch (_variant) {
      case _AppButtonVariant.primary:
        button = _PillButton(
          label: label,
          icon: icon,
          onPressed: isLoading ? null : onPressed,
          bg: AppColors.accentTeal,
          fg: AppColors.white,
          shadows: AppShadows.tealBtn,
          isLoading: isLoading,
        );
        break;

      case _AppButtonVariant.secondary:
        button = OutlinedButton.icon(
          onPressed: isLoading ? null : onPressed,
          icon: isLoading
              ? const SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    color: AppColors.white,
                  ),
                )
              : (icon != null ? Icon(icon, size: 18) : const SizedBox.shrink()),
          label: Text(label),
          style: OutlinedButton.styleFrom(
            foregroundColor: AppColors.white,
            side: const BorderSide(color: AppColors.white, width: 2),
            shape: const StadiumBorder(),
            padding: const EdgeInsets.symmetric(horizontal: 35, vertical: 16),
            textStyle: const TextStyle(
              fontWeight: FontWeight.w700,
              fontSize: 16,
            ),
          ),
        );
        break;

      case _AppButtonVariant.add:
        button = ElevatedButton.icon(
          onPressed: isLoading ? null : onPressed,
          icon: isLoading
              ? const SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    color: AppColors.white,
                  ),
                )
              : Icon(icon ?? Icons.add, size: 18),
          label: Text(label),
          style: ElevatedButton.styleFrom(
            backgroundColor: color ?? AppColors.accentTeal,
            foregroundColor: AppColors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(AppRadius.sm),
            ),
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
            textStyle: const TextStyle(
              fontWeight: FontWeight.w600,
              fontSize: 15,
            ),
            elevation: 0,
          ),
        );
        break;

      case _AppButtonVariant.submit:
        button = ElevatedButton(
          onPressed: isLoading ? null : onPressed,
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.primaryDark,
            foregroundColor: AppColors.white,
            shape: const StadiumBorder(),
            padding: const EdgeInsets.symmetric(vertical: 18),
            textStyle: const TextStyle(
              fontWeight: FontWeight.w700,
              fontSize: 18,
            ),
            elevation: 0,
          ),
          child: isLoading
              ? const SizedBox(
                  width: 24,
                  height: 24,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    color: AppColors.white,
                  ),
                )
              : Text(label),
        );
        break;

      case _AppButtonVariant.navRegister:
        button = _PillButton(
          label: label,
          onPressed: isLoading ? null : onPressed,
          bg: AppColors.accentTeal,
          fg: AppColors.white,
          shadows: AppShadows.tealBtn,
          padding: const EdgeInsets.symmetric(horizontal: 25, vertical: 12),
          isLoading: isLoading,
        );
        break;
    }

    if (fullWidth) {
      return SizedBox(width: double.infinity, child: button);
    }
    return button;
  }
}

class _PillButton extends StatelessWidget {
  final String label;
  final IconData? icon;
  final VoidCallback? onPressed;
  final Color bg;
  final Color fg;
  final List<BoxShadow> shadows;
  final EdgeInsets padding;
  final bool isLoading;

  const _PillButton({
    required this.label,
    required this.bg,
    required this.fg,
    required this.shadows,
    this.icon,
    this.onPressed,
    this.padding = const EdgeInsets.symmetric(horizontal: 35, vertical: 16),
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    return DecoratedBox(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(AppRadius.pill),
        boxShadow: shadows,
      ),
      child: ElevatedButton(
        onPressed: isLoading ? null : onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: bg,
          foregroundColor: fg,
          shape: const StadiumBorder(),
          padding: padding,
          textStyle: const TextStyle(fontWeight: FontWeight.w700, fontSize: 16),
          elevation: 0,
        ),
        child: isLoading
            ? const SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  color: AppColors.white,
                ),
              )
            : (icon != null
                  ? Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(icon, size: 18),
                        const SizedBox(width: 8),
                        Text(label),
                      ],
                    )
                  : Text(label)),
      ),
    );
  }
}
