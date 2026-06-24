import 'package:flutter/material.dart';

import '../../core/theme/app_colors.dart';
import '../../core/widgets/cards/app_create_store_card.dart';
import '../../core/constants/api_constants.dart';
import '../repositories/auth_repository.dart';
import 'package:flutter_stripe/flutter_stripe.dart';

class CrearTiendaScreen extends StatefulWidget {
  const CrearTiendaScreen({super.key});

  @override
  State<CrearTiendaScreen> createState() => _CrearTiendaScreenState();
}

class _CrearTiendaScreenState extends State<CrearTiendaScreen> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  
  final TextEditingController _storeNameController = TextEditingController();
  final TextEditingController _slugController = TextEditingController();
  final TextEditingController _domainController = TextEditingController();
  final TextEditingController _firstNameController = TextEditingController();
  final TextEditingController _lastNameController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  
  final AuthRepository _authRepository = AuthRepository();
  
  bool _isLoading = false;
  String? _errorMessage;
  bool _isSuccess = false;
  String? _successDomain;
  String? _successEmail;
  
  List<Map<String, dynamic>> _availablePlans = [];
  String? _selectedPlan;

  @override
  void initState() {
    super.initState();
    // Escuchar cambios en el nombre de la tienda para generar slug y dominio
    _storeNameController.addListener(_updateSlugAndDomain);
    _loadPlanes();
  }

  Future<void> _loadPlanes() async {
    final planes = await _authRepository.fetchPlanes();
    if (mounted) {
      setState(() {
        _availablePlans = planes;
        if (_availablePlans.isNotEmpty) {
          // Select free plan by default
          final freePlan = _availablePlans.firstWhere(
            (p) => double.tryParse(p['precio_mensual'].toString()) == 0,
            orElse: () => _availablePlans.first,
          );
          _selectedPlan = freePlan['nombre'];
        }
      });
    }
  }

  @override
  void dispose() {
    _storeNameController.removeListener(_updateSlugAndDomain);
    _storeNameController.dispose();
    _slugController.dispose();
    _domainController.dispose();
    _firstNameController.dispose();
    _lastNameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _updateSlugAndDomain() {
    final name = _storeNameController.text;
    if (name.isEmpty) {
      _slugController.clear();
      _domainController.clear();
      return;
    }

    // Reglas similares a React
    String slug = name.toLowerCase()
      // Eliminar acentos de forma simplificada
      .replaceAll('á', 'a').replaceAll('é', 'e').replaceAll('í', 'i')
      .replaceAll('ó', 'o').replaceAll('ú', 'u')
      .replaceAll('ñ', 'n')
      .replaceAll(RegExp(r'\s+'), 'x') // Espacios a 'x'
      .replaceAll(RegExp(r'[^a-z0-9]'), ''); // Eliminar todo lo demás

    _slugController.text = slug;
    
    // Obtenemos ip del VPS de nuestras constantes, o 'localhost' como fallback
    final baseIp = ApiConstants.vpsIp;
    
    // Dominio
    if (baseIp == 'localhost' || baseIp == '127.0.0.1') {
      _domainController.text = '$slug.localhost';
    } else {
      _domainController.text = '$slug.$baseIp.nip.io';
    }
  }

  Future<void> _handleCreateStore() async {
    if (!(_formKey.currentState?.validate() ?? false)) return;

    if (_storeNameController.text.isEmpty ||
        _firstNameController.text.isEmpty ||
        _lastNameController.text.isEmpty ||
        _emailController.text.isEmpty ||
        _passwordController.text.isEmpty) {
      setState(() => _errorMessage = 'Por favor, completa todos los campos.');
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    final payload = {
      "nombre_tienda": _storeNameController.text.trim(),
      "schema_name": _slugController.text,
      "dominio": _domainController.text,
      "first_name": _firstNameController.text.trim(),
      "last_name": _lastNameController.text.trim(),
      "email": _emailController.text.trim(),
      "password": _passwordController.text,
      if (_selectedPlan != null) "plan": _selectedPlan,
    };

    // Determine if it's free
    final planData = _availablePlans.firstWhere(
      (p) => p['nombre'] == _selectedPlan,
      orElse: () => <String, dynamic>{},
    );
    final bool isFree = (double.tryParse(planData['precio_mensual']?.toString() ?? '0') ?? 0) == 0;

    Map<String, dynamic> result;

    if (isFree) {
      result = await _authRepository.createStore(payload);
    } else {
      // 1. Initialize intent
      final checkoutResult = await _authRepository.checkoutSuscripcion(payload);
      if (!checkoutResult['success']) {
        setState(() {
          _errorMessage = checkoutResult['error'];
          _isLoading = false;
        });
        return;
      }
      
      final clientSecret = checkoutResult['data']['clientSecret'];
      final publishableKey = checkoutResult['data']['publishableKey'];
      
      if (clientSecret == null || publishableKey == null) {
         setState(() {
          _errorMessage = 'Faltan credenciales de pago desde el servidor.';
          _isLoading = false;
        });
        return;
      }

      // 2. Setup Stripe
      Stripe.publishableKey = publishableKey;
      
      try {
        await Stripe.instance.initPaymentSheet(
          paymentSheetParameters: SetupPaymentSheetParameters(
            paymentIntentClientSecret: clientSecret,
            merchantDisplayName: 'MiQhatu SaaS',
            appearance: const PaymentSheetAppearance(
              colors: PaymentSheetAppearanceColors(
                primary: AppColors.primaryDark,
              ),
            ),
          ),
        );
        
        // 3. Present Sheet
        await Stripe.instance.presentPaymentSheet();
      } catch (e) {
        if (e is StripeException) {
          setState(() {
            _errorMessage = 'Pago cancelado o fallido: ${e.error.localizedMessage}';
            _isLoading = false;
          });
        } else {
          setState(() {
            _errorMessage = 'Error inesperado al pagar: $e';
            _isLoading = false;
          });
        }
        return;
      }
      
      // 4. Create store after successful payment
      payload['payment_intent'] = clientSecret.split('_secret')[0]; 
      result = await _authRepository.createStoreWithPayment(payload);
    }

    if (!mounted) return;

    if (result['success']) {
      setState(() {
        _isSuccess = true;
        _successDomain = result['data']?['dominio'] ?? _domainController.text;
        _successEmail = result['data']?['admin_email'] ?? _emailController.text;
      });
    } else {
      setState(() {
         // Transformar errores que vienen como array si aplica
        final error = result['error'];
        if (error is List) {
          _errorMessage = error.join(', ');
        } else if (error is Map) {
          _errorMessage = error.values.expand((element) => element is List ? element : [element]).join('\n');
        } else {
          _errorMessage = error.toString();
        }
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
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: !_isSuccess ? BackButton(color: AppColors.primaryDark) : null,
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: AppCreateStoreCard(
            formKey: _formKey,
            storeNameController: _storeNameController,
            slugController: _slugController,
            domainController: _domainController,
            firstNameController: _firstNameController,
            lastNameController: _lastNameController,
            emailController: _emailController,
            passwordController: _passwordController,
            isLoading: _isLoading,
            errorMessage: _errorMessage,
            isSuccess: _isSuccess,
            successDomain: _successDomain,
            successEmail: _successEmail,
            availablePlans: _availablePlans,
            selectedPlan: _selectedPlan,
            onPlanSelected: (plan) {
              setState(() {
                _selectedPlan = plan;
              });
            },
            onSubmit: _handleCreateStore,
            onGoToStore: () {
               // Redirigir al inicio o pantalla de login principal
               Navigator.pushReplacementNamed(context, '/login');
            },
          ),
        ),
      ),
    );
  }
}
