import 'package:flutter/material.dart';
import '../models/resena.dart';
import 'star_rating.dart';

class ResenaCard extends StatelessWidget {
  final Resena resena;

  const ResenaCard({Key? key, required this.resena}) : super(key: key);

  String _formatDate(String dateStr) {
    try {
      final date = DateTime.parse(dateStr);
      return "${date.day}/${date.month}/${date.year}";
    } catch (e) {
      return dateStr;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 1,
      margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                CircleAvatar(
                  backgroundColor: Colors.grey.shade200,
                  child: Text(
                    resena.clienteNombre.isNotEmpty ? resena.clienteNombre[0].toUpperCase() : 'U',
                    style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.black54),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        resena.clienteNombre,
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                      ),
                      Text(
                        _formatDate(resena.fechaCreacion),
                        style: TextStyle(color: Colors.grey.shade600, fontSize: 12),
                      ),
                    ],
                  ),
                ),
                StarRating(
                  rating: resena.calificacion,
                  size: 18,
                  readOnly: true,
                ),
              ],
            ),
            if (resena.comentario != null && resena.comentario!.isNotEmpty) ...[
              const SizedBox(height: 12),
              const Divider(),
              const SizedBox(height: 8),
              Text(
                resena.comentario!,
                style: const TextStyle(fontSize: 14, color: Colors.black87, height: 1.4),
              ),
            ]
          ],
        ),
      ),
    );
  }
}
