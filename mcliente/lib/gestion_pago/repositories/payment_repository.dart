import 'dart:convert';
import 'package:flutter/material.dart';
import '../../core/network/api_client.dart';
import '../../core/constants/api_constants.dart';
import '../../core/storage/secure_storage.dart';
import 'package:flutter_stripe/flutter_stripe.dart';

class PaymentRepository {
  final ApiClient _apiClient = ApiClient();
  final SecureStorageService _storage = SecureStorageService();

  Future<String?> _buildUrl({String? tenantHostOverride}) async {
    if (tenantHostOverride != null && tenantHostOverride.isNotEmpty) {
      return '${ApiConstants.tenantBaseUrl(tenantHostOverride)}/pagos/';
    }

    final subdomain = await _storage.getSubdomain();
    if (subdomain == null || subdomain.isEmpty) return null;
    return '${ApiConstants.tenantBaseUrl(subdomain)}/pagos/';
  }

  /// Crea un PaymentIntent en el backend y devuelve el client_secret
  Future<Map<String, dynamic>> createPaymentIntent(
    int pedidoId, {
    int puntosCanjeados = 0,
    String? tenantHostOverride,
  }) async {
    final baseUrl = await _buildUrl(tenantHostOverride: tenantHostOverride);
    if (baseUrl == null) throw Exception('No hay tenant configurado.');
    final url = '${baseUrl}create-payment-intent/';

    final response = await _apiClient.post(
      url,
      {
        'pedido_id': pedidoId,
        if (puntosCanjeados > 0) 'puntos_canjeados': puntosCanjeados,
      },
      requiresAuth: true,
      includeTenantHost: true,
      tenantHostOverride: tenantHostOverride,
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Error al crear PaymentIntent: ${response.body}');
    }
  }

  /// Procesa el pago usando el Payment Sheet de Stripe
  Future<bool> processPaymentSheet(
    int pedidoId, {
    int puntosCanjeados = 0,
    String? tenantHostOverride,
  }) async {
    try {
      // 1. Obtener los datos del PaymentIntent desde el backend
      final paymentData = await createPaymentIntent(
        pedidoId,
        puntosCanjeados: puntosCanjeados,
        tenantHostOverride: tenantHostOverride,
      );

      if (paymentData['payment_required'] == false) {
        return true;
      }

      final String clientSecret = paymentData['paymentIntent'];
      final String? customerId = paymentData['customer'];
      final String? ephemeralKey = paymentData['ephemeralKey'];

      // 2. Inicializar el Payment Sheet
      await Stripe.instance.initPaymentSheet(
        paymentSheetParameters: SetupPaymentSheetParameters(
          paymentIntentClientSecret: clientSecret,
          customerId: customerId,
          customerEphemeralKeySecret: ephemeralKey,
          merchantDisplayName: 'MiQhatu Ecommerce',
          style: ThemeMode.light,
        ),
      );

      // 3. Mostrar el Payment Sheet
      await Stripe.instance.presentPaymentSheet();

      // 4. Confirmar el éxito al backend (opcional, el webhook también lo hará)
      await confirmPaymentSuccess(
        pedidoId,
        tenantHostOverride: tenantHostOverride,
      );

      return true;
    } catch (e) {
      if (e is StripeException) {
        print('Error de Stripe: ${e.error.localizedMessage}');
      } else {
        print('Error procesando pago: $e');
      }
      return false;
    }
  }

  Future<void> confirmPaymentSuccess(
    int pedidoId, {
    String? tenantHostOverride,
  }) async {
    final baseUrl = await _buildUrl(tenantHostOverride: tenantHostOverride);
    if (baseUrl == null) throw Exception('No hay tenant configurado.');
    final url = '${baseUrl}confirm-success/';
    final schemaName = await _storage.getSchemaName();
    final tenant = tenantHostOverride ?? schemaName;

    await _apiClient.post(
      url,
      {'pedido_id': pedidoId, 'tenant': tenant},
      requiresAuth: true,
      includeTenantHost: true,
      tenantHostOverride: tenantHostOverride,
    );
  }
}
