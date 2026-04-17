import 'package:flutter/material.dart';
import 'app_colors.dart';
import 'app_radius.dart';
import 'app_text_styles.dart';
class AppTheme {
  AppTheme._();

  static ThemeData get themeData => ThemeData(
    useMaterial3: true,
    scaffoldBackgroundColor: AppColors.bgLight,
    colorScheme: ColorScheme.light(
      primary: AppColors.accentTeal,
      secondary: AppColors.primaryDark,
      surface: AppColors.bgCard,
      onPrimary: AppColors.white,
      onSecondary: AppColors.white,
    ),
    textTheme: const TextTheme(
      displayLarge:  AppTextStyles.h1Hero,
      displayMedium: AppTextStyles.h1,
      headlineMedium: AppTextStyles.h2,
      titleLarge:    AppTextStyles.h3,
      bodyLarge:     AppTextStyles.bodyLg,
      bodyMedium:    AppTextStyles.body,
      bodySmall:     AppTextStyles.bodySm,
      labelLarge:    AppTextStyles.label,
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: AppColors.bgCard,
      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.md),
        borderSide: const BorderSide(color: AppColors.borderInput, width: 1.5),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.md),
        borderSide: const BorderSide(color: AppColors.borderInput, width: 1.5),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(AppRadius.md),
        borderSide: const BorderSide(color: AppColors.accentTeal, width: 1.5),
      ),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.accentTeal,
        foregroundColor: AppColors.white,
        shape: const StadiumBorder(),
        padding: const EdgeInsets.symmetric(horizontal: 35, vertical: 16),
        textStyle: const TextStyle(fontWeight: FontWeight.w700, fontSize: 16),
        elevation: 0,
      ),
    ),
    cardTheme: CardThemeData(
      color: AppColors.bgCard,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppRadius.lg),
      ),
      margin: EdgeInsets.zero,
    ),
    dividerColor: AppColors.border,
    dividerTheme: const DividerThemeData(
      color: AppColors.border,
      thickness: 1,
    ),
  );
}