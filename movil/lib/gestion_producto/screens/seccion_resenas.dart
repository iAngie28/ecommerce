import 'package:flutter/material.dart';
import '../models/resena.dart';
import '../services/resena_service.dart';
import '../widgets/resena_card.dart';
import '../widgets/star_rating.dart';

class SeccionResenas extends StatefulWidget {
  final int productoId;
  final bool usuarioAutenticado;
  final String? token; // Para enviar la reseña

  const SeccionResenas({
    Key? key,
    required this.productoId,
    this.usuarioAutenticado = false,
    this.token,
  }) : super(key: key);

  @override
  State<SeccionResenas> createState() => _SeccionResenasState();
}

class _SeccionResenasState extends State<SeccionResenas> {
  final ResenaService _resenaService = ResenaService();
  final TextEditingController _comentarioController = TextEditingController();
  
  bool _cargando = true;
  String? _error;
  List<Resena> _resenas = [];
  Map<String, dynamic> _estadisticas = {'promedio': 0.0, 'total_reseñas': 0};
  
  int _nuevaCalificacion = 0;
  bool _enviando = false;

  @override
  void initState() {
    super.initState();
    _cargarResenas();
  }

  @override
  void dispose() {
    _comentarioController.dispose();
    super.dispose();
  }

  Future<void> _cargarResenas() async {
    setState(() {
      _cargando = true;
      _error = null;
    });

    try {
      final data = await _resenaService.obtenerResenas(widget.productoId);
      setState(() {
        _resenas = data['resenas'];
        _estadisticas = data['estadisticas'];
        _cargando = false;
      });
    } catch (e) {
      setState(() {
        _error = 'Ocurrió un problema al cargar las reseñas.';
        _cargando = false;
      });
    }
  }

  Future<void> _enviarResena() async {
    if (_nuevaCalificacion == 0) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Por favor selecciona una calificación de estrellas.')),
      );
      return;
    }

    setState(() => _enviando = true);

    try {
      final success = await _resenaService.enviarResena(
        productoId: widget.productoId,
        calificacion: _nuevaCalificacion,
        comentario: _comentarioController.text,
        token: widget.token ?? '',
      );

      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Reseña enviada con éxito. Pendiente de moderación.'),
            backgroundColor: Colors.green,
          ),
        );
        setState(() {
          _nuevaCalificacion = 0;
          _comentarioController.clear();
        });
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Error al enviar la reseña. Inténtalo de nuevo.'),
          backgroundColor: Colors.red,
        ),
      );
    } finally {
      setState(() => _enviando = false);
    }
  }

  Widget _buildResumen() {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.grey.shade100,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            _estadisticas['promedio'].toStringAsFixed(1),
            style: const TextStyle(fontSize: 40, fontWeight: FontWeight.bold, color: Colors.black87),
          ),
          const SizedBox(width: 16),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              StarRating(rating: _estadisticas['promedio'].round(), readOnly: true, size: 20),
              const SizedBox(height: 4),
              Text(
                '${_estadisticas['total_reseñas']} opiniones',
                style: TextStyle(color: Colors.grey.shade600),
              ),
            ],
          )
        ],
      ),
    );
  }

  Widget _buildFormulario() {
    if (!widget.usuarioAutenticado) {
      return Container(
        margin: const EdgeInsets.all(16),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.blue.shade50,
          borderRadius: BorderRadius.circular(8),
        ),
        child: const Center(
          child: Text(
            'Inicia sesión para compartir tu experiencia sobre este producto.',
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.blueGrey),
          ),
        ),
      );
    }

    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        border: Border.all(color: Colors.grey.shade300),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Escribe una reseña', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          const Text('Tu calificación:'),
          const SizedBox(height: 8),
          StarRating(
            rating: _nuevaCalificacion,
            readOnly: false,
            onRatingChanged: (rating) {
              setState(() => _nuevaCalificacion = rating);
            },
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _comentarioController,
            maxLines: 3,
            maxLength: 1000,
            decoration: const InputDecoration(
              hintText: '¿Qué te pareció este producto?',
              border: OutlineInputBorder(),
              contentPadding: EdgeInsets.all(12),
            ),
          ),
          const SizedBox(height: 12),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _enviando ? null : _enviarResena,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 12),
              ),
              child: _enviando 
                  ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2))
                  : const Text('Enviar Reseña'),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_cargando) {
      return const Padding(
        padding: EdgeInsets.all(40.0),
        child: Center(child: CircularProgressIndicator()),
      );
    }

    if (_error != null) {
      return Padding(
        padding: const EdgeInsets.all(20.0),
        child: Center(child: Text(_error!, style: const TextStyle(color: Colors.red))),
      );
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.only(left: 16, top: 24, bottom: 8),
          child: Text(
            'Reseñas de Clientes',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
        ),
        _buildResumen(),
        _buildFormulario(),
        if (_resenas.isEmpty)
          const Padding(
            padding: EdgeInsets.all(32.0),
            child: Center(
              child: Text(
                'Aún no hay reseñas para este producto.\n¡Sé el primero en opinar!',
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.grey),
              ),
            ),
          )
        else
          ListView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: _resenas.length,
            itemBuilder: (context, index) {
              return ResenaCard(resena: _resenas[index]);
            },
          ),
      ],
    );
  }
}
