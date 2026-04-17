import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_radius.dart';
import '../../theme/app_shadows.dart';

enum _AppButtonVariant { primary, secondary, add, submit, navRegister }

class AppButton extends StatelessWidget {
  final String label;
  final IconData? icon;
  final VoidCallback? onPressed;
  final _AppButtonVariant _variant;

  const AppButton.primary({
    super.key,
    required this.label,
    this.icon,
    this.onPressed,
  }) : _variant = _AppButtonVariant.primary;

  const AppButton.secondary({
    super.key,
    required this.label,
    this.icon,
    this.onPressed,
  }) : _variant = _AppButtonVariant.secondary;

  const AppButton.add({
    super.key,
    required this.label,
    this.icon,
    this.onPressed,
  }) : _variant = _AppButtonVariant.add;

  const AppButton.submit({
    super.key,
    required this.label,
    this.onPressed,
  })  : _variant = _AppButtonVariant.submit,
        icon = null;

  const AppButton.navRegister({
    super.key,
    required this.label,
    this.onPressed,
  })  : _variant = _AppButtonVariant.navRegister,
        icon = null;

  @override
  Widget build(BuildContext context) {
    switch (_variant) {
      // ── Teal pill  (hero / features) ──
      case _AppButtonVariant.primary:
        return _PillButton(
          label: label,
          icon: icon,
          onPressed: onPressed,
          bg: AppColors.accentTeal,
          fg: AppColors.white,
          shadows: AppShadows.tealBtn,
        );

      // ── Borde blanco pill (hero secondary) ──
      case _AppButtonVariant.secondary:
        return OutlinedButton.icon(
          onPressed: onPressed,
          icon: icon != null ? Icon(icon, size: 18) : const SizedBox.shrink(),
          label: Text(label),
          style: OutlinedButton.styleFrom(
            foregroundColor: AppColors.white,
            side: const BorderSide(color: AppColors.white, width: 2),
            shape: const StadiumBorder(),
            padding: const EdgeInsets.symmetric(horizontal: 35, vertical: 16),
            textStyle: const TextStyle(fontWeight: FontWeight.w700, fontSize: 16),
          ),
        );

      // ── Teal rectangulado (dashboard + icon) ──
      case _AppButtonVariant.add:
        return ElevatedButton.icon(
          onPressed: onPressed,
          icon: Icon(icon ?? Icons.add, size: 18),
          label: Text(label),
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.accentTeal,
            foregroundColor: AppColors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(AppRadius.sm),
            ),
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
            textStyle: const TextStyle(fontWeight: FontWeight.w600, fontSize: 15),
            elevation: 0,
          ),
        );

      // ── Dark full-width (login submit) ──
      case _AppButtonVariant.submit:
        return SizedBox(
          width: double.infinity,
          child: ElevatedButton(
            onPressed: onPressed,
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primaryDark,
              foregroundColor: AppColors.white,
              shape: const StadiumBorder(),
              padding: const EdgeInsets.symmetric(vertical: 18),
              textStyle: const TextStyle(fontWeight: FontWeight.w700, fontSize: 18),
              elevation: 0,
            ),
            child: Text(label),
          ),
        );

      // ── Teal pill navbar (registrarse) ──
      case _AppButtonVariant.navRegister:
        return _PillButton(
          label: label,
          onPressed: onPressed,
          bg: AppColors.accentTeal,
          fg: AppColors.white,
          shadows: AppShadows.tealBtn,
          padding: const EdgeInsets.symmetric(horizontal: 25, vertical: 12),
        );
    }
  }
}

// Clase privada solo usada por este archivo
class _PillButton extends StatelessWidget {
  final String label;
  final IconData? icon;
  final VoidCallback? onPressed;
  final Color bg;
  final Color fg;
  final List<BoxShadow> shadows;
  final EdgeInsets padding;

  const _PillButton({
    required this.label,
    required this.bg,
    required this.fg,
    required this.shadows,
    this.icon,
    this.onPressed,
    this.padding = const EdgeInsets.symmetric(horizontal: 35, vertical: 16),
  });

  @override
  Widget build(BuildContext context) {
    return DecoratedBox(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(AppRadius.pill),
        boxShadow: shadows,
      ),
      child: ElevatedButton(
        onPressed: onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: bg,
          foregroundColor: fg,
          shape: const StadiumBorder(),
          padding: padding,
          textStyle: const TextStyle(fontWeight: FontWeight.w700, fontSize: 16),
          elevation: 0,
        ),
        child: icon != null
            ? Row(mainAxisSize: MainAxisSize.min, children: [
                Icon(icon, size: 18),
                const SizedBox(width: 8),
                Text(label),
              ])
            : Text(label),
      ),
    );
  }
}