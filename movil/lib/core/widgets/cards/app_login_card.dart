import 'package:flutter/material.dart';

import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';
import '../../theme/app_radius.dart';
import '../../theme/app_shadows.dart';

import '../inputs/app_input.dart';
import '../buttons/app_button.dart';
import '../display/app_brand.dart';

class AppLoginCard extends StatelessWidget {
  final String brandName;
  final IconData brandIcon; // ⬅️ Cambiado a IconData
  final String infoTitle;
  final String infoSubtitle;
  final GlobalKey<FormState>? formKey;
  final TextEditingController? emailController;
  final TextEditingController? passwordController;
  final VoidCallback? onSubmit;
  final VoidCallback? onForgot;
  final VoidCallback? onRegister;

  const AppLoginCard({
    super.key,
    required this.brandName,
    this.brandIcon = Icons.inventory_2, 
    required this.infoTitle,
    required this.infoSubtitle,
    this.formKey,
    this.emailController,
    this.passwordController,
    this.onSubmit,
    this.onForgot,
    this.onRegister,
  });

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final bool isDesktop = size.width > 800 && size.height > 600;

    if (isDesktop) {
      return Container(
        constraints: const BoxConstraints(maxWidth: 950, minHeight: 600),
        decoration: BoxDecoration(
          color: AppColors.bgCard,
          borderRadius: BorderRadius.circular(AppRadius.card),
          boxShadow: AppShadows.loginCard,
        ),
        child: Row(
          children: [
            // ── Lado izquierdo: Formulario ──
            Expanded(
              flex: 12,
              child: Padding(
                padding: const EdgeInsets.all(60),
                child: _buildFormContent(context, showBrand: false),
              ),
            ),

            // ── Lado derecho: Info ──
            Expanded(
              flex: 10,
              child: Container(
                decoration: const BoxDecoration(
                  color: AppColors.primaryDark,
                  borderRadius: BorderRadius.only(
                    topRight: Radius.circular(AppRadius.card),
                    bottomRight: Radius.circular(AppRadius.card),
                  ),
                ),
                padding: const EdgeInsets.all(60),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    AppBrand(
                        name: brandName,
                        icon: brandIcon, 
                        darkBackground: true),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(infoTitle,
                            style: AppTextStyles.h1Hero
                                .copyWith(fontSize: 38, color: AppColors.white)),
                        const SizedBox(height: 20),
                        Text(infoSubtitle,
                            style: AppTextStyles.bodyLg
                                .copyWith(color: Colors.white.withOpacity(0.8))),
                      ],
                    ),
                    const SizedBox(), 
                  ],
                ),
              ),
            ),
          ],
        ),
      );
    } else {
      // ── Diseño para Móviles/Vertical ──
      return SingleChildScrollView(
        child: Container(
          width: double.infinity,
          constraints: const BoxConstraints(maxWidth: 500),
          decoration: BoxDecoration(
            color: AppColors.bgCard,
            borderRadius: BorderRadius.circular(AppRadius.card),
            boxShadow: AppShadows.loginCard,
          ),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 40),
            child: _buildFormContent(context, showBrand: true),
          ),
        ),
      );
    }
  }

  Widget _buildFormContent(BuildContext context, {required bool showBrand}) {
    return Form(
      key: formKey,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (showBrand) ...[
            AppBrand(
              name: brandName,
              icon: brandIcon,
              darkBackground: false,
            ),
            const SizedBox(height: 30),
          ],
          Text('Iniciar Sesión', style: AppTextStyles.h1),
          const SizedBox(height: 30),
          AppInput(
            label: 'Correo electrónico',
            labelIcon: Icons.email_outlined,
            hint: 'tucorreo@ejemplo.com',
            controller: emailController,
          ),
          const SizedBox(height: 20),
          AppInput(
            label: 'Contraseña',
            labelIcon: Icons.lock_outline,
            obscureText: true,
            controller: passwordController,
            suffixWidget: onForgot != null
                ? GestureDetector(
                    onTap: onForgot,
                    child: Text('¿Olvidaste tu contraseña?',
                        style: AppTextStyles.link),
                  )
                : null,
          ),
          const SizedBox(height: 30),
          AppButton.submit(
              label: 'Iniciar Sesión', onPressed: onSubmit),
          if (onRegister != null) ...[
            const SizedBox(height: 30),
            Center(
              child: RichText(
                text: TextSpan(
                  style: AppTextStyles.bodySm,
                  children: [
                    const TextSpan(text: '¿No tienes cuenta? '),
                    WidgetSpan(
                      child: GestureDetector(
                        onTap: onRegister,
                        child: Text('Regístrate',
                            style: AppTextStyles.link),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}