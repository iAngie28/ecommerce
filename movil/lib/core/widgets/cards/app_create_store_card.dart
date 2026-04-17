import 'package:flutter/material.dart';

import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';
import '../../theme/app_radius.dart';
import '../../theme/app_shadows.dart';

import '../inputs/app_input.dart';
import '../buttons/app_button.dart';

class AppCreateStoreCard extends StatelessWidget {
  final GlobalKey<FormState>? formKey;
  final TextEditingController storeNameController;
  final TextEditingController slugController;
  final TextEditingController domainController;
  final TextEditingController firstNameController;
  final TextEditingController lastNameController;
  final TextEditingController emailController;
  final TextEditingController passwordController;
  
  final VoidCallback? onSubmit;
  final bool isLoading;
  final String? errorMessage;
  
  final bool isSuccess;
  final String? successDomain;
  final String? successEmail;
  final VoidCallback? onGoToStore;

  const AppCreateStoreCard({
    super.key,
    this.formKey,
    required this.storeNameController,
    required this.slugController,
    required this.domainController,
    required this.firstNameController,
    required this.lastNameController,
    required this.emailController,
    required this.passwordController,
    this.onSubmit,
    this.isLoading = false,
    this.errorMessage,
    this.isSuccess = false,
    this.successDomain,
    this.successEmail,
    this.onGoToStore,
  });

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final bool isDesktop = size.width > 800 && size.height > 600;

