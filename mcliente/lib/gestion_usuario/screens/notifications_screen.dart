import 'package:flutter/material.dart';
import '../repositories/notification_repository.dart';

class NotificationsScreen extends StatefulWidget {
  const NotificationsScreen({Key? key}) : super(key: key);

  @override
  State<NotificationsScreen> createState() => _NotificationsScreenState();
}

class _NotificationsScreenState extends State<NotificationsScreen> {
  final NotificationRepository _repo = NotificationRepository();
  List<dynamic> _notifications = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchNotifications();
  }

  Future<void> _fetchNotifications() async {
    setState(() => _isLoading = true);
    try {
      final data = await _repo.getNotifications();
      setState(() {
        _notifications = data;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error al cargar notificaciones: $e')),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _markAsRead(Map<String, dynamic> notif) async {
    try {
      final id = int.tryParse((notif['id'] ?? '').toString()) ?? 0;
      await _repo.markAsRead(
        id,
        tenantHost: notif['tienda_host']?.toString(),
        tenantSchema: notif['tienda_schema']?.toString(),
      );
      setState(() {
        final tenantSchema = notif['tienda_schema']?.toString();
        final index = _notifications.indexWhere(
          (n) =>
              n['id'] == id &&
              (n['tienda_schema']?.toString() ?? '') ==
                  (tenantSchema ?? ''),
        );
        if (index != -1) {
          _notifications[index]['leido'] = true;
        }
      });
    } catch (e) {
      print(e);
    }
  }

  Future<void> _markAllAsRead() async {
    try {
      await _repo.markAllAsRead();
      setState(() {
        for (var n in _notifications) {
          n['leido'] = true;
        }
      });
    } catch (e) {
      print(e);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mis Notificaciones'),
        actions: [
          if (_notifications.any((n) => !n['leido']))
            IconButton(
              icon: const Icon(Icons.checklist),
              tooltip: 'Marcar todas como leídas',
              onPressed: _markAllAsRead,
            ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _notifications.isEmpty
          ? const Center(child: Text('No tienes notificaciones'))
          : ListView.builder(
              itemCount: _notifications.length,
              itemBuilder: (context, index) {
                final notif = _notifications[index];
                final isRead = notif['leido'] ?? false;

                return ListTile(
                  tileColor: isRead ? null : Colors.blue.withOpacity(0.1),
                  leading: Icon(
                    notif['tipo'] == 'PAGO'
                        ? Icons.payment
                        : notif['tipo'] == 'PEDIDO'
                        ? Icons.local_shipping
                        : Icons.info,
                    color: isRead ? Colors.grey : Colors.blue,
                  ),
                  title: Text(
                    notif['titulo'] ?? '',
                    style: TextStyle(
                      fontWeight: isRead ? FontWeight.normal : FontWeight.bold,
                    ),
                  ),
                  subtitle: Text(notif['mensaje'] ?? ''),
                  isThreeLine: notif['tienda_nombre'] != null,
                  onTap: () {
                    if (!isRead) _markAsRead(Map<String, dynamic>.from(notif));
                  },
                  trailing: notif['tienda_nombre'] != null
                      ? Text(
                          notif['tienda_nombre'].toString(),
                          style: const TextStyle(fontSize: 11),
                        )
                      : null,
                );
              },
            ),
    );
  }
}
