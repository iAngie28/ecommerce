import 'package:flutter/material.dart';

// 1. Importamos tu UI Kit (Estilos y Widgets puros)
import '../../core/theme/app_colors.dart';
import '../../core/widgets/cards/app_login_card.dart'; 
import '../../core/widgets/feedback/app_toast.dart';

// 2. Importamos la lógica de negocio de este paquete
import '../repositories/auth_repository.dart';
// import '../../dashboard/screens/dashboard_screen.dart'; // A donde irás después de loguearte

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  // Controladores para leer lo que el usuario escribe
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  
  // Instanciamos a nuestro "Jefe de Obra"
  final AuthRepository _authRepository = AuthRepository();
  
  // Para bloquear el botón mientras Django responde
  bool _isLoading = false;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  // La función principal que une todo
  Future<void> _handleLogin() async {
    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();

    // Validaciones básicas antes de molestar al servidor
    if (email.isEmpty || password.isEmpty) {
      AppToast.showError(context, 'Por favor, completa todos los campos.');
      return;
    }

    setState(() => _isLoading = true);


    final bool isSuccess = await _authRepository.login(email, password);

    setState(() => _isLoading = false); 

    if (isSuccess) {

      if (!mounted) return;
      AppToast.showSuccess(context, '¡Bienvenido de vuelta!');
      
      Navigator.pushReplacementNamed(context, '/dashboard'); 
      
    } else {

      if (!mounted) return;
      AppToast.showError(context, 'Correo o contraseña incorrectos.');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bgLight, // Usamos tu token de color
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20),
          // Usamos el mega-widget que diseñaste, pasándole los controladores
          child: _isLoading 
              ? const CircularProgressIndicator(color: AppColors.accentTeal)
              : AppLoginCard(
                  brandName: 'MiQhatu',
                  brandIcon: Icons.inventory_2, // ⬅️ AQUÍ ESTÁ LA CORRECCIÓN
                  infoTitle: 'Controla tu inventario,\nsimplifica tu negocio.',
                  infoSubtitle: 'Gestiona productos, movimientos y reportes desde un solo lugar.',
                  emailController: _emailController,
                  passwordController: _passwordController,
                  onSubmit: _handleLogin, // Conectamos el botón a nuestra función
                  onForgot: () {
                    Navigator.pushNamed(context, '/recuperar-password');
                  },
                  onRegister: () {
                    Navigator.pushNamed(context, '/crear-tienda');
                  },
                ),
        ),
      ),
    );
  }
}