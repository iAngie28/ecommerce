import 'package:flutter/material.dart';

import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';
import '../../theme/app_radius.dart';
import '../../theme/app_shadows.dart';

import '../inputs/app_input.dart';
import '../buttons/app_button.dart';
import '../display/app_brand.dart';

class AppForgotPasswordCard extends StatelessWidget {
  final String brandName;
  final IconData brandIcon;
  final String infoTitle;
  final String infoSubtitle;
  final GlobalKey<FormState>? formKey;
  final TextEditingController? emailController;
  final VoidCallback? onSubmit;
  final VoidCallback? onBack;
  final bool isLoading;
  final String? errorMessage;
  final String? successMessage;
  final String? devUrl;

  const AppForgotPasswordCard({
    super.key,
    required this.brandName,
    this.brandIcon = Icons.inventory_2,
    required this.infoTitle,
    required this.infoSubtitle,
    this.formKey,
    this.emailController,
    this.onSubmit,
    this.onBack,
    this.isLoading = false,
    this.errorMessage,
    this.successMessage,
    this.devUrl,
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
          if (onBack != null)
            GestureDetector(
              onTap: onBack,
              child: Row(
                children: [
                  const Icon(Icons.arrow_back, size: 16, color: AppColors.accentTeal),
                  const SizedBox(width: 8),
                  Text('Volver al login',
                      style: AppTextStyles.link.copyWith(fontWeight: FontWeight.w500)),
                ],
              ),
            ),
          if (onBack != null) const SizedBox(height: 20),
          if (showBrand) ...[
            AppBrand(
              name: brandName,
              icon: brandIcon,
              darkBackground: false,
            ),
            const SizedBox(height: 30),
          ],
          if (showBrand) ...[
            Text(infoTitle, style: AppTextStyles.h1.copyWith(fontSize: 26, height: 1.2)),
            const SizedBox(height: 10),
            Text(
              infoSubtitle,
              style: AppTextStyles.body.copyWith(color: Colors.grey.shade600),
            ),
          ] else ...[
            Text('Recuperar Contraseña', style: AppTextStyles.h1),
            const SizedBox(height: 10),
            Text(
              'Ingresa tu correo electrónico y te enviaremos las instrucciones.',
              style: AppTextStyles.body.copyWith(color: Colors.grey.shade600),
            ),
          ],
          const SizedBox(height: 30),
          AppInput(
            label: 'Correo electrónico',
            labelIcon: Icons.email_outlined,
            hint: 'tucorreo@ejemplo.com',
            controller: emailController,
          ),
          const SizedBox(height: 30),
          
          if (successMessage != null) ...[
            Container(
              padding: const EdgeInsets.all(15),
              decoration: BoxDecoration(
                color: const Color(0xFFE3FCF7),
                border: Border.all(color: const Color(0xFFC2F5EA)),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                successMessage!,
                style: const TextStyle(color: Color(0xFF0D6E5E), fontSize: 14),
              ),
            ),
            const SizedBox(height: 20),
          ],

          if (devUrl != null && devUrl!.isNotEmpty) ...[
            Container(
               padding: const EdgeInsets.all(15),
               decoration: BoxDecoration(
                 color: const Color(0xFFFFF3CD),
                 border: const Border(left: BorderSide(color: Color(0xFFFFC107), width: 4)),
               ),
               child: Column(
                 crossAxisAlignment: CrossAxisAlignment.start,
                 children: [
                   const Text(
                     'Modo Desarrollo - Email no configurado.',
                     style: TextStyle(color: Color(0xFF856404), fontWeight: FontWeight.bold, fontSize: 14),
                   ),
                   const SizedBox(height: 8),
                   SelectableText(
                     devUrl!,
                     style: const TextStyle(color: Color(0xFF0D6EFD), fontSize: 14),
                   )
                 ],
               ),
            ),
            const SizedBox(height: 20),
          ],

          if (errorMessage != null) ...[
            Container(
              padding: const EdgeInsets.all(15),
              decoration: BoxDecoration(
                color: const Color(0xFFFFF0F0),
                border: Border.all(color: const Color(0xFFFFDADA)),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                errorMessage!,
                style: const TextStyle(color: Color(0xFFC0392B), fontSize: 14),
              ),
            ),
            const SizedBox(height: 20),
          ],
          
          AppButton.submit(
            label: isLoading ? 'Enviando...' : 'Enviar Enlace',
            onPressed: isLoading ? null : onSubmit,
          ),
        ],
      ),
    );
  }
}
