class HistorialPuntos {
  final int id;
  final String tipoOperacion;
  final int montoPuntos;
  final String? referencia;
  final String fecha;

  HistorialPuntos({
    required this.id,
    required this.tipoOperacion,
    required this.montoPuntos,
    this.referencia,
    required this.fecha,
  });

  factory HistorialPuntos.fromJson(Map<String, dynamic> json) {
    return HistorialPuntos(
      id: json['id'],
      tipoOperacion: json['tipo_operacion'],
      montoPuntos: json['monto_puntos'],
      referencia: json['referencia'],
      fecha: json['fecha'],
    );
  }
}

class CuentaPuntos {
  final int id;
  final String clienteNombre;
  final int saldoActual;
  final int puntosHistoricos;
  final String fechaActualizacion;
  final List<HistorialPuntos> historial;

  CuentaPuntos({
    required this.id,
    required this.clienteNombre,
    required this.saldoActual,
    required this.puntosHistoricos,
    required this.fechaActualizacion,
    required this.historial,
  });

  factory CuentaPuntos.fromJson(Map<String, dynamic> json) {
    var historialJson = json['historial'] as List? ?? [];
    List<HistorialPuntos> historialList = historialJson.map((h) => HistorialPuntos.fromJson(h)).toList();

    return CuentaPuntos(
      id: json['id'],
      clienteNombre: json['cliente_nombre'] ?? 'Cliente',
      saldoActual: json['saldo_actual'],
      puntosHistoricos: json['puntos_historicos'],
      fechaActualizacion: json['fecha_actualizacion'],
      historial: historialList,
    );
  }
}
