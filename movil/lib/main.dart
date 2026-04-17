import 'package:flutter/material.dart';

// 1. Importamos tu tema global
import 'core/theme/app_theme.dart';

// 2. Importamos tus pantallas
import 'gestion_usuario/screens/login_screen.dart';
import 'gestion_usuario/screens/recuperar_password_screen.dart';
import 'gestion_usuario/screens/crear_tienda_screen.dart';
import 'dashboard/screens/dashboard_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MiQhatu App',
      // ¡Aquí inyectamos todo el UI Kit que creaste!
      theme: AppTheme.themeData, 
      
      // Quitamos la etiqueta molesta de "DEBUG" arriba a la derecha
      debugShowCheckedModeBanner: false,
      
      // ── LA LÓGICA DE RUTAS ──
      
      // 1. Definimos con qué pantalla arranca la app
      initialRoute: '/login', 
      
      // 2. El "Mapa" de rutas. Asigna un string a cada pantalla
      routes: {
        '/login': (context) => const LoginScreen(),
        '/recuperar-password': (context) => const RecuperarPasswordScreen(),
        '/crear-tienda': (context) => const CrearTiendaScreen(),
        '/dashboard': (context) => const DashboardScreen(),
      },
    );
  }
}