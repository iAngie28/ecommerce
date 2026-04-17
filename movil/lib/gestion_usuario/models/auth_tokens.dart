class AuthTokens {
  final String access;
  final String refresh;
  final String schemaName;
  final String subdomain;

  AuthTokens({
    required this.access,
    required this.refresh,
    required this.schemaName,
    required this.subdomain,
  });

  factory AuthTokens.fromJson(Map<String, dynamic> json) {
    return AuthTokens(
      access: json['access'] ?? '',
      refresh: json['refresh'] ?? '',
      schemaName: json['schema_name'] ?? '',
      subdomain: json['subdomain'] ?? '',
    );
  }
}