class ApiConstants {
  static const String vpsIp = '157.173.102.129';

  // ── URL BASE (con puerto 8001) ──
  static const String mainBaseUrl = 'http://$vpsIp:8001/api';

  // ── URL para peticiones dentro de un tenant ──
  static String tenantBaseUrl(String schemaName) {
    final slug = schemaName.replaceAll('_', '');
    return 'http://$slug.$vpsIp.nip.io:8001/api';
  }

  // ── Header Host para django-tenants ──
  static String tenantHost(String schemaName) {
    final slug = schemaName.replaceAll('_', '');
    return '$slug.$vpsIp.nip.io';
  }

  // ── Auth Endpoints (IP directa, sin tenant) ──
  static const String login = '/token/';
  static const String refresh = '/token/refresh/';
  static const String logout = '/logout/';

  // ── Tenant Endpoints ──
  static const String productos = '/productos/';
  static const String categorias = '/categorias/';
  static const String pedidos = '/pedidos/';
}
