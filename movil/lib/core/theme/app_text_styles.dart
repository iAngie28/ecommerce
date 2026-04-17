import 'package:flutter/material.dart';
import 'app_colors.dart';

class AppTextStyles {
  AppTextStyles._();

  static const TextStyle h1 = TextStyle(
    fontSize: 32,
    fontWeight: FontWeight.w800,
    color: AppColors.primaryDark,
    height: 1.2,
  );

  static const TextStyle h1Hero = TextStyle(
    fontSize: 50,
    fontWeight: FontWeight.w800,
    color: AppColors.white,
    height: 1.2,
  );

  static const TextStyle h2 = TextStyle(
    fontSize: 35,
    fontWeight: FontWeight.w700,
    color: AppColors.primaryDark,
  );

  static const TextStyle h3 = TextStyle(
    fontSize: 19,
    fontWeight: FontWeight.w700,
    color: AppColors.primaryDark,
  );

  // Logo / Brand
  static const TextStyle brandName = TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.w800,
    color: AppColors.primaryDark,
  );

  static const TextStyle brandNameTeal = TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.w700,
    color: AppColors.accentTeal,
  );

  // Body
  static const TextStyle bodyLg = TextStyle(
    fontSize: 18,
    color: AppColors.white,
    height: 1.6,
  );

  static const TextStyle body = TextStyle(
    fontSize: 15,
    color: AppColors.textGray,
    height: 1.6,
  );

  static const TextStyle bodySm = TextStyle(
    fontSize: 14,
    color: AppColors.textGray,
  );

  // Labels
  static const TextStyle label = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.w600,
    color: AppColors.primaryDark,
  );

  static const TextStyle labelLight = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.w300,
    color: AppColors.primaryDark,
  );

  // Stats
  static const TextStyle statValue = TextStyle(
    fontSize: 29,
    fontWeight: FontWeight.w700,
    color: AppColors.primaryDark,
  );

  static const TextStyle statLabel = TextStyle(
    fontSize: 14,
    color: AppColors.textSlate,
  );

  static const TextStyle statChange = TextStyle(
    fontSize: 14,
    color: AppColors.success,
  );

  // Nav
  static const TextStyle navItem = TextStyle(
    fontSize: 15,
    color: AppColors.textMuted,
    fontWeight: FontWeight.w500,
  );

  static const TextStyle navItemActive = TextStyle(
    fontSize: 15,
    color: AppColors.accentTeal,
    fontWeight: FontWeight.w600,
  );

  // Badge
  static const TextStyle badgeLabel = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.w500,
    color: Color(0xFF606060),
  );

  static const TextStyle badgeValue = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.w700,
    color: AppColors.accentTeal,
  );

  // Link
  static const TextStyle link = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.w500,
    color: AppColors.accentTeal,
  );

  // Pill status
  static const TextStyle pillOk = TextStyle(
    fontSize: 13,
    fontWeight: FontWeight.w600,
    color: AppColors.successText,
  );

  static const TextStyle pillLow = TextStyle(
    fontSize: 13,
    fontWeight: FontWeight.w600,
    color: AppColors.dangerText,
  );

  // Precio
  static const TextStyle priceAmount = TextStyle(
    fontSize: 32,
    fontWeight: FontWeight.w700,
    color: AppColors.accentTeal,
  );

  // Subtitle hero
  static const TextStyle subtitle = TextStyle(
    fontSize: 15,
    color: AppColors.textGray,
  );
  // ... pega el resto de tus textos aquí
}