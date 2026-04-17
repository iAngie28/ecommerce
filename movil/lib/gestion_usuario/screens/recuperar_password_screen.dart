import 'dart:math';
import 'package:flutter/material.dart';

import '../../core/theme/app_colors.dart';
import '../../core/widgets/cards/app_forgot_password_card.dart';
import '../repositories/auth_repository.dart';

class RecuperarPasswordScreen extends StatefulWidget {
  const RecuperarPasswordScreen({super.key});

  @override
  State<RecuperarPasswordScreen> createState() => _RecuperarPasswordScreenState();
}

class _RecuperarPasswordScreenState extends State<RecuperarPasswordScreen> {
  final TextEditingController _emailController = TextEditingController();
  final AuthRepository _authRepository = AuthRepository();
  final Random _random = Random();
  
  bool _isLoading = false;
  String? _errorMessage;
  String? _successMessage;
  String? _devUrl;

  late String _currentTitle;
  late String _currentSubtitle;

  static const List<Map<String, String>> _initialPhrases = [
    {
      'title': 'No te preocupes,\na todos nos pasa.',
      'subtitle': 'Sigue los pasos que te enviaremos al correo para recuperar el acceso a tu cuenta de forma segura.'
    },
    {
      'title': 'Una vez anotado el correo en el cuadro...',
      'subtitle': 'Te llegará un enlace y la contraseña se restablecerá en 40 segundos.'
    },
    {
      'title': '¿Acaso eres el olvidadizo de la bahía?',
      'subtitle': 'se te envio el enlace en tu correo. Ve y limpia la escena.',
    },
    {
      'title': 'Mires donde mires, hay gente que también se olvida de su contraseña.',
      'subtitle': 'Pero solo a ti te acabamos de mandar un correo para solucionarlo. Ve a darle clic.',
    },
    {
      'title': 'Veo que olvidaste la contraseña. Puedo entenderlo, pero no puedo recordarla por ti.',
      'subtitle': 'El enlace de recuperación estara en tu correo. Haz clic ahí y restablecela',
    },
    {
      'title': '123456 no era......',
      'subtitle': 'Revisa tu bandeja. Te enviaremos un enlace para que pongas una nueva.',
    },
    {
      'title': '¿Otra vez?',
      'subtitle': 'Te enviaremos el enlace al correo.',
    },
    {
      'title': '👀👀👀👀👀👀',
      'subtitle': 'Te enviaremos el enlace al correo.',
    },
  ];

  static const List<Map<String, String>> _sentPhrases = [
    {
      'title': '¿Acaso eres el olvidadizo de la bahía?',
      'subtitle': 'se te envio el enlace en tu correo. Ve y limpia la escena.',
    },
    {
      'title': 'Mires donde mires, hay gente que también se olvida de su contraseña.',
      'subtitle': 'Pero solo a ti te acabamos de mandar un correo para solucionarlo. Ve a darle clic.',
    },
    {
      'title': 'Veo que olvidaste la contraseña. Puedo entenderlo, pero no puedo recordarla por ti.',
      'subtitle': 'El enlace de recuperación ya está en tu correo. Haz clic ahí y restablecela',
    },
    {
      'title': '123456 no era......',
      'subtitle': 'Revisa tu bandeja. Te enviamos un enlace para que pongas una nueva.',
    },
    {
      'title': '¿Otra vez?',
      'subtitle': 'Te mandamos el enlace al correo.',
    },
    {
      'title': '👀👀👀👀👀👀',
      'subtitle': 'Te mandamos el enlace al correo.',
    },
  ];

  @override
  void initState() {
    super.initState();
    _setRandomInitialPhrase();
  }

  void _setRandomInitialPhrase() {
    final phrase = _initialPhrases[_random.nextInt(_initialPhrases.length)];
    setState(() {
      _currentTitle = phrase['title']!;
      _currentSubtitle = phrase['subtitle']!;
    });
  }

  void _setRandomSentPhrase() {
    final phrase = _sentPhrases[_random.nextInt(_sentPhrases.length)];
    setState(() {
      _currentTitle = phrase['title']!;
      _currentSubtitle = phrase['subtitle']!;
    });
  }

  @override
  void dispose() {
    _emailController.dispose();
    super.dispose();
  }

  Future<void> _handleReset() async {
    final email = _emailController.text.trim();
    if (email.isEmpty) {
      setState(() => _errorMessage = 'Por favor, ingresa tu correo electrónico.');
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _successMessage = null;
      _devUrl = null;
    });

    final result = await _authRepository.resetPassword(email);

    if (!mounted) return;

    if (result['success']) {
      setState(() {
        _successMessage = result['message'];
        _devUrl = result['dev_reset_url'];
      });
      _setRandomSentPhrase(); // Cambiar a frase random de enviado
    } else {
      setState(() {
        _errorMessage = result['error'] ?? 'Error desconocido.';
      });
    }

    setState(() {
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bgLight,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: AppForgotPasswordCard(
            brandName: 'MiQhatu',
            infoTitle: _currentTitle,
            infoSubtitle: _currentSubtitle,
            emailController: _emailController,
            isLoading: _isLoading,
            errorMessage: _errorMessage,
            successMessage: _successMessage,
            devUrl: _devUrl,
            onSubmit: _handleReset,
            onBack: () {
              Navigator.pop(context);
            },
          ),
        ),
      ),
    );
  }
}