    if (isDesktop) {
      return Container(
        constraints: const BoxConstraints(maxWidth: 1000, minHeight: 700),
        decoration: BoxDecoration(
          color: AppColors.white,
          borderRadius: BorderRadius.circular(30),
          boxShadow: AppShadows.loginCard,
        ),
        child: isSuccess ? _buildSuccessView(context) : Row(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Lado izquierdo: Formulario
            Expanded(
              flex: 14,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 60, vertical: 40),
                child: SingleChildScrollView(
                  child: _buildFormContent(context),
                ),
              ),
            ),

            // Lado derecho: Info
            Expanded(
              flex: 10,
              child: Container(
                decoration: const BoxDecoration(
                  color: AppColors.primaryDark,
                  borderRadius: BorderRadius.only(
                    topRight: Radius.circular(30),
                    bottomRight: Radius.circular(30),
                  ),
                ),
                padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 60),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildBenefitItem(
                      icon: Icons.auto_awesome,
                      title: 'Inteligencia Artificial',
                      description: 'Predice tus ventas y optimiza tu inventario automáticamente.',
                    ),
                    const SizedBox(height: 30),
                    _buildBenefitItem(
                      icon: Icons.shield_outlined,
                      title: 'Seguridad Total',
                      description: 'Tus datos y los de tus clientes están protegidos con encriptación.',
                    ),
                    const SizedBox(height: 30),
                    _buildBenefitItem(
                      icon: Icons.language,
                      title: 'Subdominio Propio',
                      description: 'Obtén una URL personalizada y profesional para tu negocio al instante.',
                    ),
                    const Spacer(),
                    Text(
                      'Al registrarte aceptas nuestros Términos y Condiciones y Política de Privacidad.',
                      style: AppTextStyles.bodySm.copyWith(color: Colors.white60),
                    )
                  ],
                ),
              ),
            ),
          ],
        ),
      );
    } else {
      // Móvil
      return SingleChildScrollView(
        child: Container(
          width: double.infinity,
          constraints: const BoxConstraints(maxWidth: 500),
          decoration: BoxDecoration(
            color: AppColors.white,
            borderRadius: BorderRadius.circular(30),
            boxShadow: AppShadows.loginCard,
          ),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 40),
            child: isSuccess ? _buildSuccessView(context) : _buildFormContent(context),
          ),
        ),
      );
    }
  }

  Widget _buildBenefitItem({required IconData icon, required String title, required String description}) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: 45,
          height: 45,
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.1),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Icon(icon, color: AppColors.accentTeal, size: 20),
        ),
        const SizedBox(width: 15),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: AppTextStyles.h2.copyWith(color: AppColors.accentTeal, fontSize: 18)),
              const SizedBox(height: 5),
              Text(description, style: AppTextStyles.body.copyWith(color: Colors.white.withOpacity(0.8))),
            ],
          ),
        )
      ],
    );
  }

  Widget _buildSectionTitle(IconData icon, String title) {
    return Column(
      children: [
        const SizedBox(height: 20),
        Row(
          children: [
            Icon(icon, size: 18, color: AppColors.primaryDark),
            const SizedBox(width: 10),
            Text(title, style: AppTextStyles.h2.copyWith(fontSize: 18, color: AppColors.primaryDark)),
          ],
        ),
        const SizedBox(height: 10),
        const Divider(color: Color(0xFFEEEEEE), thickness: 1),
        const SizedBox(height: 15),
      ],
    );
  }

  Widget _buildFormContent(BuildContext context) {
    return Form(
      key: formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Crea tu Negocio', style: AppTextStyles.h1Hero.copyWith(color: AppColors.primaryDark, fontSize: 32)),
          const SizedBox(height: 10),
          Text('Únete a cientos de emprendedores que ya usan MiQhatu.', style: AppTextStyles.body.copyWith(color: Colors.grey.shade600)),
          
          _buildSectionTitle(Icons.storefront, 'Datos de la Tienda'),
          AppInput(
            label: 'Nombre de la Tienda',
            labelIcon: Icons.apartment,
            hint: 'Ej: Mi Boutique Online',
            controller: storeNameController,
          ),
          const SizedBox(height: 20),
          Row(
            children: [
              Expanded(
                child: AppInput(
                  label: 'Identificador (Slug)',
                  labelIcon: Icons.bolt,
                  hint: 'mi_boutique_online',
                  controller: slugController,
                  readOnly: true,
                ),
              ),
              const SizedBox(width: 20),
              Expanded(
                child: AppInput(
                  label: 'Dominio',
                  labelIcon: Icons.language,
                  hint: 'mi_boutique.localhost',
                  controller: domainController,
                  readOnly: true,
                ),
              ),
            ],
          ),

          _buildSectionTitle(Icons.person_outline, 'Datos del Dueño'),
          Row(
            children: [
              Expanded(
                child: AppInput(
                  label: 'Nombre',
                  hint: 'Tu nombre',
                  controller: firstNameController,
                ),
              ),
              const SizedBox(width: 20),
              Expanded(
                child: AppInput(
                  label: 'Apellido',
                  hint: 'Tu apellido',
                  controller: lastNameController,
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          AppInput(
            label: 'Correo Electrónico',
            labelIcon: Icons.email_outlined,
            hint: 'ejemplo@correo.com',
            controller: emailController,
          ),
          const SizedBox(height: 20),
          AppInput(
            label: 'Contraseña',
            labelIcon: Icons.lock_outline,
            hint: 'Mínimo 6 caracteres',
            obscureText: true,
            controller: passwordController,
          ),

          if (errorMessage != null) ...[
            const SizedBox(height: 20),
            Container(
              padding: const EdgeInsets.all(15),
              decoration: BoxDecoration(
                color: const Color(0xFFFFF0F0),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Row(
                children: [
                  const Text('Error: ', style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFFC0392B))),
                  Expanded(child: Text(errorMessage!, style: const TextStyle(color: Color(0xFFC0392B)))),
                ],
              ),
            ),
          ],

          const SizedBox(height: 30),
          AppButton.submit(
            label: isLoading ? 'Configurando tu tienda...' : 'Crear Mi Tienda Ahora',
            onPressed: isLoading ? null : onSubmit,
          ),
        ],
      ),
    );
  }

  Widget _buildSuccessView(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(40),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 80,
              height: 80,
              decoration: const BoxDecoration(
                color: Color(0xFF2ECC71),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.check_circle_outline, color: Colors.white, size: 48),
            ),
            const SizedBox(height: 30),
            Text('¡Tu tienda está lista!', style: AppTextStyles.h1.copyWith(fontSize: 28)),
            const SizedBox(height: 10),
            Text('Hemos configurado todo para que empieces a vender hoy mismo.', 
                 style: AppTextStyles.body.copyWith(color: Colors.grey.shade600)),
            
            const SizedBox(height: 30),
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: const Color(0xFFF0FDF4),
                border: Border.all(color: const Color(0xFF2ECC71), style: BorderStyle.solid),
                borderRadius: BorderRadius.circular(15),
              ),
              child: Column(
                children: [
                  const Text('Tu dominio exclusivo es:', style: TextStyle(color: Color(0xFF166534))),
                  const SizedBox(height: 10),
                  Text(successDomain ?? '', style: AppTextStyles.h2.copyWith(color: AppColors.primaryDark, fontSize: 20)),
                ],
              ),
            ),
            
            const SizedBox(height: 30),
            RichText(
              text: TextSpan(
                style: AppTextStyles.body.copyWith(color: Colors.grey.shade600),
                children: [
                  const TextSpan(text: 'Ya puedes iniciar sesión con tu correo '),
                  TextSpan(text: successEmail ?? '', style: const TextStyle(fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            
            const SizedBox(height: 30),
            AppButton.submit(
              label: 'Ir a mi Tienda',
              onPressed: onGoToStore,
              // width: 200, -> si el submit tuviera custom width
            ),
          ],
        ),
      ),
    );
  }
}
