import 'dart:async';

import 'package:flutter/material.dart';
import '../../../gestion_usuario/repositories/notification_repository.dart';
import '../../services/notification_badge_service.dart';
import '../../theme/app_colors.dart';
import 'app_sidebar.dart';
import 'app_topbar.dart';

class AppDashboardLayout extends StatefulWidget {
  final String brandName;
  final List<AppSidebarItem> sidebarItems;
  final String? tenantLabel;
  final String? tenantValue;
  final String userName;
  final Widget body;
  final Widget? topBarTrailing;

  const AppDashboardLayout({
    super.key,
    required this.brandName,
    required this.sidebarItems,
    this.tenantLabel,
    this.tenantValue,
    required this.userName,
    required this.body,
    this.topBarTrailing,
  });

  @override
  State<AppDashboardLayout> createState() => _AppDashboardLayoutState();
}

class _AppDashboardLayoutState extends State<AppDashboardLayout> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  final NotificationRepository _notificationRepository =
      NotificationRepository();
  Timer? _notificationTimer;
  int _unreadCount = 0;

  @override
  void initState() {
    super.initState();
    _loadUnreadCount();
    _notificationTimer = Timer.periodic(
      const Duration(seconds: 30),
      (_) => _loadUnreadCount(),
    );
    NotificationBadgeService.pulse.addListener(_loadUnreadCount);
  }

  @override
  void dispose() {
    _notificationTimer?.cancel();
    NotificationBadgeService.pulse.removeListener(_loadUnreadCount);
    super.dispose();
  }

  Future<void> _loadUnreadCount() async {
    try {
      final notifications = await _notificationRepository.getNotifications();
      final unread = notifications
          .where((notification) =>
              notification is Map && notification['leido'] != true)
          .length;
      if (!mounted || unread == _unreadCount) return;
      setState(() => _unreadCount = unread);
    } catch (_) {}
  }

  Future<void> _openNotifications() async {
    await Navigator.pushNamed(context, '/notificaciones');
    _loadUnreadCount();
  }

  Widget _buildNotificationButton() {
    final hasUnread = _unreadCount > 0;

    return Stack(
      clipBehavior: Clip.none,
      children: [
        IconButton(
          tooltip: 'Notificaciones',
          icon: Icon(
            hasUnread
                ? Icons.notifications_active
                : Icons.notifications_outlined,
            color: hasUnread ? AppColors.danger : AppColors.primaryDark,
          ),
          onPressed: _openNotifications,
        ),
        if (hasUnread)
          Positioned(
            right: 5,
            top: 5,
            child: Container(
              constraints: const BoxConstraints(minWidth: 18, minHeight: 18),
              padding: const EdgeInsets.symmetric(horizontal: 5),
              decoration: BoxDecoration(
                color: AppColors.danger,
                border: Border.all(color: AppColors.white, width: 1.5),
                borderRadius: BorderRadius.circular(999),
              ),
              alignment: Alignment.center,
              child: Text(
                _unreadCount > 99 ? '99+' : _unreadCount.toString(),
                style: const TextStyle(
                  color: AppColors.white,
                  fontSize: 10,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.sizeOf(context);
    final isMobile = size.width < 800;
    final notificationButton = _buildNotificationButton();
    final trailingWidgets = Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        notificationButton,
        if (widget.topBarTrailing != null) ...[
          const SizedBox(width: 4),
          widget.topBarTrailing!,
        ],
      ],
    );

    return Scaffold(
      key: _scaffoldKey,
      resizeToAvoidBottomInset: false,
      backgroundColor: AppColors.bgLight,
      drawer: isMobile
          ? Drawer(
              child: AppSidebar(
                brandName: widget.brandName,
                items: widget.sidebarItems,
              ),
            )
          : null,
      body: Row(
        children: [
          if (!isMobile)
            AppSidebar(
              brandName: widget.brandName,
              items: widget.sidebarItems,
            ),

          Expanded(
            child: Column(
              children: [
                if (isMobile)
                  AppBar(
                    backgroundColor: AppColors.bgCard,
                    iconTheme: const IconThemeData(
                      color: AppColors.primaryDark,
                    ),
                    elevation: 0,
                    leading: IconButton(
                      icon: const Icon(Icons.menu),
                      onPressed: () => _scaffoldKey.currentState?.openDrawer(),
                    ),
                    title: Text(
                      widget.tenantValue ?? 'Tienda',
                      style: const TextStyle(
                        color: AppColors.primaryDark,
                        fontSize: 16,
                      ),
                    ),
                    actions: [trailingWidgets],
                  )
                else
                  AppTopBar(
                    tenantLabel: widget.tenantLabel,
                    tenantValue: widget.tenantValue,
                    userName: widget.userName,
                    trailing: trailingWidgets,
                  ),

                Expanded(
                  child: SingleChildScrollView(
                    keyboardDismissBehavior:
                        ScrollViewKeyboardDismissBehavior.manual,
                    padding: EdgeInsets.fromLTRB(
                      isMobile ? 20 : 40,
                      isMobile ? 20 : 40,
                      isMobile ? 20 : 40,
                      isMobile ? 20 : 40,
                    ),
                    child: widget.body,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
