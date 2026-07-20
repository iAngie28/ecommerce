import 'package:flutter/material.dart';
import '../models/cuenta_puntos.dart';
import '../services/fidelizacion_service.dart';
import 'package:intl/intl.dart';

class BilleteraPuntosScreen extends StatefulWidget {
  final String token;

  const BilleteraPuntosScreen({Key? key, required this.token}) : super(key: key);

  @override
  State<BilleteraPuntosScreen> createState() => _BilleteraPuntosScreenState();
}

class _BilleteraPuntosScreenState extends State<BilleteraPuntosScreen> {
  final FidelizacionService _service = FidelizacionService();
  CuentaPuntos? _cuenta;
  Map<String, dynamic> _config = {};
  bool _cargando = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _cargarDatos();
  }

  Future<void> _cargarDatos() async {
    setState(() {
      _cargando = true;
      _error = null;
    });

    try {
      final config = await _service.getConfiguracion();
      final cuenta = await _service.getMiCuenta(widget.token);
      
      setState(() {
        _config = config;
        _cuenta = cuenta;
        _cargando = false;
      });
    } catch (e) {
      setState(() {
        _error = 'Ocurrió un error al cargar tu billetera.';
        _cargando = false;
      });
    }
  }

  String _formatearFecha(String fechaStr) {
    try {
      final fecha = DateTime.parse(fechaStr);
      return DateFormat('dd/MM/yyyy HH:mm').format(fecha);
    } catch (e) {
      return fechaStr;
    }
  }

  Widget _buildTarjetaSaldo() {
    if (_cuenta == null) return const SizedBox.shrink();

    final valorDescuento = _cuenta!.saldoActual * (_config['VALOR_BS_POR_PUNTO'] ?? 0.05);

    return Container(
      width: double.infinity,
      margin: const EdgeInsets.all(16.0),
      padding: const EdgeInsets.all(24.0),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF2C3E50), Color(0xFF3498DB)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: Colors.blue.withOpacity(0.3),
            blurRadius: 15,
            offset: const Offset(0, 10),
          )
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Mi Saldo Actual',
            style: TextStyle(color: Colors.white70, fontSize: 16, fontWeight: FontWeight.w500),
          ),
          const SizedBox(height: 8),
          Row(
            crossAxisAlignment: CrossAxisAlignment.baseline,
            textBaseline: TextBaseline.alphabetic,
            children: [
              Text(
                '${_cuenta!.saldoActual}',
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 48,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(width: 8),
              const Text(
                'pts',
                style: TextStyle(color: Colors.white70, fontSize: 20),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.15),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.info_outline, color: Colors.white, size: 16),
                const SizedBox(width: 8),
                Text(
                  'Equivale a \$${valorDescuento.toStringAsFixed(2)} de descuento',
                  style: const TextStyle(color: Colors.white, fontSize: 14),
                ),
              ],
            ),
          )
        ],
      ),
    );
  }

  Widget _buildHistorial() {
    if (_cuenta == null || _cuenta!.historial.isEmpty) {
      return const Padding(
        padding: EdgeInsets.all(32.0),
        child: Center(
          child: Column(
            children: [
              Icon(Icons.inbox_outlined, size: 64, color: Colors.grey),
              SizedBox(height: 16),
              Text(
                'Aún no tienes movimientos',
                style: TextStyle(color: Colors.grey, fontSize: 16),
              ),
            ],
          ),
        ),
      );
    }

    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: _cuenta!.historial.length,
      itemBuilder: (context, index) {
        final mov = _cuenta!.historial[index];
        final esAcumulacion = mov.tipoOperacion == 'ACUMULACION';

        return ListTile(
          contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
          leading: Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: esAcumulacion ? Colors.green.shade50 : Colors.red.shade50,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(
              esAcumulacion ? Icons.trending_up : Icons.shopping_bag_outlined,
              color: esAcumulacion ? Colors.green : Colors.red,
            ),
          ),
          title: Text(
            esAcumulacion ? 'Acumulación por Compra' : 'Canje por Descuento',
            style: const TextStyle(fontWeight: FontWeight.bold),
          ),
          subtitle: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 4),
              Text(mov.referencia ?? ''),
              Text(_formatearFecha(mov.fecha), style: const TextStyle(fontSize: 12)),
            ],
          ),
          trailing: Text(
            '${esAcumulacion ? '+' : ''}${mov.montoPuntos} pts',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 16,
              color: esAcumulacion ? Colors.green : Colors.red,
            ),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey.shade50,
      appBar: AppBar(
        title: const Text('Billetera de Puntos', style: TextStyle(color: Colors.black87)),
        backgroundColor: Colors.white,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.black87),
      ),
      body: _cargando
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(_error!, style: const TextStyle(color: Colors.red)),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: _cargarDatos,
                        child: const Text('Reintentar'),
                      )
                    ],
                  ),
                )
              : RefreshIndicator(
                  onRefresh: _cargarDatos,
                  child: SingleChildScrollView(
                    physics: const AlwaysScrollableScrollPhysics(),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildTarjetaSaldo(),
                        const Padding(
                          padding: EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                          child: Text(
                            'Historial de Movimientos',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                              color: Colors.black87,
                            ),
                          ),
                        ),
                        Container(
                          margin: const EdgeInsets.symmetric(horizontal: 16),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(16),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.grey.shade200,
                                blurRadius: 10,
                                offset: const Offset(0, 5),
                              )
                            ]
                          ),
                          child: _buildHistorial(),
                        ),
                        const SizedBox(height: 32),
                      ],
                    ),
                  ),
                ),
    );
  }
}
