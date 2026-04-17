class ApiConstants {
  static const String vpsIp = '157.173.102.129';

  // ── URL BASE (con puerto 8001) ──
  // El login irá a: http://157.173.102.129:8001/api/token/
  static const String mainBaseUrl = 'http://$vpsIp:8001/api';

  // ── URL para peticiones dentro de un tenant ──
  // Formato: http://empresa1.157.173.102.129.nip.io:8001/api
  static String tenantBaseUrl(String schemaName) {
    final slug = schemaName.replaceAll('_', '');
    return 'http://$slug.$vpsIp.nip.io:8001/api';
  }

  // ── Header Host para django-tenants ──
  // Django-tenants necesita leer el subdominio del Host header
  static String tenantHost(String schemaName) {
    final slug = schemaName.replaceAll('_', '');
    return '$slug.$vpsIp.nip.io';
  }

  // ── Auth Endpoints (IP directa, sin tenant) ──
  static const String login = '/token/';
  static const String refresh = '/token/refresh/';
  static const String logout = '/logout/';

  // ── Tenant Endpoints ──
  static const String dashboard = '/dashboard/';
  static const String productos = '/productos/';
}